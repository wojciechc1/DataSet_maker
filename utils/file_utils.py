import os
import json
from utils.logger import setup_logger

logger = setup_logger(__name__)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

def load_metadata(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.warning(f"Metadata file {path} is empty or corrupted. Starting fresh.")
        return {}

def save_metadata(metadata_path, metadata):
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

