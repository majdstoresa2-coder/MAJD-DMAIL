#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD-DMAIL
MAJD-DMAIL-AI-AUTOMATION-MASTERMIND-01.py

FILE 01
SOVEREIGN AUTONOMOUS AI + AUTOMATION COMPANY
FOR THE MAJD-DMAIL DOMAIN PLATFORM

VERSION 5.0.0-CLOSURE

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
    PAYMENT IMPLEMENTATION IS OUTSIDE THE CURRENT MISSION.

FORBIDDEN:
    Email hosting
    Mailboxes
    SMTP / IMAP / POP3
    Postfix / Dovecot / Webmail
    Payment implementation
    Simulation / mock / fake domain execution
    Fake external-provider success
    Fake domain availability
    Fake registration / renewal / transfer success

DOMAIN AUTHORITY POLICY:
    RDAP:
        PRIMARY REQUIRED DISCOVERY PROTOCOL.

    WHOIS:
        OPTIONAL LEGACY FALLBACK.
        NEVER REQUIRED FOR CORE READINESS.

    REGISTRAR / RESELLER ADAPTER:
        PRIMARY EXTERNAL EXECUTION PATH.

    REGISTRY / EPP:
        OPTIONAL ADVANCED DIRECT-REGISTRY PATH.
        NEVER REQUIRED FOR INITIAL PRODUCTION OPERATION.

    REGISTRATION:
        MUST NEVER EXECUTE UNTIL AUTHORITATIVE AVAILABILITY
        HAS BEEN OBTAINED FROM A VERIFIED PROVIDER.

    PROVIDER STATES:
        not_configured
        configured
        verified
        unavailable

    NO OTHER PROVIDER STATE MAY BE TREATED AS VERIFIED.

    DOMAIN NORMALIZATION:
        Every externally supplied domain MUST pass through strict
        FQDN normalization before search, registration, renewal,
        transfer, DNS, DNSSEC, nameserver or TLS operations.

    IDEMPOTENCY:
        Registration, renewal and transfer MUST require/use an
        idempotency key and MUST NOT duplicate a completed operation.

    LIFECYCLE:
        registered
        active
        expiring
        expired
        redemption
        pending_delete
        transfer_pending
        transferred
        suspended
        deleted
        unknown

AUTONOMOUS ENGINEERING PIPELINE:

    DISCOVER
        -> ANALYZE REAL CONTRACTS
        -> PLAN
        -> BUILD
        -> STATIC CONTRACT VALIDATION
        -> SYNTAX VALIDATION
        -> SAFE IMPORT
        -> INTERFACE VERIFICATION
        -> ROUTE INSPECTION
        -> INTERNAL API TEST
        -> PROVIDER STATE VERIFICATION
        -> START / RESTART RUNTIME
        -> LIVE HEALTH VERIFY
        -> TARGETED REPAIR
        -> VERIFY
        -> REPORT
        -> RETRY LATER IF REQUIRED

NO FAKE SUCCESS.

Syntax alone is never platform success.
String presence alone is never capability evidence.
HTTP 200 alone is never MAJD-DMAIL health success.
Configured does not mean verified.
Provider availability is never claimed without a real probe.
Registration is never allowed from a guessed availability result.
AI failure never replaces useful existing code with a fallback stub.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import importlib.util
import inspect
import json
import logging
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple


# ============================================================
# IDENTITY / AUTHORITY
# ============================================================

PROJECT_NAME = "MAJD-DMAIL"
PROJECT_KIND = "SOVEREIGN_DOMAIN_PLATFORM"
PROJECT_SCOPE = "DOMAINS_ONLY"
VERSION = "5.0.0-CLOSURE"

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

PROTECTED_FILES: Tuple[str, ...] = (
    THIS_FILENAME,
    PRIMARY_FILE_02,
)

AI_MANAGED_NUMBERS: Set[int] = {3, 4, 5}

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

# llama3.2:3b is not allowed to run uncontrolled giant generations.
AI_CODE_PREDICT = max(
    1024,
    min(
        6144,
        int(os.getenv("MAJD_AI_CODE_NUM_PREDICT", "4096")),
    ),
)

AI_PLAN_PREDICT = max(
    384,
    min(
        1536,
        int(os.getenv("MAJD_AI_PLAN_NUM_PREDICT", "1024")),
    ),
)

AI_TEMPERATURE = float(
    os.getenv("MAJD_AI_TEMPERATURE", "0.0")
)

# IMPORTANT:
# Old default was 900 seconds.
# Closure default is intentionally 120 seconds.
AI_TIMEOUT = max(
    30,
    min(
        300,
        int(os.getenv("MAJD_AI_TIMEOUT", "120")),
    ),
)

AI_HEALTH_TIMEOUT = max(
    2,
    min(
        20,
        int(os.getenv("MAJD_AI_HEALTH_TIMEOUT", "5")),
    ),
)

AI_REPAIR_ATTEMPTS = max(
    1,
    min(
        3,
        int(os.getenv("MAJD_AI_REPAIR_ATTEMPTS", "2")),
    ),
)

API_PORT = int(
    os.getenv("MAJD_DMAIL_API_PORT", "8080")
)

API_HOST = os.getenv(
    "MAJD_DMAIL_API_HOST",
    "127.0.0.1",
).strip()

RUNTIME_START_TIMEOUT = max(
    5,
    min(
        60,
        int(os.getenv("MAJD_RUNTIME_START_TIMEOUT", "25")),
    ),
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
# DOMAIN CONTRACT
# ============================================================

PROVIDER_STATE_NOT_CONFIGURED = "not_configured"
PROVIDER_STATE_CONFIGURED = "configured"
PROVIDER_STATE_VERIFIED = "verified"
PROVIDER_STATE_UNAVAILABLE = "unavailable"

VALID_PROVIDER_STATES: Tuple[str, ...] = (
    PROVIDER_STATE_NOT_CONFIGURED,
    PROVIDER_STATE_CONFIGURED,
    PROVIDER_STATE_VERIFIED,
    PROVIDER_STATE_UNAVAILABLE,
)

DOMAIN_LIFECYCLE_STATES: Tuple[str, ...] = (
    "registered",
    "active",
    "expiring",
    "expired",
    "redemption",
    "pending_delete",
    "transfer_pending",
    "transferred",
    "suspended",
    "deleted",
    "unknown",
)

AUTHORITATIVE_AVAILABILITY_STATES: Tuple[str, ...] = (
    "available",
    "unavailable",
    "reserved",
    "premium",
    "unknown",
)

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

ALL_REQUIRED_ENDPOINTS: Tuple[str, ...] = tuple(
    endpoint
    for endpoints in REQUIRED_API_ENDPOINTS.values()
    for endpoint in endpoints
)


# ============================================================
# REQUIRED COMPONENT INTERFACES
# ============================================================

FILE03_REQUIRED_CALLABLES: Tuple[str, ...] = (
    "normalize_fqdn",
    "provider_status",
    "authoritative_availability",
    "search_domain",
    "get_domain",
    "register_domain",
    "renew_domain",
    "transfer_domain",
    "configure_dns",
    "configure_nameservers",
    "configure_dnssec",
    "provision_domain_tls",
)

FILE04_REQUIRED_CALLABLES: Tuple[str, ...] = (
    "authorize_domain_action",
    "audit_domain_action",
    "validate_owner_authority",
    "record_security_event",
    "monitor_domain_operation",
)

FILE05_REQUIRED_CALLABLES: Tuple[str, ...] = (
    "create_app",
)

IDEMPOTENT_OPERATIONS: Tuple[str, ...] = (
    "register_domain",
    "renew_domain",
    "transfer_domain",
)

NORMALIZED_DOMAIN_OPERATIONS: Tuple[str, ...] = (
    "authoritative_availability",
    "search_domain",
    "get_domain",
    "register_domain",
    "renew_domain",
    "transfer_domain",
    "configure_dns",
    "configure_nameservers",
    "configure_dnssec",
    "provision_domain_tls",
)


# ============================================================
# CAPABILITY CONTRACT
# ============================================================

REQUIRED_CAPABILITIES: Dict[str, Dict[str, Any]] = {
    "fqdn_normalization": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "domain_search": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "authoritative_domain_availability": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "domain_registration": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "domain_renewal": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "domain_transfer": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "domain_lifecycle": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "domain_details": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "idempotent_domain_mutations": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "registrar_reseller_adapter": {
        "required_internal": True,
        "external": True,
        "production_required": True,
        "source": "03",
    },
    "rdap": {
        "required_internal": True,
        "external": True,
        "production_required": True,
        "source": "03",
    },
    "whois_legacy": {
        "required_internal": False,
        "external": True,
        "production_required": False,
        "source": "03",
    },
    "registry_epp_direct": {
        "required_internal": False,
        "external": True,
        "production_required": False,
        "source": "03",
    },
    "dns_management": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "nameserver_management": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "dnssec_management": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "domain_tls_management": {
        "required_internal": True,
        "external": False,
        "source": "03",
    },
    "owner_control": {
        "required_internal": True,
        "external": False,
        "source": "04",
    },
    "authorization": {
        "required_internal": True,
        "external": False,
        "source": "04",
    },
    "security": {
        "required_internal": True,
        "external": False,
        "source": "04",
    },
    "audit": {
        "required_internal": True,
        "external": False,
        "source": "04",
    },
    "monitoring": {
        "required_internal": True,
        "external": False,
        "source": "04",
    },
    "http_api": {
        "required_internal": True,
        "external": False,
        "source": "05",
    },
    "runtime_health": {
        "required_internal": True,
        "external": False,
        "source": "05",
    },
    "official_ui_integration": {
        "required_internal": True,
        "external": False,
        "source": "UI",
    },
}


# ============================================================
# FORBIDDEN IMPLEMENTATION
# ============================================================

FORBIDDEN_NON_DOMAIN_PATTERNS: Tuple[str, ...] = (
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

FORBIDDEN_PAYMENT_PATTERNS: Tuple[str, ...] = (
    r"\bmoyasar\b",
    r"\bstripe\b",
    r"\bpaypal\b",
    r"\bcheckout[_\s-]?payment\b",
    r"\bpayment[_\s-]?provider\b",
    r"\bprocess[_\s-]?payment\b",
    r"\bcharge[_\s-]?card\b",
)

FORBIDDEN_FAKE_OPERATION_PATTERNS: Tuple[str, ...] = (
    r"\bsimulat(?:e|ed|ion|or)\b",
    r"\bmock(?:ed|ing)?\b",
    r"\bfake\b",
    r"\bdummy\b",
    r"\bplaceholder\b",
    r"\bstub\b",
    r"\bpretend\b",
    r"\bsynthetic[_\s-]?availability\b",
)

DANGEROUS_CODE_PATTERNS: Tuple[str, ...] = (
    r"\beval\s*\(",
    r"\bexec\s*\(",
    r"\bos\.system\s*\(",
)

PRIMARY_PATTERN = re.compile(
    r"^MAJD-DMAIL-[A-Z0-9\-]+-(0[1-5])\.py$",
    re.IGNORECASE,
)


# ============================================================
# PLATFORM MISSION
# ============================================================

PLATFORM_MISSION: Dict[str, Any] = {
    "project": PROJECT_NAME,
    "kind": PROJECT_KIND,
    "scope": PROJECT_SCOPE,
    "owner_authority": OWNER_AUTHORITY,
    "protected_files": list(PROTECTED_FILES),
    "ai_managed_files": GENERATED_FILES,
    "primary_file_limit": MAX_PRIMARY_FILES,
    "required_api_endpoints": ALL_REQUIRED_ENDPOINTS,
    "provider_states": VALID_PROVIDER_STATES,
    "domain_lifecycle_states": DOMAIN_LIFECYCLE_STATES,
    "payment_enabled": False,
    "email_enabled": False,
    "rdap_required": True,
    "whois_required": False,
    "registrar_reseller_required": True,
    "direct_epp_required": False,
    "authoritative_availability_required_before_registration": True,
    "idempotency_required": list(IDEMPOTENT_OPERATIONS),
    "rules": [
        "SUPREME_OWNER is permanently highest authority.",
        "01 and 02 are protected.",
        "AI may modify only 03, 04 and 05.",
        "Never create primary 06+.",
        "Domains only.",
        "No email hosting.",
        "No payment implementation in current mission.",
        "RDAP is primary.",
        "WHOIS is optional legacy fallback.",
        "Registrar/reseller adapter is sufficient for first production path.",
        "Direct registry/EPP is optional.",
        "No simulation, mock, fake or placeholder domain execution.",
        "Configured provider is not verified provider.",
        "External success requires provider state verified.",
        "Registration requires authoritative availability.",
        "Every domain operation requires normalized FQDN.",
        "Registration, renewal and transfer require idempotency.",
        "Preserve useful working code if AI fails.",
        "Validate before installation.",
        "Rollback failed replacement.",
        "HTTP 200 alone is not platform health.",
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
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

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

        os.replace(
            temp_name,
            path,
        )

    finally:
        if os.path.exists(temp_name):
            try:
                os.unlink(temp_name)
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
            default=str,
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
                default=str,
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

    append_jsonl(
        EVENTS_FILE,
        payload,
    )

    if status.upper() in {
        "ERROR",
        "FAILED",
        "CRITICAL",
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


def extract_primary_number(
    filename: str,
) -> Optional[int]:
    match = PRIMARY_PATTERN.fullmatch(filename)

    if not match:
        return None

    return int(match.group(1))


def list_primary_files() -> List[str]:
    return sorted(
        path.name
        for path in ROOT.glob("MAJD-DMAIL-*.py")
        if extract_primary_number(path.name) is not None
    )


def enforce_generated_filename(
    filename: str,
) -> int:
    number = extract_primary_number(filename)

    if number not in AI_MANAGED_NUMBERS:
        raise PermissionError(
            "AI may modify only primary files 03, 04 and 05."
        )

    return int(number)


def safe_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except Exception:
        return str(path)


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


def extract_json_object(
    text: str,
) -> Optional[Dict[str, Any]]:
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

        if isinstance(value, dict):
            return value

    except Exception:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start >= 0 and end > start:
        try:
            value = json.loads(
                cleaned[start:end + 1]
            )

            if isinstance(value, dict):
                return value

        except Exception:
            pass

    return None


def backup_existing(
    path: Path,
) -> Optional[Path]:
    if not path.exists():
        return None

    stamp = dt.datetime.now().strftime(
        "%Y%m%d-%H%M%S-%f"
    )

    relative = safe_relative(path).replace(
        "/",
        "__",
    )

    target = (
        BACKUP_DIR
        / f"{relative}.{stamp}.bak"
    )

    shutil.copy2(
        path,
        target,
    )

    audit(
        "BACKUP_CREATED",
        details={
            "source": safe_relative(path),
            "backup": safe_relative(target),
        },
    )

    return target


def restore_backup(
    backup: Optional[Path],
    target: Path,
) -> bool:
    if backup is None or not backup.exists():
        return False

    shutil.copy2(
        backup,
        target,
    )

    audit(
        "BACKUP_RESTORED",
        details={
            "target": safe_relative(target),
            "backup": safe_relative(backup),
        },
    )

    return True


# ============================================================
# STRICT FQDN NORMALIZATION
# ============================================================

class DomainNormalizationError(ValueError):
    pass


def normalize_fqdn(
    value: str,
) -> str:
    """
    Canonical domain normalization used by 01 for validation/tests.

    Rules:
    - Accept domain only, not URL/path/email.
    - Lowercase.
    - Strip one trailing root dot.
    - IDNA encode each label.
    - Require at least two labels.
    - Reject empty labels.
    - Reject repeated adjacent labels such as example.com.com.
    - Enforce DNS label/FQDN lengths.
    """

    if not isinstance(value, str):
        raise DomainNormalizationError(
            "domain_must_be_string"
        )

    raw = value.strip()

    if not raw:
        raise DomainNormalizationError(
            "domain_empty"
        )

    if "://" in raw:
        raise DomainNormalizationError(
            "url_not_domain"
        )

    if any(
        token in raw
        for token in (
            "/",
            "\\",
            "?",
            "#",
            "@",
            ":",
        )
    ):
        raise DomainNormalizationError(
            "domain_contains_non_fqdn_components"
        )

    raw = raw.rstrip(".").strip().lower()

    if not raw:
        raise DomainNormalizationError(
            "domain_empty_after_normalization"
        )

    unicode_labels = raw.split(".")

    if len(unicode_labels) < 2:
        raise DomainNormalizationError(
            "fqdn_requires_public_suffix_label"
        )

    if any(not label for label in unicode_labels):
        raise DomainNormalizationError(
            "empty_domain_label"
        )

    ascii_labels: List[str] = []

    for label in unicode_labels:
        try:
            encoded = label.encode("idna").decode("ascii")
        except UnicodeError as exc:
            raise DomainNormalizationError(
                f"idna_error:{exc}"
            ) from exc

        if len(encoded) > 63:
            raise DomainNormalizationError(
                "domain_label_too_long"
            )

        if encoded.startswith("-") or encoded.endswith("-"):
            raise DomainNormalizationError(
                "domain_label_hyphen_boundary"
            )

        if not re.fullmatch(
            r"[a-z0-9-]+",
            encoded,
        ):
            raise DomainNormalizationError(
                "invalid_domain_label"
            )

        ascii_labels.append(encoded)

    # Prevent the exact class of malformed duplication:
    # example.com.com / example.net.net etc.
    if (
        len(ascii_labels) >= 3
        and ascii_labels[-1] == ascii_labels[-2]
    ):
        raise DomainNormalizationError(
            "duplicated_terminal_label"
        )

    fqdn = ".".join(ascii_labels)

    if len(fqdn.encode("ascii")) > 253:
        raise DomainNormalizationError(
            "fqdn_too_long"
        )

    return fqdn


# ============================================================
# SOURCE / AST ANALYSIS
# ============================================================

def parse_tree(
    content: str,
) -> Optional[ast.AST]:
    try:
        return ast.parse(content)
    except SyntaxError:
        return None


def source_metrics(
    content: str,
) -> Dict[str, Any]:
    tree = parse_tree(content)

    functions = 0
    async_functions = 0
    classes = 0

    if tree is not None:
        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.FunctionDef,
            ):
                functions += 1

            elif isinstance(
                node,
                ast.AsyncFunctionDef,
            ):
                async_functions += 1

            elif isinstance(
                node,
                ast.ClassDef,
            ):
                classes += 1

    return {
        "bytes": len(
            content.encode("utf-8")
        ),
        "lines": len(
            content.splitlines()
        ),
        "functions": functions,
        "async_functions": async_functions,
        "classes": classes,
    }


def ast_callable_names(
    content: str,
) -> Set[str]:
    tree = parse_tree(content)

    if tree is None:
        return set()

    names: Set[str] = set()

    for node in ast.walk(tree):
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            names.add(node.name)

    return names


def ast_class_names(
    content: str,
) -> Set[str]:
    tree = parse_tree(content)

    if tree is None:
        return set()

    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    }


def ast_assignment_names(
    content: str,
) -> Set[str]:
    tree = parse_tree(content)

    if tree is None:
        return set()

    result: Set[str] = set()

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.Assign,
                ast.AnnAssign,
            ),
        ):

            targets: List[ast.AST] = []

            if isinstance(node, ast.Assign):
                targets.extend(node.targets)
            else:
                targets.append(node.target)

            for target in targets:
                if isinstance(target, ast.Name):
                    result.add(target.id)

    return result


def find_function_node(
    content: str,
    function_name: str,
) -> Optional[ast.AST]:
    tree = parse_tree(content)

    if tree is None:
        return None

    for node in ast.walk(tree):
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            if node.name == function_name:
                return node

    return None


def function_argument_names(
    node: ast.AST,
) -> Set[str]:
    args = getattr(node, "args", None)

    if args is None:
        return set()

    names: Set[str] = set()

    for item in list(args.args) + list(args.kwonlyargs):
        names.add(item.arg)

    if args.vararg:
        names.add(args.vararg.arg)

    if args.kwarg:
        names.add(args.kwarg.arg)

    return names


def called_names(
    node: ast.AST,
) -> Set[str]:
    result: Set[str] = set()

    for child in ast.walk(node):

        if not isinstance(child, ast.Call):
            continue

        func = child.func

        if isinstance(func, ast.Name):
            result.add(func.id)

        elif isinstance(func, ast.Attribute):
            result.add(func.attr)

    return result


def string_constants(
    content: str,
) -> Set[str]:
    tree = parse_tree(content)

    if tree is None:
        return set()

    result: Set[str] = set()

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
        ):
            result.add(node.value)

    return result


def contains_patterns(
    content: str,
    patterns: Sequence[str],
) -> List[str]:
    return [
        pattern
        for pattern in patterns
        if re.search(
            pattern,
            content,
            re.IGNORECASE,
        )
    ]


def dangerous_patterns(
    content: str,
) -> List[str]:
    return contains_patterns(
        content,
        DANGEROUS_CODE_PATTERNS,
    )


def forbidden_scope_patterns(
    content: str,
) -> List[str]:
    return (
        contains_patterns(
            content,
            FORBIDDEN_NON_DOMAIN_PATTERNS,
        )
        + contains_patterns(
            content,
            FORBIDDEN_PAYMENT_PATTERNS,
        )
    )


def fake_operation_patterns(
    content: str,
) -> List[str]:
    """
    Generated 03/04/05 must not contain fake-operation primitives.

    These words are deliberately prohibited from generated code.
    01 may mention them because 01 is the validator.
    """

    return contains_patterns(
        content,
        FORBIDDEN_FAKE_OPERATION_PATTERNS,
    )


# ============================================================
# IDEMPOTENCY CONTRACT ANALYSIS
# ============================================================

def inspect_idempotency_contract(
    content: str,
) -> Dict[str, Any]:
    results: Dict[str, Any] = {}

    for operation in IDEMPOTENT_OPERATIONS:

        node = find_function_node(
            content,
            operation,
        )

        if node is None:
            results[operation] = {
                "ok": False,
                "reason": "operation_missing",
            }
            continue

        arguments = function_argument_names(node)

        has_key = (
            "idempotency_key" in arguments
            or "request_id" in arguments
            or "operation_id" in arguments
        )

        calls = called_names(node)

        has_storage_action = bool(
            calls.intersection(
                {
                    "get_idempotency_record",
                    "load_idempotency_record",
                    "check_idempotency",
                    "reserve_idempotency_key",
                    "save_idempotency_record",
                    "store_idempotency_result",
                    "record_idempotency_result",
                    "idempotency_lookup",
                    "idempotency_get",
                    "idempotency_set",
                }
            )
        )

        results[operation] = {
            "ok": bool(
                has_key
                and has_storage_action
            ),
            "has_idempotency_argument": has_key,
            "has_idempotency_storage_call": has_storage_action,
            "calls": sorted(calls),
        }

    return {
        "ok": all(
            item.get("ok")
            for item in results.values()
        ),
        "operations": results,
    }


# ============================================================
# AUTHORITATIVE AVAILABILITY CONTRACT ANALYSIS
# ============================================================

def inspect_registration_guard(
    content: str,
) -> Dict[str, Any]:
    node = find_function_node(
        content,
        "register_domain",
    )

    if node is None:
        return {
            "ok": False,
            "reason": "register_domain_missing",
        }

    calls = called_names(node)

    authoritative_check = bool(
        calls.intersection(
            {
                "authoritative_availability",
                "check_authoritative_availability",
            }
        )
    )

    normalization = bool(
        calls.intersection(
            {
                "normalize_fqdn",
                "normalize_domain",
            }
        )
    )

    provider_check = bool(
        calls.intersection(
            {
                "provider_status",
                "require_verified_provider",
                "ensure_verified_provider",
                "verified_provider",
            }
        )
    )

    return {
        "ok": bool(
            authoritative_check
            and normalization
            and provider_check
        ),
        "authoritative_availability_call": authoritative_check,
        "normalization_call": normalization,
        "verified_provider_check": provider_check,
        "calls": sorted(calls),
    }


# ============================================================
# DOMAIN NORMALIZATION CONTRACT ANALYSIS
# ============================================================

def inspect_domain_normalization_contract(
    content: str,
) -> Dict[str, Any]:
    results: Dict[str, Any] = {}

    for operation in NORMALIZED_DOMAIN_OPERATIONS:

        node = find_function_node(
            content,
            operation,
        )

        if node is None:
            results[operation] = {
                "ok": False,
                "reason": "operation_missing",
            }
            continue

        calls = called_names(node)

        normalized = bool(
            calls.intersection(
                {
                    "normalize_fqdn",
                    "normalize_domain",
                }
            )
        )

        # normalize_fqdn itself obviously does not call itself.
        if operation == "normalize_fqdn":
            normalized = True

        results[operation] = {
            "ok": normalized,
            "normalization_call": normalized,
        }

    return {
        "ok": all(
            item.get("ok")
            for item in results.values()
        ),
        "operations": results,
    }


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
    state = read_json(
        STATE_FILE,
        dict(DEFAULT_STATE),
    )

    if not isinstance(state, dict):
        state = dict(DEFAULT_STATE)

    if not state.get("created_at"):
        state["created_at"] = utc_now()

    state["project"] = PROJECT_NAME
    state["version"] = VERSION
    state["owner_authority"] = OWNER_AUTHORITY
    state["updated_at"] = utc_now()

    return state


def save_state(
    state: Dict[str, Any],
) -> None:
    state["project"] = PROJECT_NAME
    state["version"] = VERSION
    state["owner_authority"] = OWNER_AUTHORITY
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

        self.timeout = AI_TIMEOUT

    def health(self) -> Dict[str, Any]:
        request = urllib.request.Request(
            f"{self.base_url}/api/tags",
            method="GET",
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=AI_HEALTH_TIMEOUT,
            ) as response:
                payload = json.loads(
                    response.read().decode(
                        "utf-8",
                        errors="replace",
                    )
                )

            models = [
                str(item.get("name"))
                for item in payload.get(
                    "models",
                    [],
                )
                if isinstance(item, dict)
                and item.get("name")
            ]

            requested_base = (
                self.model.split(":")[0]
            )

            requested_available = any(
                name == self.model
                or name.startswith(
                    requested_base + ":"
                )
                for name in models
            )

            return {
                "ok": requested_available,
                "state": (
                    PROVIDER_STATE_VERIFIED
                    if requested_available
                    else PROVIDER_STATE_UNAVAILABLE
                ),
                "provider": "ollama",
                "base_url": self.base_url,
                "requested_model": self.model,
                "requested_model_available": requested_available,
                "available_models": models,
            }

        except Exception as exc:
            return {
                "ok": False,
                "state": PROVIDER_STATE_UNAVAILABLE,
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

        request = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(
                payload
            ).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
            },
        )

        started = time.time()

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
                response_payload.get(
                    "response",
                    "",
                )
            ).strip()

            done = bool(
                response_payload.get(
                    "done",
                    False,
                )
            )

            result = {
                "ok": bool(text) and done,
                "text": text,
                "provider": "ollama",
                "model": self.model,
                "done": done,
                "done_reason": response_payload.get(
                    "done_reason"
                ),
                "prompt_eval_count": response_payload.get(
                    "prompt_eval_count"
                ),
                "eval_count": response_payload.get(
                    "eval_count"
                ),
                "elapsed_seconds": round(
                    time.time() - started,
                    3,
                ),
            }

            if not text:
                result["error"] = (
                    "empty_generation"
                )

            elif not done:
                result["error"] = (
                    "generation_not_completed"
                )

            return result

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
                "elapsed_seconds": round(
                    time.time() - started,
                    3,
                ),
            }

        except TimeoutError:
            return {
                "ok": False,
                "text": "",
                "provider": "ollama",
                "model": self.model,
                "error": "ai_timeout",
                "timeout_seconds": self.timeout,
                "elapsed_seconds": round(
                    time.time() - started,
                    3,
                ),
            }

        except Exception as exc:
            return {
                "ok": False,
                "text": "",
                "provider": "ollama",
                "model": self.model,
                "error": repr(exc),
                "elapsed_seconds": round(
                    time.time() - started,
                    3,
                ),
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
                "path": safe_relative(path),
            }

        content = read_text(path)

        syntax_ok, syntax_error = (
            syntax_check_content(content)
        )

        return {
            "exists": True,
            "path": safe_relative(path),
            "sha256": sha256_text(content),
            "syntax_ok": syntax_ok,
            "syntax_error": syntax_error,
            "metrics": source_metrics(content),
        }

    def inspect_ui(self) -> Dict[str, Any]:
        if not UI_INDEX.exists():
            return {
                "exists": False,
                "path": safe_relative(UI_INDEX),
            }

        content = read_text(UI_INDEX)

        endpoints = {
            endpoint: endpoint in content
            for endpoint in ALL_REQUIRED_ENDPOINTS
        }

        forbidden = (
            forbidden_scope_patterns(content)
        )

        return {
            "exists": True,
            "path": safe_relative(UI_INDEX),
            "sha256": sha256_text(content),
            "bytes": len(
                content.encode("utf-8")
            ),
            "lines": len(
                content.splitlines()
            ),
            "rtl": (
                'dir="rtl"' in content.lower()
                or "direction: rtl" in content.lower()
            ),
            "endpoint_declarations": endpoints,
            "declares_all_required_endpoints": all(
                endpoints.values()
            ),
            "has_fetch": "fetch(" in content,
            "forbidden_hits": forbidden,
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
                number: self.inspect_file(
                    ROOT / filename
                )
                for number, filename
                in GENERATED_FILES.items()
            },
            "official_ui": self.inspect_ui(),
            "primary_files": list_primary_files(),
        }


# ============================================================
# GENERATED CODE VALIDATOR
# ============================================================

class GeneratedCodeValidator:

    def validate_common(
        self,
        number: str,
        filename: str,
        content: str,
    ) -> Optional[Dict[str, Any]]:

        enforce_generated_filename(filename)

        syntax_ok, syntax_error = (
            syntax_check_content(content)
        )

        if not syntax_ok:
            return {
                "ok": False,
                "reason": "syntax_error",
                "detail": syntax_error,
            }

        dangerous = dangerous_patterns(
            content
        )

        if dangerous:
            return {
                "ok": False,
                "reason": "dangerous_code_pattern",
                "patterns": dangerous,
            }

        forbidden_scope = (
            forbidden_scope_patterns(content)
        )

        if forbidden_scope:
            return {
                "ok": False,
                "reason": "forbidden_scope_or_payment",
                "patterns": forbidden_scope,
            }

        fake_patterns = (
            fake_operation_patterns(content)
        )

        if fake_patterns:
            return {
                "ok": False,
                "reason": "fake_or_simulated_domain_operation",
                "patterns": fake_patterns,
            }

        metrics = source_metrics(content)

        if metrics["lines"] < 80:
            return {
                "ok": False,
                "reason": "component_too_small",
                "metrics": metrics,
            }

        callable_names = ast_callable_names(
            content
        )

        assignment_names = ast_assignment_names(
            content
        )

        owner_contract = bool(
            {
                "OWNER_AUTHORITY",
                "SUPREME_OWNER",
            }.intersection(
                assignment_names
            )
            or "validate_owner_authority"
            in callable_names
            or OWNER_AUTHORITY in string_constants(
                content
            )
        )

        if not owner_contract:
            return {
                "ok": False,
                "reason": "supreme_owner_contract_missing",
            }

        return None

    def validate_03(
        self,
        content: str,
    ) -> Dict[str, Any]:

        callable_names = ast_callable_names(
            content
        )

        missing_callables = [
            name
            for name in FILE03_REQUIRED_CALLABLES
            if name not in callable_names
        ]

        if missing_callables:
            return {
                "ok": False,
                "reason": "file03_required_interfaces_missing",
                "missing": missing_callables,
            }

        assignments = ast_assignment_names(
            content
        )

        lifecycle_present = any(
            name in assignments
            for name in (
                "DOMAIN_LIFECYCLE_STATES",
                "LIFECYCLE_STATES",
                "DOMAIN_STATES",
            )
        )

        if not lifecycle_present:
            return {
                "ok": False,
                "reason": "domain_lifecycle_contract_missing",
            }

        provider_states_present = any(
            name in assignments
            for name in (
                "VALID_PROVIDER_STATES",
                "PROVIDER_STATES",
            )
        )

        if not provider_states_present:
            return {
                "ok": False,
                "reason": "provider_state_contract_missing",
                "required_states": VALID_PROVIDER_STATES,
            }

        idempotency = (
            inspect_idempotency_contract(
                content
            )
        )

        if not idempotency.get("ok"):
            return {
                "ok": False,
                "reason": "idempotency_contract_invalid",
                "contract": idempotency,
            }

        registration_guard = (
            inspect_registration_guard(
                content
            )
        )

        if not registration_guard.get(
            "ok"
        ):
            return {
                "ok": False,
                "reason": "authoritative_registration_guard_missing",
                "contract": registration_guard,
            }

        normalization = (
            inspect_domain_normalization_contract(
                content
            )
        )

        if not normalization.get("ok"):
            return {
                "ok": False,
                "reason": "fqdn_normalization_contract_incomplete",
                "contract": normalization,
            }

        return {
            "ok": True,
            "interfaces": sorted(
                callable_names.intersection(
                    FILE03_REQUIRED_CALLABLES
                )
            ),
            "idempotency": idempotency,
            "registration_guard": registration_guard,
            "normalization": normalization,
        }

    def validate_04(
        self,
        content: str,
    ) -> Dict[str, Any]:

        callable_names = ast_callable_names(
            content
        )

        missing = [
            name
            for name in FILE04_REQUIRED_CALLABLES
            if name not in callable_names
        ]

        if missing:
            return {
                "ok": False,
                "reason": "file04_required_interfaces_missing",
                "missing": missing,
            }

        return {
            "ok": True,
            "interfaces": sorted(
                callable_names.intersection(
                    FILE04_REQUIRED_CALLABLES
                )
            ),
        }

    def validate_05(
        self,
        content: str,
    ) -> Dict[str, Any]:

        callable_names = ast_callable_names(
            content
        )

        if "create_app" not in callable_names:
            return {
                "ok": False,
                "reason": "create_app_missing",
            }

        routes = RouteInspector().source_contract(
            content
        )

        if not routes.get("ok"):
            return {
                "ok": False,
                "reason": "runtime_route_contract_invalid",
                "routes": routes,
            }

        return {
            "ok": True,
            "routes": routes,
        }

    def validate(
        self,
        number: str,
        filename: str,
        content: str,
    ) -> Dict[str, Any]:

        common_failure = self.validate_common(
            number,
            filename,
            content,
        )

        if common_failure is not None:
            return common_failure

        if number == "03":
            specific = self.validate_03(
                content
            )

        elif number == "04":
            specific = self.validate_04(
                content
            )

        elif number == "05":
            specific = self.validate_05(
                content
            )

        else:
            return {
                "ok": False,
                "reason": "unsupported_generated_number",
            }

        if not specific.get("ok"):
            return specific

        return {
            "ok": True,
            "number": number,
            "filename": filename,
            "sha256": sha256_text(content),
            "metrics": source_metrics(content),
            "contract": specific,
        }


# ============================================================
# ROUTE INSPECTION
# ============================================================

class RouteInspector:

    @staticmethod
    def source_contract(
        content: str,
    ) -> Dict[str, Any]:

        strings = string_constants(content)

        detected = {
            endpoint
            for endpoint in ALL_REQUIRED_ENDPOINTS
            if endpoint in strings
        }

        # Flask/FastAPI decorators may still be represented
        # as literal AST strings.
        missing = [
            endpoint
            for endpoint in ALL_REQUIRED_ENDPOINTS
            if endpoint not in detected
        ]

        callable_names = ast_callable_names(
            content
        )

        runtime_evidence = (
            "create_app" in callable_names
        )

        return {
            "ok": bool(
                not missing
                and runtime_evidence
            ),
            "detected": sorted(detected),
            "missing": missing,
            "create_app": runtime_evidence,
        }

    def inspect_imported_routes(
        self,
        module: Any,
    ) -> Dict[str, Any]:

        app = getattr(
            module,
            "app",
            None,
        )

        if app is None:
            create_app = getattr(
                module,
                "create_app",
                None,
            )

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

        url_map = getattr(
            app,
            "url_map",
            None,
        )

        if url_map is not None:
            try:
                for rule in url_map.iter_rules():
                    routes.add(
                        str(rule.rule)
                    )
            except Exception:
                pass

        routes_attr = getattr(
            app,
            "routes",
            None,
        )

        if isinstance(
            routes_attr,
            list,
        ):
            for route in routes_attr:
                path = getattr(
                    route,
                    "path",
                    None,
                )

                if path:
                    routes.add(
                        str(path)
                    )

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

        factory = getattr(
            app,
            "test_client",
            None,
        )

        if callable(factory):
            return self._flask_test(
                factory
            )

        return {
            "ok": False,
            "reason": (
                "safe_internal_test_client_not_available"
            ),
        }

    @staticmethod
    def _flask_test(
        factory: Any,
    ) -> Dict[str, Any]:

        try:
            client = factory()

            response = client.get(
                "/api/health"
            )

            try:
                body = response.get_json()

            except Exception:
                body = None

            status_code = int(
                response.status_code
            )

            identity_ok = (
                isinstance(body, dict)
                and body.get("project")
                == PROJECT_NAME
            )

            scope_ok = (
                isinstance(body, dict)
                and body.get("scope")
                == PROJECT_SCOPE
            )

            owner_ok = (
                isinstance(body, dict)
                and body.get(
                    "owner_authority"
                )
                == OWNER_AUTHORITY
            )

            fake_success_ok = (
                isinstance(body, dict)
                and body.get(
                    "no_fake_success"
                )
                is True
            )

            return {
                "ok": bool(
                    200 <= status_code < 300
                    and identity_ok
                    and scope_ok
                    and owner_ok
                    and fake_success_ok
                ),
                "status_code": status_code,
                "json": body,
                "identity_ok": identity_ok,
                "scope_ok": scope_ok,
                "owner_ok": owner_ok,
                "no_fake_success_contract": (
                    fake_success_ok
                ),
            }

        except Exception as exc:
            return {
                "ok": False,
                "reason": "internal_api_test_failed",
                "error": repr(exc),
            }


# ============================================================
# SAFE MODULE LOADER
# ============================================================

class SafeModuleLoader:

    @staticmethod
    def load(
        path: Path,
        label: str,
    ) -> Dict[str, Any]:

        if not path.exists():
            return {
                "ok": False,
                "reason": "file_missing",
                "file": path.name,
            }

        module_name = (
            f"majd_dmail_{label}_"
            f"{uuid.uuid4().hex}"
        )

        try:
            spec = (
                importlib.util.spec_from_file_location(
                    module_name,
                    path,
                )
            )

            if (
                spec is None
                or spec.loader is None
            ):
                raise RuntimeError(
                    "invalid_module_specification"
                )

            module = (
                importlib.util.module_from_spec(
                    spec
                )
            )

            spec.loader.exec_module(
                module
            )

            return {
                "ok": True,
                "module": module,
            }

        except Exception as exc:
            return {
                "ok": False,
                "reason": "module_import_failed",
                "file": path.name,
                "error": repr(exc),
                "traceback": traceback.format_exc(
                    limit=8
                ),
            }


# ============================================================
# PROVIDER CONTRACT VERIFIER
# ============================================================

class ProviderContractVerifier:

    REQUIRED_STATUS_KEYS: Tuple[str, ...] = (
        "state",
    )

    def inspect_03(
        self,
    ) -> Dict[str, Any]:

        path = ROOT / GENERATED_FILES["03"]

        loaded = SafeModuleLoader.load(
            path,
            "provider_contract",
        )

        if not loaded.get("ok"):
            return loaded

        module = loaded["module"]

        status_function = getattr(
            module,
            "provider_status",
            None,
        )

        if not callable(status_function):
            return {
                "ok": False,
                "reason": "provider_status_interface_missing",
            }

        try:
            status = status_function()

        except TypeError:
            # Interface may require provider name.
            try:
                status = status_function(
                    "registrar"
                )
            except Exception as exc:
                return {
                    "ok": False,
                    "reason": "provider_status_failed",
                    "error": repr(exc),
                }

        except Exception as exc:
            return {
                "ok": False,
                "reason": "provider_status_failed",
                "error": repr(exc),
            }

        if not isinstance(status, dict):
            return {
                "ok": False,
                "reason": "provider_status_not_dict",
            }

        state = str(
            status.get(
                "state",
                "",
            )
        ).lower()

        if state not in VALID_PROVIDER_STATES:
            return {
                "ok": False,
                "reason": "invalid_provider_state",
                "state": state,
                "allowed": VALID_PROVIDER_STATES,
            }

        verified = (
            state
            == PROVIDER_STATE_VERIFIED
        )

        return {
            "ok": True,
            "state": state,
            "verified": verified,
            "status": status,
        }


# ============================================================
# CAPABILITY ANALYZER
# ============================================================

class CapabilityAnalyzer:

    def __init__(
        self,
        validator: GeneratedCodeValidator,
    ) -> None:
        self.validator = validator

    def analyze(
        self,
        discovery: Dict[str, Any],
    ) -> Dict[str, Any]:

        results: Dict[str, Any] = {}

        file_results: Dict[str, Any] = {}

        for number, filename in GENERATED_FILES.items():
            path = ROOT / filename

            if not path.exists():
                file_results[number] = {
                    "ok": False,
                    "reason": "missing",
                }

            else:
                file_results[number] = (
                    self.validator.validate(
                        number,
                        filename,
                        read_text(path),
                    )
                )

        f03 = file_results.get(
            "03",
            {},
        )
        f04 = file_results.get(
            "04",
            {},
        )
        f05 = file_results.get(
            "05",
            {},
        )

        def internal(
            name: str,
            ok: bool,
            evidence: Any,
        ) -> None:
            results[name] = {
                "status": (
                    "VERIFIED_INTERNAL_CONTRACT"
                    if ok
                    else "MISSING_OR_INVALID"
                ),
                "verified": bool(ok),
                "evidence": evidence,
            }

        internal(
            "fqdn_normalization",
            bool(f03.get("ok")),
            f03.get("contract"),
        )

        internal(
            "domain_search",
            bool(f03.get("ok")),
            "search_domain interface",
        )

        internal(
            "authoritative_domain_availability",
            bool(f03.get("ok")),
            "authoritative_availability interface + registration guard",
        )

        internal(
            "domain_registration",
            bool(f03.get("ok")),
            "register_domain contract",
        )

        internal(
            "domain_renewal",
            bool(f03.get("ok")),
            "renew_domain contract",
        )

        internal(
            "domain_transfer",
            bool(f03.get("ok")),
            "transfer_domain contract",
        )

        internal(
            "domain_lifecycle",
            bool(f03.get("ok")),
            "lifecycle contract",
        )

        internal(
            "domain_details",
            bool(f03.get("ok")),
            "get_domain contract",
        )

        internal(
            "idempotent_domain_mutations",
            bool(f03.get("ok")),
            (
                f03.get("contract", {})
                .get("idempotency")
            ),
        )

        internal(
            "dns_management",
            bool(f03.get("ok")),
            "configure_dns contract",
        )

        internal(
            "nameserver_management",
            bool(f03.get("ok")),
            "configure_nameservers contract",
        )

        internal(
            "dnssec_management",
            bool(f03.get("ok")),
            "configure_dnssec contract",
        )

        internal(
            "domain_tls_management",
            bool(f03.get("ok")),
            "provision_domain_tls contract",
        )

        for name in (
            "owner_control",
            "authorization",
            "security",
            "audit",
            "monitoring",
        ):
            internal(
                name,
                bool(f04.get("ok")),
                f04.get("contract"),
            )

        internal(
            "http_api",
            bool(f05.get("ok")),
            f05.get("contract"),
        )

        internal(
            "runtime_health",
            bool(f05.get("ok")),
            f05.get("contract"),
        )

        ui = discovery.get(
            "official_ui",
            {},
        )

        ui_ok = bool(
            ui.get("exists")
            and ui.get(
                "declares_all_required_endpoints"
            )
            and ui.get("has_fetch")
            and not ui.get(
                "forbidden_hits"
            )
        )

        internal(
            "official_ui_integration",
            ui_ok,
            ui,
        )

        provider = (
            ProviderContractVerifier()
            .inspect_03()
        )

        provider_state = (
            provider.get("state")
            if provider.get("ok")
            else PROVIDER_STATE_UNAVAILABLE
        )

        results[
            "registrar_reseller_adapter"
        ] = {
            "status": provider_state,
            "verified": bool(
                provider.get("verified")
            ),
            "evidence": provider,
        }

        # RDAP must have a real internal interface.
        # External success is only verified if file 03 reports it.
        rdap_verified = False
        whois_verified = False
        epp_verified = False

        path03 = (
            ROOT / GENERATED_FILES["03"]
        )

        if path03.exists():
            loaded = SafeModuleLoader.load(
                path03,
                "optional_provider_contracts",
            )

            if loaded.get("ok"):
                module = loaded["module"]

                for capability_name, variable in (
                    (
                        "rdap",
                        "rdap_verified",
                    ),
                    (
                        "whois_legacy",
                        "whois_verified",
                    ),
                    (
                        "registry_epp_direct",
                        "epp_verified",
                    ),
                ):
                    checker = getattr(
                        module,
                        f"{capability_name}_status",
                        None,
                    )

                    if callable(checker):
                        try:
                            value = checker()

                            if isinstance(
                                value,
                                dict,
                            ):
                                verified_value = (
                                    str(
                                        value.get(
                                            "state",
                                            "",
                                        )
                                    ).lower()
                                    == PROVIDER_STATE_VERIFIED
                                )

                                if variable == "rdap_verified":
                                    rdap_verified = verified_value

                                elif variable == "whois_verified":
                                    whois_verified = verified_value

                                elif variable == "epp_verified":
                                    epp_verified = verified_value

                        except Exception:
                            pass

        results["rdap"] = {
            "status": (
                PROVIDER_STATE_VERIFIED
                if rdap_verified
                else PROVIDER_STATE_NOT_CONFIGURED
            ),
            "verified": rdap_verified,
            "required_for_production": True,
        }

        results["whois_legacy"] = {
            "status": (
                PROVIDER_STATE_VERIFIED
                if whois_verified
                else PROVIDER_STATE_NOT_CONFIGURED
            ),
            "verified": whois_verified,
            "required_for_production": False,
            "optional_legacy": True,
        }

        results["registry_epp_direct"] = {
            "status": (
                PROVIDER_STATE_VERIFIED
                if epp_verified
                else PROVIDER_STATE_NOT_CONFIGURED
            ),
            "verified": epp_verified,
            "required_for_production": False,
            "optional": True,
        }

        missing_internal = [
            name
            for name, spec
            in REQUIRED_CAPABILITIES.items()
            if (
                spec.get(
                    "required_internal"
                )
                and results.get(
                    name,
                    {},
                ).get("status")
                == "MISSING_OR_INVALID"
            )
        ]

        production_external_blockers = [
            name
            for name, spec
            in REQUIRED_CAPABILITIES.items()
            if (
                spec.get("external")
                and spec.get(
                    "production_required"
                )
                and not results.get(
                    name,
                    {},
                ).get("verified")
            )
        ]

        report = {
            "timestamp": utc_now(),
            "capabilities": results,
            "file_contracts": file_results,
            "missing_internal": missing_internal,
            "production_external_blockers": (
                production_external_blockers
            ),
            "whois_required": False,
            "direct_epp_required": False,
            "rdap_required": True,
        }

        atomic_write_json(
            GAP_FILE,
            report,
        )

        return report


# ============================================================
# PLANNER
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
            "version": VERSION,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,
            "mission": PLATFORM_MISSION,
            "current_state": discovery,
            "gaps": gaps,
            "generated_files": GENERATED_FILES,
            "strategy": [
                "Preserve protected 01 and 02.",
                "Modify only 03/04/05.",
                "Use interface/AST/runtime verification rather than keyword scoring.",
                "Require strict FQDN normalization.",
                "Require verified registrar/reseller state for external mutation.",
                "Require authoritative availability before registration.",
                "Require idempotency for register/renew/transfer.",
                "Use RDAP as primary discovery protocol.",
                "Treat WHOIS only as optional legacy fallback.",
                "Treat direct registry/EPP as optional.",
                "Reject simulated or fake domain operations.",
                "Inspect real runtime routes.",
                "Verify MAJD-DMAIL live health identity.",
                "Keep external blockers honest.",
            ],
            "source": "embedded_closure_architecture",
        }

    def create(
        self,
        discovery: Dict[str, Any],
        gaps: Dict[str, Any],
        *,
        use_ai: bool = False,
    ) -> Dict[str, Any]:

        plan = self.embedded_plan(
            discovery,
            gaps,
        )

        # Architecture is fixed now.
        # AI planning is optional and never required to execute closure.
        if not use_ai:
            atomic_write_json(
                PLAN_FILE,
                plan,
            )
            return plan

        if not gaps.get(
            "missing_internal"
        ):
            atomic_write_json(
                PLAN_FILE,
                plan,
            )
            return plan

        health = self.ai.health()

        if not health.get("ok"):
            plan["ai_review"] = {
                "used": False,
                "reason": "ai_unavailable",
                "health": health,
            }

            atomic_write_json(
                PLAN_FILE,
                plan,
            )

            return plan

        system_prompt = f"""
You are a subordinate engineering reviewer for {PROJECT_NAME}.

Architecture is already fixed.
You are NOT allowed to redesign authority or scope.

HIGHEST AUTHORITY:
{OWNER_AUTHORITY}

PROTECTED:
{THIS_FILENAME}
{PRIMARY_FILE_02}

AI MANAGED:
{json.dumps(GENERATED_FILES)}

MANDATORY:
RDAP primary.
WHOIS optional legacy.
Registrar/reseller primary execution provider.
Direct EPP optional.
Strict FQDN normalization.
Authoritative availability before registration.
Idempotency for register/renew/transfer.
No email.
No payment implementation.
No simulated domain operation.
No fake provider success.

Return compact JSON only with:
{{
  "priority_repairs": [],
  "integration_notes": [],
  "verification_notes": []
}}
"""

        result = self.ai.generate(
            system_prompt,
            json.dumps(
                {
                    "missing_internal": gaps.get(
                        "missing_internal",
                        [],
                    ),
                    "external_blockers": gaps.get(
                        "production_external_blockers",
                        [],
                    ),
                },
                ensure_ascii=False,
            ),
            temperature=0.0,
            num_predict=AI_PLAN_PREDICT,
            json_mode=True,
        )

        if result.get("ok"):
            parsed = extract_json_object(
                result["text"]
            )

            if parsed:
                plan["ai_review"] = {
                    "used": True,
                    "model": result.get(
                        "model"
                    ),
                    "review": parsed,
                }

        atomic_write_json(
            PLAN_FILE,
            plan,
        )

        return plan


# ============================================================
# AUTONOMOUS PLATFORM ENGINEER
# ============================================================

class AutonomousPlatformEngineer:

    def __init__(
        self,
        ai: AIProvider,
        validator: GeneratedCodeValidator,
    ) -> None:
        self.ai = ai
        self.validator = validator

    @staticmethod
    def bounded_context(
        content: str,
        max_chars: int,
    ) -> str:

        if len(content) <= max_chars:
            return content

        half = max_chars // 2

        return (
            content[:half]
            + "\n# ... CONTEXT TRUNCATED ...\n"
            + content[-half:]
        )

    def read_context(
        self,
    ) -> Dict[str, str]:

        context: Dict[str, str] = {}

        core = ROOT / PRIMARY_FILE_02

        if core.exists():
            context["02"] = (
                self.bounded_context(
                    read_text(core),
                    10000,
                )
            )

        for number, filename in GENERATED_FILES.items():
            path = ROOT / filename

            if path.exists():
                context[number] = (
                    self.bounded_context(
                        read_text(path),
                        14000,
                    )
                )

        return context

    def repair_directive(
        self,
        number: str,
        previous_error: Optional[
            Dict[str, Any]
        ],
    ) -> str:

        if not previous_error:
            return (
                "Build the target completely according "
                "to the fixed closure contract."
            )

        return (
            "TARGETED REPAIR REQUIRED.\n"
            "Correct the exact failure below without "
            "removing working contracts:\n"
            + json.dumps(
                previous_error,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

    def system_prompt(
        self,
        number: str,
        previous_error: Optional[
            Dict[str, Any]
        ],
    ) -> str:

        filename = GENERATED_FILES[
            number
        ]

        repair = self.repair_directive(
            number,
            previous_error,
        )

        return f"""
You are the autonomous subordinate engineering company for MAJD-DMAIL.

TARGET FILE:
{filename}

PROJECT:
{PROJECT_NAME}

SCOPE:
DOMAINS ONLY

HIGHEST AUTHORITY:
{OWNER_AUTHORITY}

PROTECTED:
- {THIS_FILENAME}
- {PRIMARY_FILE_02}

YOU MAY MODIFY ONLY:
- {GENERATED_FILES['03']}
- {GENERATED_FILES['04']}
- {GENERATED_FILES['05']}

ARCHITECTURE IS FINAL.

ABSOLUTE REQUIREMENTS:

1. SUPREME_OWNER always remains highest authority.

2. No primary file 06+.

3. No email hosting or mailbox stack.

4. No payment implementation.

5. Never implement or report simulated, mocked, fake, dummy,
   placeholder or stub domain execution.

6. Never report external domain success unless the underlying provider
   is in exact state "verified".

7. Provider states are ONLY:
   not_configured
   configured
   verified
   unavailable

8. "configured" MUST NOT be treated as "verified".

9. Registrar or reseller adapter is the primary execution adapter.

10. Direct registry/EPP is OPTIONAL and must not be required for
    initial production.

11. RDAP is PRIMARY and production-required.

12. WHOIS is OPTIONAL legacy fallback and must not block production.

13. Every external domain value MUST pass through normalize_fqdn().

14. normalize_fqdn() must reject malformed duplicate suffix input such
    as:
        example.com.com

15. Registration MUST call authoritative_availability() before any
    provider registration call.

16. If authoritative availability is unknown, unavailable, reserved,
    or unverified, registration MUST NOT execute.

17. register_domain(), renew_domain() and transfer_domain() MUST accept
    an idempotency key and use persistent idempotency storage/checks.

18. Domain lifecycle states must include:
{json.dumps(DOMAIN_LIFECYCLE_STATES)}

19. Importing the file must not perform external mutation.

20. Never hard-code provider secrets.

21. Return COMPLETE Python source only.

FILE 03 MUST EXPORT THESE CALLABLES:
{json.dumps(FILE03_REQUIRED_CALLABLES)}

FILE 04 MUST EXPORT THESE CALLABLES:
{json.dumps(FILE04_REQUIRED_CALLABLES)}

FILE 05 MUST EXPORT:
create_app()

FILE 05 MUST EXPOSE THESE EXACT FINAL ROUTES:
{json.dumps(ALL_REQUIRED_ENDPOINTS)}

GET /api/health MUST RETURN JSON INCLUDING:
project = "{PROJECT_NAME}"
scope = "{PROJECT_SCOPE}"
owner_authority = "{OWNER_AUTHORITY}"
no_fake_success = true

For operations requiring external providers:
- not_configured => fail honestly
- configured => fail honestly until verification succeeds
- unavailable => fail honestly
- verified => operation may proceed subject to all other checks

{repair}
"""

    def generate_candidate(
        self,
        number: str,
        plan: Dict[str, Any],
        discovery: Dict[str, Any],
        gaps: Dict[str, Any],
        *,
        previous_error: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:

        filename = GENERATED_FILES[
            number
        ]

        health = self.ai.health()

        if not health.get("ok"):
            return {
                "ok": False,
                "reason": "ai_unavailable",
                "health": health,
            }

        context = self.read_context()

        siblings = {
            key: value
            for key, value in context.items()
            if key != number
        }

        payload = {
            "target": {
                "number": number,
                "filename": filename,
            },
            "mission": {
                "project": PROJECT_NAME,
                "scope": PROJECT_SCOPE,
                "owner_authority": OWNER_AUTHORITY,
                "rdap_required": True,
                "whois_required": False,
                "direct_epp_required": False,
            },
            "existing_target": context.get(
                number,
                "",
            ),
            "related_context": siblings,
            "missing_internal": gaps.get(
                "missing_internal",
                [],
            ),
            "previous_error": previous_error,
        }

        result = self.ai.generate(
            self.system_prompt(
                number,
                previous_error,
            ),
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
                "error": result.get(
                    "error"
                ),
                "done": result.get(
                    "done"
                ),
                "done_reason": result.get(
                    "done_reason"
                ),
                "elapsed_seconds": result.get(
                    "elapsed_seconds"
                ),
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
            "ok": bool(
                validation.get("ok")
            ),
            "code": code,
            "validation": validation,
            "provider": result.get(
                "provider"
            ),
            "model": result.get(
                "model"
            ),
            "elapsed_seconds": result.get(
                "elapsed_seconds"
            ),
        }

    def build_one(
        self,
        number: str,
        plan: Dict[str, Any],
        discovery: Dict[str, Any],
        gaps: Dict[str, Any],
        *,
        force: bool = False,
        repair_error: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:

        filename = GENERATED_FILES[
            number
        ]

        enforce_generated_filename(
            filename
        )

        path = ROOT / filename

        existing = (
            read_text(path)
            if path.exists()
            else ""
        )

        if existing:
            existing_validation = (
                self.validator.validate(
                    number,
                    filename,
                    existing,
                )
            )
        else:
            existing_validation = {
                "ok": False,
                "reason": "missing",
            }

        if (
            existing_validation.get(
                "ok"
            )
            and not force
        ):
            return {
                "ok": True,
                "action": (
                    "existing_component_preserved"
                ),
                "file": filename,
                "validation": (
                    existing_validation
                ),
            }

        previous_error = (
            repair_error
            or (
                None
                if existing_validation.get(
                    "ok"
                )
                else existing_validation
            )
        )

        seen_failures: Set[str] = set()
        candidate_result: Optional[
            Dict[str, Any]
        ] = None

        audit(
            "AUTONOMOUS_ENGINEERING_STARTED",
            details={
                "file": filename,
                "number": number,
            },
        )

        for attempt in range(
            1,
            AI_REPAIR_ATTEMPTS + 1,
        ):

            candidate_result = (
                self.generate_candidate(
                    number,
                    plan,
                    discovery,
                    gaps,
                    previous_error=(
                        previous_error
                    ),
                )
            )

            if candidate_result.get(
                "ok"
            ):
                break

            failure = {
                "attempt": attempt,
                "reason": (
                    candidate_result.get(
                        "reason"
                    )
                ),
                "validation": (
                    candidate_result.get(
                        "validation"
                    )
                ),
                "error": (
                    candidate_result.get(
                        "error"
                    )
                ),
            }

            signature = sha256_text(
                json.dumps(
                    failure,
                    sort_keys=True,
                    default=str,
                )
            )

            if signature in seen_failures:
                audit(
                    "IDENTICAL_AI_FAILURE_STOPPED",
                    status="ERROR",
                    details={
                        "file": filename,
                        "failure": failure,
                    },
                )
                break

            seen_failures.add(
                signature
            )

            previous_error = failure

            audit(
                "AUTONOMOUS_ENGINEERING_ATTEMPT_FAILED",
                status="ERROR",
                details={
                    "file": filename,
                    **failure,
                },
            )

        if (
            not candidate_result
            or not candidate_result.get(
                "ok"
            )
        ):
            return {
                "ok": False,
                "action": (
                    "existing_file_preserved_ai_failed"
                ),
                "file": filename,
                "existing_preserved": (
                    path.exists()
                ),
                "last_error": (
                    candidate_result
                    or {
                        "reason": (
                            "no_candidate"
                        )
                    }
                ),
            }

        candidate = (
            candidate_result["code"]
        )

        backup = backup_existing(
            path
        )

        atomic_write_text(
            path,
            candidate,
        )

        post_write = (
            self.validator.validate(
                number,
                filename,
                read_text(path),
            )
        )

        if not post_write.get("ok"):
            restore_backup(
                backup,
                path,
            )

            return {
                "ok": False,
                "action": (
                    "candidate_rolled_back"
                ),
                "file": filename,
                "validation": post_write,
            }

        audit(
            "AUTONOMOUS_ENGINEERING_COMPLETED",
            details={
                "file": filename,
                "sha256": (
                    post_write.get(
                        "sha256"
                    )
                ),
            },
        )

        return {
            "ok": True,
            "action": (
                "component_built_and_validated"
            ),
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

        if not (
            ROOT / PRIMARY_FILE_02
        ).exists():
            return {
                "ok": False,
                "blocked": True,
                "reason": (
                    f"{PRIMARY_FILE_02} missing"
                ),
            }

        results: Dict[str, Any] = {}

        for number in (
            "03",
            "04",
            "05",
        ):
            path = (
                ROOT
                / GENERATED_FILES[number]
            )

            current_validation = (
                self.validator.validate(
                    number,
                    GENERATED_FILES[number],
                    read_text(path),
                )
                if path.exists()
                else {
                    "ok": False,
                    "reason": "missing",
                }
            )

            should_force = bool(
                force
                and not current_validation.get(
                    "ok"
                )
            )

            results[number] = (
                self.build_one(
                    number,
                    plan,
                    discovery,
                    gaps,
                    force=should_force,
                )
            )

            discovery = (
                ProjectDiscovery()
                .snapshot()
            )

            gaps = (
                CapabilityAnalyzer(
                    self.validator
                ).analyze(
                    discovery
                )
            )

        return {
            "ok": all(
                item.get("ok")
                for item
                in results.values()
            ),
            "results": results,
        }


# ============================================================
# RUNTIME MODULE VERIFIER
# ============================================================

class RuntimeModuleVerifier:

    def __init__(self) -> None:
        self.routes = RouteInspector()

    def verify(
        self,
    ) -> Dict[str, Any]:

        path = (
            ROOT / GENERATED_FILES["05"]
        )

        loaded = SafeModuleLoader.load(
            path,
            "runtime_verify",
        )

        if not loaded.get("ok"):
            return loaded

        module = loaded["module"]

        route_result = (
            self.routes
            .inspect_imported_routes(
                module
            )
        )

        if not route_result.get(
            "ok"
        ):
            return {
                "ok": False,
                "reason": (
                    "runtime_route_map_invalid"
                ),
                "routes": {
                    key: value
                    for key, value
                    in route_result.items()
                    if key != "app"
                },
            }

        internal = (
            self.routes.internal_test(
                route_result["app"]
            )
        )

        return {
            "ok": bool(
                internal.get("ok")
            ),
            "routes": route_result.get(
                "routes"
            ),
            "internal_test": internal,
        }


# ============================================================
# RUNTIME SUPERVISOR
# ============================================================

class RuntimeSupervisor:

    def runtime_path(
        self,
    ) -> Path:
        return (
            ROOT / GENERATED_FILES["05"]
        )

    def read_pid(
        self,
    ) -> Optional[int]:

        if not RUNTIME_PID_FILE.exists():
            return None

        try:
            return int(
                read_text(
                    RUNTIME_PID_FILE
                ).strip()
            )
        except Exception:
            return None

    @staticmethod
    def pid_alive(
        pid: int,
    ) -> bool:
        try:
            os.kill(
                pid,
                0,
            )
            return True

        except OSError:
            return False

    def stop(
        self,
    ) -> Dict[str, Any]:

        pid = self.read_pid()

        if pid is None:
            return {
                "ok": True,
                "action": "runtime_not_running",
            }

        if not self.pid_alive(pid):
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
            os.kill(
                pid,
                signal.SIGTERM,
            )

            deadline = (
                time.time() + 10
            )

            while (
                time.time() < deadline
                and self.pid_alive(pid)
            ):
                time.sleep(0.25)

            if self.pid_alive(pid):
                os.kill(
                    pid,
                    signal.SIGKILL,
                )

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
                "reason": "runtime_stop_failed",
                "error": repr(exc),
            }

    def start(
        self,
    ) -> Dict[str, Any]:

        path = self.runtime_path()

        if not path.exists():
            return {
                "ok": False,
                "reason": "runtime_file_missing",
            }

        current_pid = self.read_pid()

        if (
            current_pid is not None
            and self.pid_alive(
                current_pid
            )
        ):
            return {
                "ok": True,
                "action": (
                    "runtime_already_running"
                ),
                "pid": current_pid,
            }

        stdout_handle = (
            RUNTIME_STDOUT.open(
                "ab",
                buffering=0,
            )
        )

        stderr_handle = (
            RUNTIME_STDERR.open(
                "ab",
                buffering=0,
            )
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
                    "reason": (
                        "runtime_exited_immediately"
                    ),
                    "returncode": (
                        process.returncode
                    ),
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
                "reason": (
                    "runtime_start_failed"
                ),
                "error": repr(exc),
            }

        finally:
            stdout_handle.close()
            stderr_handle.close()

    def restart(
        self,
    ) -> Dict[str, Any]:

        stop_result = self.stop()
        start_result = self.start()

        return {
            "ok": bool(
                start_result.get("ok")
            ),
            "stop": stop_result,
            "start": start_result,
        }


# ============================================================
# LIVE HEALTH
# ============================================================

class LiveHealthVerifier:

    def candidate_urls(
        self,
    ) -> List[str]:

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

        return list(
            dict.fromkeys(urls)
        )

    @staticmethod
    def identity_valid(
        payload: Any,
    ) -> bool:

        if not isinstance(
            payload,
            dict,
        ):
            return False

        if (
            payload.get("project")
            != PROJECT_NAME
        ):
            return False

        if (
            payload.get("scope")
            != PROJECT_SCOPE
        ):
            return False

        if (
            payload.get(
                "owner_authority"
            )
            != OWNER_AUTHORITY
        ):
            return False

        if (
            payload.get(
                "no_fake_success"
            )
            is not True
        ):
            return False

        return True

    def verify(
        self,
    ) -> Dict[str, Any]:

        attempts: List[
            Dict[str, Any]
        ] = []

        for base_url in self.candidate_urls():

            url = (
                base_url
                + "/api/health"
            )

            request = (
                urllib.request.Request(
                    url,
                    method="GET",
                    headers={
                        "Accept": (
                            "application/json"
                        )
                    },
                )
            )

            try:
                with urllib.request.urlopen(
                    request,
                    timeout=5,
                ) as response:
                    status_code = int(
                        getattr(
                            response,
                            "status",
                            200,
                        )
                    )

                    body = (
                        response.read()
                        .decode(
                            "utf-8",
                            errors="replace",
                        )
                    )

                try:
                    parsed = json.loads(
                        body
                    )
                except Exception:
                    parsed = None

                identity_ok = (
                    self.identity_valid(
                        parsed
                    )
                )

                attempt = {
                    "ok": bool(
                        200
                        <= status_code
                        < 300
                        and identity_ok
                    ),
                    "url": url,
                    "status_code": (
                        status_code
                    ),
                    "identity_ok": (
                        identity_ok
                    ),
                    "json": parsed,
                }

                attempts.append(
                    attempt
                )

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
            "reason": (
                "no_verified_majd_dmail_live_health"
            ),
            "attempts": attempts,
        }

    def wait_for_health(
        self,
        timeout: int = RUNTIME_START_TIMEOUT,
    ) -> Dict[str, Any]:

        deadline = (
            time.time() + timeout
        )

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
# UI DESIGNER
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
        return (
            ProjectDiscovery()
            .inspect_ui()
        )

    def validate_html(
        self,
        content: str,
    ) -> Dict[str, Any]:

        lower = content.lower()

        if (
            "<html" not in lower
            or "</html>" not in lower
        ):
            return {
                "ok": False,
                "reason": "invalid_html_document",
            }

        forbidden = (
            forbidden_scope_patterns(
                content
            )
        )

        if forbidden:
            return {
                "ok": False,
                "reason": "forbidden_scope",
                "patterns": forbidden,
            }

        fake = fake_operation_patterns(
            content
        )

        if fake:
            return {
                "ok": False,
                "reason": (
                    "fake_operation_ui_language"
                ),
                "patterns": fake,
            }

        missing = [
            endpoint
            for endpoint
            in ALL_REQUIRED_ENDPOINTS
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
                "reason": (
                    "backend_fetch_integration_missing"
                ),
            }

        return {
            "ok": True,
            "sha256": sha256_text(
                content
            ),
        }

    def improve(
        self,
        platform_report: Dict[str, Any],
        *,
        force: bool = False,
    ) -> Dict[str, Any]:

        inspection = self.inspect()

        current_valid = bool(
            inspection.get("exists")
            and inspection.get(
                "declares_all_required_endpoints"
            )
            and inspection.get(
                "has_fetch"
            )
            and not inspection.get(
                "forbidden_hits"
            )
        )

        if (
            current_valid
            and not force
        ):
            return {
                "ok": True,
                "action": (
                    "valid_official_ui_preserved"
                ),
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
                "action": (
                    "existing_ui_preserved_ai_unavailable"
                ),
            }

        current = read_text(
            UI_INDEX
        )

        if len(current) > 20000:
            current = (
                current[:10000]
                + "\n<!-- CONTEXT TRUNCATED -->\n"
                + current[-10000:]
            )

        system_prompt = f"""
You are the official subordinate frontend engineer for MAJD-DMAIL.

Scope:
DOMAINS ONLY

Highest authority:
SUPREME_OWNER

Rules:
- Preserve useful design.
- Preserve Arabic RTL when present.
- No email services.
- No payment implementation.
- Never claim domain success locally.
- All real actions use backend APIs.
- Do not create simulated/fake/mock results.
- Display provider unavailable/configured/not-configured states honestly.
- Configured is not verified.

Required backend endpoints:
{json.dumps(ALL_REQUIRED_ENDPOINTS)}

Return one complete index.html only.
"""

        result = self.ai.generate(
            system_prompt,
            json.dumps(
                {
                    "current_ui": current,
                    "platform_status": {
                        "core_ok": (
                            platform_report.get(
                                "core_ok"
                            )
                        ),
                        "production_ready": (
                            platform_report.get(
                                "production_ready"
                            )
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
                "action": (
                    "existing_ui_preserved_ai_failed"
                ),
                "error": result.get(
                    "error"
                ),
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
                "action": (
                    "ui_candidate_rejected"
                ),
                "validation": validation,
            }

        backup = backup_existing(
            UI_INDEX
        )

        atomic_write_text(
            UI_INDEX,
            candidate,
        )

        final_validation = (
            self.validate_html(
                read_text(UI_INDEX)
            )
        )

        if not final_validation.get(
            "ok"
        ):
            restore_backup(
                backup,
                UI_INDEX,
            )

            return {
                "ok": False,
                "action": "ui_rolled_back",
            }

        payload = {
            "ok": True,
            "action": "official_ui_improved",
            "validation": (
                final_validation
            ),
        }

        atomic_write_json(
            DESIGN_REPORT_FILE,
            payload,
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
        self.runtime_module = (
            RuntimeModuleVerifier()
        )
        self.live = (
            LiveHealthVerifier()
        )
        self.capabilities = (
            CapabilityAnalyzer(
                validator
            )
        )

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
            )
            > MAX_PRIMARY_FILES
        ]

        required = [
            THIS_FILENAME,
            PRIMARY_FILE_02,
            *GENERATED_FILES.values(),
        ]

        missing = [
            filename
            for filename in required
            if not (
                ROOT / filename
            ).exists()
        ]

        return {
            "ok": bool(
                not violations
                and not missing
            ),
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

            results[number] = (
                self.validator.validate(
                    number,
                    filename,
                    read_text(path),
                )
            )

        return {
            "ok": all(
                item.get("ok")
                for item
                in results.values()
            ),
            "files": results,
        }

    def verify_importability(
        self,
    ) -> Dict[str, Any]:

        results: Dict[str, Any] = {}

        for number, filename in GENERATED_FILES.items():

            loaded = (
                SafeModuleLoader.load(
                    ROOT / filename,
                    f"verify_{number}",
                )
            )

            results[number] = {
                key: value
                for key, value
                in loaded.items()
                if key != "module"
            }

        return {
            "ok": all(
                item.get("ok")
                for item
                in results.values()
            ),
            "files": results,
        }

    def verify_ui(
        self,
    ) -> Dict[str, Any]:

        inspection = (
            ProjectDiscovery()
            .inspect_ui()
        )

        return {
            "ok": bool(
                inspection.get("exists")
                and inspection.get(
                    "declares_all_required_endpoints"
                )
                and inspection.get(
                    "has_fetch"
                )
                and not inspection.get(
                    "forbidden_hits"
                )
            ),
            "inspection": inspection,
        }

    def verify_normalizer(
        self,
    ) -> Dict[str, Any]:

        valid_cases = {
            "Example.COM": "example.com",
            "example.com.": "example.com",
            "sub.example.com": (
                "sub.example.com"
            ),
        }

        invalid_cases = (
            "example",
            "example..com",
            "example.com.com",
            "https://example.com",
            "user@example.com",
            "example.com/path",
        )

        valid_results: Dict[str, Any] = {}
        invalid_results: Dict[str, Any] = {}

        for source, expected in valid_cases.items():
            try:
                actual = normalize_fqdn(
                    source
                )

                valid_results[source] = {
                    "ok": actual == expected,
                    "actual": actual,
                    "expected": expected,
                }

            except Exception as exc:
                valid_results[source] = {
                    "ok": False,
                    "error": repr(exc),
                }

        for source in invalid_cases:
            try:
                actual = normalize_fqdn(
                    source
                )

                invalid_results[source] = {
                    "ok": False,
                    "unexpected": actual,
                }

            except DomainNormalizationError:
                invalid_results[source] = {
                    "ok": True,
                    "rejected": True,
                }

            except Exception as exc:
                invalid_results[source] = {
                    "ok": False,
                    "error": repr(exc),
                }

        return {
            "ok": bool(
                all(
                    item.get("ok")
                    for item
                    in valid_results.values()
                )
                and all(
                    item.get("ok")
                    for item
                    in invalid_results.values()
                )
            ),
            "valid_cases": valid_results,
            "invalid_cases": invalid_results,
        }

    def full(
        self,
        ai: AIProvider,
        *,
        live: bool = True,
    ) -> Dict[str, Any]:

        primary = (
            self.verify_primary_policy()
        )

        generated = (
            self.verify_generated_components()
        )

        imports = (
            self.verify_importability()
        )

        normalizer = (
            self.verify_normalizer()
        )

        runtime_contract = (
            self.runtime_module.verify()
            if (
                generated.get(
                    "files",
                    {},
                )
                .get(
                    "05",
                    {},
                )
                .get("ok")
            )
            else {
                "ok": False,
                "reason": (
                    "runtime_source_invalid"
                ),
            }
        )

        live_health = (
            self.live.verify()
            if live
            else {
                "ok": False,
                "reason": (
                    "live_check_not_requested"
                ),
            }
        )

        ui = self.verify_ui()

        discovery = (
            ProjectDiscovery()
            .snapshot()
        )

        capabilities = (
            self.capabilities.analyze(
                discovery
            )
        )

        internal_structure_ok = bool(
            primary.get("ok")
            and generated.get("ok")
            and imports.get("ok")
            and normalizer.get("ok")
            and runtime_contract.get("ok")
            and not capabilities.get(
                "missing_internal"
            )
        )

        core_ok = bool(
            internal_structure_ok
            and live_health.get("ok")
            and ui.get("ok")
        )

        external_blockers = list(
            capabilities.get(
                "production_external_blockers",
                [],
            )
        )

        production_ready = bool(
            core_ok
            and not external_blockers
        )

        report = {
            "timestamp": utc_now(),
            "project": PROJECT_NAME,
            "version": VERSION,
            "scope": PROJECT_SCOPE,
            "owner_authority": OWNER_AUTHORITY,

            "architecture": {
                "rdap_primary": True,
                "whois_optional_legacy": True,
                "whois_required": False,
                "registrar_reseller_primary": True,
                "direct_epp_optional": True,
                "direct_epp_required": False,
                "authoritative_availability_before_registration": True,
                "strict_fqdn_normalization": True,
                "idempotency_required": list(
                    IDEMPOTENT_OPERATIONS
                ),
                "provider_states": (
                    VALID_PROVIDER_STATES
                ),
                "lifecycle_states": (
                    DOMAIN_LIFECYCLE_STATES
                ),
            },

            "primary_policy": primary,
            "generated_components": (
                generated
            ),
            "importability": imports,
            "fqdn_normalizer": normalizer,
            "runtime_contract": (
                runtime_contract
            ),
            "live_api_health": (
                live_health
            ),
            "official_ui": ui,
            "capabilities": capabilities,
            "ai": ai.health(),

            "internal_structure_ok": (
                internal_structure_ok
            ),
            "core_ok": core_ok,
            "production_ready": (
                production_ready
            ),

            "external_blockers": (
                external_blockers
            ),

            "optional_non_blockers": [
                "whois_legacy",
                "registry_epp_direct",
            ],

            "no_fake_success": True,
            "simulation_allowed": False,
            "payment_enabled": False,
            "email_enabled": False,
        }

        atomic_write_json(
            REPORT_FILE,
            report,
        )

        return report


# ============================================================
# TARGETED SELF REPAIR
# ============================================================

class SelfRepairEngine:

    def __init__(
        self,
        engineer: AutonomousPlatformEngineer,
    ) -> None:
        self.engineer = engineer

    def repair(
        self,
        plan: Dict[str, Any],
        discovery: Dict[str, Any],
        gaps: Dict[str, Any],
        verification: Dict[str, Any],
    ) -> Dict[str, Any]:

        results: Dict[str, Any] = {}

        generated = (
            verification.get(
                "generated_components",
                {},
            ).get(
                "files",
                {},
            )
        )

        imports = (
            verification.get(
                "importability",
                {},
            ).get(
                "files",
                {},
            )
        )

        runtime_contract = (
            verification.get(
                "runtime_contract",
                {},
            )
        )

        for number in (
            "03",
            "04",
            "05",
        ):

            failures: List[
                Dict[str, Any]
            ] = []

            generated_result = (
                generated.get(
                    number,
                    {},
                )
            )

            if not generated_result.get(
                "ok"
            ):
                failures.append(
                    {
                        "layer": (
                            "static_contract"
                        ),
                        "failure": (
                            generated_result
                        ),
                    }
                )

            import_result = (
                imports.get(
                    number,
                    {},
                )
            )

            if not import_result.get(
                "ok"
            ):
                failures.append(
                    {
                        "layer": (
                            "importability"
                        ),
                        "failure": (
                            import_result
                        ),
                    }
                )

            if (
                number == "05"
                and not runtime_contract.get(
                    "ok"
                )
            ):
                failures.append(
                    {
                        "layer": (
                            "runtime_contract"
                        ),
                        "failure": (
                            runtime_contract
                        ),
                    }
                )

            if not failures:
                results[number] = {
                    "ok": True,
                    "action": (
                        "component_contract_passed"
                    ),
                    "file": (
                        GENERATED_FILES[
                            number
                        ]
                    ),
                }
                continue

            results[number] = (
                self.engineer.build_one(
                    number,
                    plan,
                    discovery,
                    gaps,
                    force=True,
                    repair_error={
                        "reason": (
                            "targeted_repair_required"
                        ),
                        "failures": failures,
                    },
                )
            )

            discovery = (
                ProjectDiscovery()
                .snapshot()
            )

        return {
            "ok": all(
                item.get("ok")
                for item
                in results.values()
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

        self.validator = (
            GeneratedCodeValidator()
        )

        self.discovery_engine = (
            ProjectDiscovery()
        )

        self.capability_analyzer = (
            CapabilityAnalyzer(
                self.validator
            )
        )

        self.planner = (
            PlatformPlanner(
                self.ai
            )
        )

        self.engineer = (
            AutonomousPlatformEngineer(
                self.ai,
                self.validator,
            )
        )

        self.designer = (
            AutonomousUIDesigner(
                self.ai
            )
        )

        self.verifier = (
            FunctionalVerifier(
                self.validator
            )
        )

        self.repair_engine = (
            SelfRepairEngine(
                self.engineer
            )
        )

        self.runtime = (
            RuntimeSupervisor()
        )

        self.live_health = (
            LiveHealthVerifier()
        )

    def bootstrap(
        self,
    ) -> Dict[str, Any]:

        self.state["phase"] = (
            "DOMAIN_CLOSURE_ENGINEERING"
        )

        save_state(
            self.state
        )

        return {
            "ok": True,
            "project": PROJECT_NAME,
            "version": VERSION,
            "scope": PROJECT_SCOPE,
            "owner_authority": (
                OWNER_AUTHORITY
            ),
            "protected": list(
                PROTECTED_FILES
            ),
            "ai_managed": (
                GENERATED_FILES
            ),
            "primary_file_limit": (
                MAX_PRIMARY_FILES
            ),
            "rdap_required": True,
            "whois_required": False,
            "direct_epp_required": False,
            "payment_enabled": False,
            "email_enabled": False,
            "simulation_allowed": False,
            "ai_timeout_seconds": (
                AI_TIMEOUT
            ),
        }

    def discover(
        self,
    ) -> Dict[str, Any]:

        discovery = (
            self.discovery_engine
            .snapshot()
        )

        gaps = (
            self.capability_analyzer
            .analyze(
                discovery
            )
        )

        return {
            "discovery": discovery,
            "capability_analysis": (
                gaps
            ),
        }

    def status(
        self,
    ) -> Dict[str, Any]:

        report = read_json(
            REPORT_FILE,
            {},
        )

        return {
            "timestamp": utc_now(),
            "project": PROJECT_NAME,
            "version": VERSION,
            "scope": PROJECT_SCOPE,
            "owner_authority": (
                OWNER_AUTHORITY
            ),
            "phase": (
                self.state.get(
                    "phase"
                )
            ),
            "primary_files": (
                list_primary_files()
            ),
            "official_ui": (
                self.designer.inspect()
            ),
            "ai": self.ai.health(),
            "ai_timeout_seconds": (
                AI_TIMEOUT
            ),
            "architecture": {
                "rdap_required": True,
                "whois_required": False,
                "direct_epp_required": False,
                "registrar_reseller_primary": True,
                "simulation_allowed": False,
            },
            "last_verification": {
                "internal_structure_ok": (
                    report.get(
                        "internal_structure_ok"
                    )
                ),
                "core_ok": (
                    report.get(
                        "core_ok"
                    )
                ),
                "production_ready": (
                    report.get(
                        "production_ready"
                    )
                ),
                "external_blockers": (
                    report.get(
                        "external_blockers"
                    )
                ),
            },
        }

    def plan(
        self,
        *,
        use_ai: bool = False,
    ) -> Dict[str, Any]:

        discovery = (
            self.discovery_engine
            .snapshot()
        )

        gaps = (
            self.capability_analyzer
            .analyze(
                discovery
            )
        )

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

        discovery = (
            self.discovery_engine
            .snapshot()
        )

        gaps = (
            self.capability_analyzer
            .analyze(
                discovery
            )
        )

        # Closure architecture is embedded.
        # Do not waste AI time on a separate planning request.
        plan = self.planner.create(
            discovery,
            gaps,
            use_ai=False,
        )

        return self.engineer.build_all(
            plan,
            discovery,
            gaps,
            force=force,
        )

    def verify(
        self,
    ) -> Dict[str, Any]:

        return self.verifier.full(
            self.ai,
            live=True,
        )

    def repair(
        self,
    ) -> Dict[str, Any]:

        discovery = (
            self.discovery_engine
            .snapshot()
        )

        gaps = (
            self.capability_analyzer
            .analyze(
                discovery
            )
        )

        plan = self.planner.create(
            discovery,
            gaps,
            use_ai=False,
        )

        before = self.verifier.full(
            self.ai,
            live=False,
        )

        repair = (
            self.repair_engine.repair(
                plan,
                discovery,
                gaps,
                before,
            )
        )

        structural = (
            self.verifier.full(
                self.ai,
                live=False,
            )
        )

        runtime_result: Dict[
            str,
            Any,
        ] = {
            "ok": False,
            "reason": (
                "internal_structure_invalid"
            ),
        }

        live: Dict[str, Any] = {
            "ok": False,
            "reason": (
                "runtime_not_started"
            ),
        }

        if structural.get(
            "internal_structure_ok"
        ):
            runtime_result = (
                self.runtime.restart()
            )

            if runtime_result.get(
                "ok"
            ):
                live = (
                    self.live_health
                    .wait_for_health()
                )

        after = self.verifier.full(
            self.ai,
            live=True,
        )

        return {
            "ok": bool(
                after.get(
                    "core_ok"
                )
            ),
            "repair": repair,
            "runtime": runtime_result,
            "live_health": live,
            "after": after,
        }

    def design(
        self,
    ) -> Dict[str, Any]:

        verification = (
            self.verifier.full(
                self.ai,
                live=True,
            )
        )

        return self.designer.improve(
            verification
        )

    def cycle(
        self,
    ) -> Dict[str, Any]:

        started_at = utc_now()

        audit(
            "AUTONOMOUS_ENGINEERING_CYCLE_STARTED",
            details={
                "version": VERSION,
                "scope": PROJECT_SCOPE,
                "owner_authority": (
                    OWNER_AUTHORITY
                ),
                "ai_timeout": (
                    AI_TIMEOUT
                ),
            },
        )

        discovery = (
            self.discovery_engine
            .snapshot()
        )

        gaps = (
            self.capability_analyzer
            .analyze(
                discovery
            )
        )

        plan = self.planner.create(
            discovery,
            gaps,
            use_ai=False,
        )

        initial = self.verifier.full(
            self.ai,
            live=True,
        )

        build_result: Optional[
            Dict[str, Any]
        ] = None

        repair_result: Optional[
            Dict[str, Any]
        ] = None

        runtime_result: Optional[
            Dict[str, Any]
        ] = None

        design_result: Optional[
            Dict[str, Any]
        ] = None

        if not (
            ROOT / PRIMARY_FILE_02
        ).exists():
            final = initial

        else:

            if not initial.get(
                "internal_structure_ok"
            ):
                build_result = (
                    self.engineer.build_all(
                        plan,
                        discovery,
                        gaps,
                        force=True,
                    )
                )

                mid = self.verifier.full(
                    self.ai,
                    live=False,
                )

                if not mid.get(
                    "internal_structure_ok"
                ):
                    mid_discovery = (
                        self.discovery_engine
                        .snapshot()
                    )

                    mid_gaps = (
                        self.capability_analyzer
                        .analyze(
                            mid_discovery
                        )
                    )

                    repair_result = (
                        self.repair_engine
                        .repair(
                            plan,
                            mid_discovery,
                            mid_gaps,
                            mid,
                        )
                    )

            structural = (
                self.verifier.full(
                    self.ai,
                    live=False,
                )
            )

            if structural.get(
                "internal_structure_ok"
            ):
                runtime_result = (
                    self.runtime.restart()
                )

                if runtime_result.get(
                    "ok"
                ):
                    (
                        self.live_health
                        .wait_for_health()
                    )

            after_runtime = (
                self.verifier.full(
                    self.ai,
                    live=True,
                )
            )

            if not (
                after_runtime.get(
                    "official_ui",
                    {},
                ).get("ok")
            ):
                design_result = (
                    self.designer.improve(
                        after_runtime,
                        force=True,
                    )
                )

            else:
                design_result = {
                    "ok": True,
                    "action": (
                        "valid_official_ui_preserved"
                    ),
                }

            final = self.verifier.full(
                self.ai,
                live=True,
            )

        if final.get(
            "production_ready"
        ):
            phase = (
                "DOMAIN_PLATFORM_PRODUCTION_READY"
            )

        elif final.get(
            "core_ok"
        ):
            phase = (
                "DOMAIN_CORE_VERIFIED_EXTERNAL_PROVIDER_BLOCKERS"
            )

        else:
            phase = (
                "AUTONOMOUS_DOMAIN_ENGINEERING_CONTINUES"
            )

        self.state["phase"] = phase

        self.state["last_cycle"] = {
            "timestamp": utc_now(),
            "internal_structure_ok": (
                final.get(
                    "internal_structure_ok"
                )
            ),
            "core_ok": (
                final.get(
                    "core_ok"
                )
            ),
            "production_ready": (
                final.get(
                    "production_ready"
                )
            ),
            "external_blockers": (
                final.get(
                    "external_blockers"
                )
            ),
        }

        save_state(
            self.state
        )

        audit(
            "AUTONOMOUS_ENGINEERING_CYCLE_COMPLETED",
            details=(
                self.state[
                    "last_cycle"
                ]
            ),
        )

        return {
            "started_at": started_at,
            "finished_at": utc_now(),
            "project": PROJECT_NAME,
            "version": VERSION,
            "scope": PROJECT_SCOPE,
            "owner_authority": (
                OWNER_AUTHORITY
            ),
            "initial_verification": {
                "internal_structure_ok": (
                    initial.get(
                        "internal_structure_ok"
                    )
                ),
                "core_ok": (
                    initial.get(
                        "core_ok"
                    )
                ),
                "production_ready": (
                    initial.get(
                        "production_ready"
                    )
                ),
            },
            "build_result": (
                build_result
            ),
            "repair_result": (
                repair_result
            ),
            "runtime_result": (
                runtime_result
            ),
            "design_result": (
                design_result
            ),
            "final_verification": (
                final
            ),
        }


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

    interval = max(
        60,
        int(interval),
    )

    audit(
        "AUTONOMOUS_DOMAIN_COMPANY_LOOP_STARTED",
        details={
            "interval_seconds": interval,
            "scope": PROJECT_SCOPE,
            "owner_authority": (
                OWNER_AUTHORITY
            ),
            "version": VERSION,
        },
    )

    while True:
        try:
            result = (
                mastermind.cycle()
            )

            final = (
                result[
                    "final_verification"
                ]
            )

            print_json(
                {
                    "cycle_completed": (
                        utc_now()
                    ),
                    "internal_structure_ok": (
                        final.get(
                            "internal_structure_ok"
                        )
                    ),
                    "core_ok": (
                        final.get(
                            "core_ok"
                        )
                    ),
                    "production_ready": (
                        final.get(
                            "production_ready"
                        )
                    ),
                    "external_blockers": (
                        final.get(
                            "external_blockers"
                        )
                    ),
                }
            )

        except KeyboardInterrupt:
            audit(
                "AUTONOMOUS_DOMAIN_COMPANY_LOOP_STOPPED",
                details={
                    "reason": (
                        "keyboard_interrupt"
                    )
                },
            )

            return 0

        except Exception as exc:
            audit(
                "AUTONOMOUS_DOMAIN_COMPANY_CYCLE_FAILED",
                status="ERROR",
                details={
                    "error": repr(exc),
                    "traceback": (
                        traceback.format_exc()
                    ),
                },
            )

        time.sleep(
            interval
        )


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

    sub = parser.add_subparsers(
        dest="command"
    )

    sub.add_parser(
        "bootstrap"
    )

    sub.add_parser(
        "status"
    )

    sub.add_parser(
        "discover"
    )

    plan_parser = sub.add_parser(
        "plan"
    )

    plan_parser.add_argument(
        "--ai-review",
        action="store_true",
        help=(
            "Optional AI review of fixed architecture."
        ),
    )

    build_command = sub.add_parser(
        "build"
    )

    build_command.add_argument(
        "--force",
        action="store_true",
    )

    sub.add_parser(
        "verify"
    )

    sub.add_parser(
        "repair"
    )

    sub.add_parser(
        "design"
    )

    sub.add_parser(
        "cycle"
    )

    runtime_command = sub.add_parser(
        "runtime"
    )

    runtime_command.add_argument(
        "action",
        choices=(
            "start",
            "stop",
            "restart",
            "health",
        ),
    )

    normalize_command = (
        sub.add_parser(
            "normalize-domain"
        )
    )

    normalize_command.add_argument(
        "domain"
    )

    loop_command = sub.add_parser(
        "loop"
    )

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

    mastermind = (
        MajdDmailMastermind()
    )

    command = (
        args.command
        or "cycle"
    )

    if command == "bootstrap":
        result = (
            mastermind.bootstrap()
        )

    elif command == "status":
        result = (
            mastermind.status()
        )

    elif command == "discover":
        result = (
            mastermind.discover()
        )

    elif command == "plan":
        result = (
            mastermind.plan(
                use_ai=(
                    args.ai_review
                )
            )
        )

    elif command == "build":
        result = (
            mastermind.build(
                force=args.force
            )
        )

    elif command == "verify":
        result = (
            mastermind.verify()
        )

    elif command == "repair":
        result = (
            mastermind.repair()
        )

    elif command == "design":
        result = (
            mastermind.design()
        )

    elif command == "cycle":
        result = (
            mastermind.cycle()
        )

    elif command == "runtime":

        if args.action == "start":
            result = (
                mastermind.runtime
                .start()
            )

        elif args.action == "stop":
            result = (
                mastermind.runtime
                .stop()
            )

        elif args.action == "restart":
            result = (
                mastermind.runtime
                .restart()
            )

        else:
            result = (
                mastermind.live_health
                .verify()
            )

    elif command == "normalize-domain":

        try:
            normalized = normalize_fqdn(
                args.domain
            )

            result = {
                "ok": True,
                "input": args.domain,
                "normalized": normalized,
            }

        except DomainNormalizationError as exc:
            result = {
                "ok": False,
                "input": args.domain,
                "error": str(exc),
            }

    elif command == "loop":

        return run_loop(
            mastermind,
            args.interval,
        )

    else:
        parser.print_help()
        return 2

    print_json(
        result
    )

    if command == "verify":
        return (
            0
            if result.get(
                "core_ok"
            )
            else 1
        )

    if command == "cycle":
        return (
            0
            if result.get(
                "final_verification",
                {},
            ).get(
                "core_ok"
            )
            else 1
        )

    return (
        0
        if result.get(
            "ok",
            True,
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
