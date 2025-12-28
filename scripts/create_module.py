#!/usr/bin/env python3
"""
🏭 Module Factory - Scaffolding Script

Creates a new module with all the standard files following DAEMON-ONE architecture.

Usage:
    python scripts/create_module.py module_name
    python scripts/create_module.py e_commerce --multi-feature cart payment product

Examples:
    python scripts/create_module.py chatbot
    python scripts/create_module.py e_commerce --multi-feature cart payment
"""

import argparse
import sys
from pathlib import Path

# Project paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
MODULES_DIR = PROJECT_ROOT / "backend" / "modules"


def create_file(path: Path, content: str) -> None:
    """Create a file with content, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n")
    print(f"  ✅ Created: {path.relative_to(PROJECT_ROOT)}")


def create_single_feature_module(module_name: str) -> None:
    """Create a single-feature module."""
    module_dir = MODULES_DIR / module_name

    if module_dir.exists():
        print(f"❌ Module '{module_name}' already exists!")
        sys.exit(1)

    print(f"😈 Creating module: {module_name}")

    # __init__.py
    create_file(
        module_dir / "__init__.py",
        f'''
"""
📦 {module_name.title()} Module

Copy this module from DAEMON-ABYSS or create via:
    just new-module {module_name}
"""
''',
    )

    # apps.py
    class_name = module_name.title().replace("_", "")
    create_file(
        module_dir / "apps.py",
        f'''
"""
😈 {module_name.title()} Module - Django App Configuration
"""

from django.apps import AppConfig


class {class_name}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.{module_name}"
    verbose_name = "{module_name.replace("_", " ").title()}"

    def ready(self):
        """Import receivers to register signal handlers."""
        try:
            from . import receivers  # noqa: F401
        except ImportError:
            pass
''',
    )

    # interface.py
    create_file(
        module_dir / "interface.py",
        f'''
"""
🔑 Public Interface - {module_name.title()} Module

Other modules should ONLY import from here, never from internal files.

Usage:
    from modules.{module_name}.interface import (
        # your exports here
    )
"""

# =============================================================================
# 📖 Read Operations (from selectors.py)
# =============================================================================

from .selectors import (
    # Export read functions here
)

# =============================================================================
# 🔧 Write Operations (from services.py)
# =============================================================================

from .services import (
    # Export write functions here
)

# =============================================================================
# 📋 Explicit Public API
# =============================================================================

__all__ = [
    # List all public functions
]
''',
    )

    # models.py
    create_file(
        module_dir / "models.py",
        f'''
"""
📊 Models - {module_name.title()} Module
"""

from django.db import models
from modules.daemon.interface import TimestampedModel, SoftDeleteModel


# class Example{class_name}(TimestampedModel):
#     """Example model for {module_name}."""
#
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#
#     class Meta:
#         db_table = "{module_name}_example"
#         verbose_name = "{module_name.title()} Example"
''',
    )

    # services.py
    create_file(
        module_dir / "services.py",
        f'''
"""
🔧 Services - Write Operations (CUD)

Business logic for creating, updating, deleting data.
Use @transaction.atomic for data consistency.

Usage:
    from modules.{module_name}.services import create_example
"""

from typing import Optional
from django.db import transaction


# @transaction.atomic
# def create_example(*, name: str, description: str = "") -> Example:
#     """
#     Create a new example.
#
#     Args:
#         name: Example name
#         description: Optional description
#
#     Returns:
#         Created Example instance
#     """
#     return Example.objects.create(name=name, description=description)
''',
    )

    # selectors.py
    create_file(
        module_dir / "selectors.py",
        f'''
"""
📖 Selectors - Read Operations (R)

Query logic for reading data.
Optimize with select_related, prefetch_related.

Usage:
    from modules.{module_name}.selectors import get_example_by_id
"""

from typing import List, Optional


# def get_example_by_id(*, example_id: int) -> Optional[Example]:
#     """
#     Get example by ID.
#
#     Args:
#         example_id: Example primary key
#
#     Returns:
#         Example instance or None
#     """
#     try:
#         return Example.objects.get(id=example_id)
#     except Example.DoesNotExist:
#         return None
''',
    )

    # signals.py
    create_file(
        module_dir / "signals.py",
        f'''
"""
📢 Domain Events - {module_name.title()} Module

Define events that this module emits.
Other modules can subscribe via receivers.

Usage:
    from modules.{module_name}.signals import {module_name}_created
"""

from modules.daemon.interface import domain_event


# Define your domain events
# {module_name}_created = domain_event("{module_name}_created")
# {module_name}_updated = domain_event("{module_name}_updated")
# {module_name}_deleted = domain_event("{module_name}_deleted")
''',
    )

    # receivers.py
    create_file(
        module_dir / "receivers.py",
        f'''
"""
📡 Event Receivers - {module_name.title()} Module

Subscribe to events from other modules.
Register in apps.py ready() method.
"""

from django.dispatch import receiver


# Example: Subscribe to user_created event from daemon module
#
# from modules.daemon.interface import user_created
#
# @receiver(user_created)
# def handle_user_created(sender, user_id, **kwargs):
#     """Handle when a new user is created."""
#     pass
''',
    )

    # conf.py
    create_file(
        module_dir / "conf.py",
        f'''
"""
⚙️ Module Configuration - {module_name.title()}

Define default settings that can be overridden in Django settings.

Usage:
    from modules.{module_name}.conf import settings

    timeout = settings.TIMEOUT

Override in config/settings.py:
    {module_name.upper()} = {{
        "TIMEOUT": 60,
    }}
"""

from modules.daemon.interface import ModuleSettings


class {class_name}Settings(ModuleSettings):
    """Settings for {module_name} module."""

    NAMESPACE = "{module_name.upper()}"

    DEFAULTS = {{
        "ENABLED": True,
        # Add module-specific settings here
    }}


settings = {class_name}Settings()
''',
    )

    # views.py
    create_file(
        module_dir / "views.py",
        f'''
"""
🌐 Views - {module_name.title()} Module

HTMX-friendly views that return HTML fragments.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """Main page for {module_name}."""
    return render(request, "{module_name}/index.html", {{}})


# HTMX Fragment example
# def htmx_list(request: HttpRequest) -> HttpResponse:
#     """Return list as HTML fragment."""
#     items = get_all_items()
#     return render(request, "{module_name}/_list.html", {{"items": items}})
''',
    )

    # urls.py
    create_file(
        module_dir / "urls.py",
        f'''
"""
🔗 URL Configuration - {module_name.title()} Module
"""

from django.urls import path
from . import views

app_name = "{module_name}"

urlpatterns = [
    path("", views.index, name="index"),
    # HTMX endpoints
    # path("htmx/list/", views.htmx_list, name="htmx_list"),
]
''',
    )

    # admin.py
    create_file(
        module_dir / "admin.py",
        f'''
"""
🔧 Admin Configuration - {module_name.title()} Module
"""

from django.contrib import admin

# from .models import Example{class_name}
#
# @admin.register(Example{class_name})
# class Example{class_name}Admin(admin.ModelAdmin):
#     list_display = ["id", "name", "created_at"]
#     search_fields = ["name"]
#     list_filter = ["created_at"]
''',
    )

    # migrations/__init__.py
    create_file(module_dir / "migrations" / "__init__.py", "")

    # templates
    create_file(
        module_dir / "templates" / module_name / "index.html",
        f'''
{{% extends "base.html" %}}

{{% block title %}}{module_name.replace("_", " ").title()} | DAEMON-ONE{{% endblock %}}

{{% block styles %}}
.{module_name}-container {{
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}}
{{% endblock %}}

{{% block content %}}
<div class="{module_name}-container" style="position: relative; z-index: 1;">
    <div class="glass-card" style="padding: 2rem; text-align: center;">
        <h1 class="gradient-text" style="font-size: 2rem; font-weight: bold; margin-bottom: 1rem;">
            {module_name.replace("_", " ").title()}
        </h1>
        <p style="color: var(--text-secondary);">
            Welcome to the {module_name} module.
        </p>
    </div>
</div>
{{% endblock %}}
''',
    )

    create_file(
        module_dir / "templates" / module_name / "_list.html",
        f'''
{{# HTMX Fragment - Use with hx-target #}}
<div id="{module_name}-list">
    {{% for item in items %}}
    <div class="glass-card" style="padding: 1rem; margin-bottom: 0.5rem;">
        {{{{ item.name }}}}
    </div>
    {{% empty %}}
    <p style="color: var(--text-secondary);">No items yet.</p>
    {{% endfor %}}
</div>
''',
    )

    # static
    create_file(
        module_dir / "static" / module_name / "css" / "style.css",
        f"""
/* {module_name.title()} Module Styles */

.{module_name}-container {{
    /* Module-specific styles */
}}
""",
    )

    create_file(
        module_dir / "static" / module_name / "js" / "main.js",
        f"""
// {module_name.title()} Module JavaScript

document.addEventListener('DOMContentLoaded', function() {{
    console.log('😈 {module_name} module loaded');
}});
""",
    )

    print(f"\n✨ Module '{module_name}' created successfully!")
    print(f"📁 Location: {module_dir.relative_to(PROJECT_ROOT)}")
    print("\n📋 Next steps:")
    print("  1. Restart server: just dev")
    print("  2. Add URL to config/urls.py:")
    print(f'     path("{module_name}/", include("modules.{module_name}.urls")),')
    print("  3. Run migrations: just mig")


def create_multi_feature_module(module_name: str, features: list[str]) -> None:
    """Create a multi-feature module with sub-apps."""
    module_dir = MODULES_DIR / module_name

    if module_dir.exists():
        print(f"❌ Module '{module_name}' already exists!")
        sys.exit(1)

    print(f"😈 Creating multi-feature module: {module_name}")
    print(f"   Features: {', '.join(features)}")

    # Root __init__.py
    create_file(
        module_dir / "__init__.py",
        f'''
"""
📦 {module_name.title()} Module (Multi-Feature)

Features: {", ".join(features)}

Copy this module from DAEMON-ABYSS.
"""
''',
    )

    # Root interface.py
    interface_imports = "\n".join([f"# from .{feat}.services import ..." for feat in features])
    create_file(
        module_dir / "interface.py",
        f'''
"""
🔑 Public Interface - {module_name.title()} Module

Aggregates public APIs from all features.
"""

{interface_imports}

__all__ = [
    # List all public functions from all features
]
''',
    )

    # Create each feature
    for feature in features:
        feature_dir = module_dir / feature
        class_name = feature.title().replace("_", "")

        create_file(feature_dir / "__init__.py", "")

        create_file(
            feature_dir / "apps.py",
            f'''
from django.apps import AppConfig


class {class_name}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.{module_name}.{feature}"
    verbose_name = "{module_name.title()} - {feature.title()}"
''',
        )

        create_file(
            feature_dir / "models.py",
            """
from django.db import models
from modules.daemon.interface import TimestampedModel
""",
        )

        create_file(
            feature_dir / "services.py",
            """
from django.db import transaction
""",
        )

        create_file(
            feature_dir / "selectors.py",
            """
from typing import List, Optional
""",
        )

        create_file(feature_dir / "migrations" / "__init__.py", "")

        create_file(
            feature_dir / "templates" / module_name / feature / "index.html",
            f"""
{{% extends "base.html" %}}
{{% block content %}}<h1 class="gradient-text">{feature.title()}</h1>{{% endblock %}}
""",
        )

    print(f"\n✨ Multi-feature module '{module_name}' created!")
    print("\n📋 Add to INSTALLED_APPS (auto-discovered):")
    for feature in features:
        print(f"    modules.{module_name}.{feature}")


def main():
    parser = argparse.ArgumentParser(description="🏭 Create a new DAEMON-ONE module")
    parser.add_argument("module_name", help="Name of the module (snake_case)")
    parser.add_argument(
        "--multi-feature",
        "-m",
        nargs="+",
        metavar="FEATURE",
        help="Create multi-feature module with specified features",
    )

    args = parser.parse_args()

    # Validate module name
    if not args.module_name.replace("_", "").isalnum():
        print("❌ Invalid module name. Use snake_case (e.g., my_module)")
        sys.exit(1)

    # Reserved names
    if args.module_name in ["daemon", "core", "common"]:
        print(f"❌ '{args.module_name}' is a reserved module name.")
        sys.exit(1)

    if args.multi_feature:
        create_multi_feature_module(args.module_name, args.multi_feature)
    else:
        create_single_feature_module(args.module_name)


if __name__ == "__main__":
    main()
