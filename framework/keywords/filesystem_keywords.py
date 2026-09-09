"""Filesystem automation keywords."""
import logging
from typing import Optional

from framework.core.ssh_client import SSHClient
from framework.core.command_executor import CommandExecutor

logger = logging.getLogger(__name__)


class FilesystemKeywords:
    """Keywords for filesystem operations.
    
    Provides high-level keywords for file and directory operations:
    - File existence checks
    - Directory operations
    - File content inspection
    - Permissions checking
    """

    def __init__(self, ssh_client: SSHClient) -> None:
        """Initialize filesystem keywords.
        
        Args:
            ssh_client: Connected SSH client
        """
        self.ssh_client = ssh_client
        self.executor = CommandExecutor(ssh_client=ssh_client)

    def file_exists(self, server_name: str, file_path: str) -> bool:
        """Check if file exists.
        
        Args:
            server_name: Name of server
            file_path: Path to file
            
        Returns:
            True if file exists
        """
        logger.info(f"Checking if file exists: {file_path}")
        
        try:
            result = self.executor.execute(
                f"[ -f '{file_path}' ] && echo 'exists'",
                retries=1
            )
            exists = 'exists' in result.stdout
        except Exception:
            exists = False
        
        logger.info(f"File {file_path} exists: {exists}")
        return exists

    def directory_exists(self, server_name: str, dir_path: str) -> bool:
        """Check if directory exists.
        
        Args:
            server_name: Name of server
            dir_path: Path to directory
            
        Returns:
            True if directory exists
        """
        logger.info(f"Checking if directory exists: {dir_path}")
        
        try:
            result = self.executor.execute(
                f"[ -d '{dir_path}' ] && echo 'exists'",
                retries=1
            )
            exists = 'exists' in result.stdout
        except Exception:
            exists = False
        
        logger.info(f"Directory {dir_path} exists: {exists}")
        return exists

    def file_contains(self, server_name: str, file_path: str, text: str) -> bool:
        """Check if file contains text.
        
        Args:
            server_name: Name of server
            file_path: Path to file
            text: Text to search for
            
        Returns:
            True if file contains text
        """
        logger.info(f"Checking if {file_path} contains '{text}'")
        
        try:
            result = self.executor.execute(
                f"grep -q '{text}' '{file_path}' && echo 'found'",
                retries=1
            )
            contains = 'found' in result.stdout
        except Exception:
            contains = False
        
        logger.info(f"File contains text: {contains}")
        return contains

    def file_size(self, server_name: str, file_path: str) -> Optional[int]:
        """Get file size in bytes.
        
        Args:
            server_name: Name of server
            file_path: Path to file
            
        Returns:
            File size in bytes
        """
        logger.info(f"Getting size of {file_path}")
        
        try:
            result = self.executor.execute(
                f"stat -c '%s' '{file_path}'",
                retries=1
            )
            size = int(result.stdout.strip())
        except Exception:
            size = None
        
        logger.info(f"File size: {size} bytes")
        return size
