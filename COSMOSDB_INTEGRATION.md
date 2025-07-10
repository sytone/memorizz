# CosmosDB Integration for Memorizz

This document describes the CosmosDB integration added to the Memorizz library.

## Overview

CosmosDB has been added as an additional memory provider alongside the existing MongoDB provider. The CosmosDB provider implements the same interface and provides identical functionality to the MongoDB provider.

## Features

- **Full API Compatibility**: CosmosDB provider implements all the same methods as MongoDB provider
- **Memory Types Support**: Supports all memory types (personas, toolbox, conversations, etc.)
- **Vector Search**: Includes vector search capabilities for semantic similarity
- **Tools Integration**: Includes CosmosDB-specific tools for function calling
- **Drop-in Replacement**: Can be used as a direct replacement for MongoDB provider

## Usage

### Basic Configuration

```python
from memorizz import CosmosDBProvider
from memorizz.memory_provider.cosmosdb import CosmosDBConfig

# Configure CosmosDB connection
config = CosmosDBConfig(
    connection_string="your-cosmosdb-connection-string",
    db_name="memorizz"
)

# Initialize the provider
provider = CosmosDBProvider(config)
```

### Using with Memory Types

```python
from memorizz.memory_provider import MemoryType

# Store a persona
persona_data = {
    'name': 'Assistant',
    'role': 'helper',
    'background': 'AI assistant'
}
persona_id = provider.store(persona_data, MemoryType.PERSONAS)

# Retrieve by ID
persona = provider.retrieve_by_id(persona_id, MemoryType.PERSONAS)

# List all personas
all_personas = provider.list_all(MemoryType.PERSONAS)
```

### CosmosDB Tools

```python
from memorizz.database import CosmosDBTools, CosmosDBToolsConfig

# Configure tools
tools_config = CosmosDBToolsConfig(
    connection_string="your-cosmosdb-connection-string",
    db_name="function_calling_db",
    get_embedding=your_embedding_function
)

# Initialize tools
tools = CosmosDBTools(tools_config)

# Use the toolbox decorator
@tools.cosmosdb_toolbox()
def my_function(param1: str, param2: int) -> str:
    """This function does something useful."""
    return f"Result: {param1} - {param2}"
```

## Comparison with MongoDB

| Feature | MongoDB Provider | CosmosDB Provider |
|---------|------------------|-------------------|
| Connection | `uri` parameter | `connection_string` parameter |
| API Compatibility | Full MemoryProvider interface | Full MemoryProvider interface |
| Memory Types | All 9 types supported | All 9 types supported |
| Vector Search | ✅ | ✅ |
| Tools Integration | ✅ | ✅ |
| Method Signatures | Identical | Identical |

## Migration from MongoDB

To migrate from MongoDB to CosmosDB, simply replace the provider:

**Before (MongoDB):**
```python
from memorizz import MongoDBProvider
from memorizz.memory_provider.mongodb import MongoDBConfig

config = MongoDBConfig(uri="mongodb://localhost:27017/", db_name="memorizz")
provider = MongoDBProvider(config)
```

**After (CosmosDB):**
```python
from memorizz import CosmosDBProvider
from memorizz.memory_provider.cosmosdb import CosmosDBConfig

config = CosmosDBConfig(connection_string="your-cosmosdb-connection-string", db_name="memorizz")
provider = CosmosDBProvider(config)
```

## Implementation Details

- **MongoDB API Compatibility**: CosmosDB provider uses the MongoDB API for Azure Cosmos DB
- **PyMongo Client**: Uses the same pymongo client as MongoDB provider
- **Vector Indexes**: Supports vector search indexes for semantic similarity
- **Collection Management**: Automatically creates collections and indexes as needed
- **Error Handling**: Includes comprehensive error handling and logging

## Files Added

- `src/memorizz/memory_provider/cosmosdb/`
  - `__init__.py` - Module initialization
  - `provider.py` - Main CosmosDB provider implementation
- `src/memorizz/database/cosmosdb/`
  - `__init__.py` - Module initialization  
  - `cosmosdb_tools.py` - CosmosDB-specific tools implementation

## Files Modified

- `src/memorizz/memory_provider/__init__.py` - Added CosmosDB imports
- `src/memorizz/memory_provider/mongodb/__init__.py` - Added MongoDBConfig export
- `src/memorizz/database/__init__.py` - Added CosmosDB tools imports
- `src/memorizz/__init__.py` - Added CosmosDB provider to main exports

## Testing

The integration includes comprehensive tests to verify:
- All abstract methods are implemented
- Method signatures match MongoDB provider
- Configuration classes work correctly
- Import patterns function properly
- Inheritance hierarchy is correct

Run the tests with:
```bash
python test_comprehensive.py
```

## Environment Variables

For CosmosDB tools, you can set the connection string via environment variable:
```bash
export COSMOSDB_CONNECTION_STRING="your-connection-string"
```

## Notes

- CosmosDB uses MongoDB API, so most MongoDB operations are directly supported
- Vector search capabilities depend on your CosmosDB configuration
- Connection strings should use the MongoDB protocol format for CosmosDB
- Both providers can be used simultaneously in the same application if needed