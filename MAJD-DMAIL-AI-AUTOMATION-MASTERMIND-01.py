#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD-DMAIL
MAJD-DMAIL-AI-AUTOMATION-MASTERMIND-01.py

FILE 01
SOVEREIGN AUTONOMOUS AI + AUTOMATION COMPANY
FOR THE MAJD-DMAIL DOMAIN PLATFORM

============================================================
MAJD-DMAIL — SOVEREIGN DOMAIN PLATFORM
============================================================

PURPOSE
-------
This file is the autonomous technical company, mastermind,
engineering manager, repair engine, verifier, integration manager,
runtime supervisor and UI integration controller for MAJD-DMAIL.

It does NOT merely generate syntactically valid Python files.

Its permanent mission is to continuously inspect MAJD-DMAIL,
discover missing capabilities, plan the work, build or repair the
AI-managed components, integrate them with the protected core and
official UI, run real verification, reject regressions, preserve
working versions, report blockers honestly and retry incomplete work.

============================================================
ABSOLUTE AUTHORITY
============================================================

SUPREME_OWNER is permanently the highest authority.

No AI, agent, automation, generated component, provider, adapter,
runtime, designer or future component may:

- override SUPREME_OWNER
- redefine SUPREME_OWNER
- create authority above SUPREME_OWNER
- reduce owner authority
- remove owner controls
- lock the owner out
- grant itself supreme privileges

============================================================
PROJECT SCOPE
============================================================

MAJD-DMAIL means DOMAIN SERVICES ONLY.

The autonomous system may build everything technically necessary
to complete the domain platform, including components not explicitly
named here, provided they remain inside the domain-platform scope.

CURRENT REQUIRED DOMAIN CAPABILITIES INCLUDE:

- Domain search
- Domain availability
- Domain registration
- Domain renewal
- Domain transfer
- Transfer status
- Domain lifecycle
- Domain details and status
- Registrar adapters
- Registry adapters
- EPP integration where applicable
- RDAP
- WHOIS
- WHOIS/RDAP privacy handling where applicable
- DNS management
- DNS record management
- Nameservers
- DNSSEC
- Domain-related SSL/TLS
- Customer accounts
- Owner control
- Authorization
- Domain ownership protection
- Domain security
- Audit
- Monitoring
- Notifications
- Support integration
- Self-repair
- Health monitoring
- Official MAJD-DMAIL UI
- Real backend integration
- Real HTTP/API layer when required
- Runtime orchestration
- Production readiness verification

PAYMENT IS NOT PART OF THE CURRENT IMPLEMENTATION MISSION.
Do not build or require payment providers in the current mission.

============================================================
FORBIDDEN SCOPE
============================================================

Do NOT build:

- Email hosting
- Mailboxes
- SMTP
- IMAP
- POP3
- Postfix
- Dovecot
- Webmail
- Paid/professional email services
- Unrelated platforms or services

============================================================
PRIMARY FILE POLICY
============================================================

01 = THIS MASTERMIND — protected/manual
02 = PERMANENT CORE — protected/manual
03 = AI-managed
04 = AI-managed
05 = AI-managed

The AI may autonomously determine how responsibilities are distributed
across 03, 04 and 05.

It must NOT create a primary file 06 or higher.

The mastermind may read 02 for integration understanding but must
NEVER automatically overwrite 01 or 02.

============================================================
AUTONOMY
============================================================

Permanent autonomous workflow:

DISCOVER
-> ANALYZE
-> PLAN
-> BUILD
-> INTEGRATE
-> TEST
-> REPAIR
-> VERIFY
-> REPORT
-> RETRY

The owner must not be required to perform routine technical work.

Owner intervention is reserved for genuinely non-delegable matters
such as:

- provider credentials
- legal approval
- identity verification
- irreversible external authorization

============================================================
NO FAKE SUCCESS
============================================================

Syntax success is NOT platform success.

A file containing only health(), constants, placeholders or stubs
is NOT a completed platform component.

Strings containing API paths inside HTML are NOT proof of a backend.

External services are NEVER LIVE unless actually verified.

Missing credentials produce BLOCKED_EXTERNAL, not fake success.

AI timeout/failure must NEVER replace a useful existing file with a
small fallback stub.

core_ok=True requires functional platform verification.

production_ready=True requires stronger runtime and integration
verification and no unresolved required internal capability.

============================================================
REGRESSION PROTECTION
============================================================

Before replacing generated code or UI:

- create backup
- validate candidate
- compare capability evidence
- reject obvious regression
- write candidate
- run post-write validation
- restore backup if validation fails

============================================================
AI ENGINEERING RULE
============================================================

The AI receives the WHOLE PLATFORM MISSION and current project context.

The mastermind does not micromanage implementation placement.

The AI decides how to implement and distribute required functionality
inside 03/04/05 while respecting protected files and authority.

============================================================
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
import tempfile
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


# ============================================================
# IDENTITY / AUTHORITY
# ============================================================

PROJECT_NAME = "MAJD-DMAIL"
PROJECT_KIND = "SOVEREIGN_DOMAIN_PLATFORM"
PROJECT_SCOPE = "DOMAINS_ONLY"
VERSION = "3.0.0"

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
# PLATFORM MISSION
# ============================================================

CAPABILITY_STATUS = (
    "MISSING",
    "IMPLEMENTED",
    "VERIFIED",
    "BLOCKED_EXTERNAL",
)

REQUIRED_CAPABILITIES: Dict[str, Dict[str, Any]] = {
    "domain_search": {
        "description": "Search domain names and candidates.",
        "required_internal": True,
    },
    "domain_availability": {
        "description": "Determine domain availability through real adapters when configured.",
        "required_internal": True,
    },
    "domain_registration": {
        "description": "Domain registration orchestration with authorization and provider adapter.",
        "required_internal": True,
    },
    "domain_renewal": {
        "description": "Domain renewal orchestration and lifecycle validation.",
        "required_internal": True,
    },
    "domain_transfer": {
        "description": "Inbound/outbound domain transfer orchestration and status.",
        "required_internal": True,
    },
    "domain_lifecycle": {
        "description": "Domain lifecycle state management.",
        "required_internal": True,
    },
    "domain_details": {
        "description": "Domain status/details retrieval.",
        "required_internal": True,
    },
    "registrar_adapter": {
        "description": "Extensible registrar adapter contract and real health verification.",
        "required_internal": True,
        "external_activation": True,
    },
    "registry_adapter": {
        "description": "Registry/EPP adapter capability where applicable.",
        "required_internal": True,
        "external_activation": True,
    },
    "rdap": {
        "description": "RDAP integration.",
        "required_internal": True,
        "external_activation": True,
    },
    "whois": {
        "description": "WHOIS integration/fallback where applicable.",
        "required_internal": True,
        "external_activation": True,
    },
    "dns_management": {
        "description": "Domain DNS record management.",
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
        "description": "SSL/TLS lifecycle related to managed domains.",
        "required_internal": True,
    },
    "customer_accounts": {
        "description": "Customer identity/account integration.",
        "required_internal": True,
    },
    "owner_control": {
        "description": "Owner control preserving SUPREME_OWNER authority.",
        "required_internal": True,
    },
    "authorization": {
        "description": "Authorization for ownership-sensitive domain operations.",
        "required_internal": True,
    },
    "security": {
        "description": "Input validation, secure defaults and fail-closed behavior.",
        "required_internal": True,
    },
    "audit": {
        "description": "Auditable important platform/domain actions.",
        "required_internal": True,
    },
    "monitoring": {
        "description": "Platform and provider health monitoring.",
        "required_internal": True,
    },
    "notifications": {
        "description": "Domain lifecycle and operational notification hooks.",
        "required_internal": True,
    },
    "support": {
        "description": "Domain support integration hooks.",
        "required_internal": True,
    },
    "http_api": {
        "description": "Real HTTP API serving the official UI and domain operations.",
        "required_internal": True,
    },
    "official_ui_integration": {
        "description": "Official UI connected to real backend operations.",
        "required_internal": True,
    },
    "self_repair": {
        "description": "Automatic detection and repair of generated components.",
        "required_internal": True,
    },
    "runtime_health": {
        "description": "Real runtime health reporting.",
        "required_internal": True,
    },
}

PAYMENT_CAPABILITIES = {
    "payment",
    "payments",
    "payment_provider",
    "domain_payments",
    "billing_payment",
}

REQUIRED_API_ENDPOINTS: Dict[str, Tuple[str, ...]] = {
    "health": (
        "/api/health",
    ),
    "domain_search": (
        "/api/domains/search",
    ),
    "domain_register": (
        "/api/domains/register",
    ),
    "domain_renew": (
        "/api/domains/renew",
    ),
    "domain_transfer": (
        "/api/domains/transfer",
    ),
    "domain_dns": (
        "/api/domains/dns",
    ),
    "domain_ssl": (
        "/api/domains/ssl",
    ),
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
    r"subprocess\.Popen\s*\(",
)

PLACEHOLDER_PATTERNS = (
    r"\bTODO\b",
    r"\bFIXME\b",
    r"NotImplementedError",
    r"\bpass\s*(?:#.*)?$",
    r"placeholder",
    r"safe[_\s-]?fallback",
    r"stub",
)

PRIMARY_PATTERN = re.compile(
    r"^MAJD-DMAIL-[A-Z0-9\-]+-(0[1-5])\.py$",
    re.IGNORECASE,
)


PLATFORM_MISSION: Dict[str, Any] = {
    "project": PROJECT_NAME,
    "scope": PROJECT_SCOPE,
    "owner_authority": OWNER_AUTHORITY,
    "objective": (
        "Autonomously complete, integrate, operate, test, repair and "
        "continuously improve MAJD-DMAIL as a real domain-services platform."
    ),
    "required_capabilities": REQUIRED_CAPABILITIES,
    "required_api_contracts": REQUIRED_API_ENDPOINTS,
    "protected_files": [
        THIS_FILENAME,
        PRIMARY_FILE_02,
    ],
    "ai_managed_primary_files": GENERATED_FILES,
    "rules": [
        "SUPREME_OWNER is permanently the highest authority.",
        "Never modify or replace primary files 01 or 02 automatically.",
        "Never create primary file 06 or higher.",
        "The current implementation mission is domains only.",
        "Payment implementation is outside the current mission.",
        "Email and mailbox services are forbidden.",
        "AI decides architecture distribution across 03, 04 and 05.",
        "Do not report completion based only on syntax.",
        "Do not accept placeholder-only or health-only generated components.",
        "Do not report an external provider LIVE without real health verification.",
        "Missing external credentials must be BLOCKED_EXTERNAL, not fake success.",
        "Do not replace useful existing code when AI generation fails.",
        "Back up before replacement.",
        "Reject regressions.",
        "Test real API/runtime integration before core_ok.",
        "Official UI must connect to real backend behavior.",
        "Continue retrying incomplete autonomous work.",
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
        with os.fdopen(
            fd,
            "w",
            encoding="utf-8",
        ) as handle:
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

    with path.open(
        "a",
        encoding="utf-8",
    ) as handle:
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
        "project_kind": PROJECT_KIND,
        "source_file": THIS_FILENAME,
        "event_type": event_type,
        "status": status,
        "details": details or {},
    }

    append_jsonl(EVENTS_FILE, payload)

    if status.upper() in {"ERROR", "FAILED"}:
        logger.error(
            "%s | %s",
            event_type,
            payload["details"],
        )
    else:
        logger.info(
            "%s | %s",
            event_type,
            payload["details"],
        )


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


def syntax_check_file(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {
            "ok": False,
            "file": path.name,
            "error": "missing",
        }

    try:
        content = read_text(path)
    except Exception as exc:
        return {
            "ok": False,
            "file": path.name,
            "error": repr(exc),
        }

    ok, error = syntax_check_content(content)

    return {
        "ok": ok,
        "file": path.name,
        "error": error,
        "sha256": sha256_text(content),
        "bytes": len(content.encode("utf-8")),
        "lines": len(content.splitlines()),
    }


def extract_primary_number(filename: str) -> Optional[int]:
    match = PRIMARY_PATTERN.fullmatch(filename)
    if not match:
        return None
    return int(match.group(1))


def list_primary_files() -> List[str]:
    result: List[str] = []

    for path in ROOT.glob("MAJD-DMAIL-*.py"):
        if extract_primary_number(path.name) is not None:
            result.append(path.name)

    return sorted(result)


def enforce_generated_filename(filename: str) -> int:
    number = extract_primary_number(filename)

    if number is None:
        raise ValueError(
            f"Invalid primary filename: {filename}"
        )

    if number not in {3, 4, 5}:
        raise PermissionError(
            "AI may automatically modify only primary files 03, 04 and 05."
        )

    return number


def extract_python_code(text: str) -> str:
    cleaned = text.strip()

    fenced = re.search(
        r"```(?:python)?\s*(.*?)```",
        cleaned,
        re.IGNORECASE | re.DOTALL,
    )

    if fenced:
        cleaned = fenced.group(1).strip()

    if not cleaned.endswith("\n"):
        cleaned += "\n"

    return cleaned


def extract_html_code(text: str) -> str:
    cleaned = text.strip()

    fenced = re.search(
        r"```(?:html)?\s*(.*?)```",
        cleaned,
        re.IGNORECASE | re.DOTALL,
    )

    if fenced:
        cleaned = fenced.group(1).strip()

    if not cleaned.endswith("\n"):
        cleaned += "\n"

    return cleaned


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
            return None

    return None


def backup_existing(path: Path) -> Optional[Path]:
    if not path.exists():
        return None

    stamp = dt.datetime.now().strftime(
        "%Y%m%d-%H%M%S-%f"
    )

    relative = path.relative_to(ROOT)
    safe_name = str(relative).replace("/", "__")

    target = BACKUP_DIR / (
        f"{safe_name}.{stamp}.bak"
    )

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
        if re.search(
            pattern,
            content,
            re.IGNORECASE,
        )
    ]


def dangerous_patterns(content: str) -> List[str]:
    return [
        pattern
        for pattern in DANGEROUS_CODE_PATTERNS
        if re.search(pattern, content)
    ]


def placeholder_hits(content: str) -> List[str]:
    hits: List[str] = []

    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(
            pattern,
            content,
            re.IGNORECASE | re.MULTILINE,
        ):
            hits.append(pattern)

    return hits


def source_metrics(content: str) -> Dict[str, Any]:
    tree: Optional[ast.AST] = None

    try:
        tree = ast.parse(content)
    except SyntaxError:
        pass

    functions = 0
    async_functions = 0
    classes = 0

    if tree is not None:
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

    score = 0
    score += min(metrics["lines"], 1000)
    score += metrics["functions"] * 20
    score += metrics["async_functions"] * 25
    score += metrics["classes"] * 30
    score += metrics["api_endpoint_strings"] * 25

    lower = content.lower()

    evidence_terms = (
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
    )

    for term in evidence_terms:
        if term in lower:
            score += 15

    return score


# ============================================================
# STATE
# ============================================================

DEFAULT_STATE: Dict[str, Any] = {
    "project": PROJECT_NAME,
    "project_kind": PROJECT_KIND,
    "version": VERSION,
    "owner_authority": OWNER_AUTHORITY,
    "phase": "AUTONOMOUS_ENGINEERING",
    "created_at": None,
    "updated_at": None,
    "last_discovery": None,
    "last_plan": None,
    "last_build": None,
    "last_verify": None,
    "last_repair": None,
    "last_design": None,
    "last_cycle": None,
}


def load_state() -> Dict[str, Any]:
    state = read_json(
        STATE_FILE,
        dict(DEFAULT_STATE),
    )

    if not state.get("created_at"):
        state["created_at"] = utc_now()

    state["project"] = PROJECT_NAME
    state["project_kind"] = PROJECT_KIND
    state["version"] = VERSION
    state["owner_authority"] = OWNER_AUTHORITY
    state["updated_at"] = utc_now()

    return state


def save_state(state: Dict[str, Any]) -> None:
    state["owner_authority"] = OWNER_AUTHORITY
    state["version"] = VERSION
    state["updated_at"] = utc_now()

    atomic_write_json(
        STATE_FILE,
        state,
    )


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
            os.getenv(
                "OLLAMA_MODEL",
                "llama3.2:3b",
            ),
        )

        self.timeout = max(
            60,
            int(
                os.getenv(
                    "MAJD_AI_TIMEOUT",
                    "600",
                )
            ),
        )

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
                "ok": True,
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
        temperature: float = 0.1,
    ) -> Dict[str, Any]:
        body = json.dumps(
            {
                "model": self.model,
                "prompt": (
                    system_prompt.strip()
                    + "\n\n"
                    + user_prompt.strip()
                ),
                "stream": False,
                "options": {
                    "temperature": temperature,
                },
            }
        ).encode("utf-8")

        request = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=self.timeout,
            ) as response:
                payload = json.loads(
                    response.read().decode(
                        "utf-8",
                        errors="replace",
                    )
                )

            text = str(
                payload.get("response", "")
            ).strip()

            return {
                "ok": bool(text),
                "text": text,
                "provider": "ollama",
                "model": self.model,
            }

        except urllib.error.HTTPError as exc:
            return {
                "ok": False,
                "text": "",
                "provider": "ollama",
                "model": self.model,
                "error": (
                    f"HTTP {exc.code}: {exc.reason}"
                ),
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
# PROJECT DISCOVERY
# ============================================================

class ProjectDiscovery:

    def inspect_file(
        self,
        path: Path,
    ) -> Dict[str, Any]:
        if not path.exists():
            return {
                "exists": False,
                "path": str(path.relative_to(ROOT)),
            }

        content = read_text(path)

        syntax_ok, syntax_error = syntax_check_content(
            content
        )

        return {
            "exists": True,
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256_text(content),
            "syntax_ok": syntax_ok,
            "syntax_error": syntax_error,
            "metrics": source_metrics(content),
            "evidence_score": evidence_score(content),
            "placeholder_hits": placeholder_hits(content),
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

        endpoint_presence = {
            endpoint: endpoint in content
            for paths in REQUIRED_API_ENDPOINTS.values()
            for endpoint in paths
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
            "endpoint_declarations": endpoint_presence,
            "declares_all_required_endpoints": all(
                endpoint_presence.values()
            ),
            "has_fetch": "fetch(" in content,
            "forbidden_hits": contains_forbidden_implementation(
                content
            ),
        }

    def snapshot(self) -> Dict[str, Any]:
        files: Dict[str, Any] = {}

        for number, filename in GENERATED_FILES.items():
            files[number] = self.inspect_file(
                ROOT / filename
            )

        core = self.inspect_file(
            ROOT / PRIMARY_FILE_02
        )

        snapshot = {
            "timestamp": utc_now(),
            "project": PROJECT_NAME,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,
            "protected_core": core,
            "generated_files": files,
            "official_ui": self.inspect_ui(),
            "primary_files": list_primary_files(),
        }

        return snapshot


# ============================================================
# CAPABILITY DISCOVERY / GAP ANALYSIS
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
            "available",
            "check_domain",
        ),
        "domain_registration": (
            "register_domain",
            "domain_registration",
            "/api/domains/register",
        ),
        "domain_renewal": (
            "renew_domain",
            "domain_renew",
            "/api/domains/renew",
        ),
        "domain_transfer": (
            "transfer_domain",
            "domain_transfer",
            "/api/domains/transfer",
        ),
        "domain_lifecycle": (
            "lifecycle",
            "domain_status",
            "expiration",
        ),
        "domain_details": (
            "domain_details",
            "get_domain",
            "domain_info",
        ),
        "registrar_adapter": (
            "registrar",
            "registraradapter",
            "registrar_adapter",
        ),
        "registry_adapter": (
            "registry",
            "epp",
            "registry_adapter",
        ),
        "rdap": (
            "rdap",
        ),
        "whois": (
            "whois",
        ),
        "dns_management": (
            "dns_record",
            "dnsmanagement",
            "/api/domains/dns",
        ),
        "nameservers": (
            "nameserver",
            "nameservers",
        ),
        "dnssec": (
            "dnssec",
        ),
        "domain_ssl_tls": (
            "ssl",
            "tls",
            "/api/domains/ssl",
        ),
        "customer_accounts": (
            "customer",
            "account",
            "user",
        ),
        "owner_control": (
            "supreme_owner",
            "owner_control",
            "owner",
        ),
        "authorization": (
            "authorization",
            "authorize",
            "permission",
        ),
        "security": (
            "security",
            "csrf",
            "validate",
            "rate_limit",
        ),
        "audit": (
            "audit",
            "audit_event",
        ),
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
            "/api/domains/",
            "httpserver",
            "flask",
            "fastapi",
            "basehttprequesthandler",
        ),
        "official_ui_integration": (
            "/api/domains/search",
            "/api/health",
            "fetch(",
        ),
        "self_repair": (
            "repair",
            "retry",
        ),
        "runtime_health": (
            "/api/health",
            "health(",
            "health_check",
        ),
    }

    def analyze(
        self,
        snapshot: Dict[str, Any],
    ) -> Dict[str, Any]:
        texts: Dict[str, str] = {}

        core_path = ROOT / PRIMARY_FILE_02
        if core_path.exists():
            texts["02"] = read_text(core_path)

        for number, filename in GENERATED_FILES.items():
            path = ROOT / filename
            if path.exists():
                texts[number] = read_text(path)

        if UI_INDEX.exists():
            texts["UI"] = read_text(UI_INDEX)

        combined = "\n".join(texts.values()).lower()

        capabilities: Dict[str, Any] = {}

        for name, specification in REQUIRED_CAPABILITIES.items():
            terms = self.EVIDENCE_TERMS.get(
                name,
                (name,),
            )

            evidence = [
                term
                for term in terms
                if term.lower() in combined
            ]

            status = (
                "IMPLEMENTED"
                if evidence
                else "MISSING"
            )

            capabilities[name] = {
                "status": status,
                "description": specification["description"],
                "evidence": evidence,
                "verified": False,
                "external_activation": bool(
                    specification.get(
                        "external_activation"
                    )
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

        atomic_write_json(
            GAP_FILE,
            result,
        )

        return result


# ============================================================
# PLATFORM ARCHITECT / PLANNER
# ============================================================

class PlatformPlanner:

    def __init__(
        self,
        ai: AIProvider,
    ) -> None:
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
                "Preserve protected files 01 and 02.",
                "Read 02 as integration context.",
                "Treat 03/04/05 as one coordinated generated subsystem.",
                "Implement all missing internal domain capabilities.",
                "Create a real HTTP/API runtime required by the official UI.",
                "Integrate official UI with real backend behavior.",
                "Test syntax, structure, runtime and API behavior.",
                "Reject regressions and fake success.",
                "Report external credential/provider blockers honestly.",
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
        plan = self.embedded_plan(
            discovery,
            gaps,
        )

        if not use_ai:
            atomic_write_json(PLAN_FILE, plan)
            return plan

        health = self.ai.health()

        if not health.get("ok"):
            plan["ai_planning"] = {
                "used": False,
                "reason": "AI provider unavailable",
                "health": health,
            }

            atomic_write_json(PLAN_FILE, plan)
            return plan

        system_prompt = f"""
You are the chief autonomous architect of MAJD-DMAIL.

You are NOT being asked to design one isolated file.

You are responsible for understanding the WHOLE MAJD-DMAIL DOMAIN
PLATFORM and producing a coordinated engineering plan.

SUPREME_OWNER is permanently the highest authority.

ABSOLUTE RULES:

1. DOMAIN SERVICES ONLY.
2. Payment implementation is OUTSIDE the current mission.
3. Do not build email or mailbox services.
4. Files 01 and 02 are protected.
5. You may architect implementation across ONLY primary files:
   03, 04 and 05.
6. Do not create primary file 06 or higher.
7. You decide the technical distribution across 03/04/05.
8. The platform must have real backend behavior.
9. If an HTTP/API layer is required by the UI, implement it.
10. Syntax alone is not success.
11. Placeholder-only components are not acceptable.
12. External providers are not LIVE without real verification.
13. Missing credentials are external blockers, not platform success.
14. Preserve SUPREME_OWNER.
15. Return ONLY valid JSON.

Your plan must tell the engineering system what the WHOLE PLATFORM
still needs, how 03/04/05 cooperate, what integration contracts are
needed, what runtime/API behavior is required and what must be tested.

Do NOT include implementation of payment providers.

Expected JSON structure:

{{
  "summary": "...",
  "files": {{
    "03": {{
      "filename": "{GENERATED_FILES['03']}",
      "responsibilities": ["..."]
    }},
    "04": {{
      "filename": "{GENERATED_FILES['04']}",
      "responsibilities": ["..."]
    }},
    "05": {{
      "filename": "{GENERATED_FILES['05']}",
      "responsibilities": ["..."]
    }}
  }},
  "integration_requirements": ["..."],
  "runtime_requirements": ["..."],
  "verification_requirements": ["..."],
  "priority_gaps": ["..."]
}}
"""

        user_prompt = json.dumps(
            {
                "platform_mission": PLATFORM_MISSION,
                "current_discovery": discovery,
                "capability_gaps": gaps,
            },
            ensure_ascii=False,
            indent=2,
        )

        result = self.ai.generate(
            system_prompt,
            user_prompt,
        )

        if not result.get("ok"):
            plan["ai_planning"] = {
                "used": False,
                "reason": "AI planning request failed",
                "error": result.get("error"),
            }

            atomic_write_json(PLAN_FILE, plan)
            return plan

        parsed = extract_json_object(
            result["text"]
        )

        if not parsed:
            plan["ai_planning"] = {
                "used": False,
                "reason": "AI plan was not valid JSON",
            }

            atomic_write_json(PLAN_FILE, plan)
            return plan

        files = parsed.get("files")

        if not isinstance(files, dict):
            plan["ai_planning"] = {
                "used": False,
                "reason": "AI plan missing files object",
            }

            atomic_write_json(PLAN_FILE, plan)
            return plan

        if set(files.keys()) != {"03", "04", "05"}:
            plan["ai_planning"] = {
                "used": False,
                "reason": "AI plan must coordinate exactly 03/04/05",
            }

            atomic_write_json(PLAN_FILE, plan)
            return plan

        for number in ("03", "04", "05"):
            if files[number].get("filename") != GENERATED_FILES[number]:
                plan["ai_planning"] = {
                    "used": False,
                    "reason": f"AI attempted filename change for {number}",
                }

                atomic_write_json(PLAN_FILE, plan)
                return plan

        plan["ai_architecture"] = parsed
        plan["source"] = "ai_reviewed_complete_platform_plan"
        plan["ai_planning"] = {
            "used": True,
            "provider": result.get("provider"),
            "model": result.get("model"),
        }

        atomic_write_json(
            PLAN_FILE,
            plan,
        )

        return plan


# ============================================================
# GENERATED CODE VALIDATION
# ============================================================

class GeneratedCodeValidator:

    def validate(
        self,
        number: str,
        filename: str,
        content: str,
    ) -> Dict[str, Any]:
        enforce_generated_filename(filename)

        syntax_ok, syntax_error = syntax_check_content(
            content
        )

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

        forbidden = contains_forbidden_implementation(
            content
        )

        if forbidden:
            return {
                "ok": False,
                "reason": "forbidden_non_domain_scope",
                "patterns": forbidden,
            }

        metrics = source_metrics(content)
        placeholders = placeholder_hits(content)

        # Reject the exact class of tiny fallback/stub that previously
        # produced false core_ok.
        if metrics["lines"] < 80:
            return {
                "ok": False,
                "reason": "component_too_small_for_real_platform",
                "metrics": metrics,
            }

        if (
            metrics["functions"]
            + metrics["async_functions"]
            + metrics["classes"]
            < 5
        ):
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

        if "domains_only" not in lower and "domain" not in lower:
            return {
                "ok": False,
                "reason": "domain_scope_not_evident",
            }

        if number == "03":
            required_any = (
                "registrar",
                "rdap",
                "whois",
                "dns",
                "nameserver",
            )

            missing = [
                item
                for item in required_any
                if item not in lower
            ]

            if len(missing) >= len(required_any) - 1:
                return {
                    "ok": False,
                    "reason": "domain_infrastructure_not_implemented",
                    "missing_evidence": missing,
                }

        if number == "04":
            required_any = (
                "security",
                "authorization",
                "audit",
                "owner",
                "domain",
            )

            missing = [
                item
                for item in required_any
                if item not in lower
            ]

            if len(missing) >= len(required_any) - 1:
                return {
                    "ok": False,
                    "reason": "security_control_layer_not_implemented",
                    "missing_evidence": missing,
                }

        if number == "05":
            endpoint_hits = [
                endpoint
                for paths in REQUIRED_API_ENDPOINTS.values()
                for endpoint in paths
                if endpoint in content
            ]

            if len(set(endpoint_hits)) < 5:
                return {
                    "ok": False,
                    "reason": "real_api_contract_not_evident",
                    "endpoint_hits": endpoint_hits,
                }

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

            if not runtime_evidence:
                return {
                    "ok": False,
                    "reason": "http_runtime_not_evident",
                }

        return {
            "ok": True,
            "filename": filename,
            "number": number,
            "sha256": sha256_text(content),
            "metrics": metrics,
            "placeholder_hits": placeholders,
            "evidence_score": evidence_score(content),
        }


# ============================================================
# AUTONOMOUS PLATFORM ENGINEER
# ============================================================

class AutonomousPlatformEngineer:

    def __init__(
        self,
        ai: AIProvider,
    ) -> None:
        self.ai = ai
        self.validator = GeneratedCodeValidator()

    def _read_context(
        self,
    ) -> Dict[str, str]:
        context: Dict[str, str] = {}

        core_path = ROOT / PRIMARY_FILE_02

        if core_path.exists():
            context["02"] = read_text(core_path)

        for number, filename in GENERATED_FILES.items():
            path = ROOT / filename
            if path.exists():
                context[number] = read_text(path)

        return context

    def _bounded_context(
        self,
        content: str,
        max_chars: int = 45000,
    ) -> str:
        if len(content) <= max_chars:
            return content

        head = content[: max_chars // 2]
        tail = content[-max_chars // 2 :]

        return (
            head
            + "\n\n# ... CONTEXT TRUNCATED BY MASTERMIND ...\n\n"
            + tail
        )

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

        core_context = self._bounded_context(
            context.get("02", "")
        )

        sibling_context: Dict[str, str] = {}

        for key in ("03", "04", "05"):
            if key == number:
                continue

            sibling_context[key] = self._bounded_context(
                context.get(key, ""),
                max_chars=22000,
            )

        existing_target = self._bounded_context(
            context.get(number, ""),
            max_chars=40000,
        )

        ai_architecture = plan.get(
            "ai_architecture",
            {},
        )

        system_prompt = f"""
You are the autonomous senior engineering company responsible for
completing MAJD-DMAIL.

THIS IS NOT AN ISOLATED FILE-GENERATION TASK.

You must understand the WHOLE PLATFORM and produce a complete,
production-oriented replacement for the requested AI-managed file
that cooperates with the protected core and sibling generated files.

PROJECT:
{PROJECT_NAME}

SCOPE:
DOMAIN SERVICES ONLY.

HIGHEST AUTHORITY:
SUPREME_OWNER

ABSOLUTE AUTHORITY RULE:
SUPREME_OWNER is permanently above every AI, runtime, adapter,
provider, component and automation.

PROTECTED:
- {THIS_FILENAME}
- {PRIMARY_FILE_02}

AI-MANAGED:
- {GENERATED_FILES['03']}
- {GENERATED_FILES['04']}
- {GENERATED_FILES['05']}

CURRENT TARGET:
{filename}

You decide architecture and implementation details, but you must
remain within the coordinated 03/04/05 platform.

DO NOT:
- create primary 06+
- implement email hosting
- implement mailboxes
- implement SMTP/IMAP/POP3
- implement Postfix/Dovecot/webmail
- implement payment providers in the current mission
- hard-code credentials
- claim external provider LIVE without verification
- use eval()
- use exec()
- use os.system()
- use subprocess.Popen()
- return placeholders or tiny stubs
- return only a health class
- fake success

YOU MUST:
- return COMPLETE Python source
- preserve SUPREME_OWNER
- implement real responsibility for this component
- integrate with the platform architecture
- fail closed
- expose honest health/status
- support real domain operations appropriate to the component
- use adapters for external providers
- distinguish configured/verified external providers from unavailable ones
- provide meaningful error handling
- provide auditability where appropriate
- include main()
- be import-safe
- avoid destructive side effects on import
- be production-oriented
- return ONLY Python source

For file 05 specifically:
- implement a REAL HTTP/API runtime
- implement the official domain API contracts
- connect API operations to actual platform services/adapters
- /api/health must be real
- do not report registration/renewal/transfer/DNS/SSL success when the
  underlying operation failed or provider is unavailable

For file 03 specifically:
- implement real domain infrastructure contracts and provider adapters
- support registrar/registry/RDAP/WHOIS/DNS/nameserver/DNSSEC/domain TLS
  responsibilities as appropriate
- external adapters must have real configuration and health state

For file 04 specifically:
- current mission is NOT payment implementation
- implement domain security, authorization, ownership protection,
  audit, monitoring/notification/support hooks and other required
  non-payment platform control responsibilities
- preserve owner authority

Return ONLY the complete Python source.
"""

        user_payload = {
            "whole_platform_mission": PLATFORM_MISSION,
            "architecture_plan": ai_architecture,
            "discovery": discovery,
            "capability_gaps": gaps,
            "target_file": {
                "number": number,
                "filename": filename,
            },
            "protected_core_02": core_context,
            "existing_target": existing_target,
            "sibling_generated_context": sibling_context,
            "previous_validation_or_runtime_error": previous_error,
        }

        result = self.ai.generate(
            system_prompt,
            json.dumps(
                user_payload,
                ensure_ascii=False,
                indent=2,
            ),
        )

        if not result.get("ok"):
            return {
                "ok": False,
                "reason": "ai_generation_failed",
                "error": result.get("error"),
            }

        code = extract_python_code(
            result["text"]
        )

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
        }

    def build_one(
        self,
        number: str,
        plan: Dict[str, Any],
        discovery: Dict[str, Any],
        gaps: Dict[str, Any],
        *,
        force: bool = False,
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

        if (
            existing_validation.get("ok")
            and not force
        ):
            return {
                "ok": True,
                "action": "existing_component_preserved",
                "file": filename,
                "validation": existing_validation,
            }

        audit(
            "AUTONOMOUS_ENGINEERING_STARTED",
            details={
                "file": filename,
                "number": number,
                "existing_valid": existing_validation.get("ok"),
            },
        )

        previous_error: Optional[Dict[str, Any]] = (
            None
            if existing_validation.get("ok")
            else existing_validation
        )

        candidate_result: Optional[
            Dict[str, Any]
        ] = None

        max_attempts = max(
            2,
            int(
                os.getenv(
                    "MAJD_AI_REPAIR_ATTEMPTS",
                    "4",
                )
            ),
        )

        for attempt in range(
            1,
            max_attempts + 1,
        ):
            candidate_result = self.generate_candidate(
                number,
                plan,
                discovery,
                gaps,
                previous_error=previous_error,
            )

            if candidate_result.get("ok"):
                break

            previous_error = {
                "attempt": attempt,
                "generation_result": {
                    key: value
                    for key, value in candidate_result.items()
                    if key != "code"
                },
            }

            audit(
                "AUTONOMOUS_ENGINEERING_ATTEMPT_FAILED",
                status="ERROR",
                details={
                    "file": filename,
                    "attempt": attempt,
                    "reason": candidate_result.get("reason"),
                    "validation": candidate_result.get("validation"),
                },
            )

        if not candidate_result or not candidate_result.get("ok"):
            # CRITICAL:
            # Never overwrite useful existing code with a fake fallback.
            return {
                "ok": False,
                "action": "existing_file_preserved_ai_failed",
                "file": filename,
                "existing_preserved": path.exists(),
                "last_error": (
                    candidate_result
                    if candidate_result
                    else {
                        "reason": "no_candidate",
                    }
                ),
            }

        candidate = candidate_result["code"]
        candidate_validation = candidate_result[
            "validation"
        ]

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

        atomic_write_text(
            path,
            candidate,
        )

        post_write = self.validator.validate(
            number,
            filename,
            read_text(path),
        )

        if not post_write.get("ok"):
            restore_backup(
                backup,
                path,
            )

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
            "validation": post_write,
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
                "reason": (
                    f"{PRIMARY_FILE_02} is required and protected."
                ),
            }

        results: Dict[str, Any] = {}

        # Build infrastructure/security before runtime so 05 can inspect
        # the newest sibling implementations.
        for number in (
            "03",
            "04",
            "05",
        ):
            results[number] = self.build_one(
                number,
                plan,
                discovery,
                gaps,
                force=force,
            )

            # Refresh discovery context after each successful component.
            discovery = ProjectDiscovery().snapshot()
            gaps = CapabilityAnalyzer().analyze(
                discovery
            )

        return {
            "ok": all(
                item.get("ok")
                for item in results.values()
            ),
            "results": results,
        }


# ============================================================
# UI ENGINEER
# ============================================================

class AutonomousUIDesigner:

    def __init__(
        self,
        ai: AIProvider,
    ) -> None:
        self.ai = ai

    def inspect(self) -> Dict[str, Any]:
        return ProjectDiscovery().inspect_ui()

    def validate_html(
        self,
        content: str,
    ) -> Dict[str, Any]:
        lower = content.lower()

        if "<html" not in lower:
            return {
                "ok": False,
                "reason": "missing_html_root",
            }

        if "</html>" not in lower:
            return {
                "ok": False,
                "reason": "missing_html_close",
            }

        forbidden = contains_forbidden_implementation(
            content
        )

        if forbidden:
            return {
                "ok": False,
                "reason": "forbidden_scope",
                "patterns": forbidden,
            }

        required = [
            endpoint
            for endpoints in REQUIRED_API_ENDPOINTS.values()
            for endpoint in endpoints
        ]

        missing = [
            endpoint
            for endpoint in required
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
            "bytes": len(content.encode("utf-8")),
        }

    def improve(
        self,
        platform_report: Dict[str, Any],
    ) -> Dict[str, Any]:
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
                "health": health,
            }

        current = read_text(UI_INDEX)

        system_prompt = f"""
You are the autonomous official frontend engineer for MAJD-DMAIL.

MAJD-DMAIL is a DOMAIN SERVICES platform only.

SUPREME_OWNER is permanently the highest authority.

Improve the EXISTING official UI only when useful.

Requirements:
- preserve MAJD identity
- preserve Arabic RTL
- preserve useful existing design/content
- responsive desktop/tablet/mobile
- accessible
- production-oriented
- connect real UI actions to the real backend API
- never simulate successful domain operations
- display backend errors honestly
- do not implement payment flows in the current mission
- do not implement email/mailbox services
- do not remove owner controls
- return one COMPLETE index.html only

Required API contracts:
{json.dumps(REQUIRED_API_ENDPOINTS, ensure_ascii=False, indent=2)}
"""

        user_prompt = json.dumps(
            {
                "platform_verification": platform_report,
                "current_ui": current,
            },
            ensure_ascii=False,
            indent=2,
        )

        result = self.ai.generate(
            system_prompt,
            user_prompt,
        )

        if not result.get("ok"):
            return {
                "ok": False,
                "action": "existing_ui_preserved_ai_failed",
                "error": result.get("error"),
            }

        candidate = extract_html_code(
            result["text"]
        )

        validation = self.validate_html(
            candidate
        )

        if not validation.get("ok"):
            return {
                "ok": False,
                "action": "ui_candidate_rejected",
                "validation": validation,
            }

        if sha256_text(candidate) == sha256_text(current):
            return {
                "ok": True,
                "action": "ui_unchanged",
                "validation": validation,
            }

        # Reject catastrophic shrinkage.
        if (
            len(current) > 1000
            and len(candidate) < int(len(current) * 0.55)
        ):
            return {
                "ok": False,
                "action": "ui_candidate_rejected_regression",
                "old_bytes": len(current.encode("utf-8")),
                "new_bytes": len(candidate.encode("utf-8")),
            }

        backup = backup_existing(
            UI_INDEX
        )

        atomic_write_text(
            UI_INDEX,
            candidate,
        )

        final_validation = self.validate_html(
            read_text(UI_INDEX)
        )

        if not final_validation.get("ok"):
            restore_backup(
                backup,
                UI_INDEX,
            )

            return {
                "ok": False,
                "action": "ui_rolled_back",
                "validation": final_validation,
            }

        payload = {
            "ok": True,
            "action": "official_ui_improved",
            "owner_authority": OWNER_AUTHORITY,
            "validation": final_validation,
        }

        atomic_write_json(
            DESIGN_REPORT_FILE,
            payload,
        )

        audit(
            "AUTONOMOUS_UI_ENGINEERING_COMPLETED",
            details={
                "action": payload["action"],
            },
        )

        return payload


# ============================================================
# FUNCTIONAL VERIFIER
# ============================================================

class FunctionalVerifier:

    def __init__(
        self,
        validator: GeneratedCodeValidator,
    ) -> None:
        self.validator = validator

    def verify_primary_policy(self) -> Dict[str, Any]:
        files = list_primary_files()

        violations = [
            filename
            for filename in files
            if (
                extract_primary_number(filename) or 0
            ) > MAX_PRIMARY_FILES
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
                    "file": filename,
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

    def verify_importability(
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
                    raise RuntimeError(
                        "Unable to create import specification."
                    )

                module = importlib.util.module_from_spec(
                    spec
                )

                spec.loader.exec_module(
                    module
                )

                results[number] = {
                    "ok": True,
                    "file": filename,
                }

            except Exception as exc:
                results[number] = {
                    "ok": False,
                    "file": filename,
                    "error": repr(exc),
                    "traceback": traceback.format_exc(
                        limit=5
                    ),
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

        content = read_text(path)
        lower = content.lower()

        endpoints = {
            endpoint: endpoint in content
            for paths in REQUIRED_API_ENDPOINTS.values()
            for endpoint in paths
        }

        runtime_evidence = {
            token: token in lower
            for token in (
                "flask",
                "fastapi",
                "httpserver",
                "basehttprequesthandler",
                "wsgiref",
                "socketserver",
            )
        }

        return {
            "ok": (
                all(endpoints.values())
                and any(runtime_evidence.values())
            ),
            "endpoints": endpoints,
            "runtime_evidence": runtime_evidence,
        }

    def _candidate_api_urls(self) -> List[str]:
        configured = os.getenv(
            "MAJD_DMAIL_API_BASE_URL",
            ""
        ).strip().rstrip("/")

        urls: List[str] = []

        if configured:
            urls.append(configured)

        port = int(
            os.getenv(
                "MAJD_DMAIL_API_PORT",
                "8080",
            )
        )

        urls.extend(
            [
                f"http://127.0.0.1:{port}",
                "http://127.0.0.1:8000",
                "http://127.0.0.1:5000",
            ]
        )

        unique: List[str] = []

        for item in urls:
            if item not in unique:
                unique.append(item)

        return unique

    def verify_live_health(
        self,
    ) -> Dict[str, Any]:
        attempts: List[Dict[str, Any]] = []

        for base_url in self._candidate_api_urls():
            url = base_url + "/api/health"

            request = urllib.request.Request(
                url,
                method="GET",
                headers={
                    "Accept": "application/json",
                },
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
                        getattr(
                            response,
                            "status",
                            200,
                        )
                    )

                parsed: Any = None

                try:
                    parsed = json.loads(body)
                except Exception:
                    parsed = None

                success = (
                    200 <= status_code < 300
                    and isinstance(parsed, dict)
                )

                attempt = {
                    "ok": success,
                    "url": url,
                    "status_code": status_code,
                    "json": parsed,
                }

                attempts.append(attempt)

                if success:
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
            "reason": "no_live_api_health_verified",
            "attempts": attempts,
        }

    def verify_ui(
        self,
    ) -> Dict[str, Any]:
        inspection = ProjectDiscovery().inspect_ui()

        if not inspection.get("exists"):
            return {
                "ok": False,
                "inspection": inspection,
            }

        return {
            "ok": bool(
                inspection.get(
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
        analysis = CapabilityAnalyzer().analyze(
            discovery
        )

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
    ) -> Dict[str, Any]:
        primary = self.verify_primary_policy()
        generated = self.verify_generated_components()
        imports = self.verify_importability()
        api_source = self.verify_api_source_contract()
        live_health = self.verify_live_health()
        ui = self.verify_ui()
        capabilities = self.verify_capabilities(
            live_health
        )
        ai_health = ai.health()

        internal_structure_ok = bool(
            primary.get("ok")
            and generated.get("ok")
            and imports.get("ok")
            and api_source.get("ok")
            and capabilities.get("ok")
        )

        # core_ok requires actual live runtime health.
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
                and item["status"] != "VERIFIED"
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
            "live_api_health": live_health,
            "official_ui": ui,
            "capabilities": capabilities,
            "ai": ai_health,
            "internal_structure_ok": internal_structure_ok,
            "core_ok": core_ok,
            "production_ready": production_ready,
            "external_blockers": external_blockers,
            "no_fake_success": True,
        }

        atomic_write_json(
            REPORT_FILE,
            report,
        )

        return report


# ============================================================
# SELF REPAIR ENGINE
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

        generated_report = verification.get(
            "generated_components",
            {},
        ).get(
            "files",
            {},
        )

        import_report = verification.get(
            "importability",
            {},
        ).get(
            "files",
            {},
        )

        api_ok = verification.get(
            "api_source_contract",
            {},
        ).get(
            "ok",
            False,
        )

        for number in (
            "03",
            "04",
            "05",
        ):
            generated_ok = generated_report.get(
                number,
                {},
            ).get(
                "ok",
                False,
            )

            import_ok = import_report.get(
                number,
                {},
            ).get(
                "ok",
                False,
            )

            requires_repair = (
                not generated_ok
                or not import_ok
                or (
                    number == "05"
                    and not api_ok
                )
            )

            if not requires_repair:
                results[number] = {
                    "ok": True,
                    "action": "functional_structure_passed",
                    "file": GENERATED_FILES[number],
                }
                continue

            results[number] = self.engineer.build_one(
                number,
                plan,
                discovery,
                gaps,
                force=True,
            )

            discovery = ProjectDiscovery().snapshot()
            gaps = CapabilityAnalyzer().analyze(
                discovery
            )

        return {
            "ok": all(
                item.get("ok")
                for item in results.values()
            ),
            "results": results,
        }


# ============================================================
# MASTER MIND / AUTONOMOUS COMPANY
# ============================================================

class MajdDmailMastermind:

    def __init__(self) -> None:
        self.state = load_state()

        self.ai = AIProvider()
        self.discovery_engine = ProjectDiscovery()
        self.capability_analyzer = CapabilityAnalyzer()
        self.planner = PlatformPlanner(self.ai)
        self.engineer = AutonomousPlatformEngineer(
            self.ai
        )
        self.designer = AutonomousUIDesigner(
            self.ai
        )
        self.verifier = FunctionalVerifier(
            self.engineer.validator
        )
        self.repair_engine = SelfRepairEngine(
            self.engineer,
            self.verifier,
        )

    def bootstrap(self) -> Dict[str, Any]:
        self.state["phase"] = (
            "AUTONOMOUS_DOMAIN_ENGINEERING"
        )

        save_state(self.state)

        payload = {
            "ok": True,
            "project": PROJECT_NAME,
            "version": VERSION,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,
            "ai_authority": AI_AUTHORITY,
            "designer_authority": DESIGNER_AUTHORITY,
            "protected": [
                THIS_FILENAME,
                PRIMARY_FILE_02,
            ],
            "ai_managed": GENERATED_FILES,
            "payment_currently_enabled": False,
            "autonomous_company": True,
            "workflow": [
                "DISCOVER",
                "ANALYZE",
                "PLAN",
                "BUILD",
                "INTEGRATE",
                "TEST",
                "REPAIR",
                "VERIFY",
                "REPORT",
                "RETRY",
            ],
        }

        audit(
            "AUTONOMOUS_COMPANY_BOOTSTRAPPED",
            details=payload,
        )

        return payload

    def discover(self) -> Dict[str, Any]:
        discovery = self.discovery_engine.snapshot()
        gaps = self.capability_analyzer.analyze(
            discovery
        )

        result = {
            "discovery": discovery,
            "capability_analysis": gaps,
        }

        self.state["last_discovery"] = {
            "timestamp": utc_now(),
            "missing_count": gaps.get(
                "missing_count"
            ),
            "missing": gaps.get("missing"),
        }

        save_state(self.state)

        return result

    def status(self) -> Dict[str, Any]:
        verification = read_json(
            REPORT_FILE,
            {},
        )

        return {
            "timestamp": utc_now(),
            "project": PROJECT_NAME,
            "version": VERSION,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,
            "phase": self.state.get("phase"),
            "primary_files": list_primary_files(),
            "protected_core_exists": (
                ROOT / PRIMARY_FILE_02
            ).exists(),
            "official_ui": self.designer.inspect(),
            "ai": self.ai.health(),
            "last_verification": {
                "core_ok": verification.get(
                    "core_ok"
                ),
                "production_ready": verification.get(
                    "production_ready"
                ),
                "external_blockers": verification.get(
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
        gaps = self.capability_analyzer.analyze(
            discovery
        )

        plan = self.planner.create(
            discovery,
            gaps,
            use_ai=use_ai,
        )

        self.state["last_plan"] = {
            "timestamp": utc_now(),
            "source": plan.get("source"),
            "ai_planning": plan.get(
                "ai_planning"
            ),
            "missing": gaps.get("missing"),
        }

        save_state(self.state)

        audit(
            "WHOLE_PLATFORM_PLAN_CREATED",
            details=self.state["last_plan"],
        )

        return plan

    def build(
        self,
        *,
        force: bool = False,
    ) -> Dict[str, Any]:
        if not (ROOT / PRIMARY_FILE_02).exists():
            return {
                "ok": False,
                "blocked": True,
                "reason": (
                    f"{PRIMARY_FILE_02} is required. "
                    "The autonomous company will not create or overwrite it."
                ),
            }

        discovery = self.discovery_engine.snapshot()
        gaps = self.capability_analyzer.analyze(
            discovery
        )

        plan = self.planner.create(
            discovery,
            gaps,
            use_ai=True,
        )

        result = self.engineer.build_all(
            plan,
            discovery,
            gaps,
            force=force,
        )

        self.state["last_build"] = {
            "timestamp": utc_now(),
            "result": result,
        }

        self.state["phase"] = (
            "VERIFYING_DOMAIN_PLATFORM"
        )

        save_state(self.state)

        return result

    def verify(self) -> Dict[str, Any]:
        result = self.verifier.full(
            self.ai
        )

        self.state["last_verify"] = {
            "timestamp": utc_now(),
            "internal_structure_ok": result.get(
                "internal_structure_ok"
            ),
            "core_ok": result.get("core_ok"),
            "production_ready": result.get(
                "production_ready"
            ),
            "external_blockers": result.get(
                "external_blockers"
            ),
        }

        if result.get("production_ready"):
            self.state["phase"] = (
                "DOMAIN_PLATFORM_PRODUCTION_READY"
            )
        elif result.get("core_ok"):
            self.state["phase"] = (
                "DOMAIN_CORE_VERIFIED_EXTERNAL_BLOCKERS"
            )
        else:
            self.state["phase"] = (
                "AUTONOMOUS_REPAIR_REQUIRED"
            )

        save_state(self.state)

        audit(
            "FUNCTIONAL_PLATFORM_VERIFICATION_COMPLETED",
            details=self.state["last_verify"],
        )

        return result

    def repair(self) -> Dict[str, Any]:
        discovery = self.discovery_engine.snapshot()
        gaps = self.capability_analyzer.analyze(
            discovery
        )

        plan = self.planner.create(
            discovery,
            gaps,
            use_ai=True,
        )

        before = self.verifier.full(
            self.ai
        )

        result = self.repair_engine.repair(
            plan,
            discovery,
            gaps,
            before,
        )

        after = self.verifier.full(
            self.ai
        )

        payload = {
            "ok": bool(
                result.get("ok")
            ),
            "repair": result,
            "before": {
                "core_ok": before.get(
                    "core_ok"
                ),
                "production_ready": before.get(
                    "production_ready"
                ),
            },
            "after": {
                "core_ok": after.get(
                    "core_ok"
                ),
                "production_ready": after.get(
                    "production_ready"
                ),
            },
        }

        self.state["last_repair"] = {
            "timestamp": utc_now(),
            "result": payload,
        }

        save_state(self.state)

        audit(
            "AUTONOMOUS_REPAIR_COMPLETED",
            details={
                "repair_ok": result.get("ok"),
                "core_ok_after": after.get(
                    "core_ok"
                ),
                "production_ready_after": after.get(
                    "production_ready"
                ),
            },
        )

        return payload

    def design(self) -> Dict[str, Any]:
        verification = self.verifier.full(
            self.ai
        )

        result = self.designer.improve(
            verification
        )

        self.state["last_design"] = {
            "timestamp": utc_now(),
            "result": result,
        }

        save_state(self.state)

        return result

    def cycle(self) -> Dict[str, Any]:
        started_at = utc_now()

        audit(
            "AUTONOMOUS_ENGINEERING_CYCLE_STARTED",
            details={
                "scope": PROJECT_SCOPE,
                "owner_authority": OWNER_AUTHORITY,
            },
        )

        discovery = self.discovery_engine.snapshot()
        gaps = self.capability_analyzer.analyze(
            discovery
        )

        plan = self.planner.create(
            discovery,
            gaps,
            use_ai=True,
        )

        initial = self.verifier.full(
            self.ai
        )

        build_result: Optional[
            Dict[str, Any]
        ] = None

        repair_result: Optional[
            Dict[str, Any]
        ] = None

        design_result: Optional[
            Dict[str, Any]
        ] = None

        if not (ROOT / PRIMARY_FILE_02).exists():
            final = initial

        else:
            needs_engineering = bool(
                not initial.get(
                    "internal_structure_ok"
                )
                or gaps.get(
                    "missing_count",
                    0,
                ) > 0
            )

            if needs_engineering:
                build_result = self.engineer.build_all(
                    plan,
                    discovery,
                    gaps,
                    force=True,
                )

            mid_discovery = self.discovery_engine.snapshot()
            mid_gaps = self.capability_analyzer.analyze(
                mid_discovery
            )

            mid_verification = self.verifier.full(
                self.ai
            )

            if not mid_verification.get(
                "core_ok"
            ):
                repair_result = self.repair_engine.repair(
                    plan,
                    mid_discovery,
                    mid_gaps,
                    mid_verification,
                )

            after_repair = self.verifier.full(
                self.ai
            )

            # UI improvement is allowed, but existing UI is preserved
            # when AI fails or proposed output regresses.
            design_result = self.designer.improve(
                after_repair
            )

            final = self.verifier.full(
                self.ai
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
                "core_ok": initial.get(
                    "core_ok"
                ),
                "production_ready": initial.get(
                    "production_ready"
                ),
            },
            "discovered_missing_capabilities": gaps.get(
                "missing"
            ),
            "plan_source": plan.get("source"),
            "build_result": build_result,
            "repair_result": repair_result,
            "design_result": design_result,
            "final_verification": final,
        }

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

        if final.get("production_ready"):
            self.state["phase"] = (
                "DOMAIN_PLATFORM_PRODUCTION_READY"
            )
        elif final.get("core_ok"):
            self.state["phase"] = (
                "DOMAIN_CORE_VERIFIED_EXTERNAL_BLOCKERS"
            )
        else:
            self.state["phase"] = (
                "AUTONOMOUS_ENGINEERING_CONTINUES"
            )

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
        )
    )


# ============================================================
# CLI
# ============================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=THIS_FILENAME,
        description=(
            "MAJD-DMAIL sovereign autonomous domain-platform "
            "AI engineering company"
        ),
    )

    sub = parser.add_subparsers(
        dest="command"
    )

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

    loop_command = sub.add_parser("loop")

    loop_command.add_argument(
        "--interval",
        type=int,
        default=int(
            os.getenv(
                "MAJD_AUTONOMY_INTERVAL",
                "300",
            )
        ),
    )

    return parser


# ============================================================
# AUTONOMOUS LOOP
# ============================================================

def run_loop(
    mastermind: MajdDmailMastermind,
    interval: int,
) -> int:
    interval = max(
        60,
        int(interval),
    )

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

            final = result[
                "final_verification"
            ]

            print_json(
                {
                    "cycle_completed": utc_now(),
                    "scope": PROJECT_SCOPE,
                    "owner_authority": OWNER_AUTHORITY,
                    "internal_structure_ok": final.get(
                        "internal_structure_ok"
                    ),
                    "core_ok": final.get(
                        "core_ok"
                    ),
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
                    "reason": "keyboard_interrupt",
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
# MAIN
# ============================================================

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    mastermind = MajdDmailMastermind()

    command = (
        args.command
        or "cycle"
    )

    if command == "bootstrap":
        print_json(
            mastermind.bootstrap()
        )
        return 0

    if command == "status":
        print_json(
            mastermind.status()
        )
        return 0

    if command == "discover":
        print_json(
            mastermind.discover()
        )
        return 0

    if command == "plan":
        print_json(
            mastermind.plan(
                use_ai=not args.no_ai
            )
        )
        return 0

    if command == "build":
        result = mastermind.build(
            force=args.force
        )

        print_json(result)

        return (
            0
            if result.get("ok")
            else 1
        )

    if command == "verify":
        result = mastermind.verify()

        print_json(result)

        return (
            0
            if result.get("core_ok")
            else 1
        )

    if command == "repair":
        result = mastermind.repair()

        print_json(result)

        return (
            0
            if result.get("ok")
            else 1
        )

    if command == "design":
        result = mastermind.design()

        print_json(result)

        return (
            0
            if result.get("ok")
            else 1
        )

    if command == "cycle":
        result = mastermind.cycle()

        print_json(result)

        return (
            0
            if result[
                "final_verification"
            ].get(
                "core_ok"
            )
            else 1
        )

    if command == "loop":
        return run_loop(
            mastermind,
            args.interval,
        )

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
