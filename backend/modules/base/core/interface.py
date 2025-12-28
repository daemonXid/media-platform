"""
🔑 Public Interface - DAEMON Module

This file defines the PUBLIC API of the DAEMON core module.
Other modules should ONLY import from here, never from internal files.

Usage (from other modules):
    from modules.daemon.interface import (
        # Models
        TimestampedModel,
        SoftDeleteModel,
        # Events
        domain_event,
        user_created,
        # Config
        ModuleSettings,
        daemon_settings,
        # RBAC
        has_permission,
        require_permission,
        # AI (GenAI)
        get_model,
        GenAIClient,
        # User Operations
        get_user_by_id,
        create_user,
    )

DO NOT:
    from modules.daemon.services import create_user  # ❌ Internal!
    from modules.daemon.selectors import get_user_by_id  # ❌ Internal!
"""

# =============================================================================
# 📦 Models
# =============================================================================

# =============================================================================
# 📢 Events
# =============================================================================
from modules.events.interface import (
    domain_event,
    entity_created,
    entity_deleted,
    entity_updated,
    user_created,
    user_deleted,
    user_logged_in,
    user_updated,
)

# =============================================================================
# 🤖 GenAI (AI Client)
# =============================================================================
from modules.genai.interface import (
    GenAIClient,
    GenAIResponse,
)

# =============================================================================
# 🔐 RBAC (Policy-as-Code)
# =============================================================================
from modules.rbac.interface import (
    PermissionAuth,
    PolicyEngine,
    get_user_roles,
    has_permission,
    require_permission,
)

# =============================================================================
# 🗄️ Registry (Singleton Loader)
# =============================================================================
from modules.registry.interface import (
    ModelRegistry,
    get_model,
    register_model,
)

# =============================================================================
# ⚙️ Configuration
# =============================================================================
from .conf import (
    ModuleSettings,
    daemon_settings,
)
from .models import (
    SoftDeleteModel,
    TimestampedModel,
    ULIDModel,
)

# =============================================================================
# 📋 Pydantic Schemas
# =============================================================================
from .schemas import (
    AIAnalysisRequest,
    AIAnalysisResponse,
    BaseSchema,
    ErrorResponse,
    PaginationSchema,
    SuccessResponse,
    TimestampMixin,
    UserCreateSchema,
    UserListSchema,
    UserResponseSchema,
    UserUpdateSchema,
)

# =============================================================================
# 📖 Read Operations (from selectors.py)
# =============================================================================
from .selectors import (
    get_active_users,
    get_user_by_email,
    get_user_by_id,
    user_exists,
)

# =============================================================================
# 🔧 Write Operations (from services.py)
# =============================================================================
from .services import (
    create_user,
    deactivate_user,
    delete_user,
    update_user,
)

# =============================================================================
# ⚡ Rust Accelerators (daemon_one_core)
# =============================================================================

try:
    from daemon_one_core import (
        chunk_text,
        clean_text_for_ai,
        cosine_similarity,
        count_tokens_approx,
        find_top_k_similar,
        rust_hello,
    )
except ImportError:
    # Graceful fallback or mocking if Rust module isn't active
    import logging

    _logger = logging.getLogger(__name__)

    def _rust_missing(*args, **kwargs):
        _logger.warning("🦀 Rust core not found. Running in pure Python mode.")
        return None

    rust_hello = _rust_missing
    count_tokens_approx = lambda t: len(t) // 4
    clean_text_for_ai = lambda t: t.strip()
    chunk_text = lambda t, m: [t]
    cosine_similarity = lambda a, b: 0.0
    find_top_k_similar = lambda q, v, k: []


# =============================================================================
# 📋 Explicit Public API
# =============================================================================

__all__ = [
    "AIAnalysisRequest",
    "AIAnalysisResponse",
    # Schemas
    "BaseSchema",
    "ErrorResponse",
    "GenAIClient",
    "GenAIResponse",
    # AI (GenAI)
    "ModelRegistry",
    # Config
    "ModuleSettings",
    "PaginationSchema",
    "PermissionAuth",
    "PolicyEngine",
    "SoftDeleteModel",
    "SuccessResponse",
    "TimestampMixin",
    # Models
    "TimestampedModel",
    "ULIDModel",
    "UserCreateSchema",
    "UserListSchema",
    "UserResponseSchema",
    "UserUpdateSchema",
    "chunk_text",
    "clean_text_for_ai",
    "cosine_similarity",
    "count_tokens_approx",
    # Write Operations
    "create_user",
    "daemon_settings",
    "deactivate_user",
    "deactivate_user",
    "delete_user",
    "delete_user",
    # Events
    "domain_event",
    "entity_created",
    "entity_deleted",
    "entity_updated",
    "find_top_k_similar",
    "get_active_users",
    "get_model",
    "get_user_by_email",
    # Read Operations
    "get_user_by_id",
    "get_user_roles",
    # RBAC
    "has_permission",
    "register_model",
    "require_permission",
    # Rust Accelerators
    "rust_hello",
    "update_user",
    "user_created",
    "user_deleted",
    "user_exists",
    "user_logged_in",
    "user_updated",
]
