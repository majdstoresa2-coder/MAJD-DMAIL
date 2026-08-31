#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD-DMAIL
MAJD-DMAIL-DOMAIN-INFRASTRUCTURE-03.py

FILE 03 — FINAL PRIMARY FILE
Domains + Porkbun provider + security + API + runtime.

SCOPE:
    DOMAINS ONLY

HIGHEST AUTHORITY:
    SUPREME_OWNER

PRIMARY FILE:
    03 — FINAL PRIMARY FILE

PORKBUN:
    API v3
    https://api.porkbun.com/api/json/v3

SECURITY:
    Secrets are environment-only.
    No API secrets are hard-coded.
    No fake success.
    Paid/destructive operations require verified provider.
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
import uuid

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# IDENTITY
# ============================================================

PROJECT_NAME = "MAJD-DMAIL"
PROJECT_SCOPE = "DOMAINS_ONLY"
VERSION = "3.1.0-PORKBUN-FINAL"
OWNER_AUTHORITY = "SUPREME_OWNER"
FILE_NUMBER = "03"


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "majd-dmail.sqlite3"
LOG_FILE = LOG_DIR / "domain-03.log"


# ============================================================
# RUNTIME
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
# PROVIDER STATES
# ============================================================

PROVIDER_STATES: Tuple[str, ...] = (
    "not_configured",
    "configured",
    "verified",
    "unavailable",
)

VALID_PROVIDER_STATES = PROVIDER_STATES


# ============================================================
# DOMAIN STATES
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

logger = logging.getLogger("MAJD_DMAIL_03")
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


# ============================================================
# HELPERS
# ============================================================

def utc_now() -> str:
    return dt.datetime.now(
        dt.timezone.utc
    ).isoformat()


def normalize_fqdn(domain: str) -> str:

    if not isinstance(domain, str):
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

        encoded_labels.append(value)

    fqdn = ".".join(encoded_labels)

    if len(
        fqdn.encode("ascii")
    ) > 253:
        raise ValueError(
            "fqdn_too_long"
        )

    return fqdn


def bool_from_value(
    value: Any,
) -> Optional[bool]:

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return bool(value)

    text = str(
        value or ""
    ).strip().lower()

    if text in {
        "yes",
        "true",
        "1",
        "available",
        "free",
    }:
        return True

    if text in {
        "no",
        "false",
        "0",
        "unavailable",
        "taken",
        "registered",
    }:
        return False

    return None


def safe_json_load(
    body: str,
) -> Dict[str, Any]:

    if not body:
        return {}

    try:
        parsed = json.loads(body)

        if isinstance(parsed, dict):
            return parsed

        return {
            "result": parsed
        }

    except Exception:
        return {
            "raw": body[:2000]
        }


# ============================================================
# DATABASE
# ============================================================

class Store:

    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.initialize()

    def connect(
        self,
    ) -> sqlite3.Connection:

        connection = sqlite3.connect(
            str(DB_PATH),
            timeout=30,
        )

        connection.row_factory = sqlite3.Row

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
    ) -> Optional[Dict[str, Any]]:

        with self.connect() as connection:

            row = connection.execute(
                """
                SELECT *
                FROM idempotency
                WHERE idempotency_key = ?
                """,
                (key,),
            ).fetchone()

        return dict(row) if row else None

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
    ) -> Optional[Dict[str, Any]]:

        with self.connect() as connection:

            row = connection.execute(
                """
                SELECT *
                FROM domains
                WHERE domain = ?
                """,
                (domain,),
            ).fetchone()

        return dict(row) if row else None

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
# IDEMPOTENCY
# ============================================================

def get_idempotency_record(
    key: str,
) -> Optional[Dict[str, Any]]:

    return STORE.get_idempotency_record(
        key
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
# OWNER SECURITY
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
            "reason":
                "owner_authority_required",
        }

    return {
        "ok": True,
        "authorized": True,
        "authority":
            OWNER_AUTHORITY,
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
        "ok": True
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
        "ok": True
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
        "duration_ms":
            duration_ms,
    }


# ============================================================
# REGISTRAR / PORKBUN ADAPTER
# ============================================================

class RegistrarResellerAdapter:

    def __init__(self) -> None:

        provider = (
            os.getenv(
                "MAJD_REGISTRAR_PROVIDER",
                os.getenv(
                    "MAJD_REGISTRAR_NAME",
                    "",
                ),
            )
            .strip()
            .lower()
        )

        self.name = provider

        default_base = (
            "https://api.porkbun.com/api/json/v3"
            if provider == "porkbun"
            else ""
        )

        self.base_url = (
            os.getenv(
                "MAJD_REGISTRAR_BASE_URL",
                default_base,
            )
            .strip()
            .rstrip("/")
        )

        self.token = (
            os.getenv(
                "MAJD_REGISTRAR_API_TOKEN",
                "",
            )
            .strip()
        )

        self.secret = (
            os.getenv(
                "MAJD_REGISTRAR_API_SECRET",
                "",
            )
            .strip()
        )

        self.health_path = (
            os.getenv(
                "MAJD_REGISTRAR_HEALTH_PATH",
                "/ping"
                if provider == "porkbun"
                else "/health",
            )
            .strip()
        )

    def is_porkbun(
        self,
    ) -> bool:

        return (
            self.name.lower()
            == "porkbun"
        )

    def configured(
        self,
    ) -> bool:

        if self.is_porkbun():

            return bool(
                self.name
                and self.base_url
                and self.token
                and self.secret
            )

        return bool(
            self.name
            and self.base_url
            and self.token
        )

    def _url(
        self,
        path: str,
    ) -> str:

        return (
            self.base_url
            + "/"
            + path.lstrip("/")
        )

    def _headers(
        self,
        *,
        idempotency_key:
            Optional[str] = None,
    ) -> Dict[str, str]:

        headers = {
            "Accept":
                "application/json",

            "Content-Type":
                "application/json",

            "User-Agent":
                f"{PROJECT_NAME}/{VERSION}",
        }

        if self.is_porkbun():

            headers[
                "X-API-Key"
            ] = self.token

            headers[
                "X-Secret-API-Key"
            ] = self.secret

        else:

            headers[
                "Authorization"
            ] = (
                f"Bearer {self.token}"
            )

        if idempotency_key:

            headers[
                "Idempotency-Key"
            ] = idempotency_key

        return headers

    def request(
        self,
        method: str,
        path: str,
        payload: Optional[
            Dict[str, Any]
        ] = None,
        *,
        idempotency_key:
            Optional[str] = None,
    ) -> Dict[str, Any]:

        if not self.configured():

            return {
                "ok": False,
                "state":
                    "not_configured",
                "reason":
                    "registrar_reseller_not_configured",
            }

        body_payload = (
            dict(payload)
            if isinstance(
                payload,
                dict,
            )
            else None
        )

        data = (
            None
            if body_payload is None
            else json.dumps(
                body_payload,
                ensure_ascii=False,
            ).encode(
                "utf-8"
            )
        )

        request = urllib.request.Request(
            self._url(path),
            data=data,
            method=method.upper(),
            headers=self._headers(
                idempotency_key=
                    idempotency_key
            ),
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

                response_headers = {
                    str(k):
                        str(v)
                    for k, v
                    in response.headers.items()
                }

            parsed = safe_json_load(
                body
            )

            provider_success = (
                200
                <= status
                < 300
            )

            if self.is_porkbun():

                api_status = str(
                    parsed.get(
                        "status",
                        "",
                    )
                ).strip().upper()

                if api_status:
                    provider_success = (
                        provider_success
                        and
                        api_status
                        == "SUCCESS"
                    )

            return {
                "ok":
                    provider_success,

                "state":
                    (
                        "verified"
                        if provider_success
                        else "unavailable"
                    ),

                "status_code":
                    status,

                "provider":
                    self.name,

                "data":
                    parsed,

                "request_id":
                    (
                        response_headers.get(
                            "X-Request-Id"
                        )
                        or parsed.get(
                            "requestId"
                        )
                    ),

                "api_version":
                    response_headers.get(
                        "X-API-Version"
                    ),
            }

        except urllib.error.HTTPError as exc:

            try:
                error_body = (
                    exc.read()
                    .decode(
                        "utf-8",
                        errors="replace",
                    )
                )
            except Exception:
                error_body = ""

            return {
                "ok": False,
                "state":
                    "unavailable",
                "status_code":
                    int(exc.code),
                "provider":
                    self.name,
                "reason":
                    "provider_http_error",
                "data":
                    safe_json_load(
                        error_body
                    ),
            }

        except Exception as exc:

            return {
                "ok": False,
                "state":
                    "unavailable",
                "provider":
                    self.name,
                "reason":
                    "provider_request_failed",
                "error":
                    repr(exc),
            }

    def status(
        self,
    ) -> Dict[str, Any]:

        if not self.configured():

            return {
                "ok": True,
                "state":
                    "not_configured",
                "verified":
                    False,
                "provider":
                    self.name or None,
            }

        if self.is_porkbun():

            result = self.request(
                "POST",
                self.health_path,
                {},
            )

        else:

            result = self.request(
                "GET",
                self.health_path,
            )

        verified = bool(
            result.get("ok")
        )

        return {
            "ok": True,
            "state":
                (
                    "verified"
                    if verified
                    else "unavailable"
                ),
            "verified":
                verified,
            "provider":
                self.name,
            "health":
                result,
        }

    def availability(
        self,
        domain: str,
    ) -> Dict[str, Any]:

        fqdn = normalize_fqdn(
            domain
        )

        if self.is_porkbun():

            path = (
                "/domain/checkDomain/"
                + urllib.parse.quote(
                    fqdn,
                    safe="",
                )
            )

            return self.request(
                "GET",
                path,
            )

        path = os.getenv(
            "MAJD_REGISTRAR_AVAILABILITY_PATH",
            "/domains/availability",
        )

        return self.request(
            "POST",
            path,
            {
                "domain": fqdn
            },
        )

    def mutate(
        self,
        operation: str,
        payload: Dict[str, Any],
        *,
        idempotency_key:
            Optional[str] = None,
    ) -> Dict[str, Any]:

        domain = normalize_fqdn(
            str(
                payload.get(
                    "domain"
                )
                or ""
            )
        )

        body = dict(payload)
        body.pop(
            "domain",
            None,
        )

        if self.is_porkbun():

            encoded_domain = (
                urllib.parse.quote(
                    domain,
                    safe="",
                )
            )

            paths = {
                "register":
                    f"/domain/create/{encoded_domain}",

                "renew":
                    f"/domain/renew/{encoded_domain}",

                "transfer":
                    f"/domain/transfer/{encoded_domain}",

                "nameservers":
                    f"/domain/updateNs/{encoded_domain}",

                "tls":
                    f"/ssl/retrieve/{encoded_domain}",
            }

            path = paths.get(
                operation
            )

            if operation == "dns":

                records = payload.get(
                    "records"
                )

                if not isinstance(
                    records,
                    list,
                ):
                    return {
                        "ok": False,
                        "reason":
                            "records_list_required",
                    }

                results: List[
                    Dict[str, Any]
                ] = []

                for index, record in enumerate(
                    records
                ):

                    if not isinstance(
                        record,
                        dict,
                    ):
                        return {
                            "ok": False,
                            "reason":
                                "dns_record_object_required",
                            "index":
                                index,
                        }

                    record_payload = {
                        key: value
                        for key, value
                        in record.items()
                        if key
                        in {
                            "name",
                            "type",
                            "content",
                            "ttl",
                            "prio",
                        }
                    }

                    item_result = (
                        self.request(
                            "POST",
                            (
                                "/dns/create/"
                                + encoded_domain
                            ),
                            record_payload,
                            idempotency_key=(
                                (
                                    f"{idempotency_key}-"
                                    f"dns-{index}"
                                )
                                if idempotency_key
                                else None
                            ),
                        )
                    )

                    results.append(
                        item_result
                    )

                    if not item_result.get(
                        "ok"
                    ):
                        return {
                            "ok": False,
                            "state":
                                "unavailable",
                            "provider":
                                self.name,
                            "reason":
                                "dns_record_create_failed",
                            "index":
                                index,
                            "results":
                                results,
                        }

                return {
                    "ok": True,
                    "state":
                        "verified",
                    "provider":
                        self.name,
                    "results":
                        results,
                }

            if operation == "dnssec":

                custom_path = (
                    os.getenv(
                        "MAJD_REGISTRAR_DNSSEC_PATH",
                        "",
                    )
                    .strip()
                )

                if not custom_path:

                    return {
                        "ok": False,
                        "reason":
                            "porkbun_dnssec_path_not_configured",
                    }

                path = custom_path.format(
                    domain=encoded_domain
                )

            if not path:

                return {
                    "ok": False,
                    "reason":
                        "unsupported_provider_operation",
                    "operation":
                        operation,
                }

            if operation == "tls":

                return self.request(
                    "GET",
                    path,
                )

            return self.request(
                "POST",
                path,
                body,
                idempotency_key=
                    idempotency_key,
            )

        path_variable = (
            "MAJD_REGISTRAR_"
            + operation.upper()
            + "_PATH"
        )

        path = os.getenv(
            path_variable,
            "",
        ).strip()

        if not path:

            return {
                "ok": False,
                "reason":
                    "provider_operation_path_not_configured",
                "operation":
                    operation,
            }

        return self.request(
            "POST",
            path,
            payload,
            idempotency_key=
                idempotency_key,
        )


REGISTRAR = RegistrarResellerAdapter()


# ============================================================
# RDAP
# ============================================================

RDAP_BASE_URL = (
    os.getenv(
        "MAJD_RDAP_BASE_URL",
        "https://rdap.org/domain",
    )
    .strip()
    .rstrip("/")
)


def rdap_status(
) -> Dict[str, Any]:

    if not RDAP_BASE_URL:

        return {
            "ok": True,
            "state":
                "not_configured",
            "verified":
                False,
            "provider":
                "rdap",
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
            "state":
                (
                    "verified"
                    if verified
                    else "unavailable"
                ),
            "verified":
                verified,
            "provider":
                "rdap",
            "status_code":
                code,
        }

    except Exception as exc:

        return {
            "ok": True,
            "state":
                "unavailable",
            "verified":
                False,
            "provider":
                "rdap",
            "error":
                repr(exc),
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
            "state":
                "not_configured",
            "verified":
                False,
            "optional":
                True,
            "provider":
                "whois_legacy",
        }

    if name in {
        "epp",
        "registry_epp_direct",
    }:
        return {
            "ok": True,
            "state":
                "not_configured",
            "verified":
                False,
            "optional":
                True,
            "provider":
                "registry_epp_direct",
        }

    return {
        "ok": False,
        "state":
            "not_configured",
        "verified":
            False,
        "reason":
            "unknown_provider",
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
            "reason":
                "verified_registrar_reseller_required",
            "provider":
                status,
        }

    return {
        "ok": True,
        "provider":
            status,
    }


def rdap_lookup(
    domain: str,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(
        domain
    )

    request = urllib.request.Request(
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
                "application/rdap+json, application/json",
            "User-Agent":
                f"{PROJECT_NAME}/{VERSION}",
        },
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
            "ok":
                200 <= code < 300,
            "domain":
                fqdn,
            "status_code":
                code,
            "source":
                "rdap",
            "data":
                safe_json_load(
                    body
                ),
        }

    except urllib.error.HTTPError as exc:

        return {
            "ok": False,
            "domain":
                fqdn,
            "status_code":
                int(exc.code),
            "source":
                "rdap",
            "reason":
                "rdap_http_error",
        }

    except Exception as exc:

        return {
            "ok": False,
            "domain":
                fqdn,
            "source":
                "rdap",
            "reason":
                "rdap_request_failed",
            "error":
                repr(exc),
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

def _extract_porkbun_availability(
    data: Dict[str, Any],
) -> str:

    response = (
        data.get("response")
        if isinstance(
            data.get("response"),
            dict,
        )
        else {}
    )

    candidates = [
        response.get("avail"),
        response.get("available"),
        response.get("availability"),
        data.get("avail"),
        data.get("available"),
        data.get("availability"),
    ]

    for candidate in candidates:

        decision = bool_from_value(
            candidate
        )

        if decision is True:
            return "available"

        if decision is False:
            return "unavailable"

    status_text = str(
        response.get("status")
        or data.get("status")
        or ""
    ).strip().lower()

    if status_text in {
        "available",
        "premium",
        "reserved",
        "unavailable",
    }:
        return status_text

    return "unknown"


def authoritative_availability(
    domain: str,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(
        domain
    )

    verified = require_verified_provider()

    if not verified.get("ok"):

        return {
            "ok": False,
            "domain":
                fqdn,
            "availability":
                "unknown",
            "authoritative":
                False,
            "reason":
                "verified_provider_required_for_authoritative_availability",
            "provider":
                verified.get(
                    "provider"
                ),
        }

    result = REGISTRAR.availability(
        fqdn
    )

    if not result.get("ok"):

        return {
            "ok": False,
            "domain":
                fqdn,
            "availability":
                "unknown",
            "authoritative":
                False,
            "reason":
                "authoritative_availability_request_failed",
            "provider_result":
                result,
        }

    data = (
        result.get("data")
        if isinstance(
            result.get("data"),
            dict,
        )
        else {}
    )

    if REGISTRAR.is_porkbun():

        state = (
            _extract_porkbun_availability(
                data
            )
        )

    else:

        raw = str(
            data.get(
                "availability"
            )
            or data.get(
                "status"
            )
            or data.get(
                "result"
            )
            or "unknown"
        ).strip().lower()

        aliases = {
            "free":
                "available",
            "yes":
                "available",
            "true":
                "available",
            "taken":
                "unavailable",
            "registered":
                "unavailable",
            "no":
                "unavailable",
            "false":
                "unavailable",
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
        "ok":
            state != "unknown",
        "domain":
            fqdn,
        "availability":
            state,
        "authoritative":
            state != "unknown",
        "provider":
            result.get(
                "provider"
            ),
        "provider_result":
            data,
    }


# ============================================================
# SEARCH
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
        "domain":
            fqdn,
        "authoritative_availability":
            availability,
        "rdap":
            rdap,
        "whois_required":
            False,
        "direct_epp_required":
            False,
    }


def get_domain(
    domain: str,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(
        domain
    )

    local = STORE.get_domain_record(
        fqdn
    )

    rdap = rdap_lookup(
        fqdn
    )

    return {
        "ok": bool(
            local
            or rdap.get("ok")
        ),
        "domain":
            fqdn,
        "local":
            local,
        "rdap":
            rdap,
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
            "operation":
                operation,
            "domain":
                domain,
            "payload":
                payload,
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

    request_hash = _hash_request(
        operation,
        domain,
        payload,
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
                "replayed":
                    True,
                "result":
                    json.loads(
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
        "replayed":
            False,
    }


# ============================================================
# REGISTER
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
    dry_run: bool = False,
) -> Dict[str, Any]:

    started = time.time()
    fqdn = normalize_fqdn(domain)

    authorization = authorize_domain_action(
        "register",
        authority=authority,
    )

    if not authorization.get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = require_verified_provider()

    if not verified.get("ok"):
        return verified

    availability = authoritative_availability(
        fqdn
    )

    if (
        not availability.get("ok")
        or not availability.get(
            "authoritative"
        )
    ):

        return {
            "ok": False,
            "domain":
                fqdn,
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
            "domain":
                fqdn,
            "reason":
                "domain_not_available_for_registration",
            "availability":
                availability,
        }

    payload: Dict[str, Any] = {
        "domain":
            fqdn,
        "years":
            max(
                1,
                int(years),
            ),
        "registrant":
            registrant or {},
    }

    if dry_run:
        payload[
            "dryRun"
        ] = True

    existing = get_idempotency_record(
        idempotency_key
    )

    idempotency = _begin_idempotent(
        idempotency_key,
        "register",
        fqdn,
        payload,
        existing,
    )

    if idempotency.get(
        "replayed"
    ):
        return idempotency[
            "result"
        ]

    if not idempotency.get("ok"):
        return idempotency

    provider_result = REGISTRAR.mutate(
        "register",
        payload,
        idempotency_key=
            idempotency_key,
    )

    ok = bool(
        provider_result.get("ok")
    )

    result = {
        "ok":
            ok,
        "domain":
            fqdn,
        "operation":
            "register",
        "dry_run":
            bool(dry_run),
        "provider_verified":
            True,
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

    if ok and not dry_run:

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
        details={
            "dry_run":
                bool(dry_run)
        },
    )

    monitor_domain_operation(
        "register",
        domain=fqdn,
        ok=ok,
        started_at=started,
    )

    return result


# ============================================================
# RENEW
# ============================================================

def renew_domain(
    domain: str,
    idempotency_key: str,
    *,
    years: int = 1,
    authority: str = OWNER_AUTHORITY,
    dry_run: bool = False,
) -> Dict[str, Any]:

    started = time.time()
    fqdn = normalize_fqdn(domain)

    if not authorize_domain_action(
        "renew",
        authority=authority,
    ).get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = require_verified_provider()

    if not verified.get("ok"):
        return verified

    payload: Dict[str, Any] = {
        "domain":
            fqdn,
        "years":
            max(
                1,
                int(years),
            ),
    }

    if dry_run:
        payload[
            "dryRun"
        ] = True

    existing = get_idempotency_record(
        idempotency_key
    )

    idempotency = _begin_idempotent(
        idempotency_key,
        "renew",
        fqdn,
        payload,
        existing,
    )

    if idempotency.get(
        "replayed"
    ):
        return idempotency[
            "result"
        ]

    if not idempotency.get("ok"):
        return idempotency

    provider_result = REGISTRAR.mutate(
        "renew",
        payload,
        idempotency_key=
            idempotency_key,
    )

    ok = bool(
        provider_result.get("ok")
    )

    result = {
        "ok":
            ok,
        "domain":
            fqdn,
        "operation":
            "renew",
        "dry_run":
            bool(dry_run),
        "provider_verified":
            True,
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

    audit_domain_action(
        "domain_renewal",
        domain=fqdn,
        outcome=(
            "success"
            if ok
            else "failed"
        ),
        details={
            "dry_run":
                bool(dry_run)
        },
    )

    monitor_domain_operation(
        "renew",
        domain=fqdn,
        ok=ok,
        started_at=started,
    )

    return result


# ============================================================
# TRANSFER
# ============================================================

def transfer_domain(
    domain: str,
    idempotency_key: str,
    *,
    auth_code: str,
    authority: str = OWNER_AUTHORITY,
    dry_run: bool = False,
) -> Dict[str, Any]:

    started = time.time()
    fqdn = normalize_fqdn(domain)

    if not authorize_domain_action(
        "transfer",
        authority=authority,
    ).get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = require_verified_provider()

    if not verified.get("ok"):
        return verified

    if not str(
        auth_code or ""
    ).strip():

        return {
            "ok": False,
            "reason":
                "transfer_auth_code_required",
            "domain":
                fqdn,
        }

    payload: Dict[str, Any] = {
        "domain":
            fqdn,
        "authCode":
            str(
                auth_code
            ).strip(),
    }

    if dry_run:
        payload[
            "dryRun"
        ] = True

    existing = get_idempotency_record(
        idempotency_key
    )

    idempotency = _begin_idempotent(
        idempotency_key,
        "transfer",
        fqdn,
        payload,
        existing,
    )

    if idempotency.get(
        "replayed"
    ):
        return idempotency[
            "result"
        ]

    if not idempotency.get("ok"):
        return idempotency

    provider_result = REGISTRAR.mutate(
        "transfer",
        payload,
        idempotency_key=
            idempotency_key,
    )

    ok = bool(
        provider_result.get("ok")
    )

    result = {
        "ok":
            ok,
        "domain":
            fqdn,
        "operation":
            "transfer",
        "dry_run":
            bool(dry_run),
        "provider_verified":
            True,
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

    if ok and not dry_run:

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
        details={
            "dry_run":
                bool(dry_run)
        },
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
    idempotency_key:
        Optional[str] = None,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(domain)

    if not authorize_domain_action(
        "dns",
        authority=authority,
    ).get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = require_verified_provider()

    if not verified.get("ok"):
        return verified

    if not records:

        return {
            "ok": False,
            "reason":
                "dns_records_required",
        }

    return REGISTRAR.mutate(
        "dns",
        {
            "domain":
                fqdn,
            "records":
                records,
        },
        idempotency_key=(
            idempotency_key
            or str(uuid.uuid4())
        ),
    )


# ============================================================
# NAMESERVERS
# ============================================================

def configure_nameservers(
    domain: str,
    nameservers: List[str],
    *,
    authority: str = OWNER_AUTHORITY,
    idempotency_key:
        Optional[str] = None,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(domain)

    if not authorize_domain_action(
        "nameservers",
        authority=authority,
    ).get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = require_verified_provider()

    if not verified.get("ok"):
        return verified

    normalized_nameservers = [
        normalize_fqdn(value)
        for value in nameservers
    ]

    if not normalized_nameservers:

        return {
            "ok": False,
            "reason":
                "nameservers_required",
        }

    return REGISTRAR.mutate(
        "nameservers",
        {
            "domain":
                fqdn,
            "ns":
                normalized_nameservers,
        },
        idempotency_key=(
            idempotency_key
            or str(uuid.uuid4())
        ),
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
    idempotency_key:
        Optional[str] = None,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(domain)

    if not authorize_domain_action(
        "dnssec",
        authority=authority,
    ).get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = require_verified_provider()

    if not verified.get("ok"):
        return verified

    return REGISTRAR.mutate(
        "dnssec",
        {
            "domain":
                fqdn,
            "ds_records":
                ds_records,
        },
        idempotency_key=(
            idempotency_key
            or str(uuid.uuid4())
        ),
    )


# ============================================================
# TLS
# ============================================================

def provision_domain_tls(
    domain: str,
    *,
    authority: str = OWNER_AUTHORITY,
) -> Dict[str, Any]:

    fqdn = normalize_fqdn(domain)

    if not authorize_domain_action(
        "tls",
        authority=authority,
    ).get("ok"):

        return {
            "ok": False,
            "reason":
                "owner_authority_required",
        }

    verified = require_verified_provider()

    if not verified.get("ok"):
        return verified

    return REGISTRAR.mutate(
        "tls",
        {
            "domain":
                fqdn,
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

        route_paths = [
            "/api/health",
            "/api/domains/search",
            "/api/domains/register",
            "/api/domains/renew",
            "/api/domains/transfer",
            "/api/domains/dns",
            "/api/domains/nameservers",
            "/api/domains/dnssec",
            "/api/domains/ssl",
        ]

        self.routes = [
            type(
                "Route",
                (),
                {
                    "path": path
                },
            )()
            for path
            in route_paths
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
        "MAJD-DMAIL/3.1"
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

        value = json.loads(raw)

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
        ).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
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

        self.wfile.write(raw)

    def do_GET(
        self,
    ) -> None:

        parsed = urllib.parse.urlparse(
            self.path
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

                result = search_domain(
                    domain
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
                    "reason":
                        str(exc),
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

                result = search_domain(
                    domain
                )

            elif (
                path
                == "/api/domains/register"
            ):

                result = register_domain(
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
                    dry_run=bool(
                        payload.get(
                            "dry_run",
                            False,
                        )
                    ),
                )

            elif (
                path
                == "/api/domains/renew"
            ):

                result = renew_domain(
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
                    dry_run=bool(
                        payload.get(
                            "dry_run",
                            False,
                        )
                    ),
                )

            elif (
                path
                == "/api/domains/transfer"
            ):

                result = transfer_domain(
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
                    dry_run=bool(
                        payload.get(
                            "dry_run",
                            False,
                        )
                    ),
                )

            elif (
                path
                == "/api/domains/dns"
            ):

                records = payload.get(
                    "records"
                )

                if not isinstance(
                    records,
                    list,
                ):
                    raise ValueError(
                        "records_list_required"
                    )

                result = configure_dns(
                    domain,
                    records,
                    authority=
                        authority,
                    idempotency_key=(
                        str(
                            payload.get(
                                "idempotency_key"
                            )
                            or ""
                        )
                        or None
                    ),
                )

            elif (
                path
                == "/api/domains/nameservers"
            ):

                nameservers = payload.get(
                    "nameservers"
                )

                if not isinstance(
                    nameservers,
                    list,
                ):
                    raise ValueError(
                        "nameservers_list_required"
                    )

                result = configure_nameservers(
                    domain,
                    [
                        str(value)
                        for value
                        in nameservers
                    ],
                    authority=
                        authority,
                    idempotency_key=(
                        str(
                            payload.get(
                                "idempotency_key"
                            )
                            or ""
                        )
                        or None
                    ),
                )

            elif (
                path
                == "/api/domains/dnssec"
            ):

                ds_records = payload.get(
                    "ds_records"
                )

                if not isinstance(
                    ds_records,
                    list,
                ):
                    raise ValueError(
                        "ds_records_list_required"
                    )

                result = configure_dnssec(
                    domain,
                    ds_records,
                    authority=
                        authority,
                    idempotency_key=(
                        str(
                            payload.get(
                                "idempotency_key"
                            )
                            or ""
                        )
                        or None
                    ),
                )

            elif (
                path
                == "/api/domains/ssl"
            ):

                result = provision_domain_tls(
                    domain,
                    authority=
                        authority,
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
                    "reason":
                        str(exc),
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

    checks[
        "normalize"
    ] = (
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
    ] = validate_owner_authority(
        OWNER_AUTHORITY
    )

    checks[
        "routes"
    ] = (
        len(
            app.routes
        )
        == 9
    )

    checks[
        "porkbun_secret_required"
    ] = (
        True
        if not REGISTRAR.is_porkbun()
        else bool(
            REGISTRAR.secret
        )
    )

    return {
        "ok":
            all(
                checks.values()
            ),
        "project":
            PROJECT_NAME,
        "scope":
            PROJECT_SCOPE,
        "owner_authority":
            OWNER_AUTHORITY,
        "version":
            VERSION,
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

    server = ThreadingHTTPServer(
        (
            host,
            int(port),
        ),
        Handler,
    )

    logger.info(
        "MAJD-DMAIL 03 listening on %s:%s",
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

    parser = argparse.ArgumentParser(
        prog=Path(
            __file__
        ).name
    )

    sub = parser.add_subparsers(
        dest="command"
    )

    sub.add_parser(
        "health"
    )

    sub.add_parser(
        "self-test"
    )

    normalize_command = sub.add_parser(
        "normalize"
    )

    normalize_command.add_argument(
        "domain"
    )

    search_command = sub.add_parser(
        "search"
    )

    search_command.add_argument(
        "domain"
    )

    runtime_command = sub.add_parser(
        "serve"
    )

    runtime_command.add_argument(
        "--host",
        default=
            API_HOST,
    )

    runtime_command.add_argument(
        "--port",
        type=int,
        default=
            API_PORT,
    )

    return parser


# ============================================================
# MAIN
# ============================================================

def main(
) -> int:

    args = (
        build_parser()
        .parse_args()
    )

    command = (
        args.command
        or "serve"
    )

    if command == "health":

        result = health_report()

    elif command == "self-test":

        result = run_self_test()

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

            result = search_domain(
                args.domain
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
