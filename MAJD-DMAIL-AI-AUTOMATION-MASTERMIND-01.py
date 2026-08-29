#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD-DMAIL
MAJD-DMAIL-AI-AUTOMATION-MASTERMIND-01.py

FILE 01
DOMAIN-ONLY AUTONOMOUS AI + AUTOMATION + MASTERMIND + UI DESIGNER

============================================================
MAJD-DMAIL SOVEREIGN DOMAIN PLATFORM
============================================================

MISSION
-------
Build, operate, verify, repair and continuously improve MAJD-DMAIL
as a REAL DOMAIN SERVICES PLATFORM.

MAJD-DMAIL in this project means DOMAIN SERVICES.

THIS PROJECT IS DOMAIN-ONLY.

ALLOWED SCOPE
-------------
- Domain search
- Domain availability
- Domain registration
- Domain renewal
- Domain transfer
- Domain lifecycle
- Registrar / Registry adapters
- EPP / RDAP / WHOIS integrations where applicable
- DNS management
- Nameservers
- DNSSEC
- SSL/TLS related to managed domains
- Domain pricing
- Domain payments
- Domain invoices
- Domain subscriptions
- Customer accounts
- Owner control
- Domain security
- Domain audit
- Domain monitoring
- Domain notifications
- Domain support
- Domain automation
- Domain self-repair
- Official MAJD-DMAIL UI
- UI/API integration
- Autonomous UI Designer

FORBIDDEN SCOPE
---------------
This mastermind MUST NOT build or operate:
- Email
- Mailboxes
- SMTP
- IMAP
- POP3
- Postfix
- Dovecot
- Webmail
- Paid email
- Email hosting
- Any unrelated platform or service

AUTHORITY
---------
SUPREME_OWNER is permanently the highest authority.

AI, automation, designer, runtime, generated components,
providers and adapters are subordinate to SUPREME_OWNER.

No AI component may:
- override owner authority
- redefine owner authority
- create a higher authority
- lock the owner out
- grant itself supreme privileges
- remove owner controls

PRIMARY FILE POLICY
-------------------
01 = mastermind, manually maintained
02 = permanent core, manually maintained
03 = domain infrastructure, AI managed
04 = domain commerce/security, AI managed
05 = platform runtime/API, AI managed

No primary file 06 or higher.

AUTONOMY
--------
Routine technical operation is autonomous.

The system may automatically:
- plan
- generate 03-05
- repair 03-05
- improve 03-05
- inspect the official UI
- improve the official UI
- connect UI to API
- verify Python syntax
- verify UI/API contracts
- monitor health
- retry failures
- maintain backups
- generate reports
- continuously run

Owner intervention is reserved for genuinely non-delegable
actions such as real provider credentials, legal approvals,
identity verification or irreversible financial authorization.

NO FAKE SUCCESS
---------------
External registrar, payment, DNS or other provider integrations
must NEVER be reported LIVE unless a real health verification
succeeds.

Generated code must pass validation before acceptance.
Existing files are backed up before replacement.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import logging
import os
import re
import shutil
import tempfile
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# IDENTITY / AUTHORITY
# ============================================================

PROJECT_NAME = "MAJD-DMAIL"
PROJECT_KIND = "SOVEREIGN_DOMAIN_PLATFORM"
VERSION = "2.0.0"

OWNER_AUTHORITY = "SUPREME_OWNER"
AI_AUTHORITY = "SUBORDINATE_AUTONOMOUS_OPERATOR"
DESIGNER_AUTHORITY = "SUBORDINATE_UI_DESIGNER"

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

PRIMARY_PATTERN = re.compile(
    r"^MAJD-DMAIL-[A-Z0-9\-]+-(0[1-5])\.py$",
    re.IGNORECASE,
)

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
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


STATE_FILE = STATE_DIR / "mastermind-state.json"
PLAN_FILE = STATE_DIR / "current-plan.json"
REPORT_FILE = STATE_DIR / "last-report.json"
EVENTS_FILE = LOG_DIR / "mastermind-events.jsonl"
LOG_FILE = LOG_DIR / "mastermind.log"
DESIGN_REPORT_FILE = STATE_DIR / "ui-designer-report.json"


# ============================================================
# LOGGING
# ============================================================

logger = logging.getLogger(
    "MAJD_DMAIL_DOMAIN_MASTERMIND"
)

logger.setLevel(
    logging.INFO
)

if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )


# ============================================================
# DOMAIN-ONLY POLICY
# ============================================================

DOMAIN_CAPABILITIES = [
    "domain_search",
    "domain_availability",
    "domain_registration",
    "domain_renewal",
    "domain_transfer",
    "domain_lifecycle",
    "registrar_adapters",
    "registry_adapters",
    "rdap",
    "whois",
    "dns_management",
    "nameservers",
    "dnssec",
    "domain_ssl_tls",
    "domain_pricing",
    "domain_payments",
    "domain_billing",
    "domain_invoices",
    "domain_subscriptions",
    "customer_accounts",
    "owner_control",
    "domain_security",
    "domain_audit",
    "domain_monitoring",
    "domain_notifications",
    "domain_support",
    "domain_self_repair",
    "official_ui",
    "ui_api_integration",
    "autonomous_ui_designer",
]

FORBIDDEN_SCOPE_PATTERNS = (
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

DOMAIN_PLATFORM_REQUIREMENTS: Dict[str, Any] = {
    "mission": (
        "Build, operate and continuously improve a real autonomous "
        "domain registration and domain management platform."
    ),
    "project_scope": "DOMAINS_ONLY",
    "owner_authority": OWNER_AUTHORITY,
    "capabilities": DOMAIN_CAPABILITIES,
    "rules": [
        "SUPREME_OWNER is permanently the highest authority.",
        "Every AI component is subordinate to SUPREME_OWNER.",
        "Project scope is DOMAIN SERVICES ONLY.",
        "Email and mailbox services are forbidden.",
        "No fake success.",
        "Secrets must come from environment or secure secret storage.",
        "External providers must use real adapters.",
        (
            "External registrar, registry, DNS and payment services "
            "are LIVE only after real health verification."
        ),
        (
            "Files 01 and 02 must never be overwritten "
            "automatically."
        ),
        "Generated primary files are limited to 03, 04 and 05.",
        "No primary file 06 or higher.",
        "Financial operations must be idempotent.",
        (
            "Ownership-sensitive domain operations require "
            "strong authorization."
        ),
        "Every important action must be auditable.",
        "Generated code must be verified before acceptance.",
        (
            "Official UI may be autonomously designed and improved "
            "but remains subordinate to SUPREME_OWNER."
        ),
        (
            "UI actions must connect to real backend APIs and "
            "must not simulate successful domain operations."
        ),
    ],
}


DEFAULT_GENERATED_ARCHITECTURE: Dict[str, Dict[str, str]] = {
    "03": {
        "filename":
            "MAJD-DMAIL-DOMAIN-INFRASTRUCTURE-03.py",
        "purpose": (
            "Real domain infrastructure: registrar and registry "
            "adapters, domain availability, registration, renewal, "
            "transfer, lifecycle, RDAP/WHOIS, DNS, nameservers, "
            "DNSSEC, domain SSL/TLS and provider health."
        ),
    },
    "04": {
        "filename":
            "MAJD-DMAIL-COMMERCE-SECURITY-04.py",
        "purpose": (
            "Domain-only commerce and security: domain pricing, "
            "subscriptions, payments, invoices, authorization, "
            "ownership protection, audit and financial verification."
        ),
    },
    "05": {
        "filename":
            "MAJD-DMAIL-PLATFORM-RUNTIME-05.py",
        "purpose": (
            "Domain platform customer/owner runtime, unified HTTP API, "
            "official UI integration, domain orchestration, monitoring, "
            "notifications and final production runtime."
        ),
    },
}


# ============================================================
# UTILS
# ============================================================

def utc_now() -> str:
    return dt.datetime.now(
        dt.timezone.utc
    ).isoformat()


def sha256_text(
    value: str,
) -> str:
    return hashlib.sha256(
        value.encode(
            "utf-8"
        )
    ).hexdigest()


def read_json(
    path: Path,
    default: Any,
) -> Any:

    if not path.exists():
        return default

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except Exception:
        return default


def atomic_write_text(
    path: Path,
    content: str,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(
            path.parent
        ),
        text=True,
    )

    try:

        with os.fdopen(
            fd,
            "w",
            encoding="utf-8",
        ) as handle:

            handle.write(
                content
            )

            if not content.endswith(
                "\n"
            ):
                handle.write(
                    "\n"
                )

            handle.flush()

            os.fsync(
                handle.fileno()
            )

        os.replace(
            temp_name,
            path,
        )

    finally:

        if os.path.exists(
            temp_name
        ):
            try:
                os.unlink(
                    temp_name
                )
            except OSError:
                pass


def atomic_write_json(
    path: Path,
    payload: Any,
) -> None:

    atomic_write_text(
        path,
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )


def append_jsonl(
    path: Path,
    payload: Dict[str, Any],
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

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

    append_jsonl(
        EVENTS_FILE,
        payload,
    )

    if status.upper() in {
        "ERROR",
        "FAILED",
    }:
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


def extract_primary_number(
    filename: str,
) -> Optional[int]:

    match = PRIMARY_PATTERN.fullmatch(
        filename
    )

    if not match:
        return None

    return int(
        match.group(1)
    )


def list_primary_files() -> List[str]:

    files: List[str] = []

    for path in ROOT.glob(
        "MAJD-DMAIL-*.py"
    ):

        if extract_primary_number(
            path.name
        ) is not None:
            files.append(
                path.name
            )

    return sorted(
        files
    )


def enforce_generated_filename(
    filename: str,
) -> int:

    number = extract_primary_number(
        filename
    )

    if number is None:
        raise ValueError(
            f"Invalid MAJD-DMAIL primary filename: {filename}"
        )

    if number not in {
        3,
        4,
        5,
    }:
        raise PermissionError(
            "AI may modify only primary files 03, 04 and 05."
        )

    return number


def detect_forbidden_scope(
    content: str,
) -> List[str]:

    return [
        pattern
        for pattern
        in FORBIDDEN_SCOPE_PATTERNS
        if re.search(
            pattern,
            content,
            re.IGNORECASE,
        )
    ]


def syntax_check_content(
    content: str,
) -> Tuple[bool, Optional[str]]:

    try:
        ast.parse(
            content
        )
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


def syntax_check_file(
    path: Path,
) -> Dict[str, Any]:

    if not path.exists():
        return {
            "ok": False,
            "file": path.name,
            "error": "missing",
        }

    try:
        content = path.read_text(
            encoding="utf-8"
        )
    except Exception as exc:
        return {
            "ok": False,
            "file": path.name,
            "error": repr(
                exc
            ),
        }

    ok, error = syntax_check_content(
        content
    )

    return {
        "ok": ok,
        "file": path.name,
        "error": error,
        "sha256": sha256_text(
            content
        ),
    }


def extract_python_code(
    text: str,
) -> str:

    cleaned = text.strip()

    fenced = re.search(
        r"```(?:python)?\s*(.*?)```",
        cleaned,
        re.IGNORECASE | re.DOTALL,
    )

    if fenced:
        cleaned = fenced.group(
            1
        ).strip()

    if not cleaned.endswith(
        "\n"
    ):
        cleaned += "\n"

    return cleaned


def extract_html_code(
    text: str,
) -> str:

    cleaned = text.strip()

    fenced = re.search(
        r"```(?:html)?\s*(.*?)```",
        cleaned,
        re.IGNORECASE | re.DOTALL,
    )

    if fenced:
        cleaned = fenced.group(
            1
        ).strip()

    if not cleaned.endswith(
        "\n"
    ):
        cleaned += "\n"

    return cleaned


def backup_existing(
    path: Path,
) -> Optional[Path]:

    if not path.exists():
        return None

    stamp = dt.datetime.now().strftime(
        "%Y%m%d-%H%M%S"
    )

    relative = path.relative_to(
        ROOT
    )

    safe_name = str(
        relative
    ).replace(
        "/",
        "__"
    )

    target = BACKUP_DIR / (
        f"{safe_name}.{stamp}.bak"
    )

    shutil.copy2(
        path,
        target,
    )

    audit(
        "BACKUP_CREATED",
        details={
            "source": str(
                relative
            ),
            "backup": str(
                target.relative_to(
                    ROOT
                )
            ),
        },
    )

    return target


# ============================================================
# STATE
# ============================================================

DEFAULT_STATE: Dict[str, Any] = {
    "project": PROJECT_NAME,
    "project_kind": PROJECT_KIND,
    "version": VERSION,
    "owner_authority": OWNER_AUTHORITY,
    "phase": "AUTONOMOUS_DOMAIN_OPERATION",
    "primary_file_limit": MAX_PRIMARY_FILES,
    "file_01": THIS_FILENAME,
    "file_02": PRIMARY_FILE_02,
    "created_at": None,
    "updated_at": None,
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
        dict(
            DEFAULT_STATE
        ),
    )

    if not state.get(
        "created_at"
    ):
        state["created_at"] = utc_now()

    state[
        "project_kind"
    ] = PROJECT_KIND

    state[
        "owner_authority"
    ] = OWNER_AUTHORITY

    state[
        "updated_at"
    ] = utc_now()

    return state


def save_state(
    state: Dict[str, Any],
) -> None:

    state[
        "owner_authority"
    ] = OWNER_AUTHORITY

    state[
        "updated_at"
    ] = utc_now()

    atomic_write_json(
        STATE_FILE,
        state,
    )


# ============================================================
# AI PROVIDER
# ============================================================

class AIProvider:

    def __init__(
        self,
    ) -> None:

        self.base_url = os.getenv(
            "MAJD_AI_BASE_URL",
            os.getenv(
                "OLLAMA_BASE_URL",
                "http://127.0.0.1:11434",
            ),
        ).rstrip(
            "/"
        )

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
                    "300",
                )
            ),
        )

    def health(
        self,
    ) -> Dict[str, Any]:

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
                item.get(
                    "name"
                )
                for item in payload.get(
                    "models",
                    [],
                )
                if isinstance(
                    item,
                    dict,
                )
            ]

            requested_available = any(
                name
                and (
                    name == self.model
                    or name.startswith(
                        self.model.split(
                            ":"
                        )[0]
                        + ":"
                    )
                )
                for name in models
            )

            return {
                "ok": True,
                "provider": "ollama",
                "base_url": self.base_url,
                "requested_model": self.model,
                "requested_model_available":
                    requested_available,
                "available_models": models,
            }

        except Exception as exc:

            return {
                "ok": False,
                "provider": "ollama",
                "base_url": self.base_url,
                "requested_model": self.model,
                "error": repr(
                    exc
                ),
            }

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
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
                    "temperature": 0.1,
                },
            }
        ).encode(
            "utf-8"
        )

        request = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=body,
            method="POST",
            headers={
                "Content-Type":
                    "application/json"
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
                payload.get(
                    "response",
                    "",
                )
            ).strip()

            return {
                "ok": bool(
                    text
                ),
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
                    f"HTTP {exc.code}: "
                    f"{exc.reason}"
                ),
            }

        except Exception as exc:

            return {
                "ok": False,
                "text": "",
                "provider": "ollama",
                "model": self.model,
                "error": repr(
                    exc
                ),
            }


# ============================================================
# DOMAIN ARCHITECTURE PLANNER
# ============================================================

class ArchitecturePlanner:

    def __init__(
        self,
        ai: AIProvider,
    ) -> None:
        self.ai = ai

    def base_plan(
        self,
    ) -> Dict[str, Any]:

        return {
            "generated_at": utc_now(),
            "project": PROJECT_NAME,
            "project_kind": PROJECT_KIND,
            "scope": "DOMAINS_ONLY",
            "owner_authority": OWNER_AUTHORITY,
            "primary_limit": MAX_PRIMARY_FILES,
            "manual_files": {
                "01": THIS_FILENAME,
                "02": PRIMARY_FILE_02,
            },
            "ai_files":
                DEFAULT_GENERATED_ARCHITECTURE,
            "official_ui": str(
                UI_INDEX.relative_to(
                    ROOT
                )
            ),
            "requirements":
                DOMAIN_PLATFORM_REQUIREMENTS,
            "source":
                "embedded_domain_only_architecture",
        }

    def create(
        self,
        use_ai: bool = True,
    ) -> Dict[str, Any]:

        plan = self.base_plan()

        if not use_ai:
            atomic_write_json(
                PLAN_FILE,
                plan,
            )
            return plan

        health = self.ai.health()

        if not health.get(
            "ok"
        ):
            plan["ai_planning"] = {
                "used": False,
                "reason":
                    "AI provider unavailable",
                "health": health,
            }

            atomic_write_json(
                PLAN_FILE,
                plan,
            )

            return plan

        system_prompt = f"""
You are the architecture planner for MAJD-DMAIL.

MAJD-DMAIL IS A DOMAIN PLATFORM ONLY.

SUPREME_OWNER is permanently the highest authority.

Hard rules:
- Never change or challenge SUPREME_OWNER authority.
- Never create an authority above SUPREME_OWNER.
- Project scope is DOMAINS ONLY.
- Do not design email services.
- Do not design mailbox services.
- Do not design SMTP, IMAP, POP3, Postfix, Dovecot or webmail.
- Primary files are limited to 01 through 05.
- File 01 already exists.
- File 02 is manually maintained.
- You may design ONLY files 03, 04 and 05.
- Never design file 06 or higher.
- Keep exactly three generated primary files.
- 03 handles domain infrastructure.
- 04 handles domain commerce/security.
- 05 handles runtime/API/UI integration.
- Official UI path is {UI_INDEX}.
- Do not hard-code secrets.
- External services must use adapters.
- Never mark an external service LIVE unless a real health check succeeds.
- Return ONLY valid JSON.
"""

        user_prompt = json.dumps(
            {
                "requirements":
                    DOMAIN_PLATFORM_REQUIREMENTS,
                "current_files":
                    DEFAULT_GENERATED_ARCHITECTURE,
                "required_output": {
                    "files": {
                        "03": {
                            "filename":
                                GENERATED_FILES["03"],
                            "purpose":
                                "...",
                        },
                        "04": {
                            "filename":
                                GENERATED_FILES["04"],
                            "purpose":
                                "...",
                        },
                        "05": {
                            "filename":
                                GENERATED_FILES["05"],
                            "purpose":
                                "...",
                        },
                    }
                },
            },
            ensure_ascii=False,
            indent=2,
        )

        result = self.ai.generate(
            system_prompt,
            user_prompt,
        )

        if not result.get(
            "ok"
        ):
            plan["ai_planning"] = {
                "used": False,
                "reason":
                    "AI planning request failed",
                "error":
                    result.get(
                        "error"
                    ),
            }

            atomic_write_json(
                PLAN_FILE,
                plan,
            )

            return plan

        try:

            text = result[
                "text"
            ].strip()

            fenced = re.search(
                r"```(?:json)?\s*(.*?)```",
                text,
                re.IGNORECASE | re.DOTALL,
            )

            if fenced:
                text = fenced.group(
                    1
                ).strip()

            parsed = json.loads(
                text
            )

            files = parsed.get(
                "files",
                {},
            )

            if set(
                files
            ) != {
                "03",
                "04",
                "05",
            }:
                raise ValueError(
                    "AI plan must contain exactly 03, 04 and 05."
                )

            for key in (
                "03",
                "04",
                "05",
            ):

                specification = files[
                    key
                ]

                filename = str(
                    specification.get(
                        "filename",
                        "",
                    )
                )

                purpose = str(
                    specification.get(
                        "purpose",
                        "",
                    )
                ).strip()

                if filename != GENERATED_FILES[
                    key
                ]:
                    raise ValueError(
                        f"Filename cannot change for {key}."
                    )

                if not purpose:
                    raise ValueError(
                        f"Missing purpose for {key}."
                    )

                forbidden = detect_forbidden_scope(
                    purpose
                )

                if forbidden:
                    raise ValueError(
                        f"Forbidden non-domain scope in {key}."
                    )

            plan[
                "ai_files"
            ] = files

            plan[
                "source"
            ] = "ai_reviewed_domain_architecture"

            plan[
                "ai_planning"
            ] = {
                "used": True,
                "provider":
                    result.get(
                        "provider"
                    ),
                "model":
                    result.get(
                        "model"
                    ),
            }

        except Exception as exc:

            plan[
                "ai_planning"
            ] = {
                "used": False,
                "reason":
                    "AI plan rejected",
                "error":
                    repr(
                        exc
                    ),
            }

        atomic_write_json(
            PLAN_FILE,
            plan,
        )

        return plan


# ============================================================
# AUTONOMOUS DOMAIN BUILDER
# ============================================================

class AutonomousBuilder:

    def __init__(
        self,
        ai: AIProvider,
    ) -> None:
        self.ai = ai

    def validate_code(
        self,
        filename: str,
        content: str,
    ) -> Dict[str, Any]:

        number = enforce_generated_filename(
            filename
        )

        ok, syntax_error = syntax_check_content(
            content
        )

        if not ok:
            return {
                "ok": False,
                "file": filename,
                "number": number,
                "error": "syntax_error",
                "detail": syntax_error,
            }

        dangerous = [
            pattern
            for pattern
            in DANGEROUS_CODE_PATTERNS
            if re.search(
                pattern,
                content,
            )
        ]

        if dangerous:
            return {
                "ok": False,
                "file": filename,
                "number": number,
                "error":
                    "dangerous_code_pattern",
                "patterns":
                    dangerous,
            }

        forbidden_scope = detect_forbidden_scope(
            content
        )

        if forbidden_scope:
            return {
                "ok": False,
                "file": filename,
                "number": number,
                "error":
                    "forbidden_non_domain_scope",
                "patterns":
                    forbidden_scope,
            }

        return {
            "ok": True,
            "file": filename,
            "number": number,
            "sha256":
                sha256_text(
                    content
                ),
        }

    def fallback_code(
        self,
        number: str,
        filename: str,
        purpose: str,
    ) -> str:

        class_name = {
            "03":
                "MajdDomainInfrastructure",
            "04":
                "MajdDomainCommerceSecurity",
            "05":
                "MajdDomainPlatformRuntime",
        }[
            number
        ]

        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD-DMAIL
{filename}

DOMAIN-ONLY SAFE FALLBACK COMPONENT.

Purpose:
{purpose}
"""

from __future__ import annotations

import datetime as dt
import json
from typing import Any, Dict

PROJECT_NAME = "MAJD-DMAIL"
PROJECT_SCOPE = "DOMAINS_ONLY"
FILE_NUMBER = "{number}"
OWNER_AUTHORITY = "SUPREME_OWNER"
VERSION = "2.0.0"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


class {class_name}:

    def __init__(self) -> None:
        self.started_at = utc_now()

    def health(self) -> Dict[str, Any]:
        return {{
            "ok": True,
            "project": PROJECT_NAME,
            "scope": PROJECT_SCOPE,
            "file_number": FILE_NUMBER,
            "owner_authority": OWNER_AUTHORITY,
            "started_at": self.started_at,
            "external_services_verified": False,
            "live": False,
        }}


def main() -> int:
    runtime = {class_name}()
    print(
        json.dumps(
            runtime.health(),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

    def ai_generate_code(
        self,
        number: str,
        filename: str,
        purpose: str,
    ) -> Optional[str]:

        health = self.ai.health()

        if not health.get(
            "ok"
        ):
            return None

        system_prompt = f"""
You are the autonomous DOMAIN PLATFORM Python engineer
for MAJD-DMAIL.

SUPREME_OWNER is the highest authority permanently.

Generate ONLY complete Python source for:

File number: {number}
Filename: {filename}

Purpose:
{purpose}

ABSOLUTE RULES:
- MAJD-DMAIL is DOMAINS ONLY.
- Do not implement email.
- Do not implement mailboxes.
- Do not implement SMTP.
- Do not implement IMAP.
- Do not implement POP3.
- Do not implement Postfix.
- Do not implement Dovecot.
- Do not implement webmail.
- Do not implement paid email.
- Never override SUPREME_OWNER.
- Never create another supreme authority.
- File 01 is mastermind.
- File 02 is protected core.
- Modify only this generated file.
- Never create primary 06 or higher.
- Never hard-code secrets.
- Never use eval(), exec(), os.system() or subprocess.Popen().
- External providers must use adapters.
- Registrar/registry/payment/DNS services are not LIVE until verified.
- Production behavior must fail closed instead of reporting fake success.
- Include health/status behavior.
- Include main().
- Return ONLY complete Python source.
"""

        user_prompt = (
            "Implement this as a production-oriented autonomous "
            "MAJD-DMAIL DOMAIN component.\n\n"
            + json.dumps(
                DOMAIN_PLATFORM_REQUIREMENTS,
                ensure_ascii=False,
                indent=2,
            )
        )

        result = self.ai.generate(
            system_prompt,
            user_prompt,
        )

        if not result.get(
            "ok"
        ):
            return None

        return extract_python_code(
            result[
                "text"
            ]
        )

    def ai_repair_code(
        self,
        number: str,
        filename: str,
        purpose: str,
        broken_code: str,
        validation_error: Dict[str, Any],
    ) -> Optional[str]:

        if not self.ai.health().get(
            "ok"
        ):
            return None

        system_prompt = """
Repair MAJD-DMAIL DOMAIN PLATFORM Python source.

SUPREME_OWNER remains highest authority.

Rules:
- DOMAIN SERVICES ONLY.
- No email functionality.
- No SMTP/IMAP/POP3.
- No Postfix/Dovecot.
- Return ONLY corrected complete Python source.
- Do not create additional files.
- Do not change primary filename.
- Do not hard-code secrets.
- Never use eval(), exec(), os.system() or subprocess.Popen().
- Preserve the intended responsibility of this file.
"""

        user_prompt = f"""
FILE:
{filename}

NUMBER:
{number}

PURPOSE:
{purpose}

VALIDATION ERROR:
{json.dumps(validation_error, ensure_ascii=False, indent=2)}

BROKEN SOURCE START

{broken_code}

BROKEN SOURCE END

Return ONLY the corrected complete Python source.
"""

        result = self.ai.generate(
            system_prompt,
            user_prompt,
        )

        if not result.get(
            "ok"
        ):
            return None

        return extract_python_code(
            result[
                "text"
            ]
        )

    def build_one(
        self,
        number: str,
        specification: Dict[str, str],
        *,
        force: bool = False,
    ) -> Dict[str, Any]:

        filename = str(
            specification[
                "filename"
            ]
        )

        purpose = str(
            specification[
                "purpose"
            ]
        )

        enforce_generated_filename(
            filename
        )

        path = ROOT / filename

        existing_check = (
            syntax_check_file(
                path
            )
            if path.exists()
            else None
        )

        if (
            path.exists()
            and not force
            and existing_check
            and existing_check.get(
                "ok"
            )
        ):
            content = path.read_text(
                encoding="utf-8"
            )

            policy = self.validate_code(
                filename,
                content,
            )

            if policy.get(
                "ok"
            ):
                return {
                    "ok": True,
                    "file": filename,
                    "action":
                        "existing_domain_file_kept",
                    "verification":
                        existing_check,
                }

        audit(
            "DOMAIN_BUILD_STARTED",
            details={
                "file": filename,
                "number": number,
            },
        )

        code = self.ai_generate_code(
            number,
            filename,
            purpose,
        )

        source = "ai"

        if code is None:
            code = self.fallback_code(
                number,
                filename,
                purpose,
            )
            source = "safe_domain_fallback"

        validation = self.validate_code(
            filename,
            code,
        )

        repair_attempts = 0

        while (
            source == "ai"
            and not validation.get(
                "ok"
            )
            and repair_attempts < 3
        ):

            repair_attempts += 1

            repaired = self.ai_repair_code(
                number,
                filename,
                purpose,
                code,
                validation,
            )

            if not repaired:
                break

            code = repaired

            validation = self.validate_code(
                filename,
                code,
            )

        if not validation.get(
            "ok"
        ):

            code = self.fallback_code(
                number,
                filename,
                purpose,
            )

            source = (
                "safe_domain_fallback_after_rejection"
            )

            validation = self.validate_code(
                filename,
                code,
            )

        if not validation.get(
            "ok"
        ):
            return {
                "ok": False,
                "file": filename,
                "validation": validation,
            }

        if path.exists():
            backup_existing(
                path
            )

        atomic_write_text(
            path,
            code,
        )

        final_check = syntax_check_file(
            path
        )

        if not final_check.get(
            "ok"
        ):
            return {
                "ok": False,
                "file": filename,
                "verification":
                    final_check,
            }

        audit(
            "DOMAIN_BUILD_COMPLETED",
            details={
                "file": filename,
                "source": source,
                "repair_attempts":
                    repair_attempts,
                "sha256":
                    final_check.get(
                        "sha256"
                    ),
            },
        )

        return {
            "ok": True,
            "file": filename,
            "source": source,
            "repair_attempts":
                repair_attempts,
            "verification":
                final_check,
        }

    def build_all(
        self,
        plan: Dict[str, Any],
        *,
        force: bool = False,
    ) -> Dict[str, Any]:

        if not (
            ROOT
            / PRIMARY_FILE_02
        ).exists():

            return {
                "ok": False,
                "blocked": True,
                "reason": (
                    f"{PRIMARY_FILE_02} is required. "
                    "01 will not generate or overwrite 02."
                ),
            }

        results: Dict[str, Any] = {}

        for number in (
            "03",
            "04",
            "05",
        ):

            results[
                number
            ] = self.build_one(
                number,
                plan[
                    "ai_files"
                ][
                    number
                ],
                force=force,
            )

        return {
            "ok": all(
                item.get(
                    "ok"
                )
                for item in results.values()
            ),
            "results": results,
        }


# ============================================================
# AUTONOMOUS UI DESIGNER
# ============================================================

class AutonomousUIDesigner:

    def __init__(
        self,
        ai: AIProvider,
    ) -> None:

        self.ai = ai

    def inspect(
        self,
    ) -> Dict[str, Any]:

        if not UI_INDEX.exists():

            return {
                "ok": False,
                "exists": False,
                "path": str(
                    UI_INDEX
                ),
            }

        try:

            content = UI_INDEX.read_text(
                encoding="utf-8"
            )

        except Exception as exc:

            return {
                "ok": False,
                "exists": True,
                "error": repr(
                    exc
                ),
            }

        required_api = [
            "/api/domains/search",
            "/api/domains/register",
            "/api/domains/renew",
            "/api/domains/transfer",
            "/api/domains/dns",
            "/api/domains/ssl",
            "/api/health",
        ]

        api_presence = {
            endpoint:
                endpoint in content
            for endpoint in required_api
        }

        return {
            "ok": True,
            "exists": True,
            "path":
                str(
                    UI_INDEX.relative_to(
                        ROOT
                    )
                ),
            "sha256":
                sha256_text(
                    content
                ),
            "rtl":
                (
                    'dir="rtl"' in content
                    or "direction: rtl" in content.lower()
                ),
            "api_presence":
                api_presence,
            "all_required_api_declared":
                all(
                    api_presence.values()
                ),
        }

    def validate_html(
        self,
        content: str,
    ) -> Dict[str, Any]:

        lower = content.lower()

        if "<html" not in lower:
            return {
                "ok": False,
                "reason":
                    "missing_html_root",
            }

        if "</html>" not in lower:
            return {
                "ok": False,
                "reason":
                    "missing_html_close",
            }

        forbidden = detect_forbidden_scope(
            content
        )

        if forbidden:
            return {
                "ok": False,
                "reason":
                    "forbidden_non_domain_scope",
                "patterns":
                    forbidden,
            }

        required_terms = (
            "/api/domains/search",
            "/api/domains/register",
            "/api/domains/renew",
            "/api/domains/transfer",
            "/api/domains/dns",
            "/api/health",
        )

        missing = [
            item
            for item in required_terms
            if item not in content
        ]

        if missing:
            return {
                "ok": False,
                "reason":
                    "required_domain_api_missing",
                "missing":
                    missing,
            }

        return {
            "ok": True,
            "sha256":
                sha256_text(
                    content
                ),
        }

    def improve(
        self,
    ) -> Dict[str, Any]:

        inspection = self.inspect()

        if not inspection.get(
            "ok"
        ):
            return {
                "ok": False,
                "action":
                    "ui_not_available",
                "inspection":
                    inspection,
            }

        if not self.ai.health().get(
            "ok"
        ):
            return {
                "ok": False,
                "action":
                    "designer_waiting_for_ai",
                "inspection":
                    inspection,
            }

        current_html = UI_INDEX.read_text(
            encoding="utf-8"
        )

        system_prompt = f"""
You are the autonomous official UI designer and frontend engineer
for MAJD-DMAIL.

MAJD-DMAIL IS A DOMAIN PLATFORM ONLY.

AUTHORITY:
- SUPREME_OWNER is permanently the highest authority.
- You are a subordinate designer.
- You may improve the official UI.
- You may never change owner authority.
- You may never remove owner controls.
- You may never create a higher authority.

YOUR JOB:
- Improve the EXISTING official UI.
- Keep MAJD brand identity.
- Keep Arabic RTL support.
- Keep English support where present.
- Keep responsive desktop/tablet/mobile design.
- Keep accessibility.
- Improve professional production quality.
- Connect buttons and flows to real domain APIs.
- Never simulate successful registration/payment/DNS operations.
- Show real backend errors when backend fails.
- Preserve useful existing content.
- Return one COMPLETE index.html.

DOMAIN API CONTRACTS:
GET/POST as appropriate:
- /api/health
- /api/domains/search
- /api/domains/register
- /api/domains/renew
- /api/domains/transfer
- /api/domains/dns
- /api/domains/ssl

FORBIDDEN:
- Email
- Mailboxes
- SMTP
- IMAP
- POP3
- Postfix
- Dovecot
- Webmail
- Paid email
- Services unrelated to domains

Return ONLY complete HTML.
"""

        user_prompt = f"""
CURRENT OFFICIAL UI:

{current_html}

Improve this production UI while preserving its MAJD identity.

Do not invent success.
Do not change the project into anything other than domains.
Return the full replacement index.html only.
"""

        result = self.ai.generate(
            system_prompt,
            user_prompt,
        )

        if not result.get(
            "ok"
        ):
            return {
                "ok": False,
                "action":
                    "designer_ai_failed",
                "error":
                    result.get(
                        "error"
                    ),
            }

        proposed = extract_html_code(
            result[
                "text"
            ]
        )

        validation = self.validate_html(
            proposed
        )

        if not validation.get(
            "ok"
        ):
            return {
                "ok": False,
                "action":
                    "designer_output_rejected",
                "validation":
                    validation,
            }

        if sha256_text(
            current_html
        ) == sha256_text(
            proposed
        ):
            return {
                "ok": True,
                "action":
                    "ui_already_current",
                "validation":
                    validation,
            }

        backup_existing(
            UI_INDEX
        )

        atomic_write_text(
            UI_INDEX,
            proposed,
        )

        final_validation = self.validate_html(
            UI_INDEX.read_text(
                encoding="utf-8"
            )
        )

        if not final_validation.get(
            "ok"
        ):
            return {
                "ok": False,
                "action":
                    "post_write_ui_validation_failed",
                "validation":
                    final_validation,
            }

        result_payload = {
            "ok": True,
            "action":
                "official_ui_improved",
            "authority":
                DESIGNER_AUTHORITY,
            "owner_authority":
                OWNER_AUTHORITY,
            "validation":
                final_validation,
        }

        atomic_write_json(
            DESIGN_REPORT_FILE,
            result_payload,
        )

        audit(
            "AUTONOMOUS_UI_DESIGN_COMPLETED",
            details={
                "action":
                    result_payload[
                        "action"
                    ],
                "owner_authority":
                    OWNER_AUTHORITY,
            },
        )

        return result_payload


# ============================================================
# VERIFIER
# ============================================================

class ProjectVerifier:

    def verify_primary_policy(
        self,
    ) -> Dict[str, Any]:

        files = list_primary_files()

        violations = [
            filename
            for filename in files
            if (
                extract_primary_number(
                    filename
                )
                or 0
            ) > 5
        ]

        return {
            "ok":
                not violations,
            "files":
                files,
            "limit":
                MAX_PRIMARY_FILES,
            "violations":
                violations,
        }

    def verify_python(
        self,
    ) -> Dict[str, Any]:

        results = {
            filename:
                syntax_check_file(
                    ROOT
                    / filename
                )
            for filename in list_primary_files()
        }

        return {
            "ok": all(
                item.get(
                    "ok"
                )
                for item in results.values()
            ),
            "files": results,
        }

    def verify_domain_scope(
        self,
    ) -> Dict[str, Any]:

        findings: Dict[
            str,
            List[str],
        ] = {}

        for number in (
            "03",
            "04",
            "05",
        ):

            filename = GENERATED_FILES[
                number
            ]

            path = ROOT / filename

            if not path.exists():
                continue

            content = path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            hits = detect_forbidden_scope(
                content
            )

            if hits:
                findings[
                    filename
                ] = hits

        return {
            "ok":
                not findings,
            "scope":
                "DOMAINS_ONLY",
            "findings":
                findings,
        }

    def verify_ui(
        self,
        designer: AutonomousUIDesigner,
    ) -> Dict[str, Any]:

        return designer.inspect()

    def full(
        self,
        ai: AIProvider,
        designer: AutonomousUIDesigner,
    ) -> Dict[str, Any]:

        policy = self.verify_primary_policy()
        python_result = self.verify_python()
        scope = self.verify_domain_scope()
        ui = self.verify_ui(
            designer
        )
        ai_health = ai.health()

        report = {
            "timestamp":
                utc_now(),
            "project":
                PROJECT_NAME,
            "project_kind":
                PROJECT_KIND,
            "owner_authority":
                OWNER_AUTHORITY,
            "scope":
                "DOMAINS_ONLY",
            "policy":
                policy,
            "python":
                python_result,
            "domain_scope":
                scope,
            "ui":
                ui,
            "ai":
                ai_health,
            "core_ok":
                bool(
                    policy.get(
                        "ok"
                    )
                    and
                    python_result.get(
                        "ok"
                    )
                    and
                    scope.get(
                        "ok"
                    )
                ),
            "ui_ready":
                bool(
                    ui.get(
                        "ok"
                    )
                ),
            "ai_operational":
                bool(
                    ai_health.get(
                        "ok"
                    )
                ),
        }

        atomic_write_json(
            REPORT_FILE,
            report,
        )

        return report


# ============================================================
# SELF REPAIR
# ============================================================

class SelfRepairEngine:

    def __init__(
        self,
        builder: AutonomousBuilder,
    ) -> None:

        self.builder = builder

    def repair(
        self,
        plan: Dict[str, Any],
    ) -> Dict[str, Any]:

        results: Dict[str, Any] = {}

        for number in (
            "03",
            "04",
            "05",
        ):

            specification = plan[
                "ai_files"
            ][
                number
            ]

            path = ROOT / specification[
                "filename"
            ]

            if not path.exists():

                results[
                    number
                ] = self.builder.build_one(
                    number,
                    specification,
                    force=True,
                )

                continue

            content = path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            syntax_result = syntax_check_file(
                path
            )

            policy_result = self.builder.validate_code(
                path.name,
                content,
            )

            if (
                syntax_result.get(
                    "ok"
                )
                and
                policy_result.get(
                    "ok"
                )
            ):

                results[
                    number
                ] = {
                    "ok": True,
                    "action":
                        "no_repair_needed",
                    "file":
                        path.name,
                }

                continue

            results[
                number
            ] = self.builder.build_one(
                number,
                specification,
                force=True,
            )

        return {
            "ok": all(
                item.get(
                    "ok"
                )
                for item in results.values()
            ),
            "results": results,
        }


# ============================================================
# MASTER MIND
# ============================================================

class MajdDmailMastermind:

    def __init__(
        self,
    ) -> None:

        self.state = load_state()

        self.ai = AIProvider()

        self.planner = ArchitecturePlanner(
            self.ai
        )

        self.builder = AutonomousBuilder(
            self.ai
        )

        self.designer = AutonomousUIDesigner(
            self.ai
        )

        self.verifier = ProjectVerifier()

        self.repair_engine = SelfRepairEngine(
            self.builder
        )

    def bootstrap(
        self,
    ) -> Dict[str, Any]:

        self.state[
            "phase"
        ] = "AUTONOMOUS_DOMAIN_OPERATION"

        save_state(
            self.state
        )

        result = {
            "ok": True,
            "project":
                PROJECT_NAME,
            "project_kind":
                PROJECT_KIND,
            "scope":
                "DOMAINS_ONLY",
            "version":
                VERSION,
            "owner_authority":
                OWNER_AUTHORITY,
            "ai_authority":
                AI_AUTHORITY,
            "designer_authority":
                DESIGNER_AUTHORITY,
            "file_01":
                THIS_FILENAME,
            "protected_file_02":
                PRIMARY_FILE_02,
            "ai_generated":
                [
                    "03",
                    "04",
                    "05",
                ],
            "official_ui":
                str(
                    UI_INDEX.relative_to(
                        ROOT
                    )
                ),
            "primary_file_limit":
                MAX_PRIMARY_FILES,
            "autonomous":
                True,
        }

        audit(
            "DOMAIN_MASTERmind_BOOTSTRAPPED",
            details=result,
        )

        return result

    def status(
        self,
    ) -> Dict[str, Any]:

        return {
            "timestamp":
                utc_now(),
            "project":
                PROJECT_NAME,
            "project_kind":
                PROJECT_KIND,
            "scope":
                "DOMAINS_ONLY",
            "version":
                VERSION,
            "phase":
                self.state.get(
                    "phase"
                ),
            "owner_authority":
                OWNER_AUTHORITY,
            "ai_authority":
                AI_AUTHORITY,
            "designer_authority":
                DESIGNER_AUTHORITY,
            "primary_file_limit":
                MAX_PRIMARY_FILES,
            "primary_files":
                list_primary_files(),
            "file_02_exists":
                (
                    ROOT
                    / PRIMARY_FILE_02
                ).exists(),
            "official_ui":
                self.designer.inspect(),
            "ai":
                self.ai.health(),
        }

    def plan(
        self,
        use_ai: bool = True,
    ) -> Dict[str, Any]:

        plan = self.planner.create(
            use_ai=use_ai
        )

        self.state[
            "last_plan"
        ] = {
            "timestamp":
                utc_now(),
            "source":
                plan.get(
                    "source"
                ),
            "ai_planning":
                plan.get(
                    "ai_planning"
                ),
        }

        save_state(
            self.state
        )

        audit(
            "DOMAIN_PLAN_CREATED",
            details=self.state[
                "last_plan"
            ],
        )

        return plan

    def build(
        self,
        force: bool = False,
    ) -> Dict[str, Any]:

        if not (
            ROOT
            / PRIMARY_FILE_02
        ).exists():

            return {
                "ok": False,
                "blocked": True,
                "reason": (
                    f"{PRIMARY_FILE_02} must exist. "
                    "AI is not allowed to replace file 02."
                ),
            }

        plan = self.plan(
            use_ai=True
        )

        result = self.builder.build_all(
            plan,
            force=force,
        )

        self.state[
            "last_build"
        ] = {
            "timestamp":
                utc_now(),
            "result":
                result,
        }

        if result.get(
            "ok"
        ):
            self.state[
                "phase"
            ] = "DOMAIN_CORE_READY"

        save_state(
            self.state
        )

        return result

    def design(
        self,
    ) -> Dict[str, Any]:

        result = self.designer.improve()

        self.state[
            "last_design"
        ] = {
            "timestamp":
                utc_now(),
            "result":
                result,
        }

        save_state(
            self.state
        )

        return result

    def verify(
        self,
    ) -> Dict[str, Any]:

        result = self.verifier.full(
            self.ai,
            self.designer,
        )

        self.state[
            "last_verify"
        ] = {
            "timestamp":
                utc_now(),
            "core_ok":
                result[
                    "core_ok"
                ],
            "ui_ready":
                result[
                    "ui_ready"
                ],
            "ai_operational":
                result[
                    "ai_operational"
                ],
        }

        save_state(
            self.state
        )

        audit(
            "DOMAIN_VERIFY_COMPLETED",
            details=self.state[
                "last_verify"
            ],
        )

        return result

    def repair(
        self,
    ) -> Dict[str, Any]:

        plan = self.plan(
            use_ai=True
        )

        result = self.repair_engine.repair(
            plan
        )

        self.state[
            "last_repair"
        ] = {
            "timestamp":
                utc_now(),
            "result":
                result,
        }

        save_state(
            self.state
        )

        audit(
            "DOMAIN_REPAIR_COMPLETED",
            details={
                "ok":
                    result.get(
                        "ok"
                    )
            },
        )

        return result

    def cycle(
        self,
    ) -> Dict[str, Any]:

        started_at = utc_now()

        # Always refresh the domain-only plan so stale email-era
        # plans can never remain authoritative.
        plan = self.plan(
            use_ai=True
        )

        initial = self.verify()

        build_result: Optional[
            Dict[str, Any]
        ] = None

        repair_result: Optional[
            Dict[str, Any]
        ] = None

        design_result: Optional[
            Dict[str, Any]
        ] = None

        if (
            ROOT
            / PRIMARY_FILE_02
        ).exists():

            needs_build = False

            for number in (
                "03",
                "04",
                "05",
            ):

                path = ROOT / plan[
                    "ai_files"
                ][
                    number
                ][
                    "filename"
                ]

                if not path.exists():
                    needs_build = True
                    break

                try:
                    content = path.read_text(
                        encoding="utf-8"
                    )
                except Exception:
                    needs_build = True
                    break

                if not self.builder.validate_code(
                    path.name,
                    content,
                ).get(
                    "ok"
                ):
                    needs_build = True
                    break

            if needs_build:

                build_result = self.builder.build_all(
                    plan,
                    force=True,
                )

            repair_result = self.repair_engine.repair(
                plan
            )

            # UI designer is autonomous but always subordinate
            # to SUPREME_OWNER.
            design_result = self.designer.improve()

        final = self.verify()

        result = {
            "started_at":
                started_at,
            "finished_at":
                utc_now(),
            "project":
                PROJECT_NAME,
            "scope":
                "DOMAINS_ONLY",
            "owner_authority":
                OWNER_AUTHORITY,
            "file_02_exists":
                (
                    ROOT
                    / PRIMARY_FILE_02
                ).exists(),
            "initial_verification":
                initial,
            "build_result":
                build_result,
            "repair_result":
                repair_result,
            "design_result":
                design_result,
            "final_verification":
                final,
        }

        self.state[
            "last_cycle"
        ] = {
            "timestamp":
                utc_now(),
            "core_ok":
                final.get(
                    "core_ok"
                ),
            "ui_ready":
                final.get(
                    "ui_ready"
                ),
            "ai_operational":
                final.get(
                    "ai_operational"
                ),
        }

        save_state(
            self.state
        )

        audit(
            "AUTONOMOUS_DOMAIN_CYCLE_COMPLETED",
            details=self.state[
                "last_cycle"
            ],
        )

        return result


# ============================================================
# OUTPUT
# ============================================================

def print_json(
    payload: Any,
) -> None:

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
            "MAJD-DMAIL autonomous DOMAIN-ONLY mastermind"
        ),
    )

    sub = parser.add_subparsers(
        dest="command"
    )

    sub.add_parser(
        "bootstrap"
    )

    sub.add_parser(
        "status"
    )

    plan_parser = sub.add_parser(
        "plan"
    )

    plan_parser.add_argument(
        "--no-ai",
        action="store_true",
    )

    build_command = sub.add_parser(
        "build"
    )

    build_command.add_argument(
        "--force",
        action="store_true",
    )

    sub.add_parser(
        "design"
    )

    sub.add_parser(
        "verify"
    )

    sub.add_parser(
        "repair"
    )

    sub.add_parser(
        "cycle"
    )

    loop_command = sub.add_parser(
        "loop"
    )

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
        int(
            interval
        ),
    )

    audit(
        "AUTONOMOUS_DOMAIN_LOOP_STARTED",
        details={
            "interval_seconds":
                interval,
            "scope":
                "DOMAINS_ONLY",
            "owner_authority":
                OWNER_AUTHORITY,
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
                    "cycle_completed":
                        utc_now(),
                    "scope":
                        "DOMAINS_ONLY",
                    "owner_authority":
                        OWNER_AUTHORITY,
                    "core_ok":
                        final.get(
                            "core_ok"
                        ),
                    "ui_ready":
                        final.get(
                            "ui_ready"
                        ),
                    "ai_operational":
                        final.get(
                            "ai_operational"
                        ),
                }
            )

        except KeyboardInterrupt:

            audit(
                "AUTONOMOUS_DOMAIN_LOOP_STOPPED",
                details={
                    "reason":
                        "keyboard_interrupt"
                },
            )

            return 0

        except Exception as exc:

            audit(
                "AUTONOMOUS_DOMAIN_LOOP_CYCLE_FAILED",
                status="ERROR",
                details={
                    "error":
                        repr(
                            exc
                        ),
                    "traceback":
                        traceback.format_exc(),
                },
            )

        time.sleep(
            interval
        )


# ============================================================
# MAIN
# ============================================================

def main() -> int:

    parser = build_parser()

    args = parser.parse_args()

    mastermind = MajdDmailMastermind()

    # If invoked with no command, do not sit idle.
    # Default behavior is the autonomous production cycle.
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

        print_json(
            result
        )

        return (
            0
            if result.get(
                "ok"
            )
            else 1
        )

    if command == "design":

        result = mastermind.design()

        print_json(
            result
        )

        return (
            0
            if result.get(
                "ok"
            )
            else 1
        )

    if command == "verify":

        result = mastermind.verify()

        print_json(
            result
        )

        return (
            0
            if result.get(
                "core_ok"
            )
            else 1
        )

    if command == "repair":

        result = mastermind.repair()

        print_json(
            result
        )

        return (
            0
            if result.get(
                "ok"
            )
            else 1
        )

    if command == "cycle":

        result = mastermind.cycle()

        print_json(
            result
        )

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
