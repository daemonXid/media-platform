"""
🧠 Model Registry - Singleton Pattern Model Loader

"Load once, use forever. Keep the model warm in memory."

This module implements the Singleton Model Loader pattern for AI models.
Heavy models are loaded once at startup and kept warm for instant inference.

Usage:
    from modules.cortex.interface import get_model, register_model

    # Register a model loader
    @register_model("pose_detection")
    def load_pose_model():
        import mediapipe as mp
        return mp.solutions.pose.Pose()

    # Get model instance (cached)
    model = get_model("pose_detection")
    result = model.process(image)

Why Singleton?
    ❌ Without: Load model on every request → Slow (seconds of delay)
    ✅ With: Load at server startup → Instant inference
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from threading import Lock
from typing import Any, Generic, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ModelWrapper(Generic[T]):
    """
    Lazy-loading wrapper for a single model.
    Thread-safe initialization.
    """

    def __init__(self, loader: Callable[[], T], name: str):
        self._loader = loader
        self._name = name
        self._instance: T | None = None
        self._lock = Lock()
        self._loaded = False

    def get(self) -> T:
        """Get or create the model instance."""
        if not self._loaded:
            with self._lock:
                if not self._loaded:
                    logger.info(f"🧠 Loading model: {self._name}")
                    self._instance = self._loader()
                    self._loaded = True
                    logger.info(f"✅ Model loaded: {self._name}")
        return self._instance  # type: ignore

    def unload(self) -> None:
        """Unload the model to free memory."""
        with self._lock:
            if self._loaded:
                logger.info(f"🗑️ Unloading model: {self._name}")
                self._instance = None
                self._loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._loaded


class ModelRegistry:
    """
    Central registry for AI models using Singleton pattern.

    Models are loaded lazily on first access and kept warm in memory.
    Thread-safe for concurrent access.

    Example:
        registry = ModelRegistry()

        # Register models
        registry.register("yolo", lambda: YOLO("yolov8n.pt"))
        registry.register("pose", lambda: mp.solutions.pose.Pose())

        # Get models (lazy loaded)
        yolo = registry.get("yolo")
        pose = registry.get("pose")
    """

    _instance: ModelRegistry | None = None
    _lock = Lock()

    def __new__(cls) -> ModelRegistry:
        """Singleton pattern for the registry itself."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._models: dict[str, ModelWrapper] = {}
                    cls._instance._registry_lock = Lock()
        return cls._instance

    def register(self, name: str, loader: Callable[[], Any], preload: bool = False) -> None:
        """
        Register a model loader.

        Args:
            name: Unique identifier for the model
            loader: Callable that returns the model instance
            preload: If True, load immediately instead of lazily
        """
        with self._registry_lock:
            if name in self._models:
                logger.warning(f"⚠️ Model '{name}' already registered, replacing")

            wrapper = ModelWrapper(loader, name)
            self._models[name] = wrapper

            if preload:
                wrapper.get()

    def get(self, name: str) -> Any:
        """
        Get a model instance by name.

        Args:
            name: Model identifier

        Returns:
            The model instance

        Raises:
            KeyError: If model not registered
        """
        if name not in self._models:
            raise KeyError(f"Model '{name}' not registered. Available: {list(self._models.keys())}")

        return self._models[name].get()

    def unload(self, name: str) -> None:
        """Unload a specific model to free memory."""
        if name in self._models:
            self._models[name].unload()

    def unload_all(self) -> None:
        """Unload all models to free memory."""
        for wrapper in self._models.values():
            wrapper.unload()

    def list_models(self) -> list[dict[str, Any]]:
        """List all registered models with their status."""
        return [{"name": name, "loaded": wrapper.is_loaded} for name, wrapper in self._models.items()]

    def is_loaded(self, name: str) -> bool:
        """Check if a model is currently loaded."""
        if name not in self._models:
            return False
        return self._models[name].is_loaded


# ============================================
# 🛠️ Convenience Functions
# ============================================

_registry: ModelRegistry | None = None


def _get_registry() -> ModelRegistry:
    """Get the global model registry."""
    global _registry
    if _registry is None:
        _registry = ModelRegistry()
    return _registry


def get_model(name: str) -> Any:
    """
    Get a model from the global registry.

    Args:
        name: Model identifier

    Returns:
        The model instance (lazy loaded)

    Example:
        model = get_model("pose_detection")
        result = model.process(image)
    """
    return _get_registry().get(name)


def register_model(name: str, preload: bool = False) -> Callable:
    """
    Decorator to register a model loader function.

    Args:
        name: Unique identifier for the model
        preload: If True, load immediately on registration

    Example:
        @register_model("yolo_v8")
        def load_yolo():
            from ultralytics import YOLO
            return YOLO("yolov8n.pt")

        # Later in code
        model = get_model("yolo_v8")
    """

    def decorator(loader: Callable[[], Any]) -> Callable[[], Any]:
        _get_registry().register(name, loader, preload=preload)
        return loader

    return decorator


def list_models() -> list[dict[str, Any]]:
    """List all registered models."""
    return _get_registry().list_models()


def unload_model(name: str) -> None:
    """Unload a model to free memory."""
    _get_registry().unload(name)


def unload_all_models() -> None:
    """Unload all models to free memory."""
    _get_registry().unload_all()
