"""Logging configuration and utilities."""
import logging
import logging.handlers
from pathlib import Path
from typing import Optional


class Logger:
    """Configures and provides loggers."""

    _initialized = False

    @classmethod
    def configure(
        cls,
        level: str = "INFO",
        log_file: Optional[str] = None,
        format_string: Optional[str] = None
    ) -> None:
        """Configure root logger.
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file to log to
            format_string: Custom format string
        """
        if cls._initialized:
            return
        
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, level))
        
        # Default format
        if format_string is None:
            format_string = (
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        formatter = logging.Formatter(format_string)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        cls._initialized = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get logger instance.
        
        Args:
            name: Logger name (usually __name__)
            
        Returns:
            Logger instance
        """
        return logging.getLogger(name)
