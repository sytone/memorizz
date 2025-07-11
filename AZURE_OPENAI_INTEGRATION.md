# Azure OpenAI Integration

This document describes how to use Azure OpenAI with the Memorizz library alongside the existing OpenAI support.

## Overview

Memorizz now supports both standard OpenAI and Azure OpenAI configurations for:
- **Language Models (LLMs)**: Generate text, process tool metadata, and handle conversations
- **Embeddings**: Generate vector embeddings for semantic search and memory storage

## Configuration

### Azure OpenAI for LLMs

```python
from memorizz import OpenAI, AzureOpenAIConfig

# Configure Azure OpenAI
azure_config = AzureOpenAIConfig(
    api_key="your-azure-openai-key",
    azure_endpoint="https://your-resource.openai.azure.com/",
    api_version="2024-02-01"  # Optional, defaults to "2024-02-01"
)

# Create OpenAI client with Azure configuration
llm = OpenAI(azure_config=azure_config, model="gpt-4")
```

### Azure OpenAI for Embeddings

```python
from memorizz.embeddings import get_embedding, AzureOpenAIEmbeddingConfig

# Configure Azure OpenAI for embeddings
azure_embed_config = AzureOpenAIEmbeddingConfig(
    api_key="your-azure-openai-key",
    azure_endpoint="https://your-resource.openai.azure.com/",
    api_version="2024-02-01"  # Optional, defaults to "2024-02-01"
)

# Generate embeddings using Azure OpenAI
embedding = get_embedding(
    text="Your text here",
    model="text-embedding-3-small",
    dimensions=256,
    azure_config=azure_embed_config
)
```

## Usage Examples

### Using Azure OpenAI with MemAgent

```python
from memorizz import MemAgent, OpenAI, AzureOpenAIConfig
from memorizz.memory_provider.mongodb import MongoDBProvider, MongoDBConfig

# Configure Azure OpenAI
azure_config = AzureOpenAIConfig(
    api_key="your-azure-openai-key",
    azure_endpoint="https://your-resource.openai.azure.com/"
)

# Create LLM with Azure OpenAI
llm = OpenAI(azure_config=azure_config, model="gpt-4")

# Configure memory provider
mongo_config = MongoDBConfig(uri="mongodb://localhost:27017/", db_name="memorizz")
memory_provider = MongoDBProvider(mongo_config)

# Create agent with Azure OpenAI
agent = MemAgent(
    model=llm,
    memory_provider=memory_provider,
    agent_id="azure-agent"
)

# Use the agent
response = agent.chat("Hello, how are you?")
```

### Using Azure OpenAI with Knowledge Base

```python
from memorizz.long_term_memory import KnowledgeBase
from memorizz.memory_provider.mongodb import MongoDBProvider, MongoDBConfig
from memorizz.embeddings import get_embedding, AzureOpenAIEmbeddingConfig

# Configure Azure OpenAI for embeddings
azure_embed_config = AzureOpenAIEmbeddingConfig(
    api_key="your-azure-openai-key",
    azure_endpoint="https://your-resource.openai.azure.com/"
)

# Configure memory provider
mongo_config = MongoDBConfig(uri="mongodb://localhost:27017/", db_name="memorizz")
memory_provider = MongoDBProvider(mongo_config)

# Create knowledge base
kb = KnowledgeBase(memory_provider=memory_provider)

# Ingest documents with Azure OpenAI embeddings
documents = [
    {"content": "Document 1 content", "metadata": {"source": "doc1"}},
    {"content": "Document 2 content", "metadata": {"source": "doc2"}}
]

# Custom embedding function using Azure OpenAI
def azure_embedding_func(text: str):
    return get_embedding(
        text=text,
        model="text-embedding-3-small",
        dimensions=256,
        azure_config=azure_embed_config
    )

# Note: You may need to modify the knowledge base to accept custom embedding functions
# This is a conceptual example showing how Azure OpenAI embeddings could be integrated
```

## Backward Compatibility

The existing OpenAI functionality remains unchanged:

```python
from memorizz import OpenAI

# Standard OpenAI (existing functionality)
llm = OpenAI(api_key="your-openai-key", model="gpt-4o")

# Or using environment variable
import os
os.environ["OPENAI_API_KEY"] = "your-openai-key"
llm = OpenAI(model="gpt-4o")
```

## Environment Variables

You can use environment variables for Azure OpenAI configuration:

```python
import os

# Set environment variables
os.environ["AZURE_OPENAI_API_KEY"] = "your-azure-openai-key"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://your-resource.openai.azure.com/"
os.environ["AZURE_OPENAI_API_VERSION"] = "2024-02-01"

# Create configuration from environment variables
azure_config = AzureOpenAIConfig(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
)
```

## Configuration Parameters

### AzureOpenAIConfig

- **api_key** (str): Your Azure OpenAI API key
- **azure_endpoint** (str): Your Azure OpenAI endpoint URL (e.g., "https://your-resource.openai.azure.com/")
- **api_version** (str, optional): API version to use (default: "2024-02-01")

### AzureOpenAIEmbeddingConfig

- **api_key** (str): Your Azure OpenAI API key
- **azure_endpoint** (str): Your Azure OpenAI endpoint URL (e.g., "https://your-resource.openai.azure.com/")
- **api_version** (str, optional): API version to use (default: "2024-02-01")

## Model Compatibility

Azure OpenAI supports the same models as standard OpenAI, but you need to ensure:
1. The model is deployed in your Azure OpenAI resource
2. You use the correct deployment name when specifying the model

```python
# Use the deployment name from your Azure OpenAI resource
llm = OpenAI(azure_config=azure_config, model="gpt-4")  # Where "gpt-4" is your deployment name
```

## Error Handling

The library includes proper error handling for missing API keys and configuration:

```python
from memorizz import OpenAI

try:
    # This will raise an error if no API key is provided and OPENAI_API_KEY is not set
    llm = OpenAI(model="gpt-4o")
    response = llm.generate_text("Hello world")
except ValueError as e:
    print(f"Configuration error: {e}")
```

## Integration with Memory Providers

Azure OpenAI works seamlessly with all memory providers:

```python
# Works with MongoDB
from memorizz.memory_provider.mongodb import MongoDBProvider, MongoDBConfig

# Works with CosmosDB
from memorizz.memory_provider.cosmosdb import CosmosDBProvider, CosmosDBConfig

# Both providers support Azure OpenAI for embeddings and LLM operations
```

This integration provides a complete Azure-based solution when combined with CosmosDB as the memory provider and Azure OpenAI for language processing.