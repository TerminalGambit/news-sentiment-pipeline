"""
Utility functions for API responses.
"""
from typing import Any, Dict, Optional
from flask import jsonify

def create_response(
    data: Any = None,
    error: Optional[str] = None,
    message: Optional[str] = None,
    status: str = "success"
) -> Dict:
    """
    Create a standardized API response.
    
    Args:
        data: The response data
        error: Error message if any
        message: Success message if any
        status: Response status (success/error)
    
    Returns:
        Dict containing the formatted response
    """
    response = {
        "status": status,
        "data": data,
    }
    
    if error:
        response["error"] = error
        response["status"] = "error"
    
    if message:
        response["message"] = message
    
    return jsonify(response) 