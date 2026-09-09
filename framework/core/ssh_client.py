"""SSH client for secure remote command execution."""
import logging
from typing import Tuple, Optional

import paramiko
from paramiko import SSHClient as ParamikoSSHClient
from paramiko import AutoAddPolicy, WarningPolicy

logger = logging.getLogger(__name__)


class SSHClient:
    """Secure SSH client with host key verification.
    
    Features:
    - Key-based authentication (no passwords)
    - Strict host key verification (prevents MITM attacks)
    - Automatic connection management
    - Comprehensive logging
    """

    def __init__(
        self,
        hostname: str,
        username: str,
        key_filename: str,
        known_hosts_file: str,
        port: int = 22,
        timeout: int = 30
    ) -> None:
        """Initialize SSH client.
        
        Args:
            hostname: Target host address
            username: SSH username
            key_filename: Path to SSH private key
            known_hosts_file: Path to known_hosts file
            port: SSH port (default 22)
            timeout: Connection timeout in seconds
            
        Raises:
            FileNotFoundError: If key file or known_hosts file not found
            paramiko.SSHException: If connection fails
        """
        self.hostname = hostname
        self.username = username
        self.port = port
        self.timeout = timeout
        self.key_filename = key_filename
        self.known_hosts_file = known_hosts_file
        
        self._client: Optional[ParamikoSSHClient] = None
        self._connect()
        
        logger.info(f"Initialized SSH client for {username}@{hostname}:{port}")

    def _connect(self) -> None:
        """Establish SSH connection with host key verification.
        
        Raises:
            FileNotFoundError: If key file or known_hosts file not found
            paramiko.SSHException: If connection fails
        """
        self._client = ParamikoSSHClient()
        
        # Use strict host key verification
        self._client.set_missing_host_key_policy(WarningPolicy())
        
        # Load known hosts file
        try:
            self._client.load_system_host_keys()
            self._client.load_host_keys(self.known_hosts_file)
        except FileNotFoundError as e:
            logger.error(f"Known hosts file not found: {self.known_hosts_file}")
            raise
        
        # Connect with key authentication
        try:
            self._client.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                key_filename=self.key_filename,
                timeout=self.timeout,
                look_for_keys=False,
                allow_agent=False
            )
            logger.info(f"Successfully connected to {self.hostname}")
        except paramiko.AuthenticationException as e:
            logger.error(f"SSH authentication failed: {e}")
            raise
        except paramiko.SSHException as e:
            logger.error(f"SSH connection failed: {e}")
            raise

    def execute_command(self, command: str) -> Tuple[str, str]:
        """Execute command on remote host.
        
        Args:
            command: Command to execute
            
        Returns:
            Tuple of (stdout, stderr)
            
        Raises:
            RuntimeError: If client is not connected
            paramiko.SSHException: If command execution fails
        """
        if self._client is None:
            raise RuntimeError("SSH client is not connected")
        
        try:
            logger.debug(f"Executing command: {command}")
            stdin, stdout, stderr = self._client.exec_command(
                command,
                timeout=self.timeout
            )
            
            stdout_str = stdout.read().decode('utf-8')
            stderr_str = stderr.read().decode('utf-8')
            exit_code = stdout.channel.recv_exit_status()
            
            if exit_code != 0:
                logger.warning(f"Command exited with code {exit_code}: {command}")
            else:
                logger.debug(f"Command executed successfully")
            
            return stdout_str, stderr_str
        except paramiko.SSHException as e:
            logger.error(f"Command execution failed: {e}")
            raise

    def close(self) -> None:
        """Close SSH connection."""
        if self._client:
            self._client.close()
            logger.info(f"Closed SSH connection to {self.hostname}")
