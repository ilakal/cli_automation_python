"""Helper functions."""
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


def ensure_directory_exists(directory: str) -> Path:
    """Ensure directory exists, create if needed.
    
    Args:
        directory: Directory path
        
    Returns:
        Path object for directory
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {path}")
    return path


def find_files(directory: str, pattern: str) -> List[Path]:
    """Find files matching pattern in directory.
    
    Args:
        directory: Directory to search
        pattern: File pattern (e.g., '*.yaml')
        
    Returns:
        List of matching file paths
    """
    path = Path(directory)
    files = list(path.glob(pattern))
    logger.debug(f"Found {len(files)} files matching {pattern} in {directory}")
    return files


def read_file(file_path: str) -> str:
    """Read file contents.
    
    Args:
        file_path: Path to file
        
    Returns:
        File contents
        
    Raises:
        FileNotFoundError: If file not found
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        contents = f.read()
    
    return contents
