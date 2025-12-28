"""
🔑 Public Interface - Registry Module

Import from here to use the Singleton Model Loader.

Usage:
    from modules.registry.interface import (
        get_model,
        register_model,
        list_models,
        unload_model,
        ModelRegistry,
    )
"""

from .registry import (
    ModelRegistry,
    get_model,
    list_models,
    register_model,
    unload_all_models,
    unload_model,
)

__all__ = [
    "ModelRegistry",
    "get_model",
    "list_models",
    "register_model",
    "unload_all_models",
    "unload_model",
]
