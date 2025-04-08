import subprocess
import configparser
import os
import re
import textwrap
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
        
        output = result.stdout.strip()

        # Remove everything before and including "Answer:" (case-insensitive)
        #match = re.search(r"(?i)Answer\s*:\s*(.*)", output, re.DOTALL)
        match = re.search(r"(?i)Answer\s*:\s*\n?(.*)", output, re.DOTALL)
        if match:
            cleaned = match.group(1)
        else:
            cleaned = output

        # Remove "[end of text]" and strip lines
        cleaned = cleaned.split("[end of text]")[0]

        # De-indent and strip extra whitespace
        import textwrap
        cleaned = textwrap.dedent(cleaned).strip()
        
        # Optional: Ensure first line doesn't have stray space
        lines = cleaned.splitlines()
        if lines:
            lines[0] = lines[0].lstrip()
        cleaned = "\n".join(lines).strip()
        
        return cleaned

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
        return self.generate_response(prompt)

