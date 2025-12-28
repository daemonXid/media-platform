# 📦 vision Module (ai)

## 🎯 Role & Objective

vision 모듈의 역할을 여기에 기술하십시오.
(예: AI 기반 분석, 사용자 프로필 관리 등)

## 🏗️ Architecture (Vertical Slice)

- __Logic__: `services.py`, `selectors.py`
- __Data__: `models.py`, `schemas.py` (Pydantic)
- __Interface__: `interface.py` (Other modules should ONLY use this)
- __UI__: HTMX fragments in `templates/vision/`

## 🔌 Integration (DAEMON-ONE)

1. __Export__: `just export ai/vision`
2. __Register__: Add `modules.custom.ai.vision` to `INSTALLED_APPS`
3. __URL__: `path("vision/", include("modules.custom.ai.vision.urls"))`

## 📦 Dependencies

`requirements.txt`를 확인하십시오.
