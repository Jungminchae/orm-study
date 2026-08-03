---
name: cli-development
description: uv와 typer를 사용한 파이썬 CLI 개발, 레거시(poetry) 마이그레이션, 프로젝트 구조화 및 코드 리팩토링 작업을 수행할 때 반드시 이 스킬을 사용합니다.
---

# CLI Development 스킬

파이썬 기반 CLI 앱을 현대적이고 깔끔한 구조로 개발하고 마이그레이션하기 위한 지침입니다.

## 1. uv 기반 프로젝트 관리
- 기존 프로젝트가 poetry(`poetry.lock`, `pyproject.toml`의 `tool.poetry`)를 사용 중이라면, `uv init` 또는 `uv add` 등을 통해 uv 기반으로 전환합니다.
- 의존성 설치에는 항상 `uv add <package>` 또는 `uv sync`를 사용합니다.

## 2. Typer 기반 CLI 구축
- `argparse`나 `click` 대신 `typer` 프레임워크를 우선적으로 사용합니다.
- `typer.Typer()` 앱 인스턴스를 만들고, 타입 힌트(`int`, `str`, `bool` 등)를 통해 매개변수와 옵션을 정의합니다.
- 출력 스타일링이 필요한 경우 `rich` 라이브러리와의 통합(`rich.console.Console`)을 고려합니다.

## 3. 구조화 및 모듈화
- 코드는 단일 파일에 몰아넣지 않고, 역할(예: `main.py`, `commands/`, `models/`, `utils/`)에 따라 분리합니다.
- 퀴즈 데이터를 읽고 파싱하는 로직은 CLI 라우팅 로직과 철저히 분리합니다.

## 4. 품질 관리
- 모든 파이썬 파일에 대해 PEP 8 표준을 적용하며, 가능하면 `ruff`를 통해 린트와 포맷팅을 수행합니다.
