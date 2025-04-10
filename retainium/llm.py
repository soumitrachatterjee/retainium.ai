# Compute project root relative to this script
# (protect against symlinks using realpath())
import os
root = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

# Setup the default LLM CLI path
default_llm_cli_path = os.path.join(root, "bin", "llama-cli")

# Import required modules
import subprocess
import os
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
        
        return result.stdout.strip()

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
        Diagnostics.note(f"prompt for query: {prompt}")
        response = self.generate_response(prompt)

        # Clean up the response
        if response.endswith("[end of text]"):
            response = response.replace("[end of text]", "").strip()

        return response
