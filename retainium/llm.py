import subprocess
import configparser
import os
from retainium.diagnostics import Diagnostics

class LLMHandler:
    def __init__(self, config_path="etc/config.ini"):
        config = configparser.ConfigParser()
        config.read(config_path)

        self.enabled = config.getboolean("llm", "enabled", fallback=True)
        self.model_path = config.get("llm", "model_path", fallback=None)
        self.n_ctx = config.getint("llm", "n_ctx", fallback=2048)
        self.n_threads = config.getint("llm", "n_threads", fallback=4)
        self.n_gpu_layers = config.getint("llm", "n_gpu_layers", fallback=0)
        self.llama_cli_path = config.get("llm", "llama_cli_path", fallback="bin/llama-cli")

    def generate_response(self, prompt: str) -> str:
        if not self.enabled:
            raise RuntimeError("LLM integration is disabled in config.")

        if not os.path.isfile(self.model_path):
            raise FileNotFoundError(f"Model not found at: {self.model_path}")

        command = [
            self.llama_cli_path,
            "-m", self.model_path,
            "-p", prompt,
            "--ctx-size", str(self.n_ctx),
            "--threads", str(self.n_threads),
            "--n-gpu-layers", str(self.n_gpu_layers)
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
        Diagnostics.debug(f"prompt for query: {prompt}")
        response = self.generate_response(prompt)

        # Clean up the response
        if response.endswith("[end of text]"):
            response = response.replace("[end of text]", "").strip()

        return response
