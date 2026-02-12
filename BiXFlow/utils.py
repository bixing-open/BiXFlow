"""Utility functions for the BiXFlow framework.

This module provides utility functions that supplement the core functionality
of the BiXFlow framework.
"""

import logging
from typing import Dict, Any, List, Union
import yaml
import ast
from logging.handlers import RotatingFileHandler
import logging
from jinja2 import Environment, BaseLoader, StrictUndefined


def get_leaf_key_paths(data: Union[Dict, List], parent_key: str = '', separator: str = '.') -> List[str]:
    """Get all leaf node key paths from a dictionary.
    
    Args:
        data: Input dictionary or list data
        parent_key: Parent path for recursion
        separator: Path separator, defaults to '.'
        
    Returns:
        List of all leaf node key paths
    """
    paths = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            # Build the full path for the current key
            if parent_key:
                current_path = f"{parent_key}{separator}{key}"
            else:
                current_path = key
            
            # Recursively process if value is a dict or list
            if isinstance(value, (dict, list)):
                paths.extend(get_leaf_key_paths(value, current_path, separator))
            else:
                # Leaf node, add to results
                paths.append(current_path)
    
    elif isinstance(data, list):
        # For lists, use [] to represent rather than specific indices
        # Check only the first element to determine structure
        if data:  # Non-empty list
            first_item = data[0]
            current_path = f"{parent_key}[]"
            if isinstance(first_item, (dict, list)):
                paths.extend(get_leaf_key_paths(first_item, current_path, separator))
            else:
                paths.append(current_path)
        else:
            # Empty list case
            current_path = f"{parent_key}[]"
            paths.append(current_path)
    
    return paths


def replace_vars_in_dict(value: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Replace variable placeholders in a dictionary.
    
    Args:
        value: Dictionary containing variable placeholders
        context: Context dictionary for variable replacement
        
    Returns:
        Dictionary with variables replaced. If variables are not found, returns error info:
            {
                "result": "error", 
                "message": "The following variables were not found: var1, var2",
                "missing_vars": ["var1", "var2"]
            }
    """
    # Create Jinja2 environment
    env = Environment(
        loader=BaseLoader(),
        undefined=StrictUndefined,
        autoescape=False
    )
    
    def replace_in_item(item: Any) -> Any:
        """Recursively replace variables in dictionaries, lists, or strings."""
        if isinstance(item, str):
            try:
                # Render using Jinja2 template
                template = env.from_string(item)
                rendered = template.render(**context)
                try:
                    # Try to evaluate as Python literal
                    return ast.literal_eval(rendered)
                except:
                    return rendered
            except Exception as e:
                # If rendering fails, return original string
                return item

        elif isinstance(item, dict):
            # Recursively process dictionary
            return {k: replace_in_item(v) for k, v in item.items()}
        
        elif isinstance(item, list):
            # Recursively process list
            return [replace_in_item(v) for v in item]
        
        return item

    try:
        result = replace_in_item(value)
        if not isinstance(result, dict):
            return {
                "result": "error",
                "message": f"Replacement result is not a dictionary: {result}"
            }
        return result
    except Exception as e:
        return {
            "result": "error",
            "message": f"Error replacing variables: {str(e)}"
        }


def deep_update(target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
    """Deep update target dictionary with source values.
    
    If both target and source have dict values at the same path, merge them.
    
    Args:
        target: Target dictionary to update
        source: Source dictionary with new values
        
    Returns:
        Updated target dictionary
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # If target doesn't have key or its value isn't a dict, add/replace with dict
            target[key] = deep_update(target.get(key, {}), value)
        else:
            # Otherwise, directly update the value
            target[key] = value
    return target


def process_optional_params(
    args: Dict[str, Any], 
    required_params: List[str], 
    input_schema: Dict[str, Any]
) -> Dict[str, Any]:
    """Process optional parameters by setting default values.
    
    Sets default values for keys defined in inputSchema properties but not in args 
    and not in required_params.
    
    Args:
        args: User-provided argument dictionary
        required_params: List of required parameter names
        input_schema: Input schema definition containing properties field
        
    Returns:
        Processed argument dictionary with defaults applied
    """
    # Return early if no args or no inputSchema
    if not args or not input_schema or 'properties' not in input_schema:
        return args or {}
    
    # Get properties definition
    properties = input_schema['properties']
    
    # Create result dictionary, copying original args
    result_args = args.copy()
    
    # Iterate through all keys in properties
    for key, prop_def in properties.items():
        # Check if key meets conditions:
        # 1. Not in args
        # 2. Not in required_params
        # 3. Defined in properties
        if key not in args and key not in required_params:
            # Use default value if available
            if 'default' in prop_def:
                result_args[key] = prop_def['default']
            # Otherwise create appropriate empty value based on type
            elif 'type' in prop_def:
                type_name = prop_def['type']
                if type_name == 'string':
                    result_args[key] = ""
                elif type_name == 'number':
                    result_args[key] = 0
                elif type_name == 'boolean':
                    result_args[key] = False
                elif type_name == 'object':
                    result_args[key] = {}
                elif type_name == 'array':
                    result_args[key] = []
                else:
                    # For unknown types, set to None
                    result_args[key] = None
    
    return result_args


def load_workflow(workflow_path: str) -> Dict[str, Any]:
    """Load a workflow from a YAML file.
    
    Args:
        workflow_path: Path to the workflow YAML file
        
    Returns:
        Dict[str, Any]: Parsed workflow definition
    """
    with open(workflow_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def validate_workflow(workflow: Dict[str, Any]) -> bool:
    """Validate a workflow definition.
    
    Args:
        workflow: Workflow definition dictionary
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Check required fields
    if 'steps' not in workflow:
        return False
        
    if not isinstance(workflow['steps'], list):
        return False
        
    # Validate each step
    for step in workflow['steps']:
        if not isinstance(step, dict):
            return False
            
        # Check required fields in step
        if 'tool' not in step:
            return False
            
        # Check tool format
        if len(step['tool'].split('/')) != 2:
            return False
            
    return True

# Global logger instance for client logging
_LOGGER: Union[logging.Logger, None] = None


def get_logger() -> logging.Logger:
    """Get the client logger instance.
    
    Returns:
        Logger instance
    """
    global _LOGGER
    
    # Return existing logger if already configured
    if _LOGGER is not None:
        return _LOGGER
    
    _LOGGER = logging.getLogger(__name__)
    
    # Avoid duplicate handlers
    if not _LOGGER.handlers:
        log_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(module)s:%(lineno)d] - %(message)s'
        )
        
        # Set up rotating file handler: max 10MB, keep 5 backups
        log_handler = RotatingFileHandler(
            'client.log', 
            maxBytes=10*1024*1024, 
            backupCount=5,
            encoding='utf-8',
            mode='w'
        )
        log_handler.setFormatter(log_formatter)
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.addHandler(log_handler)
    
    return _LOGGER


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Set up logging for the BiXFlow framework.
    
    Args:
        level: Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger('BiXFlow')
    logger.setLevel(level)
    
    # Avoid adding multiple handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger
