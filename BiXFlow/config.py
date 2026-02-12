"""Configuration management for the BiXFlow framework.

This module provides utilities for managing configuration settings for the BiXFlow framework.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from BiXFlow.exceptions import ConfigurationError


class MCPConfig:
    """Manages MCP server configurations."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file.
                        If not provided, will look for standard locations.
        """
        self.config_path = config_path or self._find_config_file()
        self._config = self._load_config()
        
    def _find_config_file(self) -> str:
        """Find the configuration file in standard locations.
        
        Returns:
            str: Path to the configuration file
            
        Raises:
            ConfigurationError: If no configuration file is found
        """
        # Check standard locations
        standard_paths = [
            Path("mcps") / "mcp_servers_setting.json",
            Path.home() / ".BiXFlow" / "config.json",
            Path("/etc/BiXFlow/config.json")
        ]
        
        for path in standard_paths:
            if path.exists():
                return str(path)
                
        raise ConfigurationError(
            "MCP configuration file not found. Please provide a config_path "
            "or ensure a configuration file exists in a standard location."
        )
        
    def _load_config(self) -> Dict[str, Any]:
        """Load the configuration from file.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
            
        Raises:
            ConfigurationError: If there is an error loading the configuration
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration from {self.config_path}: {str(e)}")
            
    def get_server_config(self, server_name: str) -> Dict[str, Any]:
        """Get the configuration for a specific server.
        
        Args:
            server_name: Name of the server
            
        Returns:
            Dict[str, Any]: Server configuration
            
        Raises:
            ConfigurationError: If the server is not found in the configuration
        """
        if server_name not in self._config:
            raise ConfigurationError(f"Server '{server_name}' not found in configuration")
            
        return self._config[server_name]
        
    def get_all_servers(self) -> Dict[str, Any]:
        """Get all server configurations.
        
        Returns:
            Dict[str, Any]: All server configurations
        """
        return self._config.copy()
        
    def add_server(self, server_name: str, server_config: Dict[str, Any]) -> None:
        """Add a new server to the configuration.
        
        Args:
            server_name: Name of the server
            server_config: Server configuration dictionary
        """
        self._config[server_name] = server_config
        self._save_config()
        
    def remove_server(self, server_name: str) -> None:
        """Remove a server from the configuration.
        
        Args:
            server_name: Name of the server to remove
            
        Raises:
            ConfigurationError: If the server is not found in the configuration
        """
        if server_name not in self._config:
            raise ConfigurationError(f"Server '{server_name}' not found in configuration")
            
        del self._config[server_name]
        self._save_config()
        
    def _save_config(self) -> None:
        """Save the configuration to file."""
        # Create directory if it doesn't exist
        Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save configuration
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)


# Global configuration instance
_global_config: Optional[MCPConfig] = None


def get_config(config_path: Optional[str] = None) -> MCPConfig:
    """Get the global configuration instance.
    
    Args:
        config_path: Path to the configuration file (only used if creating a new instance)
        
    Returns:
        MCPConfig: Global configuration instance
    """
    global _global_config
    
    if _global_config is None:
        _global_config = MCPConfig(config_path)
        
    return _global_config
