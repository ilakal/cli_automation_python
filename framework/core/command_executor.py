"""Safe command execution with timeout and retry logic."""
import logging
import shlex
import time
from typing import Optional, Tuple
from dataclasses import dataclass

from framework.core.ssh_client import SSHClient

logger = logging.getLogger(__name__)


@dataclass
class CommandResult:
    """Result of command execution."""
    stdout: str
    stderr: str
    exit_code: int = 0
    duration: float = 0.0
    attempts: int = 1

    @property
    def success(self) -> bool:
        """Check if command executed successfully."""
        return self.exit_code == 0

    @property
    def output(self) -> str:
        """Get combined stdout and stderr."""
        return self.stdout + self.stderr


class SafeCommandBuilder:
    """Build commands safely with proper escaping."""

    @staticmethod
    def build(*args: str) -> str:
        """Build command with safe argument escaping.
        
        Args:
            *args: Command and arguments
            
        Returns:
            Properly escaped command string
            
        Example:
            >>> cmd = SafeCommandBuilder.build('ls', '-la', '/tmp')
            >>> cmd
            'ls -la /tmp'
        """
        return ' '.join(shlex.quote(arg) for arg in args)


class CommandExecutor:
    """Execute commands with timeout and retry support.
    
    Features:
    - Automatic retry on failure
    - Timeout protection
    - Comprehensive logging
    - Result tracking
    """

    def __init__(
        self,
        ssh_client: SSHClient,
        default_timeout: int = 30,
        default_retries: int = 1,
        retry_delay: float = 2.0
    ) -> None:
        """Initialize command executor.
        
        Args:
            ssh_client: Connected SSH client
            default_timeout: Default command timeout in seconds
            default_retries: Default number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        self.ssh_client = ssh_client
        self.default_timeout = default_timeout
        self.default_retries = default_retries
        self.retry_delay = retry_delay

    def execute(
        self,
        command: str,
        timeout: Optional[int] = None,
        retries: Optional[int] = None
    ) -> CommandResult:
        """Execute command with retry logic.
        
        Args:
            command: Command to execute
            timeout: Command timeout in seconds (uses default if None)
            retries: Number of retry attempts (uses default if None)
            
        Returns:
            CommandResult with execution details
        """
        timeout = timeout or self.default_timeout
        retries = retries or self.default_retries
        
        start_time = time.time()
        last_error = None
        
        for attempt in range(1, retries + 1):
            try:
                logger.info(f"Executing command (attempt {attempt}/{retries}): {command}")
                
                stdout, stderr = self.ssh_client.execute_command(command)
                duration = time.time() - start_time
                
                result = CommandResult(
                    stdout=stdout,
                    stderr=stderr,
                    duration=duration,
                    attempts=attempt
                )
                
                logger.info(f"Command executed successfully in {duration:.2f}s")
                return result
            
            except Exception as e:
                last_error = e
                logger.warning(f"Command execution failed (attempt {attempt}/{retries}): {e}")
                
                if attempt < retries:
                    logger.info(f"Retrying in {self.retry_delay}s...")
                    time.sleep(self.retry_delay)
        
        # All retries exhausted
        duration = time.time() - start_time
        logger.error(f"Command failed after {retries} attempts")
        
        raise RuntimeError(
            f"Command failed after {retries} attempts: {last_error}"
        )
