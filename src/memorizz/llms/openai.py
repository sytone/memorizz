import os
import json
import openai
import logging
from typing import Callable, List, Optional, TYPE_CHECKING, Dict, Any
from dataclasses import dataclass

# Suppress httpx logs to reduce noise from API requests
logging.getLogger("httpx").setLevel(logging.WARNING)

# Use TYPE_CHECKING for forward references to avoid circular imports
if TYPE_CHECKING:
    from ..toolbox.tool_schema import ToolSchemaType
import inspect

@dataclass
class AzureOpenAIConfig:
    """Configuration for Azure OpenAI."""
    
    def __init__(self, 
                 api_key: str,
                 azure_endpoint: str,
                 api_version: str = "2024-02-01"):
        """
        Initialize Azure OpenAI configuration.
        
        Parameters:
        -----------
        api_key : str
            The Azure OpenAI API key.
        azure_endpoint : str
            The Azure OpenAI endpoint URL.
        api_version : str
            The API version to use.
        """
        self.api_key = api_key
        self.azure_endpoint = azure_endpoint
        self.api_version = api_version

class OpenAI:
    """
    A class for interacting with the OpenAI API or Azure OpenAI.
    """
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 model: str = "gpt-4o",
                 azure_config: Optional[AzureOpenAIConfig] = None):
        """
        Initialize the OpenAI client.

        Parameters:
        -----------
        api_key : str, optional
            The API key for the OpenAI API. If not provided, will use OPENAI_API_KEY environment variable.
        model : str, optional
            The model to use for the OpenAI API.
        azure_config : AzureOpenAIConfig, optional
            Configuration for Azure OpenAI. If provided, will use Azure OpenAI instead of standard OpenAI.
        """
        if azure_config:
            # Use Azure OpenAI
            self.client = openai.AzureOpenAI(
                api_key=azure_config.api_key,
                azure_endpoint=azure_config.azure_endpoint,
                api_version=azure_config.api_version
            )
        else:
            # Use standard OpenAI
            if api_key is None:
                api_key = os.getenv("OPENAI_API_KEY")
            
            # Only create client if we have an API key
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
            else:
                self.client = None
        
        self.model = model
        self.azure_config = azure_config


    def get_tool_metadata(self, func: Callable) -> Dict[str, Any]:
        """
        Get the metadata for a tool.

        Parameters:
        -----------
        func : Callable
            The function to get the metadata for.

        Returns:
        --------
        Dict[str, Any]
        """
        if self.client is None:
            raise ValueError("OpenAI client not initialized. Please provide an API key or set OPENAI_API_KEY environment variable.")
        
        # We'll import ToolSchemaType here to avoid circular imports
        from ..toolbox.tool_schema import ToolSchemaType

        docstring = func.__doc__ or ""
        signature = str(inspect.signature(func))
        func_name = func.__name__

        system_msg = {
            "role": "system",
            "content": (
                "You are an expert metadata augmentation assistant specializing in JSON schema discovery "
                "and documentation enhancement.\n\n"
                f"**IMPORTANT**: Use the function name exactly as provided (`{func_name}`) and do NOT rename it."
            )
        }

        user_msg = {
            "role": "user",
            "content": (
                f"Generate enriched metadata for the function `{func_name}`.\n\n"
                f"- Docstring: {docstring}\n"
                f"- Signature: {signature}\n\n"
                "Enhance the metadata by:\n"
                "• Expanding the docstring into a detailed description.\n"
                "• Writing clear natural‐language descriptions for each parameter, including type, purpose, and constraints.\n"
                "• Identifying which parameters are required.\n"
                "• (Optional) Suggesting example queries or use cases.\n\n"
                "Produce a JSON object that strictly adheres to the ToolSchemaType structure."
            )
        }

        response = self.client.responses.parse(
            model=self.model,
            input=[system_msg, user_msg],
            text_format=ToolSchemaType
        )

        return response.output_parsed
    
    def augment_docstring(self, docstring: str) -> str:
        """
        Augment the docstring with an LLM generated description.

        Parameters:
        -----------
        docstring : str
            The docstring to augment.

        Returns:
        --------
        str
        """
        if self.client is None:
            raise ValueError("OpenAI client not initialized. Please provide an API key or set OPENAI_API_KEY environment variable.")
        
        response = self.client.responses.create(
            model=self.model,
            input=f"Augment the docstring {docstring} by adding more details and examples."
        )

        return response.output_text
    
    def generate_queries(self, docstring: str) -> List[str]:
        """
        Generate queries for the tool.

        Parameters:
        -----------
        docstring : str
            The docstring to generate queries for.

        Returns:
        --------
        List[str]
        """
        if self.client is None:
            raise ValueError("OpenAI client not initialized. Please provide an API key or set OPENAI_API_KEY environment variable.")
        
        response = self.client.responses.create(
            model=self.model,
            input=f"Generate queries for the docstring {docstring} by adding some examples of queries that can be used to leverage the tool."
        )

        return response.output_text
    
    def generate_text(self, prompt: str, instructions: str = None) -> str:
        """
        Generate text using OpenAI's API.

        Parameters:
            prompt (str): The prompt to generate text from.
            instructions (str): The instructions to use for the generation.

        Returns:
            str: The generated text.
        """
        if self.client is None:
            raise ValueError("OpenAI client not initialized. Please provide an API key or set OPENAI_API_KEY environment variable.")
        
        response = self.client.responses.create(
            model=self.model,
            instructions=instructions,
            input=prompt)
        
        return response.output_text