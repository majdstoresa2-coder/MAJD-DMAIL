#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
MAJD-DMAIL
MAJD-DMAIL-CORE-PLATFORM-02.py
===============================================================================

FILE 02
MAJD-DMAIL CORE PLATFORM

Permanent manually maintained core for MAJD-DMAIL.

ARCHITECTURE
============

01 - MAJD-DMAIL-AI-AUTOMATION-MASTERMIND-01.py
     AI / automation / planning / verification / repair / orchestration.

02 - MAJD-DMAIL-CORE-PLATFORM-02.py
     Permanent platform core.
     This file.

03 - AI generated.
04 - AI generated.
05 - AI generated.

There MUST NOT be a primary MAJD-DMAIL file 06 or higher.

MISSION
=======

Provide the trusted core contracts and persistent runtime foundation for:

- Domain search
- Domain registration
- Domain renewal
- Domain transfer
- Domain lifecycle
- DNS
- SSL/TLS
- Professional paid email
- Customer accounts
- Owner authority
- Pricing
- Subscriptions
- Payments
- Invoices
- Wallet/accounting records
- Security
- Audit
- Provider adapters
- Notifications
- AI integration contracts
- Runtime health
- Service verification

SECURITY PRINCIPLES
===================

- SUPREME_OWNER is the highest authority.
- Passwords are never stored as plaintext.
- API keys and secrets are never hard-coded.
- External services are NEVER marked LIVE without real verification.
- Financial operations are idempotent.
- Important operations are auditable.
- Ownership-sensitive domain operations require authorization.
- Provider implementations are replaceable adapters.
- File 02 does not automatically modify file 01.
- File 02 does not create primary source files.
- Routine operations are designed for automation.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import enum
import hashlib
import hmac
import json
import logging
import os
import secrets
import sqlite3
import tempfile
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import (
    Any,
    Dict,
    Generator,
    Iterable,
    List,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Tuple,
)


# =============================================================================
# IDENTITY
# =============================================================================

PROJECT_NAME = "MAJD-DMAIL"
FILE_ID = "02"
VERSION = "1.0.0"

OWNER_AUTHORITY = "SUPREME_OWNER"

THIS_FILENAME = "MAJD-DMAIL-CORE-PLATFORM-02.py"
MASTERMIND_FILENAME = "MAJD-DMAIL-AI-AUTOMATION-MASTERMIND-01.py"

MAX_PRIMARY_FILES = 5


# =============================================================================
# PATHS
# =============================================================================

ROOT = Path(__file__).resolve().parent

DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"
STATE_DIR = ROOT / "state"
RUNTIME_DIR = ROOT / "runtime"
BACKUP_DIR = ROOT / "backups"

DATABASE_FILE = DATA_DIR / "majd-dmail.sqlite3"
LOG_FILE = LOG_DIR / "core-platform.log"
EVENTS_FILE = LOG_DIR / "core-events.jsonl"
CORE_STATE_FILE = STATE_DIR / "core-platform-state.json"

for directory in (
    DATA_DIR,
    LOG_DIR,
    STATE_DIR,
    RUNTIME_DIR,
    BACKUP_DIR,
):
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


# =============================================================================
# LOGGING
# =============================================================================

logger = logging.getLogger(
    "MAJD_DMAIL_CORE"
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


# =============================================================================
# GENERAL HELPERS
# =============================================================================

def utc_now() -> str:
    return dt.datetime.now(
        dt.timezone.utc
    ).isoformat()


def new_id(
    prefix: str,
) -> str:

    return (
        f"{prefix}_"
        f"{uuid.uuid4().hex}"
    )


def normalize_email(
    value: str,
) -> str:

    return value.strip().lower()


def normalize_domain(
    value: str,
) -> str:

    value = value.strip().lower()

    if value.endswith("."):
        value = value[:-1]

    return value


def json_dumps(
    payload: Any,
) -> str:

    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def json_loads_safe(
    value: Optional[str],
    default: Any,
) -> Any:

    if not value:
        return default

    try:
        return json.loads(value)
    except Exception:
        return default


def sha256_text(
    value: str,
) -> str:

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def atomic_write_json(
    path: Path,
    payload: Any,
) -> None:

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

            json.dump(
                payload,
                handle,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
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


def append_jsonl(
    path: Path,
    payload: Mapping[str, Any],
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
            json_dumps(
                dict(payload)
            )
            + "\n"
        )


# =============================================================================
# ENUMS
# =============================================================================

class UserRole(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    SUPPORT_AI = "SUPPORT_AI"
    OPERATIONS_AI = "OPERATIONS_AI"
    SUPREME_OWNER = "SUPREME_OWNER"


class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DISABLED = "DISABLED"
    PENDING = "PENDING"


class ProviderState(str, enum.Enum):
    NOT_CONFIGURED = "NOT_CONFIGURED"
    CONFIGURED = "CONFIGURED"
    VERIFYING = "VERIFYING"
    LIVE = "LIVE"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"


class DomainStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    TRANSFER_PENDING = "TRANSFER_PENDING"
    SUSPENDED = "SUSPENDED"
    CANCELLED = "CANCELLED"


class SubscriptionStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    PAST_DUE = "PAST_DUE"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class InvoiceStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    PAID = "PAID"
    VOID = "VOID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class PaymentStatus(str, enum.Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class EmailServiceStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CANCELLED = "CANCELLED"


class SSLStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    EXPIRING = "EXPIRING"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"


# =============================================================================
# ERRORS
# =============================================================================

class MajdDmailError(Exception):
    pass


class AuthorizationError(MajdDmailError):
    pass


class ValidationError(MajdDmailError):
    pass


class ConflictError(MajdDmailError):
    pass


class NotFoundError(MajdDmailError):
    pass


class ProviderUnavailableError(MajdDmailError):
    pass


class PaymentError(MajdDmailError):
    pass


# =============================================================================
# PASSWORD SECURITY
# =============================================================================

PBKDF2_ITERATIONS = int(
    os.getenv(
        "MAJD_PASSWORD_ITERATIONS",
        "310000",
    )
)


def hash_password(
    password: str,
) -> str:

    if len(password) < 10:
        raise ValidationError(
            "Password must contain at least 10 characters."
        )

    salt = secrets.token_bytes(32)

    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )

    return (
        f"pbkdf2_sha256$"
        f"{PBKDF2_ITERATIONS}$"
        f"{salt.hex()}$"
        f"{derived.hex()}"
    )


def verify_password(
    password: str,
    stored: str,
) -> bool:

    try:

        algorithm, iterations, salt_hex, digest_hex = stored.split(
            "$",
            3,
        )

        if algorithm != "pbkdf2_sha256":
            return False

        derived = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
        )

        return hmac.compare_digest(
            derived.hex(),
            digest_hex,
        )

    except Exception:
        return False


# =============================================================================
# DATABASE
# =============================================================================

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL,
    display_name TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    token_hash TEXT NOT NULL UNIQUE,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    revoked_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS domains (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    domain_name TEXT NOT NULL UNIQUE,
    registrar_provider TEXT,
    registrar_reference TEXT,
    status TEXT NOT NULL,
    registered_at TEXT,
    expires_at TEXT,
    auto_renew INTEGER NOT NULL DEFAULT 1,
    transfer_lock INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS dns_records (
    id TEXT PRIMARY KEY,
    domain_id TEXT NOT NULL,
    record_type TEXT NOT NULL,
    record_name TEXT NOT NULL,
    record_value TEXT NOT NULL,
    ttl INTEGER NOT NULL,
    provider_reference TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(domain_id) REFERENCES domains(id)
);

CREATE TABLE IF NOT EXISTS ssl_certificates (
    id TEXT PRIMARY KEY,
    domain_id TEXT NOT NULL,
    provider TEXT,
    status TEXT NOT NULL,
    issued_at TEXT,
    expires_at TEXT,
    provider_reference TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(domain_id) REFERENCES domains(id)
);

CREATE TABLE IF NOT EXISTS email_services (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    domain_id TEXT NOT NULL,
    provider TEXT,
    plan_code TEXT NOT NULL,
    mailbox_count INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL,
    provider_reference TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(domain_id) REFERENCES domains(id)
);

CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    currency TEXT NOT NULL,
    price_minor INTEGER NOT NULL,
    recurring_interval TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    metadata_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TEXT,
    renews_at TEXT,
    cancelled_at TEXT,
    external_reference TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    subscription_id TEXT,
    currency TEXT NOT NULL,
    subtotal_minor INTEGER NOT NULL,
    tax_minor INTEGER NOT NULL,
    total_minor INTEGER NOT NULL,
    status TEXT NOT NULL,
    external_reference TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(subscription_id) REFERENCES subscriptions(id)
);

CREATE TABLE IF NOT EXISTS invoice_items (
    id TEXT PRIMARY KEY,
    invoice_id TEXT NOT NULL,
    description TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price_minor INTEGER NOT NULL,
    total_minor INTEGER NOT NULL,
    metadata_json TEXT NOT NULL,
    FOREIGN KEY(invoice_id) REFERENCES invoices(id)
);

CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    invoice_id TEXT,
    provider TEXT,
    idempotency_key TEXT NOT NULL UNIQUE,
    amount_minor INTEGER NOT NULL,
    currency TEXT NOT NULL,
    status TEXT NOT NULL,
    external_reference TEXT,
    failure_reason TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(invoice_id) REFERENCES invoices(id)
);

CREATE TABLE IF NOT EXISTS provider_health (
    provider_type TEXT NOT NULL,
    provider_name TEXT NOT NULL,
    state TEXT NOT NULL,
    checked_at TEXT NOT NULL,
    details_json TEXT NOT NULL,
    PRIMARY KEY(provider_type, provider_name)
);

CREATE TABLE IF NOT EXISTS audit_events (
    id TEXT PRIMARY KEY,
    actor_id TEXT,
    actor_role TEXT,
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id TEXT,
    status TEXT NOT NULL,
    details_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    channel TEXT NOT NULL,
    destination_masked TEXT,
    subject TEXT,
    body TEXT NOT NULL,
    status TEXT NOT NULL,
    provider_reference TEXT,
    created_at TEXT NOT NULL,
    sent_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_domains_user
ON domains(user_id);

CREATE INDEX IF NOT EXISTS idx_dns_domain
ON dns_records(domain_id);

CREATE INDEX IF NOT EXISTS idx_email_user
ON email_services(user_id);

CREATE INDEX IF NOT EXISTS idx_subscriptions_user
ON subscriptions(user_id);

CREATE INDEX IF NOT EXISTS idx_invoices_user
ON invoices(user_id);

CREATE INDEX IF NOT EXISTS idx_payments_user
ON payments(user_id);

CREATE INDEX IF NOT EXISTS idx_audit_created
ON audit_events(created_at);
"""


class Database:

    def __init__(
        self,
        path: Path = DATABASE_FILE,
    ) -> None:

        self.path = path
        self._lock = threading.RLock()


    def connect(
        self,
    ) -> sqlite3.Connection:

        connection = sqlite3.connect(
            str(self.path),
            timeout=30,
            isolation_level=None,
        )

        connection.row_factory = sqlite3.Row

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        connection.execute(
            "PRAGMA journal_mode = WAL"
        )

        connection.execute(
            "PRAGMA busy_timeout = 30000"
        )

        return connection


    def initialize(
        self,
    ) -> None:

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self._lock:

            connection = self.connect()

            try:

                connection.executescript(
                    SCHEMA
                )

            finally:

                connection.close()


    @contextmanager
    def transaction(
        self,
    ) -> Generator[
        sqlite3.Connection,
        None,
        None,
    ]:

        with self._lock:

            connection = self.connect()

            try:

                connection.execute(
                    "BEGIN IMMEDIATE"
                )

                yield connection

                connection.execute(
                    "COMMIT"
                )

            except Exception:

                try:
                    connection.execute(
                        "ROLLBACK"
                    )
                except Exception:
                    pass

                raise

            finally:

                connection.close()


    def fetch_one(
        self,
        query: str,
        parameters: Sequence[Any] = (),
    ) -> Optional[Dict[str, Any]]:

        connection = self.connect()

        try:

            row = connection.execute(
                query,
                tuple(parameters),
            ).fetchone()

            if row is None:
                return None

            return dict(row)

        finally:

            connection.close()


    def fetch_all(
        self,
        query: str,
        parameters: Sequence[Any] = (),
    ) -> List[Dict[str, Any]]:

        connection = self.connect()

        try:

            rows = connection.execute(
                query,
                tuple(parameters),
            ).fetchall()

            return [
                dict(row)
                for row in rows
            ]

        finally:

            connection.close()


# =============================================================================
# AUDIT
# =============================================================================

class AuditService:

    def __init__(
        self,
        database: Database,
    ) -> None:

        self.database = database


    def record(
        self,
        action: str,
        *,
        actor_id: Optional[str] = None,
        actor_role: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        status: str = "SUCCESS",
        details: Optional[Mapping[str, Any]] = None,
    ) -> str:

        event_id = new_id(
            "audit"
        )

        timestamp = utc_now()

        payload = {
            "id": event_id,
            "actor_id": actor_id,
            "actor_role": actor_role,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "status": status,
            "details": dict(details or {}),
            "created_at": timestamp,
        }

        with self.database.transaction() as connection:

            connection.execute(
                """
                INSERT INTO audit_events (
                    id,
                    actor_id,
                    actor_role,
                    action,
                    resource_type,
                    resource_id,
                    status,
                    details_json,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    actor_id,
                    actor_role,
                    action,
                    resource_type,
                    resource_id,
                    status,
                    json_dumps(
                        dict(details or {})
                    ),
                    timestamp,
                ),
            )

        append_jsonl(
            EVENTS_FILE,
            payload,
        )

        return event_id


# =============================================================================
# AUTHORITY
# =============================================================================

@dataclasses.dataclass(frozen=True)
class Actor:
    id: str
    role: UserRole


class AuthorityService:

    @staticmethod
    def require_owner(
        actor: Actor,
    ) -> None:

        if actor.role != UserRole.SUPREME_OWNER:
            raise AuthorizationError(
                "SUPREME_OWNER authority required."
            )


    @staticmethod
    def require_self_or_owner(
        actor: Actor,
        target_user_id: str,
    ) -> None:

        if (
            actor.role == UserRole.SUPREME_OWNER
            or actor.id == target_user_id
        ):
            return

        raise AuthorizationError(
            "Access denied."
        )


# =============================================================================
# USERS / AUTHENTICATION
# =============================================================================

class UserService:

    def __init__(
        self,
        database: Database,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.audit = audit


    def create_user(
        self,
        email: str,
        password: str,
        *,
        display_name: Optional[str] = None,
        role: UserRole = UserRole.CUSTOMER,
    ) -> Dict[str, Any]:

        email = normalize_email(
            email
        )

        if "@" not in email:
            raise ValidationError(
                "Invalid email address."
            )

        user_id = new_id(
            "usr"
        )

        now = utc_now()

        try:

            with self.database.transaction() as connection:

                connection.execute(
                    """
                    INSERT INTO users (
                        id,
                        email,
                        password_hash,
                        role,
                        status,
                        display_name,
                        created_at,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        email,
                        hash_password(
                            password
                        ),
                        role.value,
                        UserStatus.ACTIVE.value,
                        display_name,
                        now,
                        now,
                    ),
                )

        except sqlite3.IntegrityError as exc:

            raise ConflictError(
                "User already exists."
            ) from exc

        self.audit.record(
            "USER_CREATED",
            actor_id=user_id,
            actor_role=role.value,
            resource_type="USER",
            resource_id=user_id,
        )

        return self.get_user(
            user_id
        )


    def get_user(
        self,
        user_id: str,
    ) -> Dict[str, Any]:

        row = self.database.fetch_one(
            """
            SELECT
                id,
                email,
                role,
                status,
                display_name,
                created_at,
                updated_at
            FROM users
            WHERE id = ?
            """,
            (
                user_id,
            ),
        )

        if not row:
            raise NotFoundError(
                "User not found."
            )

        return row


    def authenticate(
        self,
        email: str,
        password: str,
    ) -> Dict[str, Any]:

        email = normalize_email(
            email
        )

        row = self.database.fetch_one(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (
                email,
            ),
        )

        if not row:
            raise AuthorizationError(
                "Invalid credentials."
            )

        if row["status"] != UserStatus.ACTIVE.value:
            raise AuthorizationError(
                "User is not active."
            )

        if not verify_password(
            password,
            row["password_hash"],
        ):
            raise AuthorizationError(
                "Invalid credentials."
            )

        return {
            "id": row["id"],
            "email": row["email"],
            "role": row["role"],
            "status": row["status"],
            "display_name": row["display_name"],
        }


    def create_session(
        self,
        user_id: str,
        *,
        ttl_hours: int = 24,
    ) -> str:

        session_id = new_id(
            "ses"
        )

        token = secrets.token_urlsafe(
            48
        )

        token_hash = sha256_text(
            token
        )

        now = dt.datetime.now(
            dt.timezone.utc
        )

        expires = now + dt.timedelta(
            hours=max(
                1,
                ttl_hours,
            )
        )

        with self.database.transaction() as connection:

            connection.execute(
                """
                INSERT INTO sessions (
                    id,
                    user_id,
                    token_hash,
                    expires_at,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    user_id,
                    token_hash,
                    expires.isoformat(),
                    now.isoformat(),
                ),
            )

        return token


    def resolve_session(
        self,
        token: str,
    ) -> Optional[Actor]:

        token_hash = sha256_text(
            token
        )

        row = self.database.fetch_one(
            """
            SELECT
                s.id AS session_id,
                s.expires_at,
                s.revoked_at,
                u.id AS user_id,
                u.role,
                u.status
            FROM sessions s
            JOIN users u
                ON u.id = s.user_id
            WHERE s.token_hash = ?
            """,
            (
                token_hash,
            ),
        )

        if not row:
            return None

        if row["revoked_at"]:
            return None

        if row["status"] != UserStatus.ACTIVE.value:
            return None

        try:

            expires = dt.datetime.fromisoformat(
                row["expires_at"]
            )

        except ValueError:
            return None

        if expires <= dt.datetime.now(
            dt.timezone.utc
        ):
            return None

        return Actor(
            id=row["user_id"],
            role=UserRole(
                row["role"]
            ),
        )


# =============================================================================
# PROVIDER CONTRACTS
# =============================================================================

@dataclasses.dataclass
class ProviderHealth:
    ok: bool
    provider_type: str
    provider_name: str
    state: ProviderState
    checked_at: str
    details: Dict[str, Any]


class BaseProvider(Protocol):

    provider_name: str

    def health(
        self,
    ) -> ProviderHealth:
        ...


class RegistrarProvider(Protocol):

    provider_name: str

    def health(
        self,
    ) -> ProviderHealth:
        ...

    def search_domain(
        self,
        domain_name: str,
    ) -> Dict[str, Any]:
        ...

    def register_domain(
        self,
        domain_name: str,
        years: int,
        customer_reference: str,
        idempotency_key: str,
    ) -> Dict[str, Any]:
        ...

    def renew_domain(
        self,
        external_reference: str,
        years: int,
        idempotency_key: str,
    ) -> Dict[str, Any]:
        ...


class DNSProvider(Protocol):

    provider_name: str

    def health(
        self,
    ) -> ProviderHealth:
        ...

    def upsert_record(
        self,
        domain_name: str,
        record_type: str,
        name: str,
        value: str,
        ttl: int,
    ) -> Dict[str, Any]:
        ...


class PaymentProvider(Protocol):

    provider_name: str

    def health(
        self,
    ) -> ProviderHealth:
        ...

    def create_payment(
        self,
        amount_minor: int,
        currency: str,
        idempotency_key: str,
        metadata: Mapping[str, Any],
    ) -> Dict[str, Any]:
        ...


class EmailProvider(Protocol):

    provider_name: str

    def health(
        self,
    ) -> ProviderHealth:
        ...

    def provision_mailbox_service(
        self,
        domain_name: str,
        mailbox_count: int,
        plan_code: str,
        customer_reference: str,
    ) -> Dict[str, Any]:
        ...


class CertificateProvider(Protocol):

    provider_name: str

    def health(
        self,
    ) -> ProviderHealth:
        ...

    def provision_certificate(
        self,
        domain_name: str,
    ) -> Dict[str, Any]:
        ...


# =============================================================================
# DISABLED PROVIDER
# =============================================================================

class UnconfiguredProvider:

    def __init__(
        self,
        provider_type: str,
        provider_name: str = "UNCONFIGURED",
    ) -> None:

        self.provider_type = provider_type
        self.provider_name = provider_name


    def health(
        self,
    ) -> ProviderHealth:

        return ProviderHealth(
            ok=False,
            provider_type=self.provider_type,
            provider_name=self.provider_name,
            state=ProviderState.NOT_CONFIGURED,
            checked_at=utc_now(),
            details={
                "reason": (
                    "No real external adapter is configured."
                )
            },
        )


# =============================================================================
# PROVIDER REGISTRY
# =============================================================================

class ProviderRegistry:

    def __init__(
        self,
        database: Database,
    ) -> None:

        self.database = database

        self._providers: Dict[
            str,
            Any,
        ] = {}


    def register(
        self,
        provider_type: str,
        provider: Any,
    ) -> None:

        self._providers[
            provider_type
        ] = provider


    def get(
        self,
        provider_type: str,
    ) -> Any:

        provider = self._providers.get(
            provider_type
        )

        if provider is None:

            return UnconfiguredProvider(
                provider_type
            )

        return provider


    def verify(
        self,
        provider_type: str,
    ) -> ProviderHealth:

        provider = self.get(
            provider_type
        )

        try:

            health = provider.health()

        except Exception as exc:

            health = ProviderHealth(
                ok=False,
                provider_type=provider_type,
                provider_name=getattr(
                    provider,
                    "provider_name",
                    "UNKNOWN",
                ),
                state=ProviderState.FAILED,
                checked_at=utc_now(),
                details={
                    "error": repr(exc)
                },
            )

        with self.database.transaction() as connection:

            connection.execute(
                """
                INSERT INTO provider_health (
                    provider_type,
                    provider_name,
                    state,
                    checked_at,
                    details_json
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(provider_type, provider_name)
                DO UPDATE SET
                    state = excluded.state,
                    checked_at = excluded.checked_at,
                    details_json = excluded.details_json
                """,
                (
                    provider_type,
                    health.provider_name,
                    health.state.value,
                    health.checked_at,
                    json_dumps(
                        health.details
                    ),
                ),
            )

        return health


    def require_live(
        self,
        provider_type: str,
    ) -> Any:

        provider = self.get(
            provider_type
        )

        health = self.verify(
            provider_type
        )

        if (
            not health.ok
            or health.state != ProviderState.LIVE
        ):

            raise ProviderUnavailableError(
                (
                    f"{provider_type} provider "
                    f"is not verified LIVE."
                )
            )

        return provider


    def health_all(
        self,
    ) -> Dict[str, Any]:

        result: Dict[
            str,
            Any,
        ] = {}

        for provider_type in (
            "registrar",
            "dns",
            "payment",
            "email",
            "certificate",
            "notification",
        ):

            health = self.verify(
                provider_type
            )

            result[
                provider_type
            ] = dataclasses.asdict(
                health
            )

            result[
                provider_type
            ][
                "state"
            ] = health.state.value

        return result


# =============================================================================
# DOMAIN SERVICE
# =============================================================================

class DomainService:

    def __init__(
        self,
        database: Database,
        providers: ProviderRegistry,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.providers = providers
        self.audit = audit


    def search(
        self,
        domain_name: str,
    ) -> Dict[str, Any]:

        domain_name = normalize_domain(
            domain_name
        )

        if "." not in domain_name:

            raise ValidationError(
                "Invalid domain name."
            )

        registrar = self.providers.require_live(
            "registrar"
        )

        result = registrar.search_domain(
            domain_name
        )

        return {
            "domain": domain_name,
            "provider": registrar.provider_name,
            "result": result,
            "verified_external_provider": True,
        }


    def create_local_record(
        self,
        user_id: str,
        domain_name: str,
        *,
        registrar_provider: Optional[str] = None,
        registrar_reference: Optional[str] = None,
        status: DomainStatus = DomainStatus.PENDING,
        expires_at: Optional[str] = None,
    ) -> Dict[str, Any]:

        domain_name = normalize_domain(
            domain_name
        )

        domain_id = new_id(
            "dom"
        )

        now = utc_now()

        try:

            with self.database.transaction() as connection:

                connection.execute(
                    """
                    INSERT INTO domains (
                        id,
                        user_id,
                        domain_name,
                        registrar_provider,
                        registrar_reference,
                        status,
                        expires_at,
                        created_at,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        domain_id,
                        user_id,
                        domain_name,
                        registrar_provider,
                        registrar_reference,
                        status.value,
                        expires_at,
                        now,
                        now,
                    ),
                )

        except sqlite3.IntegrityError as exc:

            raise ConflictError(
                "Domain already exists in platform."
            ) from exc

        self.audit.record(
            "DOMAIN_RECORD_CREATED",
            actor_id=user_id,
            actor_role=UserRole.CUSTOMER.value,
            resource_type="DOMAIN",
            resource_id=domain_id,
            details={
                "domain": domain_name,
                "status": status.value,
            },
        )

        return self.get(
            domain_id
        )


    def get(
        self,
        domain_id: str,
    ) -> Dict[str, Any]:

        row = self.database.fetch_one(
            """
            SELECT *
            FROM domains
            WHERE id = ?
            """,
            (
                domain_id,
            ),
        )

        if not row:
            raise NotFoundError(
                "Domain not found."
            )

        return row


    def list_for_user(
        self,
        actor: Actor,
        user_id: str,
    ) -> List[Dict[str, Any]]:

        AuthorityService.require_self_or_owner(
            actor,
            user_id,
        )

        return self.database.fetch_all(
            """
            SELECT *
            FROM domains
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (
                user_id,
            ),
        )


# =============================================================================
# DNS SERVICE
# =============================================================================

class DNSService:

    ALLOWED_TYPES = {
        "A",
        "AAAA",
        "CNAME",
        "MX",
        "TXT",
        "SRV",
        "CAA",
        "NS",
    }


    def __init__(
        self,
        database: Database,
        providers: ProviderRegistry,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.providers = providers
        self.audit = audit


    def upsert(
        self,
        actor: Actor,
        domain_id: str,
        record_type: str,
        record_name: str,
        record_value: str,
        *,
        ttl: int = 300,
    ) -> Dict[str, Any]:

        domain = self.database.fetch_one(
            """
            SELECT *
            FROM domains
            WHERE id = ?
            """,
            (
                domain_id,
            ),
        )

        if not domain:
            raise NotFoundError(
                "Domain not found."
            )

        AuthorityService.require_self_or_owner(
            actor,
            domain["user_id"],
        )

        record_type = record_type.upper()

        if record_type not in self.ALLOWED_TYPES:
            raise ValidationError(
                "Unsupported DNS record type."
            )

        ttl = max(
            60,
            min(
                int(ttl),
                86400,
            ),
        )

        provider = self.providers.require_live(
            "dns"
        )

        external = provider.upsert_record(
            domain["domain_name"],
            record_type,
            record_name,
            record_value,
            ttl,
        )

        record_id = new_id(
            "dns"
        )

        now = utc_now()

        with self.database.transaction() as connection:

            connection.execute(
                """
                INSERT INTO dns_records (
                    id,
                    domain_id,
                    record_type,
                    record_name,
                    record_value,
                    ttl,
                    provider_reference,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    domain_id,
                    record_type,
                    record_name,
                    record_value,
                    ttl,
                    external.get(
                        "reference"
                    ),
                    now,
                    now,
                ),
            )

        self.audit.record(
            "DNS_RECORD_UPSERTED",
            actor_id=actor.id,
            actor_role=actor.role.value,
            resource_type="DNS_RECORD",
            resource_id=record_id,
            details={
                "domain_id": domain_id,
                "type": record_type,
            },
        )

        return {
            "id": record_id,
            "domain_id": domain_id,
            "provider": provider.provider_name,
            "external": external,
        }


# =============================================================================
# SSL SERVICE
# =============================================================================

class SSLService:

    def __init__(
        self,
        database: Database,
        providers: ProviderRegistry,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.providers = providers
        self.audit = audit


    def provision(
        self,
        actor: Actor,
        domain_id: str,
    ) -> Dict[str, Any]:

        domain = self.database.fetch_one(
            """
            SELECT *
            FROM domains
            WHERE id = ?
            """,
            (
                domain_id,
            ),
        )

        if not domain:
            raise NotFoundError(
                "Domain not found."
            )

        AuthorityService.require_self_or_owner(
            actor,
            domain["user_id"],
        )

        provider = self.providers.require_live(
            "certificate"
        )

        external = provider.provision_certificate(
            domain["domain_name"]
        )

        certificate_id = new_id(
            "ssl"
        )

        now = utc_now()

        with self.database.transaction() as connection:

            connection.execute(
                """
                INSERT INTO ssl_certificates (
                    id,
                    domain_id,
                    provider,
                    status,
                    issued_at,
                    expires_at,
                    provider_reference,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    certificate_id,
                    domain_id,
                    provider.provider_name,
                    SSLStatus.ACTIVE.value,
                    external.get(
                        "issued_at"
                    ),
                    external.get(
                        "expires_at"
                    ),
                    external.get(
                        "reference"
                    ),
                    now,
                    now,
                ),
            )

        self.audit.record(
            "SSL_PROVISIONED",
            actor_id=actor.id,
            actor_role=actor.role.value,
            resource_type="SSL",
            resource_id=certificate_id,
            details={
                "domain_id": domain_id
            },
        )

        return {
            "id": certificate_id,
            "provider": provider.provider_name,
            "external": external,
        }


# =============================================================================
# PRODUCT / PRICING SERVICE
# =============================================================================

class ProductService:

    def __init__(
        self,
        database: Database,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.audit = audit


    def create_product(
        self,
        actor: Actor,
        *,
        code: str,
        name: str,
        category: str,
        price_minor: int,
        currency: str = "SAR",
        recurring_interval: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:

        AuthorityService.require_owner(
            actor
        )

        if price_minor < 0:
            raise ValidationError(
                "Price cannot be negative."
            )

        product_id = new_id(
            "prd"
        )

        now = utc_now()

        try:

            with self.database.transaction() as connection:

                connection.execute(
                    """
                    INSERT INTO products (
                        id,
                        code,
                        name,
                        category,
                        currency,
                        price_minor,
                        recurring_interval,
                        active,
                        metadata_json,
                        created_at,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
                    """,
                    (
                        product_id,
                        code,
                        name,
                        category,
                        currency.upper(),
                        int(price_minor),
                        recurring_interval,
                        json_dumps(
                            dict(metadata or {})
                        ),
                        now,
                        now,
                    ),
                )

        except sqlite3.IntegrityError as exc:

            raise ConflictError(
                "Product code already exists."
            ) from exc

        self.audit.record(
            "PRODUCT_CREATED",
            actor_id=actor.id,
            actor_role=actor.role.value,
            resource_type="PRODUCT",
            resource_id=product_id,
            details={
                "code": code
            },
        )

        return self.get_product(
            product_id
        )


    def get_product(
        self,
        product_id: str,
    ) -> Dict[str, Any]:

        row = self.database.fetch_one(
            """
            SELECT *
            FROM products
            WHERE id = ?
            """,
            (
                product_id,
            ),
        )

        if not row:
            raise NotFoundError(
                "Product not found."
            )

        row["metadata"] = json_loads_safe(
            row.pop(
                "metadata_json"
            ),
            {},
        )

        return row


    def list_active(
        self,
    ) -> List[Dict[str, Any]]:

        rows = self.database.fetch_all(
            """
            SELECT *
            FROM products
            WHERE active = 1
            ORDER BY category, price_minor
            """
        )

        for row in rows:

            row["metadata"] = json_loads_safe(
                row.pop(
                    "metadata_json"
                ),
                {},
            )

        return rows


# =============================================================================
# SUBSCRIPTIONS
# =============================================================================

class SubscriptionService:

    def __init__(
        self,
        database: Database,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.audit = audit


    def create(
        self,
        user_id: str,
        product_id: str,
    ) -> Dict[str, Any]:

        product = self.database.fetch_one(
            """
            SELECT *
            FROM products
            WHERE id = ?
              AND active = 1
            """,
            (
                product_id,
            ),
        )

        if not product:
            raise NotFoundError(
                "Active product not found."
            )

        subscription_id = new_id(
            "sub"
        )

        now = utc_now()

        with self.database.transaction() as connection:

            connection.execute(
                """
                INSERT INTO subscriptions (
                    id,
                    user_id,
                    product_id,
                    status,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    subscription_id,
                    user_id,
                    product_id,
                    SubscriptionStatus.PENDING.value,
                    now,
                    now,
                ),
            )

        self.audit.record(
            "SUBSCRIPTION_CREATED",
            actor_id=user_id,
            actor_role=UserRole.CUSTOMER.value,
            resource_type="SUBSCRIPTION",
            resource_id=subscription_id,
        )

        return self.get(
            subscription_id
        )


    def get(
        self,
        subscription_id: str,
    ) -> Dict[str, Any]:

        row = self.database.fetch_one(
            """
            SELECT *
            FROM subscriptions
            WHERE id = ?
            """,
            (
                subscription_id,
            ),
        )

        if not row:
            raise NotFoundError(
                "Subscription not found."
            )

        return row


# =============================================================================
# INVOICES
# =============================================================================

class InvoiceService:

    def __init__(
        self,
        database: Database,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.audit = audit


    def create(
        self,
        user_id: str,
        items: Iterable[Mapping[str, Any]],
        *,
        subscription_id: Optional[str] = None,
        currency: str = "SAR",
        tax_rate: float = 0.0,
    ) -> Dict[str, Any]:

        normalized_items: List[
            Dict[str, Any]
        ] = []

        subtotal = 0

        for item in items:

            quantity = max(
                1,
                int(
                    item.get(
                        "quantity",
                        1,
                    )
                ),
            )

            unit_price = int(
                item.get(
                    "unit_price_minor",
                    0,
                )
            )

            if unit_price < 0:
                raise ValidationError(
                    "Negative invoice price is invalid."
                )

            total = quantity * unit_price

            subtotal += total

            normalized_items.append(
                {
                    "description": str(
                        item.get(
                            "description",
                            "Service",
                        )
                    ),
                    "quantity": quantity,
                    "unit_price_minor": unit_price,
                    "total_minor": total,
                    "metadata": dict(
                        item.get(
                            "metadata",
                            {},
                        )
                    ),
                }
            )

        if not normalized_items:
            raise ValidationError(
                "Invoice requires at least one item."
            )

        tax = max(
            0,
            int(
                round(
                    subtotal
                    * max(
                        0.0,
                        float(tax_rate),
                    )
                )
            ),
        )

        total = subtotal + tax

        invoice_id = new_id(
            "inv"
        )

        now = utc_now()

        with self.database.transaction() as connection:

            connection.execute(
                """
                INSERT INTO invoices (
                    id,
                    user_id,
                    subscription_id,
                    currency,
                    subtotal_minor,
                    tax_minor,
                    total_minor,
                    status,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    invoice_id,
                    user_id,
                    subscription_id,
                    currency.upper(),
                    subtotal,
                    tax,
                    total,
                    InvoiceStatus.OPEN.value,
                    now,
                    now,
                ),
            )

            for item in normalized_items:

                connection.execute(
                    """
                    INSERT INTO invoice_items (
                        id,
                        invoice_id,
                        description,
                        quantity,
                        unit_price_minor,
                        total_minor,
                        metadata_json
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        new_id(
                            "itm"
                        ),
                        invoice_id,
                        item["description"],
                        item["quantity"],
                        item["unit_price_minor"],
                        item["total_minor"],
                        json_dumps(
                            item["metadata"]
                        ),
                    ),
                )

        self.audit.record(
            "INVOICE_CREATED",
            actor_id=user_id,
            actor_role=UserRole.CUSTOMER.value,
            resource_type="INVOICE",
            resource_id=invoice_id,
            details={
                "total_minor": total,
                "currency": currency.upper(),
            },
        )

        return self.get(
            invoice_id
        )


    def get(
        self,
        invoice_id: str,
    ) -> Dict[str, Any]:

        invoice = self.database.fetch_one(
            """
            SELECT *
            FROM invoices
            WHERE id = ?
            """,
            (
                invoice_id,
            ),
        )

        if not invoice:
            raise NotFoundError(
                "Invoice not found."
            )

        invoice["items"] = self.database.fetch_all(
            """
            SELECT *
            FROM invoice_items
            WHERE invoice_id = ?
            """,
            (
                invoice_id,
            ),
        )

        return invoice


# =============================================================================
# PAYMENTS
# =============================================================================

class PaymentService:

    def __init__(
        self,
        database: Database,
        providers: ProviderRegistry,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.providers = providers
        self.audit = audit


    def create_for_invoice(
        self,
        actor: Actor,
        invoice_id: str,
        *,
        idempotency_key: str,
    ) -> Dict[str, Any]:

        if not idempotency_key.strip():
            raise ValidationError(
                "Idempotency key is required."
            )

        existing = self.database.fetch_one(
            """
            SELECT *
            FROM payments
            WHERE idempotency_key = ?
            """,
            (
                idempotency_key,
            ),
        )

        if existing:
            return existing

        invoice = self.database.fetch_one(
            """
            SELECT *
            FROM invoices
            WHERE id = ?
            """,
            (
                invoice_id,
            ),
        )

        if not invoice:
            raise NotFoundError(
                "Invoice not found."
            )

        AuthorityService.require_self_or_owner(
            actor,
            invoice["user_id"],
        )

        if invoice["status"] == InvoiceStatus.PAID.value:
            raise ConflictError(
                "Invoice is already paid."
            )

        provider = self.providers.require_live(
            "payment"
        )

        payment_id = new_id(
            "pay"
        )

        now = utc_now()

        with self.database.transaction() as connection:

            connection.execute(
                """
                INSERT INTO payments (
                    id,
                    user_id,
                    invoice_id,
                    provider,
                    idempotency_key,
                    amount_minor,
                    currency,
                    status,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payment_id,
                    invoice["user_id"],
                    invoice_id,
                    provider.provider_name,
                    idempotency_key,
                    invoice["total_minor"],
                    invoice["currency"],
                    PaymentStatus.CREATED.value,
                    now,
                    now,
                ),
            )

        try:

            external = provider.create_payment(
                invoice["total_minor"],
                invoice["currency"],
                idempotency_key,
                {
                    "payment_id": payment_id,
                    "invoice_id": invoice_id,
                    "user_id": invoice["user_id"],
                },
            )

        except Exception as exc:

            with self.database.transaction() as connection:

                connection.execute(
                    """
                    UPDATE payments
                    SET
                        status = ?,
                        failure_reason = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        PaymentStatus.FAILED.value,
                        repr(exc),
                        utc_now(),
                        payment_id,
                    ),
                )

            self.audit.record(
                "PAYMENT_FAILED",
                actor_id=actor.id,
                actor_role=actor.role.value,
                resource_type="PAYMENT",
                resource_id=payment_id,
                status="FAILED",
                details={
                    "error": repr(exc)
                },
            )

            raise PaymentError(
                "Payment provider request failed."
            ) from exc

        external_status = str(
            external.get(
                "status",
                "PENDING",
            )
        ).upper()

        if external_status in {
            "SUCCEEDED",
            "PAID",
            "SUCCESS",
        }:
            local_status = PaymentStatus.SUCCEEDED
        else:
            local_status = PaymentStatus.PENDING

        with self.database.transaction() as connection:

            connection.execute(
                """
                UPDATE payments
                SET
                    status = ?,
                    external_reference = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    local_status.value,
                    external.get(
                        "reference"
                    ),
                    utc_now(),
                    payment_id,
                ),
            )

            if local_status == PaymentStatus.SUCCEEDED:

                connection.execute(
                    """
                    UPDATE invoices
                    SET
                        status = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        InvoiceStatus.PAID.value,
                        utc_now(),
                        invoice_id,
                    ),
                )

        self.audit.record(
            "PAYMENT_CREATED",
            actor_id=actor.id,
            actor_role=actor.role.value,
            resource_type="PAYMENT",
            resource_id=payment_id,
            details={
                "provider": provider.provider_name,
                "status": local_status.value,
            },
        )

        result = self.database.fetch_one(
            """
            SELECT *
            FROM payments
            WHERE id = ?
            """,
            (
                payment_id,
            ),
        )

        if result is None:
            raise MajdDmailError(
                "Payment disappeared after creation."
            )

        return result


# =============================================================================
# PROFESSIONAL PAID EMAIL
# =============================================================================

class ProfessionalEmailService:

    def __init__(
        self,
        database: Database,
        providers: ProviderRegistry,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.providers = providers
        self.audit = audit


    def provision(
        self,
        actor: Actor,
        domain_id: str,
        *,
        plan_code: str,
        mailbox_count: int = 1,
    ) -> Dict[str, Any]:

        domain = self.database.fetch_one(
            """
            SELECT *
            FROM domains
            WHERE id = ?
            """,
            (
                domain_id,
            ),
        )

        if not domain:
            raise NotFoundError(
                "Domain not found."
            )

        AuthorityService.require_self_or_owner(
            actor,
            domain["user_id"],
        )

        mailbox_count = max(
            1,
            int(
                mailbox_count
            ),
        )

        provider = self.providers.require_live(
            "email"
        )

        external = provider.provision_mailbox_service(
            domain["domain_name"],
            mailbox_count,
            plan_code,
            domain["user_id"],
        )

        service_id = new_id(
            "mail"
        )

        now = utc_now()

        with self.database.transaction() as connection:

            connection.execute(
                """
                INSERT INTO email_services (
                    id,
                    user_id,
                    domain_id,
                    provider,
                    plan_code,
                    mailbox_count,
                    status,
                    provider_reference,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    service_id,
                    domain["user_id"],
                    domain_id,
                    provider.provider_name,
                    plan_code,
                    mailbox_count,
                    EmailServiceStatus.ACTIVE.value,
                    external.get(
                        "reference"
                    ),
                    now,
                    now,
                ),
            )

        self.audit.record(
            "PROFESSIONAL_EMAIL_PROVISIONED",
            actor_id=actor.id,
            actor_role=actor.role.value,
            resource_type="EMAIL_SERVICE",
            resource_id=service_id,
            details={
                "domain_id": domain_id,
                "mailbox_count": mailbox_count,
                "plan_code": plan_code,
            },
        )

        return {
            "id": service_id,
            "provider": provider.provider_name,
            "status": EmailServiceStatus.ACTIVE.value,
            "external": external,
        }


# =============================================================================
# NOTIFICATIONS
# =============================================================================

class NotificationService:

    def __init__(
        self,
        database: Database,
        providers: ProviderRegistry,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.providers = providers
        self.audit = audit


    def queue(
        self,
        *,
        channel: str,
        body: str,
        user_id: Optional[str] = None,
        subject: Optional[str] = None,
        destination_masked: Optional[str] = None,
    ) -> Dict[str, Any]:

        notification_id = new_id(
            "ntf"
        )

        now = utc_now()

        with self.database.transaction() as connection:

            connection.execute(
                """
                INSERT INTO notifications (
                    id,
                    user_id,
                    channel,
                    destination_masked,
                    subject,
                    body,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    notification_id,
                    user_id,
                    channel,
                    destination_masked,
                    subject,
                    body,
                    "QUEUED",
                    now,
                ),
            )

        return {
            "id": notification_id,
            "status": "QUEUED",
        }


# =============================================================================
# OWNER SERVICE
# =============================================================================

class OwnerService:

    def __init__(
        self,
        database: Database,
        providers: ProviderRegistry,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.providers = providers
        self.audit = audit


    def overview(
        self,
        actor: Actor,
    ) -> Dict[str, Any]:

        AuthorityService.require_owner(
            actor
        )

        counters: Dict[str, int] = {}

        for name, table in (
            ("users", "users"),
            ("domains", "domains"),
            ("subscriptions", "subscriptions"),
            ("invoices", "invoices"),
            ("payments", "payments"),
            ("email_services", "email_services"),
        ):

            row = self.database.fetch_one(
                f"SELECT COUNT(*) AS count FROM {table}"
            )

            counters[name] = int(
                row["count"]
                if row
                else 0
            )

        return {
            "timestamp": utc_now(),
            "authority": OWNER_AUTHORITY,
            "counters": counters,
            "providers": self.providers.health_all(),
        }


# =============================================================================
# CORE PLATFORM
# =============================================================================

class MajdDmailCorePlatform:

    def __init__(
        self,
        database_path: Path = DATABASE_FILE,
    ) -> None:

        self.started_at = utc_now()

        self.database = Database(
            database_path
        )

        self.database.initialize()

        self.audit = AuditService(
            self.database
        )

        self.providers = ProviderRegistry(
            self.database
        )

        self.users = UserService(
            self.database,
            self.audit,
        )

        self.domains = DomainService(
            self.database,
            self.providers,
            self.audit,
        )

        self.dns = DNSService(
            self.database,
            self.providers,
            self.audit,
        )

        self.ssl = SSLService(
            self.database,
            self.providers,
            self.audit,
        )

        self.products = ProductService(
            self.database,
            self.audit,
        )

        self.subscriptions = SubscriptionService(
            self.database,
            self.audit,
        )

        self.invoices = InvoiceService(
            self.database,
            self.audit,
        )

        self.payments = PaymentService(
            self.database,
            self.providers,
            self.audit,
        )

        self.professional_email = ProfessionalEmailService(
            self.database,
            self.providers,
            self.audit,
        )

        self.notifications = NotificationService(
            self.database,
            self.providers,
            self.audit,
        )

        self.owner = OwnerService(
            self.database,
            self.providers,
            self.audit,
        )


    def bootstrap(
        self,
    ) -> Dict[str, Any]:

        state = {
            "project": PROJECT_NAME,
            "version": VERSION,
            "file": THIS_FILENAME,
            "owner_authority": OWNER_AUTHORITY,
            "started_at": self.started_at,
            "database": str(
                self.database.path
            ),
            "primary_file_limit": MAX_PRIMARY_FILES,
            "next_ai_files": [
                "03",
                "04",
                "05",
            ],
            "external_services": (
                "REQUIRE_REAL_VERIFICATION"
            ),
        }

        atomic_write_json(
            CORE_STATE_FILE,
            state,
        )

        self.audit.record(
            "CORE_BOOTSTRAPPED",
            actor_role=OWNER_AUTHORITY,
            resource_type="SYSTEM",
            resource_id=PROJECT_NAME,
            details={
                "version": VERSION
            },
        )

        return state


    def health(
        self,
        *,
        verify_external: bool = False,
    ) -> Dict[str, Any]:

        database_ok = False
        database_error: Optional[str] = None

        try:

            row = self.database.fetch_one(
                "SELECT 1 AS ok"
            )

            database_ok = bool(
                row
                and row.get(
                    "ok"
                ) == 1
            )

        except Exception as exc:

            database_error = repr(
                exc
            )

        mastermind_exists = (
            ROOT
            / MASTERMIND_FILENAME
        ).exists()

        external: Dict[
            str,
            Any,
        ]

        if verify_external:

            external = self.providers.health_all()

        else:

            external = {
                "status": (
                    "NOT_CHECKED"
                ),
                "note": (
                    "Use --external to perform "
                    "real provider health checks."
                ),
            }

        core_ok = (
            database_ok
            and mastermind_exists
        )

        return {
            "ok": core_ok,
            "project": PROJECT_NAME,
            "file": THIS_FILENAME,
            "version": VERSION,
            "owner_authority": OWNER_AUTHORITY,
            "started_at": self.started_at,
            "database": {
                "ok": database_ok,
                "path": str(
                    self.database.path
                ),
                "error": database_error,
            },
            "mastermind_file": {
                "exists": mastermind_exists,
                "filename": MASTERMIND_FILENAME,
            },
            "primary_file_limit": MAX_PRIMARY_FILES,
            "external_services": external,
        }


    def seed_owner_from_environment(
        self,
    ) -> Dict[str, Any]:

        email = os.getenv(
            "MAJD_OWNER_EMAIL",
            "",
        ).strip()

        password = os.getenv(
            "MAJD_OWNER_PASSWORD",
            "",
        )

        if not email or not password:

            return {
                "ok": False,
                "created": False,
                "reason": (
                    "MAJD_OWNER_EMAIL and "
                    "MAJD_OWNER_PASSWORD are required."
                ),
            }

        existing = self.database.fetch_one(
            """
            SELECT
                id,
                email,
                role,
                status
            FROM users
            WHERE email = ?
            """,
            (
                normalize_email(
                    email
                ),
            ),
        )

        if existing:

            if existing["role"] != UserRole.SUPREME_OWNER.value:

                raise ConflictError(
                    "Configured owner email belongs to a non-owner account."
                )

            return {
                "ok": True,
                "created": False,
                "owner": existing,
            }

        owner = self.users.create_user(
            email,
            password,
            display_name="MAJD SUPREME OWNER",
            role=UserRole.SUPREME_OWNER,
        )

        return {
            "ok": True,
            "created": True,
            "owner": owner,
        }


# =============================================================================
# COMMAND LINE
# =============================================================================

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


def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog=THIS_FILENAME,
        description=(
            "MAJD-DMAIL permanent core platform."
        ),
    )

    subcommands = parser.add_subparsers(
        dest="command"
    )

    subcommands.add_parser(
        "bootstrap"
    )

    health_parser = subcommands.add_parser(
        "health"
    )

    health_parser.add_argument(
        "--external",
        action="store_true",
        help=(
            "Perform real configured external provider checks."
        ),
    )

    subcommands.add_parser(
        "seed-owner"
    )

    subcommands.add_parser(
        "providers"
    )

    return parser


def main() -> int:

    parser = build_parser()

    args = parser.parse_args()

    command = (
        args.command
        or "health"
    )

    try:

        platform = MajdDmailCorePlatform()

        if command == "bootstrap":

            print_json(
                platform.bootstrap()
            )

            return 0

        if command == "health":

            result = platform.health(
                verify_external=bool(
                    getattr(
                        args,
                        "external",
                        False,
                    )
                )
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

        if command == "seed-owner":

            result = platform.seed_owner_from_environment()

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

        if command == "providers":

            print_json(
                platform.providers.health_all()
            )

            return 0

        parser.print_help()

        return 2

    except MajdDmailError as exc:

        logger.error(
            "MAJD-DMAIL error: %s",
            exc,
        )

        print_json(
            {
                "ok": False,
                "error_type": (
                    exc.__class__.__name__
                ),
                "error": str(
                    exc
                ),
            }
        )

        return 1

    except Exception as exc:

        logger.exception(
            "Unhandled MAJD-DMAIL core failure."
        )

        print_json(
            {
                "ok": False,
                "error_type": (
                    exc.__class__.__name__
                ),
                "error": repr(
                    exc
                ),
            }
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())
