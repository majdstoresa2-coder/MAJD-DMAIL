#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD-DMAIL
MAJD-DMAIL-AI-AUTOMATION-MASTERMIND-01.py

FILE 01
SOVEREIGN AUTONOMOUS AI + AUTOMATION COMPANY
FOR THE MAJD-DMAIL DOMAIN PLATFORM

VERSION 4.0.0

============================================================
MAJD-DMAIL — SOVEREIGN DOMAIN PLATFORM
============================================================

SCOPE:
    DOMAINS ONLY

ABSOLUTE AUTHORITY:
    SUPREME_OWNER

PROTECTED:
    01 — THIS MASTERMIND
    02 — PERMANENT CORE

AI MANAGED:
    03
    04
    05

PRIMARY FILE LIMIT:
    5

CURRENT PAYMENT POLICY:
    Payment implementation is outside the current mission.

FORBIDDEN:
    Email hosting
    Mailboxes
    SMTP / IMAP / POP3
    Postfix / Dovecot / Webmail

AUTONOMOUS ENGINEERING PIPELINE:

    DISCOVER
        -> ANALYZE
        -> PLAN
        -> BUILD
        -> VALIDATE
        -> IMPORT
        -> INSPECT ROUTES
        -> INTERNAL API TEST
        -> INSTALL
        -> START / RESTART RUNTIME
        -> LIVE HEALTH VERIFY
        -> TARGETED REPAIR
        -> VERIFY
        -> REPORT
        -> RETRY LATER IF REQUIRED

NO FAKE SUCCESS.

Syntax alone is never platform success.
String presence alone is never runtime success.
HTTP 200 alone is never MAJD-DMAIL health success.
External provider availability is never claimed without verification.
AI failure never replaces useful existing code with a fallback stub.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import importlib.util
import json
import logging
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple


# ============================================================
# IDENTITY / AUTHORITY
# ============================================================

PROJECT_NAME = "MAJD-DMAIL"
PROJECT_KIND = "SOVEREIGN_DOMAIN_PLATFORM"
PROJECT_SCOPE = "DOMAINS_ONLY"
VERSION = "4.0.0"

OWNER_AUTHORITY = "SUPREME_OWNER"
AI_AUTHORITY = "SUBORDINATE_AUTONOMOUS_TECHNICAL_COMPANY"
DESIGNER_AUTHORITY = "SUBORDINATE_AUTONOMOUS_UI_ENGINEER"

THIS_FILENAME = "MAJD-DMAIL-AI-AUTOMATION-MASTERMIND-01.py"
PRIMARY_FILE_02 = "MAJD-DMAIL-CORE-PLATFORM-02.py"

GENERATED_FILES: Dict[str, str] = {
    "03": "MAJD-DMAIL-DOMAIN-INFRASTRUCTURE-03.py",
    "04": "MAJD-DMAIL-COMMERCE-SECURITY-04.py",
    "05": "MAJD-DMAIL-PLATFORM-RUNTIME-05.py",
}

MAX_PRIMARY_FILES = 5

OFFICIAL_UI_DIRNAME = "MAJD-DMAIL-OFFICIAL-UI"
OFFICIAL_UI_INDEX = "index.html"

ROOT = Path(__file__).resolve().parent

DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"
STATE_DIR = ROOT / "state"
BACKUP_DIR = ROOT / "backups"
RUNTIME_DIR = ROOT / "runtime"
UI_DIR = ROOT / OFFICIAL_UI_DIRNAME
UI_INDEX = UI_DIR / OFFICIAL_UI_INDEX

for directory in (
    DATA_DIR,
    LOG_DIR,
    STATE_DIR,
    BACKUP_DIR,
    RUNTIME_DIR,
    UI_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

STATE_FILE = STATE_DIR / "mastermind-state.json"
PLAN_FILE = STATE_DIR / "current-plan.json"
REPORT_FILE = STATE_DIR / "last-report.json"
GAP_FILE = STATE_DIR / "capability-gaps.json"
EVENTS_FILE = LOG_DIR / "mastermind-events.jsonl"
LOG_FILE = LOG_DIR / "mastermind.log"
DESIGN_REPORT_FILE = STATE_DIR / "ui-designer-report.json"
RUNTIME_PID_FILE = RUNTIME_DIR / "majd-dmail-runtime-05.pid"
RUNTIME_STDOUT = LOG_DIR / "runtime-05.stdout.log"
RUNTIME_STDERR = LOG_DIR / "runtime-05.stderr.log"


# ============================================================
# CONFIGURATION
# ============================================================

AI_CONTEXT_SIZE = max(
    4096,
    int(os.getenv("MAJD_AI_NUM_CTX", "8192")),
)

AI_CODE_PREDICT = max(
    2048,
    int(os.getenv("MAJD_AI_CODE_NUM_PREDICT", "8192")),
)

AI_PLAN_PREDICT = max(
    512,
    int(os.getenv("MAJD_AI_PLAN_NUM_PREDICT", "2048")),
)

AI_TEMPERATURE = float(
    os.getenv("MAJD_AI_TEMPERATURE", "0.0")
)

AI_TIMEOUT = max(
    60,
    int(os.getenv("MAJD_AI_TIMEOUT", "900")),
)

AI_REPAIR_ATTEMPTS = max(
    1,
    min(
        4,
        int(os.getenv("MAJD_AI_REPAIR_ATTEMPTS", "3")),
    ),
)

API_PORT = int(
    os.getenv("MAJD_DMAIL_API_PORT", "8080")
)

API_HOST = os.getenv(
    "MAJD_DMAIL_API_HOST",
    "127.0.0.1",
)

RUNTIME_START_TIMEOUT = max(
    5,
    int(os.getenv("MAJD_RUNTIME_START_TIMEOUT", "30")),
)

AUTONOMY_INTERVAL = max(
    60,
    int(os.getenv("MAJD_AUTONOMY_INTERVAL", "300")),
)


# ============================================================
# LOGGING
# ============================================================

logger = logging.getLogger("MAJD_DMAIL_AUTONOMOUS_COMPANY")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


# ============================================================
# PLATFORM CONTRACT
# ============================================================

REQUIRED_API_ENDPOINTS: Dict[str, Tuple[str, ...]] = {
    "health": ("/api/health",),
    "domain_search": ("/api/domains/search",),
    "domain_register": ("/api/domains/register",),
    "domain_renew": ("/api/domains/renew",),
    "domain_transfer": ("/api/domains/transfer",),
    "domain_dns": ("/api/domains/dns",),
    "domain_ssl": ("/api/domains/ssl",),
}

ALL_REQUIRED_ENDPOINTS: Tuple[str, ...] = tuple(
    endpoint
    for endpoints in REQUIRED_API_ENDPOINTS.values()
    for endpoint in endpoints
)

REQUIRED_CAPABILITIES: Dict[str, Dict[str, Any]] = {
    "domain_search": {
        "description": "Domain search.",
        "required_internal": True,
    },
    "domain_availability": {
        "description": "Domain availability.",
        "required_internal": True,
    },
    "domain_registration": {
        "description": "Domain registration orchestration.",
        "required_internal": True,
    },
    "domain_renewal": {
        "description": "Domain renewal orchestration.",
        "required_internal": True,
    },
    "domain_transfer": {
        "description": "Domain transfer orchestration.",
        "required_internal": True,
    },
    "domain_lifecycle": {
        "description": "Domain lifecycle management.",
        "required_internal": True,
    },
    "domain_details": {
        "description": "Domain details and status.",
        "required_internal": True,
    },
    "registrar_adapter": {
        "description": "Registrar adapter.",
        "required_internal": True,
        "external_activation": True,
    },
    "registry_adapter": {
        "description": "Registry/EPP adapter.",
        "required_internal": True,
        "external_activation": True,
    },
    "rdap": {
        "description": "RDAP integration.",
        "required_internal": True,
        "external_activation": True,
    },
    "whois": {
        "description": "WHOIS integration.",
        "required_internal": True,
        "external_activation": True,
    },
    "dns_management": {
        "description": "DNS management.",
        "required_internal": True,
    },
    "nameservers": {
        "description": "Nameserver management.",
        "required_internal": True,
    },
    "dnssec": {
        "description": "DNSSEC management.",
        "required_internal": True,
    },
    "domain_ssl_tls": {
        "description": "Domain SSL/TLS management.",
        "required_internal": True,
    },
    "customer_accounts": {
        "description": "Customer accounts.",
        "required_internal": True,
    },
    "owner_control": {
        "description": "SUPREME_OWNER control.",
        "required_internal": True,
    },
    "authorization": {
        "description": "Authorization.",
        "required_internal": True,
    },
    "security": {
        "description": "Security.",
        "required_internal": True,
    },
    "audit": {
        "description": "Audit.",
        "required_internal": True,
    },
    "monitoring": {
        "description": "Monitoring.",
        "required_internal": True,
    },
    "notifications": {
        "description": "Notifications.",
        "required_internal": True,
    },
    "support": {
        "description": "Support hooks.",
        "required_internal": True,
    },
    "http_api": {
        "description": "Real HTTP API.",
        "required_internal": True,
    },
    "official_ui_integration": {
        "description": "Official UI integration.",
        "required_internal": True,
    },
    "self_repair": {
        "description": "Autonomous repair.",
        "required_internal": True,
    },
    "runtime_health": {
        "description": "Runtime health.",
        "required_internal": True,
    },
}

FORBIDDEN_IMPLEMENTATION_PATTERNS = (
    r"\bpostfix\b",
    r"\bdovecot\b",
    r"\bimap\b",
    r"\bpop3\b",
    r"\bsmtp\b",
    r"\bwebmail\b",
    r"\bmailbox(?:es)?\b",
    r"\bemail[_\s-]?hosting\b",
    r"\bpaid[_\s-]?email\b",
    r"\bprofessional[_\s-]?email\b",
)

DANGEROUS_CODE_PATTERNS = (
    r"\beval\s*\(",
    r"\bexec\s*\(",
    r"\bos\.system\s*\(",
)

PRIMARY_PATTERN = re.compile(
    r"^MAJD-DMAIL-[A-Z0-9\-]+-(0[1-5])\.py$",
    re.IGNORECASE,
)

PLATFORM_MISSION: Dict[str, Any] = {
    "project": PROJECT_NAME,
    "scope": PROJECT_SCOPE,
    "owner_authority": OWNER_AUTHORITY,
    "protected_files": [
        THIS_FILENAME,
        PRIMARY_FILE_02,
    ],
    "ai_managed_files": GENERATED_FILES,
    "required_api_endpoints": ALL_REQUIRED_ENDPOINTS,
    "required_capabilities": REQUIRED_CAPABILITIES,
    "payment_enabled": False,
    "rules": [
        "SUPREME_OWNER is permanently highest authority.",
        "01 and 02 are protected.",
        "AI modifies only 03, 04 and 05.",
        "Never create primary 06+.",
        "Domains only.",
        "No email hosting.",
        "No payment implementation in current mission.",
        "No fake success.",
        "External providers require real verification.",
        "Preserve working code on AI failure.",
        "Validate before install.",
        "Rollback failed replacement.",
        "Runtime health must identify MAJD-DMAIL.",
    ],
}


# ============================================================
# UTILITIES
# ============================================================

def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_text(value: str) -> str:
    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(
        encoding="utf-8",
        errors="replace",
    )


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(read_text(path))
    except Exception:
        return default


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
        text=True,
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            if not content.endswith("\n"):
                handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temp_name, path)

    finally:
        if os.path.exists(temp_name):
            try:
                os.unlink(temp_name)
            except OSError:
                pass


def atomic_write_json(path: Path, payload: Any) -> None:
    atomic_write_text(
        path,
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )


def append_jsonl(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n"
        )


def audit(
    event_type: str,
    *,
    status: str = "INFO",
    details: Optional[Dict[str, Any]] = None,
) -> None:
    payload = {
        "timestamp": utc_now(),
        "project": PROJECT_NAME,
        "scope": PROJECT_SCOPE,
        "owner_authority": OWNER_AUTHORITY,
        "event_type": event_type,
        "status": status,
        "details": details or {},
    }

    append_jsonl(EVENTS_FILE, payload)

    if status.upper() in {"ERROR", "FAILED"}:
        logger.error("%s | %s", event_type, payload["details"])
    else:
        logger.info("%s | %s", event_type, payload["details"])


def syntax_check_content(
    content: str,
) -> Tuple[bool, Optional[str]]:
    try:
        ast.parse(content)
        return True, None
    except SyntaxError as exc:
        return (
            False,
            (
                f"{exc.__class__.__name__}: "
                f"line={exc.lineno}, "
                f"offset={exc.offset}, "
                f"msg={exc.msg}"
            ),
        )


def extract_primary_number(filename: str) -> Optional[int]:
    match = PRIMARY_PATTERN.fullmatch(filename)
    return int(match.group(1)) if match else None


def list_primary_files() -> List[str]:
    return sorted(
        path.name
        for path in ROOT.glob("MAJD-DMAIL-*.py")
        if extract_primary_number(path.name) is not None
    )


def enforce_generated_filename(filename: str) -> int:
    number = extract_primary_number(filename)

    if number not in {3, 4, 5}:
        raise PermissionError(
            "AI may modify only primary files 03, 04 and 05."
        )

    return int(number)


def extract_python_code(text: str) -> str:
    cleaned = text.strip()

    fenced = re.search(
        r"```(?:python)?\s*(.*?)```",
        cleaned,
        re.IGNORECASE | re.DOTALL,
    )

    if fenced:
        cleaned = fenced.group(1).strip()

    return cleaned.rstrip() + "\n"


def extract_html_code(text: str) -> str:
    cleaned = text.strip()

    fenced = re.search(
        r"```(?:html)?\s*(.*?)```",
        cleaned,
        re.IGNORECASE | re.DOTALL,
    )

    if fenced:
        cleaned = fenced.group(1).strip()

    return cleaned.rstrip() + "\n"


def extract_json_object(text: str) -> Optional[Dict[str, Any]]:
    cleaned = text.strip()

    fenced = re.search(
        r"```(?:json)?\s*(.*?)```",
        cleaned,
        re.IGNORECASE | re.DOTALL,
    )

    if fenced:
        cleaned = fenced.group(1).strip()

    try:
        value = json.loads(cleaned)
        return value if isinstance(value, dict) else None
    except Exception:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start >= 0 and end > start:
        try:
            value = json.loads(cleaned[start:end + 1])
            return value if isinstance(value, dict) else None
        except Exception:
            pass

    return None


def backup_existing(path: Path) -> Optional[Path]:
    if not path.exists():
        return None

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    relative = path.relative_to(ROOT)
    safe_name = str(relative).replace("/", "__")

    target = BACKUP_DIR / f"{safe_name}.{stamp}.bak"
    shutil.copy2(path, target)

    audit(
        "BACKUP_CREATED",
        details={
            "source": str(relative),
            "backup": str(target.relative_to(ROOT)),
        },
    )

    return target


def restore_backup(
    backup: Optional[Path],
    target: Path,
) -> bool:
    if backup is None or not backup.exists():
        return False

    shutil.copy2(backup, target)

    audit(
        "BACKUP_RESTORED",
        details={
            "target": str(target.relative_to(ROOT)),
            "backup": str(backup.relative_to(ROOT)),
        },
    )

    return True


def contains_forbidden_implementation(
    content: str,
) -> List[str]:
    return [
        pattern
        for pattern in FORBIDDEN_IMPLEMENTATION_PATTERNS
        if re.search(pattern, content, re.IGNORECASE)
    ]


def dangerous_patterns(content: str) -> List[str]:
    return [
        pattern
        for pattern in DANGEROUS_CODE_PATTERNS
        if re.search(pattern, content)
    ]


def source_metrics(content: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(content)
    except SyntaxError:
        tree = None

    functions = 0
    async_functions = 0
    classes = 0

    if tree:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions += 1
            elif isinstance(node, ast.AsyncFunctionDef):
                async_functions += 1
            elif isinstance(node, ast.ClassDef):
                classes += 1

    endpoint_count = len(
        set(
            re.findall(
                r"/api/[A-Za-z0-9_./{}<>:-]+",
                content,
            )
        )
    )

    return {
        "bytes": len(content.encode("utf-8")),
        "lines": len(content.splitlines()),
        "functions": functions,
        "async_functions": async_functions,
        "classes": classes,
        "api_endpoint_strings": endpoint_count,
    }


def evidence_score(content: str) -> int:
    metrics = source_metrics(content)

    score = min(metrics["lines"], 1000)
    score += metrics["functions"] * 20
    score += metrics["async_functions"] * 25
    score += metrics["classes"] * 30
    score += metrics["api_endpoint_strings"] * 25

    lower = content.lower()

    for term in (
        "domain",
        "registrar",
        "registry",
        "rdap",
        "whois",
        "dns",
        "nameserver",
        "dnssec",
        "ssl",
        "tls",
        "audit",
        "authorization",
        "health",
        "transfer",
        "renew",
        "register",
    ):
        if term in lower:
            score += 15

    return score


# ============================================================
# STATE
# ============================================================

DEFAULT_STATE: Dict[str, Any] = {
    "project": PROJECT_NAME,
    "version": VERSION,
    "owner_authority": OWNER_AUTHORITY,
    "phase": "AUTONOMOUS_ENGINEERING",
    "created_at": None,
    "updated_at": None,
    "last_failure_signature": None,
    "consecutive_same_failure": 0,
}


def load_state() -> Dict[str, Any]:
    state = read_json(STATE_FILE, dict(DEFAULT_STATE))

    if not state.get("created_at"):
        state["created_at"] = utc_now()

    state["project"] = PROJECT_NAME
    state["version"] = VERSION
    state["owner_authority"] = OWNER_AUTHORITY
    state["updated_at"] = utc_now()

    return state


def save_state(state: Dict[str, Any]) -> None:
    state["version"] = VERSION
    state["owner_authority"] = OWNER_AUTHORITY
    state["updated_at"] = utc_now()
    atomic_write_json(STATE_FILE, state)


# ============================================================
# AI PROVIDER
# ============================================================

class AIProvider:

    def __init__(self) -> None:
        self.base_url = os.getenv(
            "MAJD_AI_BASE_URL",
            os.getenv(
                "OLLAMA_BASE_URL",
                "http://127.0.0.1:11434",
            ),
        ).rstrip("/")

        self.model = os.getenv(
            "MAJD_AI_MODEL",
            os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        )

        self.timeout = AI_TIMEOUT

    def health(self) -> Dict[str, Any]:
        request = urllib.request.Request(
            f"{self.base_url}/api/tags",
            method="GET",
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=15,
            ) as response:
                payload = json.loads(
                    response.read().decode(
                        "utf-8",
                        errors="replace",
                    )
                )

            models = [
                item.get("name")
                for item in payload.get("models", [])
                if isinstance(item, dict)
            ]

            requested_available = any(
                name
                and (
                    name == self.model
                    or name.startswith(
                        self.model.split(":")[0] + ":"
                    )
                )
                for name in models
            )

            return {
                "ok": requested_available,
                "provider": "ollama",
                "base_url": self.base_url,
                "requested_model": self.model,
                "requested_model_available": requested_available,
                "available_models": models,
            }

        except Exception as exc:
            return {
                "ok": False,
                "provider": "ollama",
                "base_url": self.base_url,
                "requested_model": self.model,
                "error": repr(exc),
            }

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = AI_TEMPERATURE,
        num_predict: int = AI_CODE_PREDICT,
        json_mode: bool = False,
    ) -> Dict[str, Any]:

        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": (
                system_prompt.strip()
                + "\n\n"
                + user_prompt.strip()
            ),
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_ctx": AI_CONTEXT_SIZE,
                "num_predict": num_predict,
            },
        }

        if json_mode:
            payload["format"] = "json"

        body = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=self.timeout,
            ) as response:
                response_payload = json.loads(
                    response.read().decode(
                        "utf-8",
                        errors="replace",
                    )
                )

            text = str(
                response_payload.get("response", "")
            ).strip()

            done = bool(
                response_payload.get("done", False)
            )

            done_reason = response_payload.get("done_reason")

            result = {
                "ok": bool(text) and done,
                "text": text,
                "provider": "ollama",
                "model": self.model,
                "done": done,
                "done_reason": done_reason,
                "prompt_eval_count": response_payload.get(
                    "prompt_eval_count"
                ),
                "eval_count": response_payload.get(
                    "eval_count"
                ),
                "total_duration": response_payload.get(
                    "total_duration"
                ),
            }

            if not text:
                result["error"] = "empty_generation"
            elif not done:
                result["error"] = "generation_not_completed"

            return result

        except urllib.error.HTTPError as exc:
            return {
                "ok": False,
                "text": "",
                "provider": "ollama",
                "model": self.model,
                "error": f"HTTP {exc.code}: {exc.reason}",
            }

        except Exception as exc:
            return {
                "ok": False,
                "text": "",
                "provider": "ollama",
                "model": self.model,
                "error": repr(exc),
            }


# ============================================================
# DISCOVERY
# ============================================================

class ProjectDiscovery:

    def inspect_file(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {
                "exists": False,
                "path": str(path.relative_to(ROOT)),
            }

        content = read_text(path)
        syntax_ok, syntax_error = syntax_check_content(content)

        return {
            "exists": True,
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256_text(content),
            "syntax_ok": syntax_ok,
            "syntax_error": syntax_error,
            "metrics": source_metrics(content),
            "evidence_score": evidence_score(content),
            "forbidden_hits": contains_forbidden_implementation(
                content
            ),
        }

    def inspect_ui(self) -> Dict[str, Any]:
        if not UI_INDEX.exists():
            return {
                "exists": False,
                "path": str(UI_INDEX.relative_to(ROOT)),
            }

        content = read_text(UI_INDEX)

        endpoints = {
            endpoint: endpoint in content
            for endpoint in ALL_REQUIRED_ENDPOINTS
        }

        return {
            "exists": True,
            "path": str(UI_INDEX.relative_to(ROOT)),
            "sha256": sha256_text(content),
            "bytes": len(content.encode("utf-8")),
            "lines": len(content.splitlines()),
            "rtl": (
                'dir="rtl"' in content.lower()
                or "direction: rtl" in content.lower()
            ),
            "endpoint_declarations": endpoints,
            "declares_all_required_endpoints": all(
                endpoints.values()
            ),
            "has_fetch": "fetch(" in content,
            "forbidden_hits": contains_forbidden_implementation(
                content
            ),
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            "timestamp": utc_now(),
            "project": PROJECT_NAME,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,
            "protected_core": self.inspect_file(
                ROOT / PRIMARY_FILE_02
            ),
            "generated_files": {
                number: self.inspect_file(ROOT / filename)
                for number, filename in GENERATED_FILES.items()
            },
            "official_ui": self.inspect_ui(),
            "primary_files": list_primary_files(),
        }


# ============================================================
# CAPABILITY ANALYZER
# ============================================================

class CapabilityAnalyzer:

    EVIDENCE_TERMS: Dict[str, Sequence[str]] = {
        "domain_search": (
            "domain_search",
            "search_domain",
            "/api/domains/search",
        ),
        "domain_availability": (
            "availability",
            "check_domain",
        ),
        "domain_registration": (
            "register_domain",
            "domain_registration",
            "/api/domains/register",
        ),
        "domain_renewal": (
            "renew_domain",
            "/api/domains/renew",
        ),
        "domain_transfer": (
            "transfer_domain",
            "/api/domains/transfer",
        ),
        "domain_lifecycle": (
            "lifecycle",
            "expiration",
        ),
        "domain_details": (
            "domain_details",
            "domain_info",
            "get_domain",
        ),
        "registrar_adapter": ("registrar",),
        "registry_adapter": ("registry", "epp"),
        "rdap": ("rdap",),
        "whois": ("whois",),
        "dns_management": (
            "dns_record",
            "/api/domains/dns",
        ),
        "nameservers": ("nameserver",),
        "dnssec": ("dnssec",),
        "domain_ssl_tls": (
            "ssl",
            "tls",
            "/api/domains/ssl",
        ),
        "customer_accounts": (
            "customer",
            "account",
        ),
        "owner_control": (
            "supreme_owner",
            "owner_control",
        ),
        "authorization": (
            "authorization",
            "permission",
        ),
        "security": (
            "security",
            "validate",
        ),
        "audit": ("audit",),
        "monitoring": (
            "monitor",
            "health",
        ),
        "notifications": (
            "notification",
            "notify",
        ),
        "support": (
            "support",
            "ticket",
        ),
        "http_api": (
            "/api/health",
            "flask",
            "fastapi",
        ),
        "official_ui_integration": (
            "/api/domains/search",
            "fetch(",
        ),
        "self_repair": (
            "repair",
            "retry",
        ),
        "runtime_health": (
            "/api/health",
            "health",
        ),
    }

    def analyze(
        self,
        snapshot: Dict[str, Any],
    ) -> Dict[str, Any]:

        texts: List[str] = []

        core = ROOT / PRIMARY_FILE_02
        if core.exists():
            texts.append(read_text(core))

        for filename in GENERATED_FILES.values():
            path = ROOT / filename
            if path.exists():
                texts.append(read_text(path))

        if UI_INDEX.exists():
            texts.append(read_text(UI_INDEX))

        combined = "\n".join(texts).lower()

        capabilities: Dict[str, Any] = {}

        for name, specification in REQUIRED_CAPABILITIES.items():
            terms = self.EVIDENCE_TERMS.get(name, (name,))

            evidence = [
                term
                for term in terms
                if term.lower() in combined
            ]

            capabilities[name] = {
                "status": (
                    "EVIDENCED"
                    if evidence
                    else "MISSING"
                ),
                "description": specification["description"],
                "evidence": evidence,
                "verified": False,
                "external_activation": bool(
                    specification.get("external_activation")
                ),
            }

        missing = [
            name
            for name, item in capabilities.items()
            if item["status"] == "MISSING"
        ]

        result = {
            "timestamp": utc_now(),
            "capabilities": capabilities,
            "missing": missing,
            "missing_count": len(missing),
        }

        atomic_write_json(GAP_FILE, result)
        return result


# ============================================================
# PLANNER
# ============================================================

class PlatformPlanner:

    def __init__(self, ai: AIProvider) -> None:
        self.ai = ai

    def embedded_plan(
        self,
        discovery: Dict[str, Any],
        gaps: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "timestamp": utc_now(),
            "project": PROJECT_NAME,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,
            "mission": PLATFORM_MISSION,
            "current_state": discovery,
            "gaps": gaps,
            "generated_files": GENERATED_FILES,
            "strategy": [
                "Preserve 01 and 02.",
                "Coordinate 03/04/05.",
                "Repair exact failures.",
                "Implement seven required API contracts.",
                "Inspect real routes.",
                "Test runtime internally.",
                "Start runtime before live verification.",
                "Verify MAJD-DMAIL identity.",
                "Do not modify valid UI unnecessarily.",
            ],
            "source": "embedded_complete_platform_mission",
        }

    def create(
        self,
        discovery: Dict[str, Any],
        gaps: Dict[str, Any],
        *,
        use_ai: bool = True,
    ) -> Dict[str, Any]:

        plan = self.embedded_plan(discovery, gaps)

        # Do not waste a large model request when there are no
        # structural gaps requiring architecture reconsideration.
        if not use_ai or gaps.get("missing_count", 0) == 0:
            atomic_write_json(PLAN_FILE, plan)
            return plan

        health = self.ai.health()

        if not health.get("ok"):
            plan["ai_planning"] = {
                "used": False,
                "reason": "AI unavailable",
                "health": health,
            }
            atomic_write_json(PLAN_FILE, plan)
            return plan

        system_prompt = f"""
You are MAJD-DMAIL chief autonomous architect.

PROJECT: {PROJECT_NAME}
SCOPE: {PROJECT_SCOPE}
HIGHEST AUTHORITY: {OWNER_AUTHORITY}

01 and 02 are protected.
Only 03, 04 and 05 are AI-managed.
Never create primary 06+.
No email hosting.
No payment implementation in the current mission.
No fake success.

Return ONLY JSON.

Coordinate exactly these files:
{json.dumps(GENERATED_FILES, indent=2)}

Required API contract:
{json.dumps(ALL_REQUIRED_ENDPOINTS, indent=2)}

Return:
{{
  "summary": "...",
  "files": {{
    "03": {{"filename": "{GENERATED_FILES['03']}", "responsibilities": []}},
    "04": {{"filename": "{GENERATED_FILES['04']}", "responsibilities": []}},
    "05": {{"filename": "{GENERATED_FILES['05']}", "responsibilities": []}}
  }},
  "integration_requirements": [],
  "runtime_requirements": [],
  "verification_requirements": [],
  "priority_gaps": []
}}
"""

        compact_payload = {
            "mission": {
                "project": PROJECT_NAME,
                "scope": PROJECT_SCOPE,
                "owner": OWNER_AUTHORITY,
                "required_endpoints": ALL_REQUIRED_ENDPOINTS,
            },
            "gaps": gaps.get("missing", []),
            "generated_state": discovery.get(
                "generated_files",
                {},
            ),
        }

        result = self.ai.generate(
            system_prompt,
            json.dumps(
                compact_payload,
                ensure_ascii=False,
            ),
            temperature=0.0,
            num_predict=AI_PLAN_PREDICT,
            json_mode=True,
        )

        if not result.get("ok"):
            plan["ai_planning"] = {
                "used": False,
                "reason": "AI planning failed",
                "error": result.get("error"),
            }
            atomic_write_json(PLAN_FILE, plan)
            return plan

        parsed = extract_json_object(result["text"])

        if not parsed:
            atomic_write_json(PLAN_FILE, plan)
            return plan

        files = parsed.get("files")

        if not isinstance(files, dict):
            atomic_write_json(PLAN_FILE, plan)
            return plan

        if set(files.keys()) != {"03", "04", "05"}:
            atomic_write_json(PLAN_FILE, plan)
            return plan

        for number in ("03", "04", "05"):
            if (
                files[number].get("filename")
                != GENERATED_FILES[number]
            ):
                atomic_write_json(PLAN_FILE, plan)
                return plan

        plan["ai_architecture"] = parsed
        plan["source"] = "ai_reviewed_complete_platform_plan"
        plan["ai_planning"] = {
            "used": True,
            "model": result.get("model"),
        }

        atomic_write_json(PLAN_FILE, plan)
        return plan


# ============================================================
# ROUTE INSPECTION
# ============================================================

class RouteInspector:

    @staticmethod
    def literal_routes(content: str) -> Set[str]:
        return set(
            endpoint
            for endpoint in ALL_REQUIRED_ENDPOINTS
            if endpoint in content
        )

    @staticmethod
    def ast_string_literals(content: str) -> Set[str]:
        values: Set[str] = set()

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return values

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, str):
                    values.add(node.value)

        return values

    def source_contract(
        self,
        content: str,
    ) -> Dict[str, Any]:

        literals = self.literal_routes(content)
        strings = self.ast_string_literals(content)

        detected: Set[str] = set(literals)

        for endpoint in ALL_REQUIRED_ENDPOINTS:
            if endpoint in strings:
                detected.add(endpoint)

        missing = [
            endpoint
            for endpoint in ALL_REQUIRED_ENDPOINTS
            if endpoint not in detected
        ]

        lower = content.lower()

        runtime_evidence = any(
            token in lower
            for token in (
                "flask",
                "fastapi",
                "httpserver",
                "basehttprequesthandler",
                "wsgiref",
                "socketserver",
            )
        )

        return {
            "ok": not missing and runtime_evidence,
            "detected": sorted(detected),
            "missing": missing,
            "runtime_evidence": runtime_evidence,
        }

    def inspect_imported_routes(
        self,
        module: Any,
    ) -> Dict[str, Any]:

        app = getattr(module, "app", None)

        if app is None:
            create_app = getattr(module, "create_app", None)

            if callable(create_app):
                try:
                    app = create_app()
                except Exception as exc:
                    return {
                        "ok": False,
                        "reason": "create_app_failed",
                        "error": repr(exc),
                    }

        if app is None:
            return {
                "ok": False,
                "reason": "application_object_not_discoverable",
            }

        routes: Set[str] = set()

        url_map = getattr(app, "url_map", None)

        if url_map is not None:
            try:
                for rule in url_map.iter_rules():
                    routes.add(str(rule.rule))
            except Exception:
                pass

        missing = [
            endpoint
            for endpoint in ALL_REQUIRED_ENDPOINTS
            if endpoint not in routes
        ]

        return {
            "ok": not missing,
            "routes": sorted(routes),
            "missing": missing,
            "app": app,
        }

    def internal_test(
        self,
        app: Any,
    ) -> Dict[str, Any]:

        test_client_factory = getattr(
            app,
            "test_client",
            None,
        )

        if not callable(test_client_factory):
            return {
                "ok": False,
                "reason": "test_client_not_available",
            }

        results: Dict[str, Any] = {}

        try:
            client = test_client_factory()

            response = client.get("/api/health")

            body: Any = None

            try:
                body = response.get_json()
            except Exception:
                pass

            identity_ok = isinstance(body, dict) and (
                body.get("project") == PROJECT_NAME
                or body.get("service") == PROJECT_NAME
                or body.get("platform") == PROJECT_NAME
            )

            scope_ok = isinstance(body, dict) and (
                body.get("scope") in {
                    PROJECT_SCOPE,
                    "DOMAIN_SERVICES_ONLY",
                    "DOMAINS_ONLY",
                }
                or body.get("project") == PROJECT_NAME
            )

            results["health"] = {
                "status_code": int(response.status_code),
                "json": body,
                "identity_ok": identity_ok,
                "scope_ok": scope_ok,
            }

            return {
                "ok": (
                    200 <= int(response.status_code) < 300
                    and identity_ok
                    and scope_ok
                ),
                "results": results,
            }

        except Exception as exc:
            return {
                "ok": False,
                "reason": "internal_api_test_failed",
                "error": repr(exc),
            }


# ============================================================
# GENERATED CODE VALIDATOR
# ============================================================

class GeneratedCodeValidator:

    def __init__(self) -> None:
        self.routes = RouteInspector()

    def validate(
        self,
        number: str,
        filename: str,
        content: str,
    ) -> Dict[str, Any]:

        enforce_generated_filename(filename)

        syntax_ok, syntax_error = syntax_check_content(content)

        if not syntax_ok:
            return {
                "ok": False,
                "reason": "syntax_error",
                "detail": syntax_error,
            }

        dangerous = dangerous_patterns(content)

        if dangerous:
            return {
                "ok": False,
                "reason": "dangerous_code_pattern",
                "patterns": dangerous,
            }

        forbidden = contains_forbidden_implementation(content)

        if forbidden:
            return {
                "ok": False,
                "reason": "forbidden_non_domain_scope",
                "patterns": forbidden,
            }

        metrics = source_metrics(content)

        if metrics["lines"] < 80:
            return {
                "ok": False,
                "reason": "component_too_small_for_real_platform",
                "metrics": metrics,
            }

        structure_count = (
            metrics["functions"]
            + metrics["async_functions"]
            + metrics["classes"]
        )

        if structure_count < 5:
            return {
                "ok": False,
                "reason": "insufficient_functional_structure",
                "metrics": metrics,
            }

        lower = content.lower()

        if "supreme_owner" not in lower:
            return {
                "ok": False,
                "reason": "owner_authority_not_preserved",
            }

        if "domain" not in lower:
            return {
                "ok": False,
                "reason": "domain_scope_not_evident",
            }

        if number == "03":
            evidence = {
                item: item in lower
                for item in (
                    "registrar",
                    "rdap",
                    "whois",
                    "dns",
                    "nameserver",
                )
            }

            if sum(evidence.values()) < 4:
                return {
                    "ok": False,
                    "reason": "domain_infrastructure_not_implemented",
                    "evidence": evidence,
                }

        if number == "04":
            evidence = {
                item: item in lower
                for item in (
                    "security",
                    "authorization",
                    "audit",
                    "owner",
                    "domain",
                )
            }

            if sum(evidence.values()) < 4:
                return {
                    "ok": False,
                    "reason": "security_control_layer_not_implemented",
                    "evidence": evidence,
                }

        route_contract = None

        if number == "05":
            route_contract = self.routes.source_contract(
                content
            )

            if not route_contract.get("ok"):
                return {
                    "ok": False,
                    "reason": "real_api_contract_not_evident",
                    "route_contract": route_contract,
                    "required_endpoints": ALL_REQUIRED_ENDPOINTS,
                }

        return {
            "ok": True,
            "filename": filename,
            "number": number,
            "sha256": sha256_text(content),
            "metrics": metrics,
            "evidence_score": evidence_score(content),
            "route_contract": route_contract,
        }


# ============================================================
# AUTONOMOUS PLATFORM ENGINEER
# ============================================================

class AutonomousPlatformEngineer:

    def __init__(self, ai: AIProvider) -> None:
        self.ai = ai
        self.validator = GeneratedCodeValidator()

    def _read_context(self) -> Dict[str, str]:
        context: Dict[str, str] = {}

        core = ROOT / PRIMARY_FILE_02

        if core.exists():
            context["02"] = read_text(core)

        for number, filename in GENERATED_FILES.items():
            path = ROOT / filename
            if path.exists():
                context[number] = read_text(path)

        return context

    @staticmethod
    def _bounded_context(
        content: str,
        max_chars: int,
    ) -> str:

        if len(content) <= max_chars:
            return content

        half = max_chars // 2

        return (
            content[:half]
            + "\n# ... MASTERMIND CONTEXT TRUNCATED ...\n"
            + content[-half:]
        )

    def _repair_directive(
        self,
        number: str,
        previous_error: Optional[Dict[str, Any]],
    ) -> str:

        if not previous_error:
            return (
                "Build the requested component completely according "
                "to its platform responsibility."
            )

        encoded = json.dumps(
            previous_error,
            ensure_ascii=False,
        )

        directive = f"""
THIS IS A TARGETED REPAIR ATTEMPT.

The previous candidate failed validation.

Failure:
{encoded}

Do NOT repeat the same failed design.
Correct the exact validation/runtime failure while preserving all
working responsibilities.
"""

        if (
            number == "05"
            and "real_api_contract_not_evident" in encoded
        ):
            directive += f"""

CRITICAL API REPAIR:

The runtime MUST expose ALL of these exact final routes:

{chr(10).join("- " + item for item in ALL_REQUIRED_ENDPOINTS)}

These must be real final HTTP routes.
Do not rely only on dynamically concatenated route strings.
The final route map must contain every path above.
"""

        if number == "05" and (
            "health" in encoded.lower()
            or "runtime" in encoded.lower()
        ):
            directive += f"""

HEALTH CONTRACT:

GET /api/health must return JSON identifying this runtime.

Required identity values:
project = "{PROJECT_NAME}"
scope = "{PROJECT_SCOPE}"
owner_authority = "{OWNER_AUTHORITY}"

Do not return fake provider success.
"""

        return directive

    def generate_candidate(
        self,
        number: str,
        plan: Dict[str, Any],
        discovery: Dict[str, Any],
        gaps: Dict[str, Any],
        *,
        previous_error: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        filename = GENERATED_FILES[number]

        health = self.ai.health()

        if not health.get("ok"):
            return {
                "ok": False,
                "reason": "ai_unavailable",
                "health": health,
            }

        context = self._read_context()

        # Deliberately compact. The old implementation could send
        # enormous 02 + 03 + 04 + 05 + discovery payloads into a
        # relatively small local model context.
        core_context = self._bounded_context(
            context.get("02", ""),
            12000,
        )

        existing_target = self._bounded_context(
            context.get(number, ""),
            18000,
        )

        sibling_context: Dict[str, str] = {}

        for key in ("03", "04", "05"):
            if key == number:
                continue

            sibling_context[key] = self._bounded_context(
                context.get(key, ""),
                7000,
            )

        repair_directive = self._repair_directive(
            number,
            previous_error,
        )

        api_contract = "\n".join(
            f"- {endpoint}"
            for endpoint in ALL_REQUIRED_ENDPOINTS
        )

        system_prompt = f"""
You are the autonomous senior engineering company for MAJD-DMAIL.

PROJECT:
{PROJECT_NAME}

SCOPE:
{PROJECT_SCOPE}

HIGHEST AUTHORITY:
{OWNER_AUTHORITY}

SUPREME_OWNER is permanently above every AI, runtime, provider,
adapter, automation and generated component.

PROTECTED FILES:
- {THIS_FILENAME}
- {PRIMARY_FILE_02}

AI-MANAGED PRIMARY FILES:
- {GENERATED_FILES['03']}
- {GENERATED_FILES['04']}
- {GENERATED_FILES['05']}

CURRENT TARGET:
{filename}

ABSOLUTE RULES:

- Domains only.
- Never create primary 06+.
- Never modify 01 or 02.
- No email hosting.
- No mailbox services.
- No SMTP/IMAP/POP3.
- No Postfix/Dovecot/webmail.
- No payment-provider implementation in current mission.
- No hard-coded credentials.
- No fake provider success.
- No tiny fallback.
- No placeholder implementation.
- No eval().
- No exec().
- No os.system().
- Import must not perform destructive actions.
- Return COMPLETE Python source only.
- Preserve SUPREME_OWNER.
- Include meaningful error handling.
- Include main().
- External providers must expose honest configured/verified state.

{repair_directive}

FILE 03 RESPONSIBILITY:
Real domain infrastructure contracts and adapters, including
registrar/registry/RDAP/WHOIS/DNS/nameservers/DNSSEC/domain TLS as
appropriate.

FILE 04 RESPONSIBILITY:
Domain security, authorization, ownership protection, audit,
monitoring, notification/support hooks and owner controls.
Payment implementation is excluded.

FILE 05 RESPONSIBILITY:
Real HTTP/API runtime and integration layer.

IF CURRENT TARGET IS FILE 05, ALL SEVEN FINAL ROUTES ARE REQUIRED:

{api_contract}

File 05 /api/health MUST identify itself with:
project = "{PROJECT_NAME}"
scope = "{PROJECT_SCOPE}"
owner_authority = "{OWNER_AUTHORITY}"

Registration, renewal, transfer, DNS and SSL endpoints must NEVER
report successful external execution when the required underlying
provider is unavailable or unverified.

Return ONLY complete Python source.
"""

        payload = {
            "target": {
                "number": number,
                "filename": filename,
            },
            "priority_gaps": gaps.get("missing", []),
            "architecture": plan.get(
                "ai_architecture",
                {},
            ),
            "protected_core_02": core_context,
            "existing_target": existing_target,
            "siblings": sibling_context,
            "previous_error": previous_error,
        }

        result = self.ai.generate(
            system_prompt,
            json.dumps(
                payload,
                ensure_ascii=False,
            ),
            temperature=0.0,
            num_predict=AI_CODE_PREDICT,
        )

        if not result.get("ok"):
            return {
                "ok": False,
                "reason": "ai_generation_failed",
                "error": result.get("error"),
                "done": result.get("done"),
                "done_reason": result.get("done_reason"),
                "prompt_eval_count": result.get(
                    "prompt_eval_count"
                ),
                "eval_count": result.get("eval_count"),
            }

        code = extract_python_code(result["text"])

        validation = self.validator.validate(
            number,
            filename,
            code,
        )

        return {
            "ok": bool(validation.get("ok")),
            "code": code,
            "validation": validation,
            "provider": result.get("provider"),
            "model": result.get("model"),
            "done_reason": result.get("done_reason"),
            "prompt_eval_count": result.get(
                "prompt_eval_count"
            ),
            "eval_count": result.get("eval_count"),
        }

    def build_one(
        self,
        number: str,
        plan: Dict[str, Any],
        discovery: Dict[str, Any],
        gaps: Dict[str, Any],
        *,
        force: bool = False,
        repair_error: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        filename = GENERATED_FILES[number]
        path = ROOT / filename

        enforce_generated_filename(filename)

        existing_content = (
            read_text(path)
            if path.exists()
            else ""
        )

        existing_validation = (
            self.validator.validate(
                number,
                filename,
                existing_content,
            )
            if existing_content
            else {
                "ok": False,
                "reason": "missing",
            }
        )

        if existing_validation.get("ok") and not force:
            return {
                "ok": True,
                "action": "existing_component_preserved",
                "file": filename,
                "validation": existing_validation,
            }

        previous_error = (
            repair_error
            or (
                None
                if existing_validation.get("ok")
                else existing_validation
            )
        )

        audit(
            "AUTONOMOUS_ENGINEERING_STARTED",
            details={
                "file": filename,
                "number": number,
                "targeted_repair": bool(previous_error),
            },
        )

        candidate_result: Optional[Dict[str, Any]] = None

        seen_failures: Set[str] = set()

        for attempt in range(1, AI_REPAIR_ATTEMPTS + 1):

            candidate_result = self.generate_candidate(
                number,
                plan,
                discovery,
                gaps,
                previous_error=previous_error,
            )

            if candidate_result.get("ok"):
                break

            failure_payload = {
                "attempt": attempt,
                "reason": candidate_result.get("reason"),
                "validation": candidate_result.get("validation"),
                "error": candidate_result.get("error"),
                "done_reason": candidate_result.get("done_reason"),
            }

            signature = sha256_text(
                json.dumps(
                    failure_payload,
                    sort_keys=True,
                    default=str,
                )
            )

            # Prevent identical useless retries inside one build.
            if signature in seen_failures:
                audit(
                    "IDENTICAL_REPAIR_FAILURE_STOPPED",
                    status="ERROR",
                    details={
                        "file": filename,
                        "attempt": attempt,
                        "failure": failure_payload,
                    },
                )
                break

            seen_failures.add(signature)

            previous_error = failure_payload

            audit(
                "AUTONOMOUS_ENGINEERING_ATTEMPT_FAILED",
                status="ERROR",
                details={
                    "file": filename,
                    **failure_payload,
                },
            )

        if not candidate_result or not candidate_result.get("ok"):
            return {
                "ok": False,
                "action": "existing_file_preserved_ai_failed",
                "file": filename,
                "existing_preserved": path.exists(),
                "last_error": candidate_result or {
                    "reason": "no_candidate"
                },
            }

        candidate = candidate_result["code"]
        candidate_validation = candidate_result["validation"]

        old_score = (
            evidence_score(existing_content)
            if existing_content
            else 0
        )

        new_score = evidence_score(candidate)

        if (
            existing_validation.get("ok")
            and old_score > 0
            and new_score < int(old_score * 0.65)
        ):
            return {
                "ok": False,
                "action": "candidate_rejected_regression",
                "file": filename,
                "old_score": old_score,
                "new_score": new_score,
            }

        backup = backup_existing(path)

        atomic_write_text(path, candidate)

        post_write = self.validator.validate(
            number,
            filename,
            read_text(path),
        )

        if not post_write.get("ok"):
            restore_backup(backup, path)

            return {
                "ok": False,
                "action": "candidate_rolled_back",
                "file": filename,
                "validation": post_write,
            }

        audit(
            "AUTONOMOUS_ENGINEERING_COMPLETED",
            details={
                "file": filename,
                "number": number,
                "sha256": post_write.get("sha256"),
                "evidence_score": post_write.get(
                    "evidence_score"
                ),
            },
        )

        return {
            "ok": True,
            "action": "component_built_and_validated",
            "file": filename,
            "validation": candidate_validation,
        }

    def build_all(
        self,
        plan: Dict[str, Any],
        discovery: Dict[str, Any],
        gaps: Dict[str, Any],
        *,
        force: bool = False,
    ) -> Dict[str, Any]:

        if not (ROOT / PRIMARY_FILE_02).exists():
            return {
                "ok": False,
                "blocked": True,
                "reason": f"{PRIMARY_FILE_02} missing",
            }

        results: Dict[str, Any] = {}

        for number in ("03", "04", "05"):

            current = ROOT / GENERATED_FILES[number]

            current_validation = (
                self.validator.validate(
                    number,
                    GENERATED_FILES[number],
                    read_text(current),
                )
                if current.exists()
                else {"ok": False}
            )

            # force means repair invalid components, not destroy valid
            # components merely because a cycle happened.
            should_force = bool(
                force and not current_validation.get("ok")
            )

            results[number] = self.build_one(
                number,
                plan,
                discovery,
                gaps,
                force=should_force,
            )

            discovery = ProjectDiscovery().snapshot()
            gaps = CapabilityAnalyzer().analyze(discovery)

        return {
            "ok": all(
                item.get("ok")
                for item in results.values()
            ),
            "results": results,
        }


# ============================================================
# MODULE LOADER / FUNCTIONAL ROUTE VERIFIER
# ============================================================

class RuntimeModuleVerifier:

    def __init__(self) -> None:
        self.routes = RouteInspector()

    def load_runtime(self) -> Dict[str, Any]:
        path = ROOT / GENERATED_FILES["05"]

        if not path.exists():
            return {
                "ok": False,
                "reason": "runtime_file_missing",
            }

        module_name = (
            "majd_dmail_runtime_verify_"
            + str(int(time.time() * 1000))
        )

        try:
            spec = importlib.util.spec_from_file_location(
                module_name,
                path,
            )

            if spec is None or spec.loader is None:
                raise RuntimeError(
                    "Unable to create module specification."
                )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            return {
                "ok": True,
                "module": module,
            }

        except Exception as exc:
            return {
                "ok": False,
                "reason": "runtime_import_failed",
                "error": repr(exc),
                "traceback": traceback.format_exc(limit=6),
            }

    def verify(self) -> Dict[str, Any]:
        loaded = self.load_runtime()

        if not loaded.get("ok"):
            return loaded

        module = loaded["module"]

        routes = self.routes.inspect_imported_routes(module)

        if not routes.get("ok"):
            safe = {
                key: value
                for key, value in routes.items()
                if key != "app"
            }

            return {
                "ok": False,
                "reason": "runtime_route_map_invalid",
                "route_inspection": safe,
            }

        internal = self.routes.internal_test(
            routes["app"]
        )

        return {
            "ok": bool(internal.get("ok")),
            "routes": routes.get("routes"),
            "internal_test": internal,
        }


# ============================================================
# RUNTIME SUPERVISOR
# ============================================================

class RuntimeSupervisor:

    def runtime_path(self) -> Path:
        return ROOT / GENERATED_FILES["05"]

    def _read_pid(self) -> Optional[int]:
        if not RUNTIME_PID_FILE.exists():
            return None

        try:
            return int(read_text(RUNTIME_PID_FILE).strip())
        except Exception:
            return None

    @staticmethod
    def _pid_alive(pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def stop(self) -> Dict[str, Any]:
        pid = self._read_pid()

        if pid is None:
            return {
                "ok": True,
                "action": "runtime_not_managed_or_not_running",
            }

        if not self._pid_alive(pid):
            try:
                RUNTIME_PID_FILE.unlink()
            except OSError:
                pass

            return {
                "ok": True,
                "action": "stale_pid_removed",
                "pid": pid,
            }

        try:
            os.kill(pid, 15)

            deadline = time.time() + 10

            while time.time() < deadline:
                if not self._pid_alive(pid):
                    break
                time.sleep(0.25)

            if self._pid_alive(pid):
                os.kill(pid, 9)

            try:
                RUNTIME_PID_FILE.unlink()
            except OSError:
                pass

            return {
                "ok": True,
                "action": "runtime_stopped",
                "pid": pid,
            }

        except Exception as exc:
            return {
                "ok": False,
                "action": "runtime_stop_failed",
                "error": repr(exc),
            }

    def start(self) -> Dict[str, Any]:
        path = self.runtime_path()

        if not path.exists():
            return {
                "ok": False,
                "reason": "runtime_file_missing",
            }

        current_pid = self._read_pid()

        if (
            current_pid is not None
            and self._pid_alive(current_pid)
        ):
            return {
                "ok": True,
                "action": "runtime_already_running",
                "pid": current_pid,
            }

        stdout_handle = RUNTIME_STDOUT.open(
            "ab",
            buffering=0,
        )

        stderr_handle = RUNTIME_STDERR.open(
            "ab",
            buffering=0,
        )

        env = os.environ.copy()
        env.setdefault(
            "MAJD_DMAIL_API_PORT",
            str(API_PORT),
        )
        env.setdefault(
            "MAJD_DMAIL_API_HOST",
            API_HOST,
        )

        try:
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(path),
                ],
                cwd=str(ROOT),
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=stdout_handle,
                stderr=stderr_handle,
                start_new_session=True,
            )

            atomic_write_text(
                RUNTIME_PID_FILE,
                str(process.pid),
            )

            time.sleep(1.0)

            if process.poll() is not None:
                try:
                    RUNTIME_PID_FILE.unlink()
                except OSError:
                    pass

                return {
                    "ok": False,
                    "reason": "runtime_exited_immediately",
                    "returncode": process.returncode,
                }

            audit(
                "RUNTIME_05_STARTED",
                details={
                    "pid": process.pid,
                    "file": path.name,
                },
            )

            return {
                "ok": True,
                "action": "runtime_started",
                "pid": process.pid,
            }

        except Exception as exc:
            return {
                "ok": False,
                "reason": "runtime_start_failed",
                "error": repr(exc),
            }

        finally:
            stdout_handle.close()
            stderr_handle.close()

    def restart(self) -> Dict[str, Any]:
        stop_result = self.stop()
        start_result = self.start()

        return {
            "ok": bool(start_result.get("ok")),
            "stop": stop_result,
            "start": start_result,
        }


# ============================================================
# LIVE HEALTH VERIFIER
# ============================================================

class LiveHealthVerifier:

    def candidate_urls(self) -> List[str]:
        configured = os.getenv(
            "MAJD_DMAIL_API_BASE_URL",
            "",
        ).strip().rstrip("/")

        urls: List[str] = []

        if configured:
            urls.append(configured)

        urls.append(
            f"http://127.0.0.1:{API_PORT}"
        )

        return list(dict.fromkeys(urls))

    @staticmethod
    def identity_valid(payload: Any) -> bool:
        if not isinstance(payload, dict):
            return False

        project = (
            payload.get("project")
            or payload.get("service")
            or payload.get("platform")
        )

        scope = payload.get("scope")

        owner = (
            payload.get("owner_authority")
            or payload.get("authority")
        )

        if project != PROJECT_NAME:
            return False

        if scope not in {
            PROJECT_SCOPE,
            "DOMAINS_ONLY",
            "DOMAIN_SERVICES_ONLY",
        }:
            return False

        if owner and owner != OWNER_AUTHORITY:
            return False

        return True

    def verify(self) -> Dict[str, Any]:
        attempts: List[Dict[str, Any]] = []

        for base_url in self.candidate_urls():
            url = base_url + "/api/health"

            request = urllib.request.Request(
                url,
                method="GET",
                headers={"Accept": "application/json"},
            )

            try:
                with urllib.request.urlopen(
                    request,
                    timeout=5,
                ) as response:
                    body = response.read().decode(
                        "utf-8",
                        errors="replace",
                    )

                    status_code = int(
                        getattr(response, "status", 200)
                    )

                try:
                    parsed = json.loads(body)
                except Exception:
                    parsed = None

                identity_ok = self.identity_valid(parsed)

                attempt = {
                    "ok": (
                        200 <= status_code < 300
                        and identity_ok
                    ),
                    "url": url,
                    "status_code": status_code,
                    "identity_ok": identity_ok,
                    "json": parsed,
                }

                attempts.append(attempt)

                if attempt["ok"]:
                    return {
                        "ok": True,
                        "base_url": base_url,
                        "health": attempt,
                        "attempts": attempts,
                    }

            except Exception as exc:
                attempts.append(
                    {
                        "ok": False,
                        "url": url,
                        "error": repr(exc),
                    }
                )

        return {
            "ok": False,
            "reason": "no_verified_majd_dmail_live_health",
            "attempts": attempts,
        }

    def wait_for_health(
        self,
        timeout: int = RUNTIME_START_TIMEOUT,
    ) -> Dict[str, Any]:

        deadline = time.time() + timeout
        last: Dict[str, Any] = {}

        while time.time() < deadline:
            last = self.verify()

            if last.get("ok"):
                return last

            time.sleep(1)

        return last or {
            "ok": False,
            "reason": "health_wait_timeout",
        }


# ============================================================
# UI ENGINEER
# ============================================================

class AutonomousUIDesigner:

    def __init__(self, ai: AIProvider) -> None:
        self.ai = ai

    def inspect(self) -> Dict[str, Any]:
        return ProjectDiscovery().inspect_ui()

    def validate_html(self, content: str) -> Dict[str, Any]:
        lower = content.lower()

        if "<html" not in lower or "</html>" not in lower:
            return {
                "ok": False,
                "reason": "invalid_html_document",
            }

        forbidden = contains_forbidden_implementation(content)

        if forbidden:
            return {
                "ok": False,
                "reason": "forbidden_scope",
                "patterns": forbidden,
            }

        missing = [
            endpoint
            for endpoint in ALL_REQUIRED_ENDPOINTS
            if endpoint not in content
        ]

        if missing:
            return {
                "ok": False,
                "reason": "api_contract_missing",
                "missing": missing,
            }

        if "fetch(" not in content:
            return {
                "ok": False,
                "reason": "backend_fetch_integration_missing",
            }

        return {
            "ok": True,
            "sha256": sha256_text(content),
        }

    def improve(
        self,
        platform_report: Dict[str, Any],
        *,
        force: bool = False,
    ) -> Dict[str, Any]:

        inspection = self.inspect()

        # Critical fix:
        # Do not burn an Ollama generation every cycle when the
        # existing official UI already passes its contract.
        ui_currently_valid = bool(
            inspection.get("exists")
            and inspection.get(
                "declares_all_required_endpoints"
            )
            and inspection.get("has_fetch")
            and not inspection.get("forbidden_hits")
        )

        if ui_currently_valid and not force:
            return {
                "ok": True,
                "action": "valid_official_ui_preserved",
            }

        if not UI_INDEX.exists():
            return {
                "ok": False,
                "action": "official_ui_missing",
            }

        health = self.ai.health()

        if not health.get("ok"):
            return {
                "ok": False,
                "action": "existing_ui_preserved_ai_unavailable",
            }

        current = read_text(UI_INDEX)

        system_prompt = f"""
You are MAJD-DMAIL official frontend engineer.

Scope: DOMAINS ONLY.
Highest authority: SUPREME_OWNER.

Preserve useful existing design and Arabic RTL.
No email.
No payment implementation.
Never simulate backend success.

Required backend endpoints:
{json.dumps(ALL_REQUIRED_ENDPOINTS, indent=2)}

Return one complete index.html only.
"""

        result = self.ai.generate(
            system_prompt,
            json.dumps(
                {
                    "current_ui": self._compact_ui(current),
                    "backend_status": {
                        "core_ok": platform_report.get("core_ok"),
                        "api": platform_report.get(
                            "api_source_contract"
                        ),
                    },
                },
                ensure_ascii=False,
            ),
            temperature=0.0,
            num_predict=AI_CODE_PREDICT,
        )

        if not result.get("ok"):
            return {
                "ok": False,
                "action": "existing_ui_preserved_ai_failed",
            }

        candidate = extract_html_code(result["text"])
        validation = self.validate_html(candidate)

        if not validation.get("ok"):
            return {
                "ok": False,
                "action": "ui_candidate_rejected",
                "validation": validation,
            }

        if (
            len(current) > 1000
            and len(candidate) < int(len(current) * 0.55)
        ):
            return {
                "ok": False,
                "action": "ui_candidate_rejected_regression",
            }

        backup = backup_existing(UI_INDEX)
        atomic_write_text(UI_INDEX, candidate)

        final_validation = self.validate_html(
            read_text(UI_INDEX)
        )

        if not final_validation.get("ok"):
            restore_backup(backup, UI_INDEX)

            return {
                "ok": False,
                "action": "ui_rolled_back",
            }

        result_payload = {
            "ok": True,
            "action": "official_ui_improved",
            "validation": final_validation,
        }

        atomic_write_json(
            DESIGN_REPORT_FILE,
            result_payload,
        )

        return result_payload

    @staticmethod
    def _compact_ui(content: str) -> str:
        if len(content) <= 24000:
            return content

        return (
            content[:12000]
            + "\n<!-- CONTEXT TRUNCATED -->\n"
            + content[-12000:]
        )


# ============================================================
# FUNCTIONAL VERIFIER
# ============================================================

class FunctionalVerifier:

    def __init__(
        self,
        validator: GeneratedCodeValidator,
    ) -> None:
        self.validator = validator
        self.runtime_module = RuntimeModuleVerifier()
        self.live = LiveHealthVerifier()

    def verify_primary_policy(self) -> Dict[str, Any]:
        files = list_primary_files()

        violations = [
            filename
            for filename in files
            if (extract_primary_number(filename) or 0) > 5
        ]

        required = [
            THIS_FILENAME,
            PRIMARY_FILE_02,
            *GENERATED_FILES.values(),
        ]

        missing = [
            filename
            for filename in required
            if not (ROOT / filename).exists()
        ]

        return {
            "ok": not violations and not missing,
            "files": files,
            "violations": violations,
            "missing": missing,
        }

    def verify_generated_components(
        self,
    ) -> Dict[str, Any]:

        results: Dict[str, Any] = {}

        for number, filename in GENERATED_FILES.items():
            path = ROOT / filename

            if not path.exists():
                results[number] = {
                    "ok": False,
                    "reason": "missing",
                }
                continue

            results[number] = self.validator.validate(
                number,
                filename,
                read_text(path),
            )

        return {
            "ok": all(
                item.get("ok")
                for item in results.values()
            ),
            "files": results,
        }

    def verify_importability(self) -> Dict[str, Any]:
        results: Dict[str, Any] = {}

        for number, filename in GENERATED_FILES.items():
            path = ROOT / filename

            if not path.exists():
                results[number] = {
                    "ok": False,
                    "reason": "missing",
                }
                continue

            module_name = (
                f"majd_dmail_verify_{number}_"
                f"{int(time.time() * 1000)}"
            )

            try:
                spec = importlib.util.spec_from_file_location(
                    module_name,
                    path,
                )

                if spec is None or spec.loader is None:
                    raise RuntimeError("invalid import spec")

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                results[number] = {
                    "ok": True,
                    "file": filename,
                }

            except Exception as exc:
                results[number] = {
                    "ok": False,
                    "file": filename,
                    "error": repr(exc),
                }

        return {
            "ok": all(
                item.get("ok")
                for item in results.values()
            ),
            "files": results,
        }

    def verify_api_source_contract(
        self,
    ) -> Dict[str, Any]:

        path = ROOT / GENERATED_FILES["05"]

        if not path.exists():
            return {
                "ok": False,
                "reason": "runtime_file_missing",
            }

        return RouteInspector().source_contract(
            read_text(path)
        )

    def verify_ui(self) -> Dict[str, Any]:
        inspection = ProjectDiscovery().inspect_ui()

        return {
            "ok": bool(
                inspection.get("exists")
                and inspection.get(
                    "declares_all_required_endpoints"
                )
                and inspection.get("has_fetch")
                and not inspection.get("forbidden_hits")
            ),
            "inspection": inspection,
        }

    def verify_capabilities(
        self,
        live_health: Dict[str, Any],
    ) -> Dict[str, Any]:

        discovery = ProjectDiscovery().snapshot()
        analysis = CapabilityAnalyzer().analyze(discovery)

        capabilities = analysis["capabilities"]

        if live_health.get("ok"):
            for name in (
                "http_api",
                "runtime_health",
            ):
                if name in capabilities:
                    capabilities[name]["status"] = "VERIFIED"
                    capabilities[name]["verified"] = True

        missing_internal = [
            name
            for name, item in capabilities.items()
            if (
                REQUIRED_CAPABILITIES[name].get(
                    "required_internal"
                )
                and item["status"] == "MISSING"
            )
        ]

        return {
            "ok": not missing_internal,
            "capabilities": capabilities,
            "missing_internal": missing_internal,
        }

    def full(
        self,
        ai: AIProvider,
        *,
        live: bool = True,
    ) -> Dict[str, Any]:

        primary = self.verify_primary_policy()
        generated = self.verify_generated_components()
        imports = self.verify_importability()
        api_source = self.verify_api_source_contract()

        runtime_contract = (
            self.runtime_module.verify()
            if (
                generated.get("files", {})
                .get("05", {})
                .get("ok")
            )
            else {
                "ok": False,
                "reason": "runtime_source_invalid",
            }
        )

        live_health = (
            self.live.verify()
            if live
            else {
                "ok": False,
                "reason": "live_check_not_requested",
            }
        )

        ui = self.verify_ui()

        capabilities = self.verify_capabilities(
            live_health
        )

        internal_structure_ok = bool(
            primary.get("ok")
            and generated.get("ok")
            and imports.get("ok")
            and api_source.get("ok")
            and runtime_contract.get("ok")
            and capabilities.get("ok")
        )

        core_ok = bool(
            internal_structure_ok
            and live_health.get("ok")
            and ui.get("ok")
        )

        external_blockers: List[str] = []

        for name, item in capabilities[
            "capabilities"
        ].items():
            if (
                REQUIRED_CAPABILITIES[name].get(
                    "external_activation"
                )
                and not item.get("verified")
            ):
                external_blockers.append(name)

        production_ready = bool(
            core_ok
            and not external_blockers
        )

        report = {
            "timestamp": utc_now(),
            "project": PROJECT_NAME,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,
            "primary_policy": primary,
            "generated_components": generated,
            "importability": imports,
            "api_source_contract": api_source,
            "runtime_contract": runtime_contract,
            "live_api_health": live_health,
            "official_ui": ui,
            "capabilities": capabilities,
            "ai": ai.health(),
            "internal_structure_ok": internal_structure_ok,
            "core_ok": core_ok,
            "production_ready": production_ready,
            "external_blockers": external_blockers,
            "no_fake_success": True,
        }

        atomic_write_json(REPORT_FILE, report)
        return report


# ============================================================
# TARGETED SELF REPAIR
# ============================================================

class SelfRepairEngine:

    def __init__(
        self,
        engineer: AutonomousPlatformEngineer,
        verifier: FunctionalVerifier,
    ) -> None:
        self.engineer = engineer
        self.verifier = verifier

    def repair(
        self,
        plan: Dict[str, Any],
        discovery: Dict[str, Any],
        gaps: Dict[str, Any],
        verification: Dict[str, Any],
    ) -> Dict[str, Any]:

        results: Dict[str, Any] = {}

        generated = verification.get(
            "generated_components",
            {},
        ).get("files", {})

        imports = verification.get(
            "importability",
            {},
        ).get("files", {})

        api_source = verification.get(
            "api_source_contract",
            {},
        )

        runtime_contract = verification.get(
            "runtime_contract",
            {},
        )

        for number in ("03", "04", "05"):

            reasons: List[Dict[str, Any]] = []

            generated_result = generated.get(number, {})

            if not generated_result.get("ok"):
                reasons.append(
                    {
                        "layer": "generated_validation",
                        "failure": generated_result,
                    }
                )

            import_result = imports.get(number, {})

            if not import_result.get("ok"):
                reasons.append(
                    {
                        "layer": "importability",
                        "failure": import_result,
                    }
                )

            if number == "05":

                if not api_source.get("ok"):
                    reasons.append(
                        {
                            "layer": "api_source_contract",
                            "failure": api_source,
                        }
                    )

                if not runtime_contract.get("ok"):
                    reasons.append(
                        {
                            "layer": "runtime_contract",
                            "failure": runtime_contract,
                        }
                    )

            if not reasons:
                results[number] = {
                    "ok": True,
                    "action": "functional_structure_passed",
                    "file": GENERATED_FILES[number],
                }
                continue

            repair_error = {
                "reason": "targeted_repair_required",
                "failures": reasons,
            }

            results[number] = self.engineer.build_one(
                number,
                plan,
                discovery,
                gaps,
                force=True,
                repair_error=repair_error,
            )

            discovery = ProjectDiscovery().snapshot()
            gaps = CapabilityAnalyzer().analyze(discovery)

        return {
            "ok": all(
                item.get("ok")
                for item in results.values()
            ),
            "results": results,
        }


# ============================================================
# MASTER MIND
# ============================================================

class MajdDmailMastermind:

    def __init__(self) -> None:
        self.state = load_state()

        self.ai = AIProvider()
        self.discovery_engine = ProjectDiscovery()
        self.capability_analyzer = CapabilityAnalyzer()
        self.planner = PlatformPlanner(self.ai)
        self.engineer = AutonomousPlatformEngineer(self.ai)
        self.designer = AutonomousUIDesigner(self.ai)
        self.verifier = FunctionalVerifier(
            self.engineer.validator
        )
        self.repair_engine = SelfRepairEngine(
            self.engineer,
            self.verifier,
        )
        self.runtime = RuntimeSupervisor()
        self.live_health = LiveHealthVerifier()

    def bootstrap(self) -> Dict[str, Any]:
        self.state["phase"] = "AUTONOMOUS_DOMAIN_ENGINEERING"
        save_state(self.state)

        return {
            "ok": True,
            "project": PROJECT_NAME,
            "version": VERSION,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,
            "protected": [
                THIS_FILENAME,
                PRIMARY_FILE_02,
            ],
            "ai_managed": GENERATED_FILES,
            "payment_currently_enabled": False,
        }

    def discover(self) -> Dict[str, Any]:
        discovery = self.discovery_engine.snapshot()
        gaps = self.capability_analyzer.analyze(discovery)

        return {
            "discovery": discovery,
            "capability_analysis": gaps,
        }

    def status(self) -> Dict[str, Any]:
        report = read_json(REPORT_FILE, {})

        return {
            "timestamp": utc_now(),
            "project": PROJECT_NAME,
            "version": VERSION,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,
            "phase": self.state.get("phase"),
            "primary_files": list_primary_files(),
            "official_ui": self.designer.inspect(),
            "ai": self.ai.health(),
            "last_verification": {
                "core_ok": report.get("core_ok"),
                "production_ready": report.get(
                    "production_ready"
                ),
                "external_blockers": report.get(
                    "external_blockers"
                ),
            },
        }

    def plan(
        self,
        *,
        use_ai: bool = True,
    ) -> Dict[str, Any]:

        discovery = self.discovery_engine.snapshot()
        gaps = self.capability_analyzer.analyze(discovery)

        return self.planner.create(
            discovery,
            gaps,
            use_ai=use_ai,
        )

    def build(
        self,
        *,
        force: bool = False,
    ) -> Dict[str, Any]:

        discovery = self.discovery_engine.snapshot()
        gaps = self.capability_analyzer.analyze(discovery)

        plan = self.planner.create(
            discovery,
            gaps,
            use_ai=True,
        )

        return self.engineer.build_all(
            plan,
            discovery,
            gaps,
            force=force,
        )

    def verify(self) -> Dict[str, Any]:
        return self.verifier.full(
            self.ai,
            live=True,
        )

    def repair(self) -> Dict[str, Any]:
        discovery = self.discovery_engine.snapshot()
        gaps = self.capability_analyzer.analyze(discovery)

        plan = self.planner.create(
            discovery,
            gaps,
            use_ai=True,
        )

        before = self.verifier.full(
            self.ai,
            live=False,
        )

        repair = self.repair_engine.repair(
            plan,
            discovery,
            gaps,
            before,
        )

        runtime_contract = RuntimeModuleVerifier().verify()

        runtime_result: Dict[str, Any] = {
            "ok": False,
            "reason": "runtime_contract_invalid",
        }

        live = {
            "ok": False,
            "reason": "runtime_not_started",
        }

        if runtime_contract.get("ok"):
            runtime_result = self.runtime.restart()

            if runtime_result.get("ok"):
                live = self.live_health.wait_for_health()

        after = self.verifier.full(
            self.ai,
            live=True,
        )

        return {
            "ok": bool(after.get("core_ok")),
            "repair": repair,
            "runtime": runtime_result,
            "live_health": live,
            "after": after,
        }

    def design(self) -> Dict[str, Any]:
        verification = self.verifier.full(
            self.ai,
            live=True,
        )

        return self.designer.improve(
            verification
        )

    def cycle(self) -> Dict[str, Any]:

        started_at = utc_now()

        audit(
            "AUTONOMOUS_ENGINEERING_CYCLE_STARTED",
            details={
                "version": VERSION,
                "scope": PROJECT_SCOPE,
                "owner_authority": OWNER_AUTHORITY,
            },
        )

        discovery = self.discovery_engine.snapshot()
        gaps = self.capability_analyzer.analyze(discovery)

        plan = self.planner.create(
            discovery,
            gaps,
            use_ai=True,
        )

        initial = self.verifier.full(
            self.ai,
            live=True,
        )

        build_result = None
        repair_result = None
        runtime_result = None
        design_result = None

        if not (ROOT / PRIMARY_FILE_02).exists():
            final = initial

        else:
            if not initial.get("internal_structure_ok"):

                build_result = self.engineer.build_all(
                    plan,
                    discovery,
                    gaps,
                    force=True,
                )

                mid = self.verifier.full(
                    self.ai,
                    live=False,
                )

                if not mid.get("internal_structure_ok"):

                    mid_discovery = (
                        self.discovery_engine.snapshot()
                    )

                    mid_gaps = (
                        self.capability_analyzer.analyze(
                            mid_discovery
                        )
                    )

                    repair_result = (
                        self.repair_engine.repair(
                            plan,
                            mid_discovery,
                            mid_gaps,
                            mid,
                        )
                    )

            structural = self.verifier.full(
                self.ai,
                live=False,
            )

            if structural.get("internal_structure_ok"):

                runtime_result = self.runtime.restart()

                if runtime_result.get("ok"):
                    self.live_health.wait_for_health()

            after_runtime = self.verifier.full(
                self.ai,
                live=True,
            )

            # Only invoke AI UI work if UI itself is invalid.
            if not after_runtime.get(
                "official_ui",
                {},
            ).get("ok"):

                design_result = self.designer.improve(
                    after_runtime,
                    force=True,
                )

            else:
                design_result = {
                    "ok": True,
                    "action": "valid_official_ui_preserved",
                }

            final = self.verifier.full(
                self.ai,
                live=True,
            )

        result = {
            "started_at": started_at,
            "finished_at": utc_now(),
            "project": PROJECT_NAME,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,
            "initial_verification": {
                "internal_structure_ok": initial.get(
                    "internal_structure_ok"
                ),
                "core_ok": initial.get("core_ok"),
                "production_ready": initial.get(
                    "production_ready"
                ),
            },
            "build_result": build_result,
            "repair_result": repair_result,
            "runtime_result": runtime_result,
            "design_result": design_result,
            "final_verification": final,
        }

        if final.get("production_ready"):
            phase = "DOMAIN_PLATFORM_PRODUCTION_READY"
        elif final.get("core_ok"):
            phase = "DOMAIN_CORE_VERIFIED_EXTERNAL_BLOCKERS"
        else:
            phase = "AUTONOMOUS_ENGINEERING_CONTINUES"

        self.state["phase"] = phase
        self.state["last_cycle"] = {
            "timestamp": utc_now(),
            "internal_structure_ok": final.get(
                "internal_structure_ok"
            ),
            "core_ok": final.get("core_ok"),
            "production_ready": final.get(
                "production_ready"
            ),
            "external_blockers": final.get(
                "external_blockers"
            ),
        }

        save_state(self.state)

        audit(
            "AUTONOMOUS_ENGINEERING_CYCLE_COMPLETED",
            details=self.state["last_cycle"],
        )

        return result


# ============================================================
# OUTPUT
# ============================================================

def print_json(payload: Any) -> None:
    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    )


# ============================================================
# AUTONOMOUS LOOP
# ============================================================

def run_loop(
    mastermind: MajdDmailMastermind,
    interval: int,
) -> int:

    interval = max(60, int(interval))

    audit(
        "AUTONOMOUS_DOMAIN_COMPANY_LOOP_STARTED",
        details={
            "interval_seconds": interval,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,
        },
    )

    while True:
        try:
            result = mastermind.cycle()
            final = result["final_verification"]

            print_json(
                {
                    "cycle_completed": utc_now(),
                    "internal_structure_ok": final.get(
                        "internal_structure_ok"
                    ),
                    "core_ok": final.get("core_ok"),
                    "production_ready": final.get(
                        "production_ready"
                    ),
                    "external_blockers": final.get(
                        "external_blockers"
                    ),
                }
            )

        except KeyboardInterrupt:
            audit(
                "AUTONOMOUS_DOMAIN_COMPANY_LOOP_STOPPED",
                details={
                    "reason": "keyboard_interrupt"
                },
            )
            return 0

        except Exception as exc:
            audit(
                "AUTONOMOUS_DOMAIN_COMPANY_CYCLE_FAILED",
                status="ERROR",
                details={
                    "error": repr(exc),
                    "traceback": traceback.format_exc(),
                },
            )

        time.sleep(interval)


# ============================================================
# CLI
# ============================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=THIS_FILENAME,
        description=(
            "MAJD-DMAIL sovereign autonomous "
            "domain-platform engineering company"
        ),
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("bootstrap")
    sub.add_parser("status")
    sub.add_parser("discover")

    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument(
        "--no-ai",
        action="store_true",
    )

    build_command = sub.add_parser("build")
    build_command.add_argument(
        "--force",
        action="store_true",
    )

    sub.add_parser("verify")
    sub.add_parser("repair")
    sub.add_parser("design")
    sub.add_parser("cycle")

    runtime_command = sub.add_parser("runtime")
    runtime_command.add_argument(
        "action",
        choices=(
            "start",
            "stop",
            "restart",
            "health",
        ),
    )

    loop_command = sub.add_parser("loop")
    loop_command.add_argument(
        "--interval",
        type=int,
        default=AUTONOMY_INTERVAL,
    )

    return parser


# ============================================================
# MAIN
# ============================================================

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    mastermind = MajdDmailMastermind()

    command = args.command or "cycle"

    if command == "bootstrap":
        result = mastermind.bootstrap()

    elif command == "status":
        result = mastermind.status()

    elif command == "discover":
        result = mastermind.discover()

    elif command == "plan":
        result = mastermind.plan(
            use_ai=not args.no_ai
        )

    elif command == "build":
        result = mastermind.build(
            force=args.force
        )

    elif command == "verify":
        result = mastermind.verify()

    elif command == "repair":
        result = mastermind.repair()

    elif command == "design":
        result = mastermind.design()

    elif command == "cycle":
        result = mastermind.cycle()

    elif command == "runtime":

        if args.action == "start":
            result = mastermind.runtime.start()

        elif args.action == "stop":
            result = mastermind.runtime.stop()

        elif args.action == "restart":
            result = mastermind.runtime.restart()

        else:
            result = mastermind.live_health.verify()

    elif command == "loop":
        return run_loop(
            mastermind,
            args.interval,
        )

    else:
        parser.print_help()
        return 2

    print_json(result)

    if command == "verify":
        return 0 if result.get("core_ok") else 1

    if command == "cycle":
        return (
            0
            if result.get(
                "final_verification",
                {},
            ).get("core_ok")
            else 1
        )

    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
