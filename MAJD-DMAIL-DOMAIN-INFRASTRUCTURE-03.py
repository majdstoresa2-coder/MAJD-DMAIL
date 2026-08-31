#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD-DMAIL
MAJD-DMAIL-DOMAIN-INFRASTRUCTURE-03.py

FILE 03 — FINAL PRIMARY FILE
Domains + provider contracts + security + API + runtime.

SCOPE:
    DOMAINS ONLY

HIGHEST AUTHORITY:
    SUPREME_OWNER

PRIMARY FILE:
    03 — FINAL PRIMARY FILE

This file contains:
- Strict FQDN normalization
- Registrar / Reseller provider interface
- RDAP primary discovery
- WHOIS optional legacy status
- Direct Registry/EPP optional status
- Authoritative availability
- Domain search/details
- Registration
- Renewal
- Transfer
- Idempotency
- Lifecycle
- DNS
- Nameservers
- DNSSEC
- Domain TLS
- Owner authority
- Authorization
- Security events
- Audit
- Monitoring
- HTTP API
- Runtime
- Self-test

External mutations are never reported successful unless the
configured registrar/reseller provider is verified and returns
a successful result.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import hmac
import json
import logging
import os
import re
import sqlite3
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

from http.server import (
    BaseHTTPRequestHandler,
    ThreadingHTTPServer,
)

from pathlib import Path

from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)


# ============================================================
# IDENTITY / AUTHORITY
# ============================================================

PROJECT_NAME = "MAJD-DMAIL"
PROJECT_SCOPE = "DOMAINS_ONLY"
VERSION = "3.0.0-FINAL"

OWNER_AUTHORITY = "SUPREME_OWNER"

FILE_NUMBER = "03"


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent

DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"

for directory in (
    DATA_DIR,
    LOG_DIR,
):
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

DB_PATH = (
    DATA_DIR
    / "majd-dmail.sqlite3"
)

LOG_FILE = (
    LOG_DIR
    / "domain-03.log"
)


# ============================================================
# RUNTIME CONFIG
# ============================================================

API_HOST = os.getenv(
    "MAJD_DMAIL_API_HOST",
    "127.0.0.1",
).strip()

API_PORT = int(
    os.getenv(
        "MAJD_DMAIL_API_PORT",
        "8080",
    )
)

HTTP_TIMEOUT = max(
    3,
    min(
        60,
        int(
            os.getenv(
                "MAJD_DMAIL_HTTP_TIMEOUT",
                "15",
            )
        ),
    ),
)


# ============================================================
# PROVIDER CONTRACT
# ============================================================

PROVIDER_STATES: Tuple[str, ...] = (
    "not_configured",
    "configured",
    "verified",
    "unavailable",
)

VALID_PROVIDER_STATES = (
    PROVIDER_STATES
)


# ============================================================
# DOMAIN LIFECYCLE CONTRACT
# ============================================================

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


# ============================================================
# LOGGING
# ============================================================

logger = logging.getLogger(
    "MAJD_DMAIL_03"
)

logger.setLevel(
    logging.INFO
)

if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )

    file_handler = (
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        )
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )


# ============================================================
# HELPERS
# ============================================================

def utc_now() -> str:
    return (
        dt.datetime.now(
            dt.timezone.utc
        ).isoformat()
    )


def normalize_fqdn(
    domain: str,
) -> str:

    if not isinstance(
        domain,
        str,
    ):
        raise ValueError(
            "domain_must_be_string"
        )

    raw = (
        domain
        .strip()
        .lower()
        .rstrip(".")
    )

    if not raw:
        raise ValueError(
            "domain_empty"
        )

    if "://" in raw:
        raise ValueError(
            "url_not_allowed"
        )

    if any(
        value in raw
        for value in (
            "/",
            "\\",
            "?",
            "#",
            "@",
            ":",
        )
    ):
        raise ValueError(
            "invalid_fqdn_input"
        )

    labels = raw.split(".")

    if len(labels) < 2:
        raise ValueError(
            "fqdn_requires_suffix"
        )

    if any(
        not label
        for label in labels
    ):
        raise ValueError(
            "invalid_fqdn_labels"
        )

    encoded_labels: List[str] = []

    for label in labels:

        try:
            value = (
                label
                .encode("idna")
                .decode("ascii")
            )

        except UnicodeError as exc:
            raise ValueError(
                "idna_encoding_failed"
            ) from exc

        if len(value) > 63:
            raise ValueError(
                "fqdn_label_too_long"
            )

        if (
            value.startswith("-")
            or value.endswith("-")
        ):
            raise ValueError(
                "invalid_fqdn_label"
            )

        if not re.fullmatch(
            r"[a-z0-9-]+",
            value,
        ):
            raise ValueError(
                "invalid_fqdn_characters"
            )

        encoded_labels.append(
            value
        )

    if (
        len(encoded_labels) >= 3
        and encoded_labels[-1]
        == encoded_labels[-2]
    ):
        raise ValueError(
            "duplicated_terminal_label"
        )

    fqdn = ".".join(
        encoded_labels
    )

    if len(
        fqdn.encode("ascii")
    ) > 253:
        raise ValueError(
            "fqdn_too_long"
        )

    return fqdn


# ============================================================
# DATABASE
# ============================================================

class Store:

    def __init__(self) -> None:

        self.lock = (
            threading.RLock()
        )

        self.initialize()

    def connect(
        self,
    ) -> sqlite3.Connection:

        connection = (
            sqlite3.connect(
                str(DB_PATH),
                timeout=30,
            )
        )

        connection.row_factory = (
            sqlite3.Row
        )

        return connection

    def initialize(
        self,
    ) -> None:

        with (
            self.lock,
            self.connect() as connection,
        ):

            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS domains (
                    domain TEXT PRIMARY KEY,
                    lifecycle_state TEXT NOT NULL,
                    provider TEXT,
                    expires_at TEXT,
                    metadata_json TEXT NOT NULL DEFAULT '{}',
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS idempotency (
                    idempotency_key TEXT PRIMARY KEY,
                    operation TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    request_hash TEXT NOT NULL,
                    status TEXT NOT NULL,
                    result_json TEXT,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    domain TEXT,
                    actor TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    details_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS security_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    details_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    domain TEXT,
                    ok INTEGER NOT NULL,
                    duration_ms INTEGER NOT NULL
                );
                """
            )

            connection.commit()

    def get_idempotency_record(
        self,
        key: str,
    ) -> Optional[
        Dict[str, Any]
    ]:

        with self.connect() as connection:

            row = connection.execute(
                """
                SELECT *
                FROM idempotency
                WHERE idempotency_key = ?
                """,
                (key,),
            ).fetchone()

        return (
            dict(row)
            if row
            else None
        )

    def reserve_idempotency_key(
        self,
        key: str,
        operation: str,
        domain: str,
        request_hash: str,
    ) -> None:

        with (
            self.lock,
            self.connect() as connection,
        ):

            connection.execute(
                """
                INSERT INTO idempotency
                (
                    idempotency_key,
                    operation,
                    domain,
                    request_hash,
                    status,
                    result_json,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    operation,
                    domain,
                    request_hash,
                    "in_progress",
                    None,
                    utc_now(),
                ),
            )

            connection.commit()

    def store_idempotency_result(
        self,
        key: str,
        status: str,
        result: Dict[str, Any],
    ) -> None:

        with (
            self.lock,
            self.connect() as connection,
        ):

            connection.execute(
                """
                UPDATE idempotency
                SET
                    status = ?,
                    result_json = ?,
                    updated_at = ?
                WHERE idempotency_key = ?
                """,
                (
                    status,
                    json.dumps(
                        result,
                        ensure_ascii=False,
                        default=str,
                    ),
                    utc_now(),
                    key,
                ),
            )

            connection.commit()

    def upsert_domain(
        self,
        domain: str,
        lifecycle_state: str,
        provider: Optional[str],
        expires_at: Optional[str],
        metadata: Dict[str, Any],
    ) -> None:

        if (
            lifecycle_state
            not in DOMAIN_LIFECYCLE_STATES
        ):
            lifecycle_state = "unknown"

        with (
            self.lock,
            self.connect() as connection,
        ):

            connection.execute(
                """
                INSERT INTO domains
                (
                    domain,
                    lifecycle_state,
                    provider,
                    expires_at,
                    metadata_json,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?)

                ON CONFLICT(domain)
                DO UPDATE SET
                    lifecycle_state =
                        excluded.lifecycle_state,

                    provider =
                        COALESCE(
                            excluded.provider,
                            domains.provider
                        ),

                    expires_at =
                        COALESCE(
                            excluded.expires_at,
                            domains.expires_at
                        ),

                    metadata_json =
                        excluded.metadata_json,

                    updated_at =
                        excluded.updated_at
                """,
                (
                    domain,
                    lifecycle_state,
                    provider,
                    expires_at,
                    json.dumps(
                        metadata,
                        ensure_ascii=False,
                        default=str,
                    ),
                    utc_now(),
                ),
            )

            connection.commit()

    def get_domain_record(
        self,
        domain: str,
    ) -> Optional[
        Dict[str, Any]
    ]:

        with self.connect() as connection:

            row = connection.execute(
                """
                SELECT *
                FROM domains
                WHERE domain = ?
                """,
                (domain,),
            ).fetchone()

        return (
            dict(row)
            if row
            else None
        )

    def audit(
        self,
        event_type: str,
        domain: Optional[str],
        actor: str,
        outcome: str,
        details: Dict[str, Any],
    ) -> None:

        with (
            self.lock,
            self.connect() as connection,
        ):

            connection.execute(
                """
                INSERT INTO audit_events
                (
                    timestamp,
                    event_type,
                    domain,
                    actor,
                    outcome,
                    details_json
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    utc_now(),
                    event_type,
                    domain,
                    actor,
                    outcome,
                    json.dumps(
                        details,
                        ensure_ascii=False,
                        default=str,
                    ),
                ),
            )

            connection.commit()

    def security(
        self,
        event_type: str,
        severity: str,
        details: Dict[str, Any],
    ) -> None:

        with (
            self.lock,
            self.connect() as connection,
        ):

            connection.execute(
                """
                INSERT INTO security_events
                (
                    timestamp,
                    event_type,
                    severity,
                    details_json
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    utc_now(),
                    event_type,
                    severity,
                    json.dumps(
                        details,
                        ensure_ascii=False,
                        default=str,
                    ),
                ),
            )

            connection.commit()

    def metric(
        self,
        operation: str,
        domain: Optional[str],
        ok: bool,
        duration_ms: int,
    ) -> None:

        with (
            self.lock,
            self.connect() as connection,
        ):

            connection.execute(
                """
                INSERT INTO metrics
                (
                    timestamp,
                    operation,
                    domain,
                    ok,
                    duration_ms
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    utc_now(),
                    operation,
                    domain,
                    1 if ok else 0,
                    duration_ms,
                ),
            )

            connection.commit()


STORE = Store()


# ============================================================
# IDEMPOTENCY PUBLIC INTERFACES
# ============================================================

def get_idempotency_record(
    key: str,
) -> Optional[
    Dict[str, Any]
]:
    return (
        STORE
        .get_idempotency_record(
            key
        )
    )


def reserve_idempotency_key(
    key: str,
    operation: str,
    domain: str,
    request_hash: str,
) -> None:

    STORE.reserve_idempotency_key(
        key,
        operation,
        domain,
        request_hash,
    )


def store_idempotency_result(
    key: str,
    status: str,
    result: Dict[str, Any],
) -> None:

    STORE.store_idempotency_result(
        key,
        status,
        result,
    )


# ============================================================
# OWNER / AUTHORIZATION / SECURITY
# ============================================================

def validate_owner_authority(
    authority: str,
) -> bool:

    return hmac.compare_digest(
        str(authority),
        OWNER_AUTHORITY,
    )


def authorize_domain_action(
    action: str,
    *,
    authority: str = OWNER_AUTHORITY,
    actor: str = OWNER_AUTHORITY,
) -> Dict[str, Any]:

    if not validate_owner_authority(
        authority
    ):

        record_security_event(
            "authority_rejected",
            severity="high",
            details={
                "action": action,
                "actor": actor,
            },
        )

        return {
            "ok": False,
            "authorized": False,
            "reason": (
                "owner_authority_required"
            ),
        }

    return {
        "ok": True,
        "authorized": True,
        "authority": OWNER_AUTHORITY,
        "action": action,
    }


def audit_domain_action(
    event_type: str,
    *,
    domain: Optional[str] = None,
    actor: str = OWNER_AUTHORITY,
    outcome: str = "recorded",
    details: Optional[
        Dict[str, Any]
    ] = None,
) -> Dict[str, Any]:

    STORE.audit(
        event_type,
        domain,
        actor,
        outcome,
        details or {},
    )

    return {
        "ok": True,
    }


def record_security_event(
    event_type: str,
    *,
    severity: str = "medium",
    details: Optional[
        Dict[str, Any]
    ] = None,
) -> Dict[str, Any]:

    STORE.security(
        event_type,
        severity,
        details or {},
    )

    return {
        "ok": True,
    }


def monitor_domain_operation(
    operation: str,
    *,
    domain: Optional[str],
    ok: bool,
    started_at: float,
    details: Optional[
        Dict[str, Any]
    ] = None,
) -> Dict[str, Any]:

    duration_ms = max(
        0,
        int(
            (
                time.time()
                - started_at
            )
            * 1000
        ),
    )

    STORE.metric(
        operation,
        domain,
        ok,
        duration_ms,
    )

    return {
        "ok": True,
        "duration_ms": duration_ms,
    }


# ============================================================
# REGISTRAR / RESELLER ADAPTER
# ============================================================

class RegistrarResellerAdapter:

    def __init__(self) -> None:

        self.name = os.getenv(
            "MAJD_REGISTRAR_PROVIDER",
            "",
        ).strip()

        self.base_url = os.getenv(
            "MAJD_REGISTRAR_BASE_URL",
            "",
        ).strip().rstrip("/")

        self.token = os.getenv(
            "MAJD_REGISTRAR_API_TOKEN",
            "",
        ).strip()

        self.paths = {

            "health": os.getenv(
                "MAJD_REGISTRAR_HEALTH_PATH",
                "/health",
            ),

            "availability": os.getenv(
                "MAJD_REGISTRAR_AVAILABILITY_PATH",
                "/domains/availability",
            ),

            "register": os.getenv(
                "MAJD_REGISTRAR_REGISTER_PATH",
                "/domains/register",
            ),

            "renew": os.getenv(
                "MAJD_REGISTRAR_RENEW_PATH",
                "/domains/renew",
            ),

            "transfer": os.getenv(
                "MAJD_REGISTRAR_TRANSFER_PATH",
                "/domains/transfer",
            ),

            "dns": os.getenv(
                "MAJD_REGISTRAR_DNS_PATH",
                "/domains/dns",
            ),

            "nameservers": os.getenv(
                "MAJD_REGISTRAR_NAMESERVER_PATH",
                "/domains/nameservers",
            ),

            "dnssec": os.getenv(
                "MAJD_REGISTRAR_DNSSEC_PATH",
                "/domains/dnssec",
            ),

            "tls": os.getenv(
                "MAJD_REGISTRAR_TLS_PATH",
                "/domains/tls",
            ),
        }

    def configured(
        self,
    ) -> bool:

        return bool(
            self.name
            and self.base_url
            and self.token
        )

    def request(
        self,
        method: str,
        path: str,
        payload: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:

        if not self.configured():

            return {
                "ok": False,
                "state": "not_configured",
                "reason": (
                    "registrar_reseller_not_configured"
                ),
            }

        data = (
            None
            if payload is None
            else json.dumps(
                payload
            ).encode(
                "utf-8"
            )
        )

        request = (
            urllib.request.Request(
                (
                    self.base_url
                    + "/"
                    + path.lstrip("/")
                ),
                data=data,
                method=method,
                headers={
                    "Accept":
                        "application/json",

                    "Content-Type":
                        "application/json",

                    "Authorization":
                        f"Bearer {self.token}",

                    "User-Agent":
                        f"{PROJECT_NAME}/{VERSION}",
                },
            )
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=HTTP_TIMEOUT,
            ) as response:

                status = int(
                    getattr(
                        response,
                        "status",
                        200,
                    )
                )

                body = (
                    response
                    .read()
                    .decode(
                        "utf-8",
                        errors="replace",
                    )
                )

            try:
                parsed = (
                    json.loads(body)
                    if body
                    else {}
                )

            except Exception:
                parsed = {
                    "raw": body[:2000]
                }

            return {
                "ok": (
                    200
                    <= status
                    < 300
                ),
                "state": (
                    "verified"
                    if (
                        200
                        <= status
                        < 300
                    )
                    else "unavailable"
                ),
                "status_code": status,
                "provider": self.name,
                "data": parsed,
            }

        except urllib.error.HTTPError as exc:

            return {
                "ok": False,
                "state": "unavailable",
                "status_code": exc.code,
                "provider": self.name,
                "reason": (
                    "provider_http_error"
                ),
            }

        except Exception as exc:

            return {
                "ok": False,
                "state": "unavailable",
                "provider": self.name,
                "reason": (
                    "provider_request_failed"
                ),
                "error": repr(exc),
            }

    def status(
        self,
    ) -> Dict[str, Any]:

        if not self.configured():

            return {
                "ok": True,
                "state": "not_configured",
                "verified": False,
                "provider": (
                    self.name
                    or None
                ),
            }

        result = self.request(
            "GET",
            self.paths["health"],
        )

        verified = bool(
            result.get("ok")
        )

        return {
            "ok": True,
            "state": (
                "verified"
                if verified
                else "unavailable"
            ),
            "verified": verified,
            "provider": self.name,
            "health": result,
        }

    def availability(
        self,
        domain: str,
    ) -> Dict[str, Any]:

        return self.request(
            "POST",
            self.paths[
                "availability"
            ],
            {
                "domain": domain,
            },
        )

    def mutate(
        self,
        operation: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:

        if operation not in self.paths:

            return {
                "ok": False,
                "reason": (
                    "unsupported_provider_operation"
                ),
            }

        return self.request(
            "POST",
            self.paths[operation],
            payload,
        )


REGISTRAR = (
    RegistrarResellerAdapter()
)


# ============================================================
# RDAP
# ============================================================

RDAP_BASE_URL = os.getenv(
    "MAJD_RDAP_BASE_URL",
    "https://rdap.org/domain",
).strip().rstrip("/")


def rdap_status() -> Dict[str, Any]:

    if not RDAP_BASE_URL:

        return {
            "ok": True,
            "state": "not_configured",
            "verified": False,
            "provider": "rdap",
        }

    try:

        request = urllib.request.Request(
            "https://rdap.org/",
            headers={
                "User-Agent":
                    f"{PROJECT_NAME}/{VERSION}"
            },
        )

        with urllib.request.urlopen(
            request,
            timeout=min(
                HTTP_TIMEOUT,
                8,
            ),
        ) as response:

            code = int(
                getattr(
                    response,
                    "status",
                    200,
                )
            )

        verified = (
            200
            <= code
            < 500
        )

        return {
            "ok": True,
            "state": (
                "verified"
                if verified
                else "unavailable"
            ),
            "verified": verified,
            "provider": "rdap",
            "status_code": code,
        }

    except Exception as exc:

        return {
            "ok": True,
            "state": "unavailable",
            "verified": False,
            "provider": "rdap",
            "error": repr(exc),
        }


def provider_status(
    provider: str = "registrar",
) -> Dict[str, Any]:

    name = (
        str(provider)
        .strip()
        .lower()
    )

    if name in {
        "registrar",
        "reseller",
        "registrar_reseller",
    }:
        return REGISTRAR.status()

    if name == "rdap":
        return rdap_status()

    if name in {
        "whois",
        "whois_legacy",
    }:
        return {
            "ok": True,
            "state": "not_configured",
            "verified": False,
            "optional": True,
            "provider": "whois_legacy",
        }

    if name in {
        "epp",
        "registry_epp_direct",
    }:
        return {
            "ok": True,
            "state": "not_configured",
            "verified": False,
            "optional": True,
            "provider":
                "registry_epp_direct",
        }

    return {
        "ok": False,
        "state": "not_configured",
        "verified": False,
        "reason": "unknown_provider",
    }


def require_verified_provider(
) -> Dict[str, Any]:

    status = provider_status(
        "registrar"
    )

    if (
        status.get("state")
        != "verified"
        or not status.get(
            "verified"
        )
    ):

        return {
            "ok": False,
            "reason": (
                "verified_registrar_reseller_required"
            ),
            "provider": status,
        }

    return {
        "ok": True,
        "provider": status,
    }


def rdap_lookup(
    domain: str,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(
        domain
    )

    request = (
        urllib.request.Request(
            (
                RDAP_BASE_URL
                + "/"
                + urllib.parse.quote(
                    fqdn,
                    safe="",
                )
            ),
            headers={
                "Accept":
                    "application/rdap+json, "
                    "application/json",

                "User-Agent":
                    f"{PROJECT_NAME}/{VERSION}",
            },
        )
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=HTTP_TIMEOUT,
        ) as response:

            code = int(
                getattr(
                    response,
                    "status",
                    200,
                )
            )

            body = (
                response
                .read()
                .decode(
                    "utf-8",
                    errors="replace",
                )
            )

        return {
            "ok": (
                200
                <= code
                < 300
            ),
            "domain": fqdn,
            "status_code": code,
            "source": "rdap",
            "data": (
                json.loads(body)
                if body
                else {}
            ),
        }

    except urllib.error.HTTPError as exc:

        return {
            "ok": False,
            "domain": fqdn,
            "status_code": exc.code,
            "source": "rdap",
            "reason": (
                "rdap_http_error"
            ),
        }

    except Exception as exc:

        return {
            "ok": False,
            "domain": fqdn,
            "source": "rdap",
            "reason": (
                "rdap_request_failed"
            ),
            "error": repr(exc),
        }


def rdap_verified_status(
) -> Dict[str, Any]:

    return rdap_status()


def whois_legacy_status(
) -> Dict[str, Any]:

    return provider_status(
        "whois_legacy"
    )


def registry_epp_direct_status(
) -> Dict[str, Any]:

    return provider_status(
        "registry_epp_direct"
    )


# ============================================================
# AUTHORITATIVE AVAILABILITY
# ============================================================

def authoritative_availability(
    domain: str,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(
        domain
    )

    verified = (
        require_verified_provider()
    )

    if not verified.get("ok"):

        return {
            "ok": False,
            "domain": fqdn,
            "availability": "unknown",
            "authoritative": False,
            "reason": (
                "verified_provider_required_for_authoritative_availability"
            ),
            "provider": (
                verified.get(
                    "provider"
                )
            ),
        }

    result = (
        REGISTRAR
        .availability(
            fqdn
        )
    )

    if not result.get("ok"):

        return {
            "ok": False,
            "domain": fqdn,
            "availability": "unknown",
            "authoritative": False,
            "reason": (
                "authoritative_availability_request_failed"
            ),
            "provider_result": result,
        }

    data = (
        result.get("data")
        if isinstance(
            result.get("data"),
            dict,
        )
        else {}
    )

    raw = str(
        data.get("availability")
        or data.get("status")
        or data.get("result")
        or "unknown"
    ).strip().lower()

    aliases = {
        "free": "available",
        "yes": "available",
        "true": "available",
        "taken": "unavailable",
        "registered": "unavailable",
        "no": "unavailable",
        "false": "unavailable",
    }

    state = aliases.get(
        raw,
        raw,
    )

    if state not in {
        "available",
        "unavailable",
        "reserved",
        "premium",
        "unknown",
    }:
        state = "unknown"

    return {
        "ok": (
            state
            != "unknown"
        ),
        "domain": fqdn,
        "availability": state,
        "authoritative": True,
        "provider": (
            result.get(
                "provider"
            )
        ),
        "provider_result": data,
    }


# ============================================================
# SEARCH / DETAILS
# ============================================================

def search_domain(
    domain: str,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(
        domain
    )

    availability = (
        authoritative_availability(
            fqdn
        )
    )

    rdap = rdap_lookup(
        fqdn
    )

    return {
        "ok": bool(
            availability.get("ok")
            or rdap.get("ok")
        ),
        "domain": fqdn,
        "authoritative_availability":
            availability,
        "rdap": rdap,
        "whois_required": False,
        "direct_epp_required": False,
    }


def get_domain(
    domain: str,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(
        domain
    )

    local = (
        STORE
        .get_domain_record(
            fqdn
        )
    )

    rdap = rdap_lookup(
        fqdn
    )

    return {
        "ok": bool(
            local
            or rdap.get("ok")
        ),
        "domain": fqdn,
        "local": local,
        "rdap": rdap,
    }


# ============================================================
# IDEMPOTENCY INTERNAL
# ============================================================

def _hash_request(
    operation: str,
    domain: str,
    payload: Dict[str, Any],
) -> str:

    raw = json.dumps(
        {
            "operation": operation,
            "domain": domain,
            "payload": payload,
        },
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


def _begin_idempotent(
    key: str,
    operation: str,
    domain: str,
    payload: Dict[str, Any],
    existing: Optional[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:

    key = str(
        key or ""
    ).strip()

    if not key:

        return {
            "ok": False,
            "reason":
                "idempotency_key_required",
        }

    request_hash = (
        _hash_request(
            operation,
            domain,
            payload,
        )
    )

    if existing:

        if (
            existing.get(
                "request_hash"
            )
            != request_hash
        ):

            return {
                "ok": False,
                "reason":
                    "idempotency_key_request_mismatch",
            }

        if (
            existing.get("status")
            == "completed"
            and existing.get(
                "result_json"
            )
        ):

            return {
                "ok": True,
                "replayed": True,
                "result": json.loads(
                    existing[
                        "result_json"
                    ]
                ),
            }

        return {
            "ok": False,
            "reason":
                "operation_already_in_progress",
        }

    reserve_idempotency_key(
        key,
        operation,
        domain,
        request_hash,
    )

    return {
        "ok": True,
        "replayed": False,
    }


# ============================================================
# REGISTER DOMAIN
# ============================================================

def register_domain(
    domain: str,
    idempotency_key: str,
    *,
    years: int = 1,
    registrant: Optional[
        Dict[str, Any]
    ] = None,
    authority: str = OWNER_AUTHORITY,
) -> Dict[str, Any]:

    started = time.time()

    fqdn = normalize_fqdn(
        domain
    )

    authorization = (
        authorize_domain_action(
            "register",
            authority=authority,
        )
    )

    if not authorization.get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = (
        require_verified_provider()
    )

    if not verified.get("ok"):
        return verified

    availability = (
        authoritative_availability(
            fqdn
        )
    )

    if (
        not availability.get("ok")
        or not availability.get(
            "authoritative"
        )
    ):

        return {
            "ok": False,
            "domain": fqdn,
            "reason":
                "authoritative_availability_required",
            "availability":
                availability,
        }

    if (
        availability.get(
            "availability"
        )
        not in {
            "available",
            "premium",
        }
    ):

        return {
            "ok": False,
            "domain": fqdn,
            "reason":
                "domain_not_available_for_registration",
            "availability":
                availability,
        }

    payload = {
        "domain": fqdn,
        "years": max(
            1,
            int(years),
        ),
        "registrant":
            registrant or {},
    }

    existing = (
        get_idempotency_record(
            idempotency_key
        )
    )

    idempotency = (
        _begin_idempotent(
            idempotency_key,
            "register",
            fqdn,
            payload,
            existing,
        )
    )

    if idempotency.get(
        "replayed"
    ):
        return idempotency[
            "result"
        ]

    if not idempotency.get("ok"):
        return idempotency

    provider_result = (
        REGISTRAR.mutate(
            "register",
            payload,
        )
    )

    ok = bool(
        provider_result.get("ok")
    )

    result = {
        "ok": ok,
        "domain": fqdn,
        "operation": "register",
        "provider_verified": True,
        "provider_result":
            provider_result,
    }

    store_idempotency_result(
        idempotency_key,
        (
            "completed"
            if ok
            else "failed"
        ),
        result,
    )

    if ok:

        data = (
            provider_result.get("data")
            if isinstance(
                provider_result.get(
                    "data"
                ),
                dict,
            )
            else {}
        )

        STORE.upsert_domain(
            fqdn,
            "active",
            REGISTRAR.name,
            data.get(
                "expires_at"
            ),
            {
                "registration":
                    data
            },
        )

    audit_domain_action(
        "domain_registration",
        domain=fqdn,
        outcome=(
            "success"
            if ok
            else "failed"
        ),
    )

    monitor_domain_operation(
        "register",
        domain=fqdn,
        ok=ok,
        started_at=started,
    )

    return result


# ============================================================
# RENEW DOMAIN
# ============================================================

def renew_domain(
    domain: str,
    idempotency_key: str,
    *,
    years: int = 1,
    authority: str = OWNER_AUTHORITY,
) -> Dict[str, Any]:

    started = time.time()

    fqdn = normalize_fqdn(
        domain
    )

    authorization = (
        authorize_domain_action(
            "renew",
            authority=authority,
        )
    )

    if not authorization.get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = (
        require_verified_provider()
    )

    if not verified.get("ok"):
        return verified

    payload = {
        "domain": fqdn,
        "years": max(
            1,
            int(years),
        ),
    }

    existing = (
        get_idempotency_record(
            idempotency_key
        )
    )

    idempotency = (
        _begin_idempotent(
            idempotency_key,
            "renew",
            fqdn,
            payload,
            existing,
        )
    )

    if idempotency.get(
        "replayed"
    ):
        return idempotency[
            "result"
        ]

    if not idempotency.get("ok"):
        return idempotency

    provider_result = (
        REGISTRAR.mutate(
            "renew",
            payload,
        )
    )

    ok = bool(
        provider_result.get("ok")
    )

    result = {
        "ok": ok,
        "domain": fqdn,
        "operation": "renew",
        "provider_verified": True,
        "provider_result":
            provider_result,
    }

    store_idempotency_result(
        idempotency_key,
        (
            "completed"
            if ok
            else "failed"
        ),
        result,
    )

    if ok:

        data = (
            provider_result.get("data")
            if isinstance(
                provider_result.get(
                    "data"
                ),
                dict,
            )
            else {}
        )

        STORE.upsert_domain(
            fqdn,
            "active",
            REGISTRAR.name,
            data.get(
                "expires_at"
            ),
            {
                "renewal": data
            },
        )

    audit_domain_action(
        "domain_renewal",
        domain=fqdn,
        outcome=(
            "success"
            if ok
            else "failed"
        ),
    )

    monitor_domain_operation(
        "renew",
        domain=fqdn,
        ok=ok,
        started_at=started,
    )

    return result


# ============================================================
# TRANSFER DOMAIN
# ============================================================

def transfer_domain(
    domain: str,
    idempotency_key: str,
    *,
    auth_code: str,
    authority: str = OWNER_AUTHORITY,
) -> Dict[str, Any]:

    started = time.time()

    fqdn = normalize_fqdn(
        domain
    )

    authorization = (
        authorize_domain_action(
            "transfer",
            authority=authority,
        )
    )

    if not authorization.get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = (
        require_verified_provider()
    )

    if not verified.get("ok"):
        return verified

    if not str(
        auth_code or ""
    ).strip():

        return {
            "ok": False,
            "reason":
                "transfer_auth_code_required",
            "domain": fqdn,
        }

    payload = {
        "domain": fqdn,
        "auth_code":
            str(auth_code).strip(),
    }

    existing = (
        get_idempotency_record(
            idempotency_key
        )
    )

    idempotency = (
        _begin_idempotent(
            idempotency_key,
            "transfer",
            fqdn,
            payload,
            existing,
        )
    )

    if idempotency.get(
        "replayed"
    ):
        return idempotency[
            "result"
        ]

    if not idempotency.get("ok"):
        return idempotency

    provider_result = (
        REGISTRAR.mutate(
            "transfer",
            payload,
        )
    )

    ok = bool(
        provider_result.get("ok")
    )

    result = {
        "ok": ok,
        "domain": fqdn,
        "operation": "transfer",
        "provider_verified": True,
        "provider_result":
            provider_result,
    }

    store_idempotency_result(
        idempotency_key,
        (
            "completed"
            if ok
            else "failed"
        ),
        result,
    )

    if ok:

        STORE.upsert_domain(
            fqdn,
            "transfer_pending",
            REGISTRAR.name,
            None,
            {
                "transfer":
                    provider_result.get(
                        "data"
                    )
                    or {}
            },
        )

    audit_domain_action(
        "domain_transfer",
        domain=fqdn,
        outcome=(
            "success"
            if ok
            else "failed"
        ),
    )

    monitor_domain_operation(
        "transfer",
        domain=fqdn,
        ok=ok,
        started_at=started,
    )

    return result


# ============================================================
# DNS
# ============================================================

def configure_dns(
    domain: str,
    records: List[
        Dict[str, Any]
    ],
    *,
    authority: str = OWNER_AUTHORITY,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(
        domain
    )

    if not authorize_domain_action(
        "dns",
        authority=authority,
    ).get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = (
        require_verified_provider()
    )

    if not verified.get("ok"):
        return verified

    return REGISTRAR.mutate(
        "dns",
        {
            "domain": fqdn,
            "records": records,
        },
    )


# ============================================================
# NAMESERVERS
# ============================================================

def configure_nameservers(
    domain: str,
    nameservers: List[str],
    *,
    authority: str = OWNER_AUTHORITY,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(
        domain
    )

    if not authorize_domain_action(
        "nameservers",
        authority=authority,
    ).get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = (
        require_verified_provider()
    )

    if not verified.get("ok"):
        return verified

    normalized_nameservers = [
        normalize_fqdn(
            value
        )
        for value in nameservers
    ]

    return REGISTRAR.mutate(
        "nameservers",
        {
            "domain": fqdn,
            "nameservers":
                normalized_nameservers,
        },
    )


# ============================================================
# DNSSEC
# ============================================================

def configure_dnssec(
    domain: str,
    ds_records: List[
        Dict[str, Any]
    ],
    *,
    authority: str = OWNER_AUTHORITY,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(
        domain
    )

    if not authorize_domain_action(
        "dnssec",
        authority=authority,
    ).get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = (
        require_verified_provider()
    )

    if not verified.get("ok"):
        return verified

    return REGISTRAR.mutate(
        "dnssec",
        {
            "domain": fqdn,
            "ds_records":
                ds_records,
        },
    )


# ============================================================
# DOMAIN TLS
# ============================================================

def provision_domain_tls(
    domain: str,
    *,
    authority: str = OWNER_AUTHORITY,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(
        domain
    )

    if not authorize_domain_action(
        "tls",
        authority=authority,
    ).get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = (
        require_verified_provider()
    )

    if not verified.get("ok"):
        return verified

    return REGISTRAR.mutate(
        "tls",
        {
            "domain": fqdn,
        },
    )


# ============================================================
# HEALTH
# ============================================================

def health_report(
) -> Dict[str, Any]:

    return {
        "ok": True,
        "project":
            PROJECT_NAME,
        "scope":
            PROJECT_SCOPE,
        "version":
            VERSION,
        "owner_authority":
            OWNER_AUTHORITY,
        "no_fake_success":
            True,
        "primary_files_limit":
            3,
        "registrar_reseller":
            provider_status(
                "registrar"
            ),
        "rdap":
            provider_status(
                "rdap"
            ),
        "whois_required":
            False,
        "direct_epp_required":
            False,
        "timestamp":
            utc_now(),
    }


# ============================================================
# APPLICATION CONTRACT
# ============================================================

class MajdDmailApplication:

    def __init__(
        self,
    ) -> None:

        self.routes = [

            type(
                "Route",
                (),
                {
                    "path":
                        "/api/health"
                },
            )(),

            type(
                "Route",
                (),
                {
                    "path":
                        "/api/domains/search"
                },
            )(),

            type(
                "Route",
                (),
                {
                    "path":
                        "/api/domains/register"
                },
            )(),

            type(
                "Route",
                (),
                {
                    "path":
                        "/api/domains/renew"
                },
            )(),

            type(
                "Route",
                (),
                {
                    "path":
                        "/api/domains/transfer"
                },
            )(),

            type(
                "Route",
                (),
                {
                    "path":
                        "/api/domains/dns"
                },
            )(),

            type(
                "Route",
                (),
                {
                    "path":
                        "/api/domains/ssl"
                },
            )(),
        ]


def create_app(
) -> MajdDmailApplication:

    return MajdDmailApplication()


app = create_app()


# ============================================================
# HTTP HANDLER
# ============================================================

class Handler(
    BaseHTTPRequestHandler
):

    server_version = (
        "MAJD-DMAIL/3"
    )

    def log_message(
        self,
        fmt: str,
        *args: Any,
    ) -> None:

        logger.info(
            "HTTP | " + fmt,
            *args,
        )

    def body(
        self,
    ) -> Dict[str, Any]:

        length = int(
            self.headers.get(
                "Content-Length",
                "0",
            )
            or "0"
        )

        if length <= 0:
            return {}

        if length > 2_000_000:
            raise ValueError(
                "request_body_too_large"
            )

        raw = (
            self.rfile
            .read(length)
            .decode("utf-8")
        )

        value = json.loads(
            raw
        )

        if not isinstance(
            value,
            dict,
        ):
            raise ValueError(
                "json_object_required"
            )

        return value

    def send_json(
        self,
        status: int,
        payload: Dict[str, Any],
    ) -> None:

        raw = json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            default=str,
        ).encode(
            "utf-8"
        )

        self.send_response(
            status
        )

        self.send_header(
            "Content-Type",
            "application/json; "
            "charset=utf-8",
        )

        self.send_header(
            "Content-Length",
            str(len(raw)),
        )

        self.send_header(
            "Cache-Control",
            "no-store",
        )

        self.end_headers()

        self.wfile.write(
            raw
        )

    def do_GET(
        self,
    ) -> None:

        parsed = (
            urllib.parse
            .urlparse(
                self.path
            )
        )

        try:

            if (
                parsed.path
                == "/api/health"
            ):

                self.send_json(
                    200,
                    health_report(),
                )

                return

            if (
                parsed.path
                == "/api/domains/search"
            ):

                query = (
                    urllib.parse
                    .parse_qs(
                        parsed.query
                    )
                )

                domain = (
                    query.get(
                        "domain"
                    )
                    or [""]
                )[0]

                result = (
                    search_domain(
                        domain
                    )
                )

                self.send_json(
                    (
                        200
                        if result.get("ok")
                        else 503
                    ),
                    result,
                )

                return

            self.send_json(
                404,
                {
                    "ok": False,
                    "reason":
                        "route_not_found",
                },
            )

        except ValueError as exc:

            self.send_json(
                400,
                {
                    "ok": False,
                    "reason": str(exc),
                },
            )

        except Exception as exc:

            logger.exception(
                "GET failed"
            )

            self.send_json(
                500,
                {
                    "ok": False,
                    "reason":
                        "internal_error",
                    "error":
                        repr(exc),
                },
            )

    def do_POST(
        self,
    ) -> None:

        path = (
            urllib.parse
            .urlparse(
                self.path
            )
            .path
        )

        try:

            payload = self.body()

            domain = str(
                payload.get(
                    "domain"
                )
                or ""
            )

            authority = str(
                payload.get(
                    "authority"
                )
                or OWNER_AUTHORITY
            )

            if (
                path
                == "/api/domains/search"
            ):

                result = (
                    search_domain(
                        domain
                    )
                )

            elif (
                path
                == "/api/domains/register"
            ):

                result = (
                    register_domain(
                        domain,
                        str(
                            payload.get(
                                "idempotency_key"
                            )
                            or ""
                        ),
                        years=int(
                            payload.get(
                                "years"
                            )
                            or 1
                        ),
                        registrant=(
                            payload.get(
                                "registrant"
                            )
                            if isinstance(
                                payload.get(
                                    "registrant"
                                ),
                                dict,
                            )
                            else {}
                        ),
                        authority=
                            authority,
                    )
                )

            elif (
                path
                == "/api/domains/renew"
            ):

                result = (
                    renew_domain(
                        domain,
                        str(
                            payload.get(
                                "idempotency_key"
                            )
                            or ""
                        ),
                        years=int(
                            payload.get(
                                "years"
                            )
                            or 1
                        ),
                        authority=
                            authority,
                    )
                )

            elif (
                path
                == "/api/domains/transfer"
            ):

                result = (
                    transfer_domain(
                        domain,
                        str(
                            payload.get(
                                "idempotency_key"
                            )
                            or ""
                        ),
                        auth_code=str(
                            payload.get(
                                "auth_code"
                            )
                            or ""
                        ),
                        authority=
                            authority,
                    )
                )

            elif (
                path
                == "/api/domains/dns"
            ):

                records = (
                    payload.get(
                        "records"
                    )
                )

                if not isinstance(
                    records,
                    list,
                ):
                    raise ValueError(
                        "records_list_required"
                    )

                result = (
                    configure_dns(
                        domain,
                        records,
                        authority=
                            authority,
                    )
                )

            elif (
                path
                == "/api/domains/ssl"
            ):

                result = (
                    provision_domain_tls(
                        domain,
                        authority=
                            authority,
                    )
                )

            else:

                self.send_json(
                    404,
                    {
                        "ok": False,
                        "reason":
                            "route_not_found",
                    },
                )

                return

            self.send_json(
                (
                    200
                    if result.get("ok")
                    else 409
                ),
                result,
            )

        except ValueError as exc:

            self.send_json(
                400,
                {
                    "ok": False,
                    "reason": str(exc),
                },
            )

        except Exception as exc:

            logger.exception(
                "POST failed"
            )

            self.send_json(
                500,
                {
                    "ok": False,
                    "reason":
                        "internal_error",
                    "error":
                        repr(exc),
                },
            )


# ============================================================
# SELF TEST
# ============================================================

def run_self_test(
) -> Dict[str, Any]:

    checks: Dict[
        str,
        bool,
    ] = {}

    checks["normalize"] = (
        normalize_fqdn(
            "Example.COM"
        )
        == "example.com"
        and
        normalize_fqdn(
            "example.com."
        )
        == "example.com"
    )

    duplicate_rejected = False

    try:
        normalize_fqdn(
            "example.com.com"
        )

    except ValueError:
        duplicate_rejected = True

    checks[
        "duplicate_rejected"
    ] = duplicate_rejected

    checks[
        "provider_states"
    ] = (
        set(
            PROVIDER_STATES
        )
        == {
            "not_configured",
            "configured",
            "verified",
            "unavailable",
        }
    )

    checks[
        "owner"
    ] = (
        validate_owner_authority(
            OWNER_AUTHORITY
        )
    )

    checks[
        "routes"
    ] = (
        len(
            app.routes
        )
        == 7
    )

    return {
        "ok": all(
            checks.values()
        ),
        "project":
            PROJECT_NAME,
        "scope":
            PROJECT_SCOPE,
        "owner_authority":
            OWNER_AUTHORITY,
        "checks":
            checks,
    }


# ============================================================
# SERVER
# ============================================================

def serve(
    host: str = API_HOST,
    port: int = API_PORT,
) -> int:

    server = (
        ThreadingHTTPServer(
            (
                host,
                int(port),
            ),
            Handler,
        )
    )

    logger.info(
        "MAJD-DMAIL 03 "
        "listening on %s:%s",
        host,
        port,
    )

    try:

        server.serve_forever(
            poll_interval=0.5
        )

    except KeyboardInterrupt:
        pass

    finally:
        server.server_close()

    return 0


# ============================================================
# CLI
# ============================================================

def build_parser(
) -> argparse.ArgumentParser:

    parser = (
        argparse.ArgumentParser(
            prog=(
                Path(__file__).name
            )
        )
    )

    sub = (
        parser
        .add_subparsers(
            dest="command"
        )
    )

    sub.add_parser(
        "health"
    )

    sub.add_parser(
        "self-test"
    )

    normalize_command = (
        sub.add_parser(
            "normalize"
        )
    )

    normalize_command.add_argument(
        "domain"
    )

    search_command = (
        sub.add_parser(
            "search"
        )
    )

    search_command.add_argument(
        "domain"
    )

    runtime_command = (
        sub.add_parser(
            "serve"
        )
    )

    runtime_command.add_argument(
        "--host",
        default=API_HOST,
    )

    runtime_command.add_argument(
        "--port",
        type=int,
        default=API_PORT,
    )

    return parser


# ============================================================
# MAIN
# ============================================================

def main() -> int:

    args = (
        build_parser()
        .parse_args()
    )

    command = (
        args.command
        or "serve"
    )

    if command == "health":

        result = (
            health_report()
        )

    elif command == "self-test":

        result = (
            run_self_test()
        )

    elif command == "normalize":

        try:

            result = {
                "ok": True,
                "domain":
                    normalize_fqdn(
                        args.domain
                    ),
            }

        except ValueError as exc:

            result = {
                "ok": False,
                "reason":
                    str(exc),
            }

    elif command == "search":

        try:

            result = (
                search_domain(
                    args.domain
                )
            )

        except ValueError as exc:

            result = {
                "ok": False,
                "reason":
                    str(exc),
            }

    elif command == "serve":

        return serve(
            args.host,
            args.port,
        )

    else:
        return 2

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    )

    return (
        0
        if result.get("ok")
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
