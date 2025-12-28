"""
🗄️ Registry Module

Singleton Model Loader for heavy objects.
Load once, use forever.

Usage:
    from modules.registry.interface import get_model, register_model

    @register_model("yolo")
    def load_yolo():
        return YOLO("yolov8n.pt")

    model = get_model("yolo")
"""
