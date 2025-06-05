"""
Logging utility module.
"""
import logging
import os
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create formatters
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_formatter = logging.Formatter(
        "%(levelname)s - %(message)s"
    )
    
    # File handler
    log_file = os.path.join(
        logs_dir,
        f"{datetime.now().strftime('%Y-%m-%d')}.log"
    )
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 