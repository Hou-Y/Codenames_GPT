"""
env_setup.py

This submission requires env_setup.py to be present in the same directory. 
It handles credential loading and can start the local Ollama server

Detects whether code is running on Kaggle or locally, and runs the
appropriate setup (starting Ollama, loading credentials, resolving file
paths) so the rest of the codebase can stay environment-agnostic.

Usage, at the top of any notebook/script:

    from env_setup import setup_environment
    env = setup_environment()

    # env is a dict like:
    # {
    #   "is_kaggle": True/False,
    #   "openai_api_key": "...",
    #   "azure_api_key": "...",
    #   "azure_endpoint": "...",
    #   "azure_api_version": "...",
    #   "wordlist_path": "players/cm_wordlist.txt",
    #   "vocab_path": "clue_vocabulary.txt",
    # }
"""

import os


def is_kaggle() -> bool:
    """Kaggle notebooks always set this env var; local machines never do."""
    return "KAGGLE_KERNEL_RUN_TYPE" in os.environ


def _setup_kaggle():
    """Kaggle-specific setup: start Ollama if needed, read Kaggle Secrets."""
    import subprocess
    import time

    config = {"is_kaggle": True}

    # kaggle secrets are only available in the notebook environment, not locally
    try:
        from kaggle_secrets import UserSecretsClient
        secrets = UserSecretsClient()

        def _try_secret(name):
            try:
                return secrets.get_secret(name)
            except Exception:
                return None

        config["azure_api_key"] = _try_secret("AZURE_OPENAI_API_KEY")
        config["azure_endpoint"] = _try_secret("AZURE_OPENAI_ENDPOINT")
    except Exception as e:
        print(f"Warning: could not read Kaggle Secrets ({e})")

    # Start Ollama server 
    def _ollama_running():
        try:
            import requests
            requests.get("http://localhost:11434", timeout=1)
            return True
        except Exception:
            return False
        
    def _ollama_installed():
        return subprocess.run(["which", "ollama"], capture_output=True).returncode == 0
 
    if not _ollama_installed():
        print("Installing Ollama ")
        subprocess.run(
            "curl -fsSL https://ollama.com/install.sh | sh",
            shell=True, check=True
        )

    if not _ollama_running():
            print("Starting Ollama server...")
            subprocess.Popen(["ollama", "serve"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for _ in range(20):
                if _ollama_running():
                    break
            time.sleep(1)
    # Paths
    config["wordlist_path"] = "/kaggle/working/players/cm_wordlist.txt"
    config["vocab_path"] = "/kaggle/working/clue_vocabulary.txt"

    return config


def _setup_local():
    """Local-specific setup: load .env via python-dotenv."""
    config = {"is_kaggle": False}

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("Warning: python-dotenv not installed, relying on shell env vars.")

    config["openAI_api_key"] = os.environ.get("AZURE_OPENAI_API_KEY")
    config["azure_endpoint"] = os.environ.get("AZURE_OPENAI_ENDPOINT")

    config["wordlist_path"] = "players/cm_wordlist.txt"
    config["vocab_path"] = "clue_vocabulary.txt"

    return config


def _propagate_to_environ(config: dict):
    """
    Write resolved credentials back into os.environ, any module that
    has os.environ.get("OPENAI_API_KEY") (e.g. gpt_manager.py) works
    regardless of coming from a Kaggle Secret or a local .env file.
    """
    mapping = {
        "openAI_api_key": "AZURE_OPENAI_API_KEY",
        "azure_endpoint": "AZURE_OPENAI_ENDPOINT",
    }
    for config_key, env_key in mapping.items():
        value = config.get(config_key)
        if value:
            os.environ[env_key] = value


def setup_environment() -> dict:

    if is_kaggle():
        print("Detected Kaggle environment.")
        config = _setup_kaggle()
    else:
        print("Detected local environment.")
        config = _setup_local()

    _propagate_to_environ(config)
    return config
