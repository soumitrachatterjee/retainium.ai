# Copyright (C) 2024-2025 Soumitra Chatterjee
# Licensed under the GNU AGPL-3.0. See LICENSE file for details.

# Compute project root relative to this script
# (protect against symlinks using realpath())
import os
root = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

# Setup the default LLM CLI path
default_llm_cli_path = os.path.join(root, "bin", "llama-cli")

# Import required modules
import re
import subprocess
from retainium.diagnostics import Diagnostics

class LLMHandler:
    def __init__(self, config):
        # Fetch all configured values, or use defaults
        self.enabled = config.getboolean("llm", "enabled", fallback=True)
        self.model_path = config.get("llm", "model_path", fallback=None)
        self.cli_path = config.get("llm", "cli_path", fallback=default_llm_cli_path) 
        self.context_length = config.getint("llm", "context_length", fallback=2048)
        self.temperature = config.getfloat("llm", "temperature", fallback=0.7)
        self.threads = config.getint("llm", "threads", fallback=4)
        self.gpu_layers = config.getint("llm", "gpu_layers", fallback=0)
        Diagnostics.note(f"LLM {self.cli_path} initialized with model {self.model_path}, context={self.context_length}, temp={self.temperature}")

    # Generate a response from the underlying LLM for the specified prompt
    def generate_response(self, prompt: str) -> str:
        if not self.enabled:
            raise RuntimeError("LLM integration is disabled in config.")

        if not os.path.isfile(self.model_path):
            raise FileNotFoundError(f"Model not found at: {self.model_path}")

        command = [
            self.cli_path,
            "-m", self.model_path,
            "-p", prompt,
            "--ctx-size", str(self.context_length),
            "--threads", str(self.threads),
            "--n-gpu-layers", str(self.gpu_layers)
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"LLM execution failed:\n{result.stderr}")
        Diagnostics.debug(f"response from LLM: {result.stdout}")
        
        # Cleanup the results to make it more human-friendly
        match = re.search(r"Answer:\s*(.*?)\s*\[end of text\]", result.stdout, re.DOTALL)
        if match:
            response = match.group(1).strip()
        else:
            response = ""
        return response

    # Normalize text
    def normalize_text(self, text: str):
        # Remove leading bullet symbols or numbers (e.g., "1.", "-", "*", "")
        text = re.sub(r'^\s*(?:[\d]+[\.\)]|[-*])\s*', '', text)

        # Remove special characters (keep only letters, numbers, and whitespace)
        text = re.sub(r'[^A-Za-z0-9\s]', '', text)

        # Normalize whitespace
        return ' '.join(text.split())

    # Auto generate tags for the given text
    def auto_tags(self, text: str):
        # Synthesize the prompt for the LLM
        prompt = (
                    "Generate the most relevant tags for the given text "
                    "that can be used as metadata to index or search "
                    "this text in future, excluding common words such as "
                    "\"and\", \"of\", \"in\", \"to\", etc. as well as "
                    "punctuation marks and symbols as tags."
                 )
        prompt += f"\n\nText:\n{text}\n\nAnswer:"
        Diagnostics.debug(f"prompt for LLM based auto tag generation: {prompt}")
        response = self.generate_response(prompt)

        # Process the response
        words = response.split()
        seen = set()
        result = []
        
        for tag in words:
            original = tag.strip()

            if not original:
                continue

            cleaned = self.normalize_text(original)
            if cleaned and cleaned not in seen:
                seen.add(cleaned)
                result.append(cleaned)

        # Return the processed tags
        return result

    # Summarize key information from given text, leveraging prior context, if any
    def summarize_info(self, text: str, context: str = "") -> str:
        # Synthesize the prompt for the LLM
        prompt = (
                    "Extract the key information from the given text "
                    "portion into a brief form, ensuring no key data is "
                    "missed."
                 )
        
        if context:
            prompt += (
                        "The provided context is a summary from the prior "
                        "portion of the extract. Do not replicate the same "
                        "in your answer, but use the context to fill in "
                        "any missing information, if required. "
                        "In case the context provides all the key "
                        "information present in the text and hence no "
                        "further extraction is necessary, then just repond "
                        "with the word \"REPEATED\"."
                      )
            prompt += f"\n\nText:\n{text}\n\nContext:\n{context}\n\nAnswer:"
        else:
            prompt += f"\n\nText:\n{text}\n\nAnswer:"
        Diagnostics.debug(f"prompt for LLM based summarization: {prompt}")

        # Return the response generated from the LLM
        response = self.generate_response(prompt)
        if response.lower() == "repeated":
            Diagnostics.debug(f"Summarization of chunk caused repetition; ignored")
            response = None
        return response

    # Use an optional context to build up a prompt for the LLM query
    def query(self, question: str, context: str = "") -> str:
        # Synthesize the prompt for the LLM
        # Method 1
        #prompt = f"Use the context below to answer the question."
        # Method 2
        prompt = f"Answer the following query using the context."
        # Method 3
        #prompt = f"Only answer the query based strictly on the context below."

        # Append the necessary context, question and the placeholder for the answer
        prompt += f"\n\nContext:\n{context}\n\nQuery:\n{question}\n\nAnswer:"
        Diagnostics.debug(f"prompt for LLM query: {prompt}")
        return self.generate_response(prompt)

