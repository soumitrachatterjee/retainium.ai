# Retainium.ai

**Retainium.ai** is a local knowledge database and retrieval system that allows users to store, semantically search, and query information using embeddings and a locally hosted Large Language Model (LLM). It is modular, privacy-respecting, and can run entirely offline.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Model Setup](#model-setup)
  - [Installing ](#installing-llamacpp-and-llama-cli)[`llama.cpp`](#installing-llamacpp-and-llama-cli)[ and ](#installing-llamacpp-and-llama-cli)[`llama-cli`](#installing-llamacpp-and-llama-cli)
  - [Downloading the Model](#downloading-the-model)
- [Command-Line Usage](#command-line-usage)
  - [Adding Knowledge](#adding-knowledge)
  - [Querying Knowledge](#querying-knowledge)
  - [Similarity-Only Mode](#similarity-only-mode)
  - [Debug Mode](#debug-mode)
- [Example Use Cases](#example-use-cases)
- [References](#references)

---

## Features

- Local vector-based semantic search using ChromaDB and sentence-transformer embeddings.
- Query responses enhanced by a local LLM using `llama.cpp`.
- Modular structure for extensibility.
- CLI interface for data ingestion and querying.
- Configurable via `etc/config.ini`.

---

## Project Structure

```text
retainium.ai/
├── bin/                    # llama-cli binary location
├── data/                   # Knowledge DB and vector store
├── etc/
│   └── config.ini          # Config file
├── lib/
│   ├── cli.py              # CLI handlers
│   ├── knowledge.py        # ChromaDB operations
│   ├── embeddings.py       # Sentence transformer embeddings
│   └── llm.py              # LLM integration (llama.cpp)
├── retainium.py            # Main CLI entry point
├── requirements.txt        # Python dependencies
```

---

## Installation
(_See the section on dependencies below for more details_)

```bash
# Clone the repository
git clone git@github.com:soumitrachatterjee/retainium.ai.git
cd retainium.ai

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Edit `etc/config.ini` to control behavior.

### `[llm]` section

```ini
[llm]
enabled = true
model_path = data/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf
n_ctx = 2048
n_threads = 4
n_gpu_layers = 0
llama_cli_path = bin/llama-cli
```

**Explanation**:

- `enabled`: Toggle LLM usage.
- `model_path`: Path to the GGUF model file.
- `n_ctx`: Context window size.
- `n_threads`: Number of CPU threads to use.
- `n_gpu_layers`: Number of layers to run on GPU (set to 0 for CPU-only).
- `llama_cli_path`: Path to the compiled `llama-cli` binary.

---

## Dependencies

The following will help install the required dependencies:

```bash
sudo apt update
sudo apt install git-lfs

git lfs install
git clone https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF
cp Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q4_K_M.gguf \
     Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q4_K_M.gguf

pip install -r requirements.txt
```

**Key packages**:

- `chromadb`
- `sentence-transformers`
- `transformers`
- `torch`
- `faiss-cpu` or `faiss-gpu`

---

## Model Setup

### Installing `llama.cpp` and `llama-cli`

```bash
# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

# Build the CLI
mkdir build && cd build
cmake ..
cmake --build . --config Release

# Copy the llama-cli binary to your project
cp ./bin/llama-cli ../../retainium.ai/bin/llama-cli

```

### Downloading the Model

You can download a quantized model such as:

**Mistral-7B-Instruct (Q4\_K\_M)** from:

- [TheBloke on Hugging Face](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)

Example using `huggingface-cli`:

```bash
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.1-GGUF mistral-7b-instruct-v0.1.Q4_K_M.gguf --local-dir ./data/models/
```

### Validating the model with Llama

You can test Llama with the model using the following command:

```
./bin/llama-cli \
  -m ~/models/llama/Mistral-7B-Instruct-v0.1.Q4_K_M.gguf \
    -p "What is the capital of France?"
```

---

## Command-Line Usage

Run using:

```bash
python3 retainium.py <command> [options]
```

### Adding Knowledge

```bash
python3 retainium.py add --text "Auli is a skiing destination in Uttarakhand."
```

### Querying Knowledge

```bash
python3 retainium.py query --text "What are the skiing destinations in India?"
```

### Similarity-Only Mode

Returns top similar documents without LLM reasoning:

```bash
python3 retainium.py query --text "dehradun" --similarity_only
```

### Debug Mode

Shows the context, prompt, and full intermediate steps:

```bash
python3 retainium.py query --text "why is sleep important for health" --debug
```

---

## Example Use Cases

### 1. Local Knowledge Assistant

Store company policies, personal notes, or documentation, then query in natural language.

### 2. Offline Research Companion

Ingest articles or documents, then ask questions without internet access.

### 3. Personal Knowledge Base

Use for journaling, storing key ideas, travel notes, or reading summaries.

---

## References

- [`llama.cpp`](https://github.com/ggerganov/llama.cpp): Lightweight LLM inference engine.
- [`TheBloke`](https://huggingface.co/TheBloke)[ on Hugging Face](https://huggingface.co/TheBloke): Quantized models for offline use.
- [`sentence-transformers`](https://www.sbert.net/): Embedding generator.
- [`Chroma`](https://www.trychroma.com/): Local vector database.

