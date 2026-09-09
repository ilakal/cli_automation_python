"""Server automation keywords."""
import logging
from typing import Optional

from framework.core.ssh_client import SSHClient
from framework.core.command_executor import CommandExecutor
from framework.parsers.unix_parser import UnixParser

logger = logging.getLogger(__name__)


class ServerKeywords:
    """Keywords for server operations.
    
    Provides high-level keywords for common server operations:
    - Hostname verification
    - Service management
    - Process inspection
    - System information
    """

    def __init__(self, ssh_client: SSHClient) -> None:
        """Initialize server keywords.
        
        Args:
            ssh_client: Connected SSH client
        """
        self.ssh_client = ssh_client
        self.executor = CommandExecutor(ssh_client=ssh_client)
        self.parser = UnixParser()

    def hostname(self, server_name: str) -> Optional[str]:
        """Get server hostname.
        
        Args:
            server_name: Name of server (for logging)
            
        Returns:
            Server hostname
        """
        logger.info(f"Getting hostname for {server_name}")
        
        result = self.executor.execute("hostname -f")
        hostname = result.stdout.strip()
        
        logger.info(f"Hostname: {hostname}")
        return hostname

    def service_status(self, server_name: str, service_name: str) -> Optional[str]:
        """Get service status.
        
        Args:
            server_name: Name of server
            service_name: Name of service
            
        Returns:
            Service status (active, inactive, not-found)
        """
        logger.info(f"Getting status of {service_name} on {server_name}")
        
        try:
            result = self.executor.execute(
                f"systemctl status {service_name}",
                retries=1
            )
            
            if result.success:
                status = "active"
            else:
                status = "inactive"
        except Exception:
            status = "not-found"
        
        logger.info(f"Service {service_name} status: {status}")
        return status

    def process_exists(self, server_name: str, process_name: str) -> bool:
        """Check if process exists.
        
        Args:
            server_name: Name of server
            process_name: Name of process
            
        Returns:
            True if process exists
        """
        logger.info(f"Checking if process {process_name} exists on {server_name}")
        
        try:
            result = self.executor.execute(
                f"pgrep -f {process_name}",
                retries=1
            )
            exists = result.success
        except Exception:
            exists = False
        
        logger.info(f"Process {process_name} exists: {exists}")
        return exists

    def uptime(self, server_name: str) -> Optional[str]:
        """Get server uptime.
        
        Args:
            server_name: Name of server
            
        Returns:
            Uptime string
        """
        logger.info(f"Getting uptime for {server_name}")
        
        result = self.executor.execute("uptime")
        uptime = result.stdout.strip()
        
        logger.info(f"Uptime: {uptime}")
        return uptime
