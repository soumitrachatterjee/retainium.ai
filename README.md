# retainium.ai
Personal knowledge database with contextual retrieval, powered by a pre-trained language model and a local storage system to persist new information


## Project structure
```
retainium.ai/
│── lib/
│   ├── knowledge_db.py      # Handles ChromaDB operations
│   ├── embeddings.py        # Handles text embeddings
│   ├── cli_handler.py       # Manages command-line options
│── etc/
│   ├── config.py            # Stores configurable options
│── main.py                  # Top-level driver script
│── README.md                # Project documentation
```

retainium.ai/
│── lib/                    
│   ├── __init__.py          # Makes 'lib' a package
│   ├── knowledge.py         # Handles ChromaDB operations
│   ├── embeddings.py        # Handles text embeddings
│   ├── cli.py               # Manages command-line options
│   ├── config.py            # Parses configuration settings
│── etc/
│   ├── config.ini           # Configuration file
│── data/                    # Stores knowledge database files
│── main.py                  # Top-level driver script
│── README.md                # Documentation
