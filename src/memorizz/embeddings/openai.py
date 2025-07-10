# ./embeddings/openai.py

import logging
import openai
import os
from typing import List, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress httpx logs to reduce noise from API requests
logging.getLogger("httpx").setLevel(logging.WARNING)

@dataclass
class AzureOpenAIEmbeddingConfig:
    """Configuration for Azure OpenAI embeddings."""
    
    def __init__(self, 
                 api_key: str,
                 azure_endpoint: str,
                 api_version: str = "2024-02-01"):
        """
        Initialize Azure OpenAI embedding configuration.
        
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

# Global client for backward compatibility - initialized lazily
_openai_client = None

def _get_openai_client():
    """Get or create the OpenAI client."""
    global _openai_client
    if _openai_client is None:
        _openai_client = openai.OpenAI()
    return _openai_client

def get_embedding(text: str, 
                 model: str = "text-embedding-3-small", 
                 dimensions: int = 256,
                 azure_config: Optional[AzureOpenAIEmbeddingConfig] = None) -> List[float]:
    """
    Get the embedding of a text using OpenAI's API or Azure OpenAI.

    Parameters:
        text (str): The text to get the embedding of.
        model (str): The model to use for the embedding.
        dimensions (int): The dimensions of the embedding.
        azure_config (AzureOpenAIEmbeddingConfig, optional): Configuration for Azure OpenAI.

    Returns:
        List[float]: The embedding of the text.
    """
    text = text.replace("\n", " ")
    
    try:
        if azure_config:
            # Use Azure OpenAI
            client = openai.AzureOpenAI(
                api_key=azure_config.api_key,
                azure_endpoint=azure_config.azure_endpoint,
                api_version=azure_config.api_version
            )
        else:
            # Use standard OpenAI (backward compatibility)
            client = _get_openai_client()
            
        return client.embeddings.create(input=[text], model=model, dimensions=dimensions).data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        raise

def get_embedding_dimensions(model: str = "text-embedding-3-small") -> int:
    """
    Get the dimensions of the embedding for a given model.

    Parameters:
        model (str): The model to get the dimensions of.

    Returns:
        int: The dimensions of the embedding.
    """
    if model == "text-embedding-3-small":
        return 256
    else:
        raise ValueError(f"Unsupported model: {model}")


