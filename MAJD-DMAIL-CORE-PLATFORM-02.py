#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
MAJD-DMAIL
MAJD-DMAIL-CORE-PLATFORM-02.py
===============================================================================

FILE 02
PERMANENT MAJD-DMAIL CORE PLATFORM

VERSION 2.0.0

ARCHITECTURE
============

01 - MAJD-DMAIL-AI-AUTOMATION-MASTERMIND-01.py
     AI / automation / planning / verification / repair / orchestration.

02 - MAJD-DMAIL-CORE-PLATFORM-02.py
     Permanent trusted platform core.
     THIS FILE.

03 - Domain infrastructure.
04 - AI generated application/API layer.
05 - AI generated runtime/integration layer.

NO PRIMARY FILE 06 OR HIGHER.

IMPORTANT DATABASE RULE
=======================

File 03 already owns its domain-infrastructure runtime database.

File 02 MUST NOT reuse File 03's incompatible SQLite schema.

Therefore this permanent core uses:

    data/majd-dmail-core.sqlite3

This prevents destructive schema collisions with File 03 while allowing
File 04/05 to bridge both systems safely.

MISSION
=======

Trusted persistent foundation for:

- Customer accounts
- SUPREME_OWNER authority
- Email ownership verification
- Password reset
- Secure sessions
- Logout / session revocation
- User settings
- Domain ownership references
- DNS metadata
- SSL metadata
- Professional paid email services
- Mailboxes
- Products / pricing
- Subscriptions
- Invoices
- Payments
- Provider verification
- Notifications
- Audit
- Runtime health
- AI / automation contracts

SECURITY RULES
==============

- SUPREME_OWNER is highest authority.
- Customer accounts begin PENDING.
- Customer account becomes ACTIVE only after email verification.
- Owner seed account may be created ACTIVE.
- Passwords are never stored as plaintext.
- Verification/reset codes are never stored as plaintext.
- Session tokens are never stored as plaintext.
- External providers are NEVER treated as LIVE without real verification.
- Payment operations are idempotent.
- Sensitive operations are auditable.
- No external success is fabricated.
- No secrets are hard-coded.
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
import re
import secrets
import sqlite3
import tempfile
import threading
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
)


# =============================================================================
# IDENTITY
# =============================================================================

PROJECT_NAME = "MAJD-DMAIL"
FILE_ID = "02"
VERSION = "2.0.0"

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

# IMPORTANT:
# Separate from File 03 database to avoid incompatible schema collisions.
DATABASE_FILE = DATA_DIR / "majd-dmail-core.sqlite3"

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
# HELPERS
# =============================================================================

def utc_dt() -> dt.datetime:
    return dt.datetime.now(
        dt.timezone.utc
    )


def utc_now() -> str:
    return utc_dt().isoformat()


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

    return str(
        value or ""
    ).strip().lower()


def normalize_domain(
    value: str,
) -> str:

    value = str(
        value or ""
    ).strip().lower()

    value = re.sub(
        r"^https?://",
        "",
        value,
    )

    value = re.sub(
        r"^www\.",
        "",
        value,
    )

    value = value.split(
        "/",
        1,
    )[0]

    return value.rstrip(".")


def valid_email(
    email: str,
) -> bool:

    if len(email) > 254:
        return False

    return bool(
        re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email,
        )
    )


def valid_domain(
    domain: str,
) -> bool:

    if (
        not domain
        or len(domain) > 253
        or "." not in domain
    ):
        return False

    labels = domain.split(".")

    if len(labels) < 2:
        return False

    pattern = re.compile(
        r"^(?!-)[a-z0-9-]{1,63}(?<!-)$",
        re.IGNORECASE,
    )

    return all(
        pattern.fullmatch(label)
        for label in labels
    )


def json_dumps(
    payload: Any,
) -> str:

    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )


def json_loads_safe(
    value: Optional[str],
    default: Any,
) -> Any:

    if not value:
        return default

    try:
        return json.loads(
            value
        )
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
                default=str,
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


def mask_email(
    email: str,
) -> str:

    email = normalize_email(
        email
    )

    if "@" not in email:
        return "***"

    local, domain = email.split(
        "@",
        1,
    )

    if len(local) <= 2:
        local_masked = (
            local[:1] + "*"
        )
    else:
        local_masked = (
            local[:1]
            + ("*" * min(6, len(local) - 2))
            + local[-1:]
        )

    return (
        f"{local_masked}@{domain}"
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
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DISABLED = "DISABLED"


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


class MailboxStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DISABLED = "DISABLED"


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


class VerificationError(MajdDmailError):
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

    password = str(
        password or ""
    )

    if len(password) < 10:
        raise ValidationError(
            "Password must contain at least 10 characters."
        )

    salt = secrets.token_bytes(
        32
    )

    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(
            "utf-8"
        ),
        salt,
        PBKDF2_ITERATIONS,
    )

    return (
        "pbkdf2_sha256$"
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
            password.encode(
                "utf-8"
            ),
            bytes.fromhex(
                salt_hex
            ),
            int(
                iterations
            ),
        )

        return hmac.compare_digest(
            derived.hex(),
            digest_hex,
        )

    except Exception:
        return False


# =============================================================================
# DATABASE SCHEMA
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
    verified_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS email_verifications (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    code_hash TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    consumed_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS password_resets (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    code_hash TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    consumed_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    token_hash TEXT NOT NULL UNIQUE,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    revoked_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS domains (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    domain_name TEXT NOT NULL UNIQUE,
    infrastructure_reference TEXT,
    registrar_provider TEXT,
    registrar_reference TEXT,
    status TEXT NOT NULL,
    registered_at TEXT,
    expires_at TEXT,
    auto_renew INTEGER NOT NULL DEFAULT 0,
    transfer_lock INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
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
    FOREIGN KEY(domain_id) REFERENCES domains(id) ON DELETE CASCADE
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
    FOREIGN KEY(domain_id) REFERENCES domains(id) ON DELETE CASCADE
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
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(domain_id) REFERENCES domains(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mailboxes (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    domain_id TEXT NOT NULL,
    email_service_id TEXT,
    local_part TEXT NOT NULL,
    address TEXT NOT NULL UNIQUE,
    provider TEXT,
    provider_reference TEXT,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(domain_id) REFERENCES domains(id) ON DELETE CASCADE,
    FOREIGN KEY(email_service_id) REFERENCES email_services(id) ON DELETE SET NULL
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
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
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
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
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
    FOREIGN KEY(invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
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
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
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

CREATE INDEX IF NOT EXISTS idx_users_email
ON users(email);

CREATE INDEX IF NOT EXISTS idx_sessions_user
ON sessions(user_id);

CREATE INDEX IF NOT EXISTS idx_email_verifications_user
ON email_verifications(user_id);

CREATE INDEX IF NOT EXISTS idx_password_resets_user
ON password_resets(user_id);

CREATE INDEX IF NOT EXISTS idx_domains_user
ON domains(user_id);

CREATE INDEX IF NOT EXISTS idx_dns_domain
ON dns_records(domain_id);

CREATE INDEX IF NOT EXISTS idx_email_services_user
ON email_services(user_id);

CREATE INDEX IF NOT EXISTS idx_mailboxes_user
ON mailboxes(user_id);

CREATE INDEX IF NOT EXISTS idx_mailboxes_domain
ON mailboxes(domain_id);

CREATE INDEX IF NOT EXISTS idx_subscriptions_user
ON subscriptions(user_id);

CREATE INDEX IF NOT EXISTS idx_invoices_user
ON invoices(user_id);

CREATE INDEX IF NOT EXISTS idx_payments_user
ON payments(user_id);

CREATE INDEX IF NOT EXISTS idx_audit_created
ON audit_events(created_at);
"""


# =============================================================================
# DATABASE
# =============================================================================

class Database:

    def __init__(
        self,
        path: Path = DATABASE_FILE,
    ) -> None:

        self.path = Path(
            path
        )

        self._lock = threading.RLock()


    def connect(
        self,
    ) -> sqlite3.Connection:

        connection = sqlite3.connect(
            str(
                self.path
            ),
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
                tuple(
                    parameters
                ),
            ).fetchone()

            return (
                dict(row)
                if row
                else None
            )

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
                tuple(
                    parameters
                ),
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
        details: Optional[
            Mapping[str, Any]
        ] = None,
    ) -> str:

        event_id = new_id(
            "audit"
        )

        timestamp = utc_now()

        details_dict = dict(
            details or {}
        )

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
                        details_dict
                    ),
                    timestamp,
                ),
            )

        append_jsonl(
            EVENTS_FILE,
            {
                "id": event_id,
                "actor_id": actor_id,
                "actor_role": actor_role,
                "action": action,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "status": status,
                "details": details_dict,
                "created_at": timestamp,
            },
        )

        return event_id


# =============================================================================
# AUTHORITY
# =============================================================================

@dataclasses.dataclass(
    frozen=True
)
class Actor:
    id: str
    role: UserRole


class AuthorityService:

    @staticmethod
    def require_owner(
        actor: Actor,
    ) -> None:

        if (
            actor.role
            != UserRole.SUPREME_OWNER
        ):
            raise AuthorizationError(
                "SUPREME_OWNER authority required."
            )


    @staticmethod
    def require_self_or_owner(
        actor: Actor,
        target_user_id: str,
    ) -> None:

        if (
            actor.role
            == UserRole.SUPREME_OWNER
            or actor.id
            == target_user_id
        ):
            return

        raise AuthorizationError(
            "Access denied."
        )


# =============================================================================
# USER / ACCOUNT / AUTHENTICATION
# =============================================================================

class UserService:

    VERIFICATION_TTL_MINUTES = int(
        os.getenv(
            "MAJD_EMAIL_VERIFICATION_TTL_MINUTES",
            "15",
        )
    )

    RESET_TTL_MINUTES = int(
        os.getenv(
            "MAJD_PASSWORD_RESET_TTL_MINUTES",
            "20",
        )
    )

    MAX_CODE_ATTEMPTS = int(
        os.getenv(
            "MAJD_AUTH_CODE_MAX_ATTEMPTS",
            "7",
        )
    )


    def __init__(
        self,
        database: Database,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.audit = audit


    def _public_user(
        self,
        row: Mapping[str, Any],
    ) -> Dict[str, Any]:

        return {
            "id": row["id"],
            "email": row["email"],
            "role": row["role"],
            "status": row["status"],
            "display_name": row.get(
                "display_name"
            ),
            "verified_at": row.get(
                "verified_at"
            ),
            "created_at": row.get(
                "created_at"
            ),
            "updated_at": row.get(
                "updated_at"
            ),
        }


    def create_user(
        self,
        email: str,
        password: str,
        *,
        display_name: Optional[str] = None,
        role: UserRole = UserRole.CUSTOMER,
        initially_active: bool = False,
    ) -> Dict[str, Any]:

        email = normalize_email(
            email
        )

        if not valid_email(
            email
        ):
            raise ValidationError(
                "Invalid email address."
            )

        display_name = (
            str(
                display_name or ""
            ).strip()
            or None
        )

        user_id = new_id(
            "usr"
        )

        now = utc_now()

        status = (
            UserStatus.ACTIVE
            if initially_active
            else UserStatus.PENDING
        )

        verified_at = (
            now
            if initially_active
            else None
        )

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
                        verified_at,
                        created_at,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        email,
                        hash_password(
                            password
                        ),
                        role.value,
                        status.value,
                        display_name,
                        verified_at,
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
            details={
                "status": status.value,
                "verified": bool(
                    verified_at
                ),
            },
        )

        return self.get_user(
            user_id
        )


    def register_customer(
        self,
        email: str,
        password: str,
        *,
        display_name: Optional[str] = None,
    ) -> Dict[str, Any]:

        user = self.create_user(
            email,
            password,
            display_name=display_name,
            role=UserRole.CUSTOMER,
            initially_active=False,
        )

        verification = self.issue_email_verification(
            user["id"]
        )

        return {
            "user": user,
            "verification": verification,
        }


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
                verified_at,
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


    def get_user_by_email(
        self,
        email: str,
    ) -> Dict[str, Any]:

        email = normalize_email(
            email
        )

        row = self.database.fetch_one(
            """
            SELECT
                id,
                email,
                role,
                status,
                display_name,
                verified_at,
                created_at,
                updated_at
            FROM users
            WHERE email = ?
            """,
            (
                email,
            ),
        )

        if not row:
            raise NotFoundError(
                "User not found."
            )

        return row


    def update_profile(
        self,
        actor: Actor,
        *,
        display_name: str,
    ) -> Dict[str, Any]:

        display_name = str(
            display_name or ""
        ).strip()

        if not display_name:
            raise ValidationError(
                "Display name is required."
            )

        now = utc_now()

        with self.database.transaction() as connection:

            cursor = connection.execute(
                """
                UPDATE users
                SET
                    display_name = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    display_name,
                    now,
                    actor.id,
                ),
            )

            if cursor.rowcount != 1:
                raise NotFoundError(
                    "User not found."
                )

        self.audit.record(
            "USER_PROFILE_UPDATED",
            actor_id=actor.id,
            actor_role=actor.role.value,
            resource_type="USER",
            resource_id=actor.id,
        )

        return self.get_user(
            actor.id
        )


    def issue_email_verification(
        self,
        user_id: str,
    ) -> Dict[str, Any]:

        user = self.get_user(
            user_id
        )

        if (
            user["status"]
            == UserStatus.ACTIVE.value
            and user.get(
                "verified_at"
            )
        ):
            return {
                "required": False,
                "already_verified": True,
                "destination_masked": mask_email(
                    user["email"]
                ),
            }

        code = (
            f"{secrets.randbelow(1000000):06d}"
        )

        code_hash = sha256_text(
            code
        )

        verification_id = new_id(
            "verify"
        )

        now = utc_dt()

        expires = now + dt.timedelta(
            minutes=max(
                1,
                self.VERIFICATION_TTL_MINUTES,
            )
        )

        with self.database.transaction() as connection:

            connection.execute(
                """
                UPDATE email_verifications
                SET consumed_at = ?
                WHERE user_id = ?
                  AND consumed_at IS NULL
                """,
                (
                    now.isoformat(),
                    user_id,
                ),
            )

            connection.execute(
                """
                INSERT INTO email_verifications (
                    id,
                    user_id,
                    code_hash,
                    expires_at,
                    attempts,
                    created_at
                )
                VALUES (?, ?, ?, ?, 0, ?)
                """,
                (
                    verification_id,
                    user_id,
                    code_hash,
                    expires.isoformat(),
                    now.isoformat(),
                ),
            )

        self.audit.record(
            "EMAIL_VERIFICATION_ISSUED",
            actor_id=user_id,
            actor_role=user["role"],
            resource_type="USER",
            resource_id=user_id,
            details={
                "destination": mask_email(
                    user["email"]
                ),
            },
        )

        # Internal delivery payload.
        # File 04/05 must send this through a verified notification provider.
        # The plaintext code is not persisted in SQLite.
        return {
            "required": True,
            "verification_id": verification_id,
            "destination": user["email"],
            "destination_masked": mask_email(
                user["email"]
            ),
            "code": code,
            "expires_at": expires.isoformat(),
        }


    def verify_email(
        self,
        email: str,
        code: str,
    ) -> Dict[str, Any]:

        email = normalize_email(
            email
        )

        code = str(
            code or ""
        ).strip()

        user_row = self.database.fetch_one(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (
                email,
            ),
        )

        if not user_row:
            raise VerificationError(
                "Invalid verification request."
            )

        if (
            user_row["status"]
            == UserStatus.ACTIVE.value
            and user_row["verified_at"]
        ):
            return self._public_user(
                user_row
            )

        record = self.database.fetch_one(
            """
            SELECT *
            FROM email_verifications
            WHERE user_id = ?
              AND consumed_at IS NULL
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (
                user_row["id"],
            ),
        )

        if not record:
            raise VerificationError(
                "Verification code not found."
            )

        expires_at = dt.datetime.fromisoformat(
            record["expires_at"]
        )

        if expires_at <= utc_dt():

            with self.database.transaction() as connection:

                connection.execute(
                    """
                    UPDATE email_verifications
                    SET consumed_at = ?
                    WHERE id = ?
                    """,
                    (
                        utc_now(),
                        record["id"],
                    ),
                )

            raise VerificationError(
                "Verification code expired."
            )

        attempts = int(
            record["attempts"]
        )

        if attempts >= self.MAX_CODE_ATTEMPTS:
            raise VerificationError(
                "Verification attempts exceeded."
            )

        if not hmac.compare_digest(
            sha256_text(
                code
            ),
            record["code_hash"],
        ):

            with self.database.transaction() as connection:

                connection.execute(
                    """
                    UPDATE email_verifications
                    SET attempts = attempts + 1
                    WHERE id = ?
                    """,
                    (
                        record["id"],
                    ),
                )

            raise VerificationError(
                "Invalid verification code."
            )

        now = utc_now()

        with self.database.transaction() as connection:

            connection.execute(
                """
                UPDATE email_verifications
                SET consumed_at = ?
                WHERE id = ?
                """,
                (
                    now,
                    record["id"],
                ),
            )

            connection.execute(
                """
                UPDATE users
                SET
                    status = ?,
                    verified_at = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    UserStatus.ACTIVE.value,
                    now,
                    now,
                    user_row["id"],
                ),
            )

        self.audit.record(
            "EMAIL_VERIFIED",
            actor_id=user_row["id"],
            actor_role=user_row["role"],
            resource_type="USER",
            resource_id=user_row["id"],
        )

        return self.get_user(
            user_row["id"]
        )


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

        if not verify_password(
            password,
            row["password_hash"],
        ):

            raise AuthorizationError(
                "Invalid credentials."
            )

        if (
            row["status"]
            == UserStatus.PENDING.value
        ):

            raise AuthorizationError(
                "Email verification required."
            )

        if (
            row["status"]
            != UserStatus.ACTIVE.value
        ):

            raise AuthorizationError(
                "User is not active."
            )

        if (
            row["role"]
            != UserRole.SUPREME_OWNER.value
            and not row["verified_at"]
        ):

            raise AuthorizationError(
                "Email verification required."
            )

        self.audit.record(
            "USER_AUTHENTICATED",
            actor_id=row["id"],
            actor_role=row["role"],
            resource_type="USER",
            resource_id=row["id"],
        )

        return self._public_user(
            row
        )


    def create_session(
        self,
        user_id: str,
        *,
        ttl_hours: int = 24,
    ) -> str:

        user = self.get_user(
            user_id
        )

        if (
            user["status"]
            != UserStatus.ACTIVE.value
        ):

            raise AuthorizationError(
                "User is not active."
            )

        session_id = new_id(
            "ses"
        )

        token = secrets.token_urlsafe(
            48
        )

        token_hash = sha256_text(
            token
        )

        now = utc_dt()

        expires = now + dt.timedelta(
            hours=max(
                1,
                int(
                    ttl_hours
                ),
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

        self.audit.record(
            "SESSION_CREATED",
            actor_id=user_id,
            actor_role=user["role"],
            resource_type="SESSION",
            resource_id=session_id,
        )

        return token


    def resolve_session(
        self,
        token: str,
    ) -> Optional[Actor]:

        token = str(
            token or ""
        ).strip()

        if not token:
            return None

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

        if (
            row["status"]
            != UserStatus.ACTIVE.value
        ):
            return None

        try:

            expires = dt.datetime.fromisoformat(
                row["expires_at"]
            )

        except ValueError:
            return None

        if expires <= utc_dt():
            return None

        try:

            role = UserRole(
                row["role"]
            )

        except ValueError:
            return None

        return Actor(
            id=row["user_id"],
            role=role,
        )


    def revoke_session(
        self,
        token: str,
    ) -> bool:

        token = str(
            token or ""
        ).strip()

        if not token:
            return False

        token_hash = sha256_text(
            token
        )

        with self.database.transaction() as connection:

            cursor = connection.execute(
                """
                UPDATE sessions
                SET revoked_at = ?
                WHERE token_hash = ?
                  AND revoked_at IS NULL
                """,
                (
                    utc_now(),
                    token_hash,
                ),
            )

        return (
            cursor.rowcount > 0
        )


    def revoke_all_sessions(
        self,
        user_id: str,
    ) -> int:

        with self.database.transaction() as connection:

            cursor = connection.execute(
                """
                UPDATE sessions
                SET revoked_at = ?
                WHERE user_id = ?
                  AND revoked_at IS NULL
                """,
                (
                    utc_now(),
                    user_id,
                ),
            )

        return int(
            cursor.rowcount
        )


    def issue_password_reset(
        self,
        email: str,
    ) -> Dict[str, Any]:

        email = normalize_email(
            email
        )

        user = self.database.fetch_one(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (
                email,
            ),
        )

        # Do not disclose whether account exists.
        if not user:

            return {
                "accepted": True,
                "destination_masked": mask_email(
                    email
                ),
                "delivery_required": False,
            }

        code = (
            f"{secrets.randbelow(1000000):06d}"
        )

        code_hash = sha256_text(
            code
        )

        reset_id = new_id(
            "reset"
        )

        now = utc_dt()

        expires = now + dt.timedelta(
            minutes=max(
                1,
                self.RESET_TTL_MINUTES,
            )
        )

        with self.database.transaction() as connection:

            connection.execute(
                """
                UPDATE password_resets
                SET consumed_at = ?
                WHERE user_id = ?
                  AND consumed_at IS NULL
                """,
                (
                    now.isoformat(),
                    user["id"],
                ),
            )

            connection.execute(
                """
                INSERT INTO password_resets (
                    id,
                    user_id,
                    code_hash,
                    expires_at,
                    attempts,
                    created_at
                )
                VALUES (?, ?, ?, ?, 0, ?)
                """,
                (
                    reset_id,
                    user["id"],
                    code_hash,
                    expires.isoformat(),
                    now.isoformat(),
                ),
            )

        self.audit.record(
            "PASSWORD_RESET_ISSUED",
            actor_id=user["id"],
            actor_role=user["role"],
            resource_type="USER",
            resource_id=user["id"],
        )

        return {
            "accepted": True,
            "reset_id": reset_id,
            "destination": user["email"],
            "destination_masked": mask_email(
                user["email"]
            ),
            "delivery_required": True,
            "code": code,
            "expires_at": expires.isoformat(),
        }


    def reset_password(
        self,
        email: str,
        code: str,
        new_password: str,
    ) -> Dict[str, Any]:

        email = normalize_email(
            email
        )

        user = self.database.fetch_one(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (
                email,
            ),
        )

        if not user:
            raise VerificationError(
                "Invalid reset request."
            )

        record = self.database.fetch_one(
            """
            SELECT *
            FROM password_resets
            WHERE user_id = ?
              AND consumed_at IS NULL
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (
                user["id"],
            ),
        )

        if not record:
            raise VerificationError(
                "Password reset code not found."
            )

        expires = dt.datetime.fromisoformat(
            record["expires_at"]
        )

        if expires <= utc_dt():
            raise VerificationError(
                "Password reset code expired."
            )

        if int(
            record["attempts"]
        ) >= self.MAX_CODE_ATTEMPTS:

            raise VerificationError(
                "Password reset attempts exceeded."
            )

        if not hmac.compare_digest(
            sha256_text(
                str(
                    code or ""
                ).strip()
            ),
            record["code_hash"],
        ):

            with self.database.transaction() as connection:

                connection.execute(
                    """
                    UPDATE password_resets
                    SET attempts = attempts + 1
                    WHERE id = ?
                    """,
                    (
                        record["id"],
                    ),
                )

            raise VerificationError(
                "Invalid password reset code."
            )

        password_hash = hash_password(
            new_password
        )

        now = utc_now()

        with self.database.transaction() as connection:

            connection.execute(
                """
                UPDATE password_resets
                SET consumed_at = ?
                WHERE id = ?
                """,
                (
                    now,
                    record["id"],
                ),
            )

            connection.execute(
                """
                UPDATE users
                SET
                    password_hash = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    password_hash,
                    now,
                    user["id"],
                ),
            )

            connection.execute(
                """
                UPDATE sessions
                SET revoked_at = ?
                WHERE user_id = ?
                  AND revoked_at IS NULL
                """,
                (
                    now,
                    user["id"],
                ),
            )

        self.audit.record(
            "PASSWORD_RESET_COMPLETED",
            actor_id=user["id"],
            actor_role=user["role"],
            resource_type="USER",
            resource_id=user["id"],
        )

        return {
            "ok": True,
            "user_id": user["id"],
        }


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

    def create_mailbox(
        self,
        address: str,
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
# UNCONFIGURED PROVIDER
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
                    "No real verified external adapter is configured."
                )
            },
        )


# =============================================================================
# PROVIDER REGISTRY
# =============================================================================

class ProviderRegistry:

    PROVIDER_TYPES = (
        "registrar",
        "dns",
        "payment",
        "email",
        "certificate",
        "notification",
    )


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

        if (
            provider_type
            not in self.PROVIDER_TYPES
        ):
            raise ValidationError(
                "Unsupported provider type."
            )

        self._providers[
            provider_type
        ] = provider


    def get(
        self,
        provider_type: str,
    ) -> Any:

        return self._providers.get(
            provider_type,
            UnconfiguredProvider(
                provider_type
            ),
        )


    def verify(
        self,
        provider_type: str,
    ) -> ProviderHealth:

        provider = self.get(
            provider_type
        )

        try:

            health = provider.health()

            if not isinstance(
                health,
                ProviderHealth,
            ):
                raise TypeError(
                    "Provider health must return ProviderHealth."
                )

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
                    "error": repr(
                        exc
                    )
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
            or health.state
            != ProviderState.LIVE
        ):

            raise ProviderUnavailableError(
                f"{provider_type} provider is not verified LIVE."
            )

        return provider


    def health_all(
        self,
    ) -> Dict[str, Any]:

        result: Dict[
            str,
            Any,
        ] = {}

        for provider_type in self.PROVIDER_TYPES:

            health = self.verify(
                provider_type
            )

            data = dataclasses.asdict(
                health
            )

            data["state"] = (
                health.state.value
            )

            result[
                provider_type
            ] = data

        return result


# =============================================================================
# DOMAIN ACCOUNT RECORDS
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


    def create_local_record(
        self,
        user_id: str,
        domain_name: str,
        *,
        infrastructure_reference: Optional[str] = None,
        registrar_provider: Optional[str] = None,
        registrar_reference: Optional[str] = None,
        status: DomainStatus = DomainStatus.PENDING,
        expires_at: Optional[str] = None,
    ) -> Dict[str, Any]:

        domain_name = normalize_domain(
            domain_name
        )

        if not valid_domain(
            domain_name
        ):
            raise ValidationError(
                "Invalid domain name."
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
                        infrastructure_reference,
                        registrar_provider,
                        registrar_reference,
                        status,
                        expires_at,
                        created_at,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        domain_id,
                        user_id,
                        domain_name,
                        infrastructure_reference,
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
                "Domain already exists in customer core."
            ) from exc

        self.audit.record(
            "DOMAIN_ACCOUNT_RECORD_CREATED",
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
# PROFESSIONAL EMAIL / MAILBOXES
# =============================================================================

class ProfessionalEmailService:

    LOCAL_PART_PATTERN = re.compile(
        r"^[a-z0-9][a-z0-9._+-]{0,63}$",
        re.IGNORECASE,
    )


    def __init__(
        self,
        database: Database,
        providers: ProviderRegistry,
        audit: AuditService,
    ) -> None:

        self.database = database
        self.providers = providers
        self.audit = audit


    def provision_service(
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

        if not isinstance(
            external,
            Mapping,
        ):
            raise ProviderUnavailableError(
                "Invalid email provider response."
            )

        service_id = new_id(
            "mailservice"
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
            "EMAIL_SERVICE_PROVISIONED",
            actor_id=actor.id,
            actor_role=actor.role.value,
            resource_type="EMAIL_SERVICE",
            resource_id=service_id,
            details={
                "domain_id": domain_id,
                "mailbox_count": mailbox_count,
                "provider": provider.provider_name,
            },
        )

        return self.get_service(
            service_id
        )


    def get_service(
        self,
        service_id: str,
    ) -> Dict[str, Any]:

        row = self.database.fetch_one(
            """
            SELECT *
            FROM email_services
            WHERE id = ?
            """,
            (
                service_id,
            ),
        )

        if not row:
            raise NotFoundError(
                "Email service not found."
            )

        return row


    def create_mailbox(
        self,
        actor: Actor,
        domain_id: str,
        local_part: str,
        *,
        email_service_id: Optional[str] = None,
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

        local_part = str(
            local_part or ""
        ).strip().lower()

        if not self.LOCAL_PART_PATTERN.fullmatch(
            local_part
        ):
            raise ValidationError(
                "Invalid mailbox local part."
            )

        address = (
            f"{local_part}@"
            f"{domain['domain_name']}"
        )

        provider = self.providers.require_live(
            "email"
        )

        external = provider.create_mailbox(
            address,
            domain["user_id"],
        )

        if not isinstance(
            external,
            Mapping,
        ):
            raise ProviderUnavailableError(
                "Invalid mailbox provider response."
            )

        mailbox_id = new_id(
            "mbx"
        )

        now = utc_now()

        try:

            with self.database.transaction() as connection:

                connection.execute(
                    """
                    INSERT INTO mailboxes (
                        id,
                        user_id,
                        domain_id,
                        email_service_id,
                        local_part,
                        address,
                        provider,
                        provider_reference,
                        status,
                        created_at,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        mailbox_id,
                        domain["user_id"],
                        domain_id,
                        email_service_id,
                        local_part,
                        address,
                        provider.provider_name,
                        external.get(
                            "reference"
                        ),
                        MailboxStatus.ACTIVE.value,
                        now,
                        now,
                    ),
                )

        except sqlite3.IntegrityError as exc:

            raise ConflictError(
                "Mailbox already exists."
            ) from exc

        self.audit.record(
            "MAILBOX_CREATED",
            actor_id=actor.id,
            actor_role=actor.role.value,
            resource_type="MAILBOX",
            resource_id=mailbox_id,
            details={
                "address": address,
                "provider": provider.provider_name,
            },
        )

        return self.get_mailbox(
            mailbox_id
        )


    def get_mailbox(
        self,
        mailbox_id: str,
    ) -> Dict[str, Any]:

        row = self.database.fetch_one(
            """
            SELECT *
            FROM mailboxes
            WHERE id = ?
            """,
            (
                mailbox_id,
            ),
        )

        if not row:
            raise NotFoundError(
                "Mailbox not found."
            )

        return row


    def list_mailboxes(
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
            FROM mailboxes
            WHERE user_id = ?
            ORDER BY address
            """,
            (
                user_id,
            ),
        )


# =============================================================================
# PRODUCT / PRICING
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
        metadata: Optional[
            Mapping[str, Any]
        ] = None,
    ) -> Dict[str, Any]:

        AuthorityService.require_owner(
            actor
        )

        code = str(
            code or ""
        ).strip().upper()

        name = str(
            name or ""
        ).strip()

        category = str(
            category or ""
        ).strip().upper()

        if not code:
            raise ValidationError(
                "Product code is required."
            )

        if not name:
            raise ValidationError(
                "Product name is required."
            )

        if int(
            price_minor
        ) < 0:

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
                        int(
                            price_minor
                        ),
                        recurring_interval,
                        json_dumps(
                            dict(
                                metadata or {}
                            )
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
# INVOICE
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
        items: Iterable[
            Mapping[str, Any]
        ],
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

            total = (
                quantity
                * unit_price
            )

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
                        float(
                            tax_rate
                        ),
                    )
                )
            ),
        )

        total = (
            subtotal
            + tax
        )

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
                        item[
                            "description"
                        ],
                        item[
                            "quantity"
                        ],
                        item[
                            "unit_price_minor"
                        ],
                        item[
                            "total_minor"
                        ],
                        json_dumps(
                            item[
                                "metadata"
                            ]
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

        idempotency_key = str(
            idempotency_key or ""
        ).strip()

        if not idempotency_key:
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

        if (
            invoice["status"]
            == InvoiceStatus.PAID.value
        ):
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
                        repr(
                            exc
                        ),
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
                    "error": repr(
                        exc
                    )
                },
            )

            raise PaymentError(
                "Payment provider request failed."
            ) from exc

        if not isinstance(
            external,
            Mapping,
        ):
            raise PaymentError(
                "Invalid payment provider response."
            )

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

            local_status = (
                PaymentStatus.SUCCEEDED
            )

        else:

            local_status = (
                PaymentStatus.PENDING
            )

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

            if (
                local_status
                == PaymentStatus.SUCCEEDED
            ):

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

        if not result:
            raise MajdDmailError(
                "Payment disappeared after creation."
            )

        return result


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

    SAFE_COUNT_TABLES = (
        "users",
        "domains",
        "mailboxes",
        "email_services",
        "subscriptions",
        "invoices",
        "payments",
        "notifications",
    )


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

        counters: Dict[
            str,
            int,
        ] = {}

        for table in self.SAFE_COUNT_TABLES:

            row = self.database.fetch_one(
                f"SELECT COUNT(*) AS count FROM {table}"
            )

            counters[
                table
            ] = int(
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
            "ok": True,
            "project": PROJECT_NAME,
            "file_id": FILE_ID,
            "version": VERSION,
            "file": THIS_FILENAME,
            "owner_authority": OWNER_AUTHORITY,
            "started_at": self.started_at,
            "database": str(
                self.database.path
            ),
            "database_isolated_from_file_03": True,
            "primary_file_limit": MAX_PRIMARY_FILES,
            "next_ai_files": [
                "03",
                "04",
                "05",
            ],
            "customer_account_flow": (
                "PENDING_EMAIL_VERIFICATION_TO_ACTIVE"
            ),
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
                "version": VERSION,
                "database": str(
                    self.database.path
                ),
            },
        )

        return state


    def health(
        self,
        *,
        verify_external: bool = False,
    ) -> Dict[str, Any]:

        database_ok = False
        database_error: Optional[
            str
        ] = None

        schema_ok = False

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

            required_tables = {
                "users",
                "email_verifications",
                "password_resets",
                "sessions",
                "domains",
                "email_services",
                "mailboxes",
                "provider_health",
                "audit_events",
            }

            rows = self.database.fetch_all(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                """
            )

            actual_tables = {
                row["name"]
                for row in rows
            }

            schema_ok = (
                required_tables
                <= actual_tables
            )

        except Exception as exc:

            database_error = repr(
                exc
            )

        mastermind_exists = (
            ROOT
            / MASTERMIND_FILENAME
        ).exists()

        if verify_external:

            external = (
                self.providers.health_all()
            )

        else:

            external = {
                "status": "NOT_CHECKED",
                "note": (
                    "External providers are not assumed LIVE. "
                    "Use --external for real health checks."
                ),
            }

        core_ok = (
            database_ok
            and schema_ok
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
                "schema_ok": schema_ok,
                "path": str(
                    self.database.path
                ),
                "isolated_from_file_03": True,
                "error": database_error,
            },
            "mastermind_file": {
                "exists": mastermind_exists,
                "filename": MASTERMIND_FILENAME,
            },
            "auth": {
                "customer_default_status": (
                    UserStatus.PENDING.value
                ),
                "email_verification": True,
                "password_reset": True,
                "session_revocation": True,
            },
            "mail": {
                "mailbox_records": True,
                "external_mail_provider_required": True,
                "fake_live_status_forbidden": True,
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

        normalized = normalize_email(
            email
        )

        existing = self.database.fetch_one(
            """
            SELECT
                id,
                email,
                role,
                status,
                display_name,
                verified_at,
                created_at,
                updated_at
            FROM users
            WHERE email = ?
            """,
            (
                normalized,
            ),
        )

        if existing:

            if (
                existing["role"]
                != UserRole.SUPREME_OWNER.value
            ):

                raise ConflictError(
                    "Configured owner email belongs to a non-owner account."
                )

            return {
                "ok": True,
                "created": False,
                "owner": existing,
            }

        owner = self.users.create_user(
            normalized,
            password,
            display_name=(
                "MAJD SUPREME OWNER"
            ),
            role=UserRole.SUPREME_OWNER,
            initially_active=True,
        )

        return {
            "ok": True,
            "created": True,
            "owner": owner,
        }


# =============================================================================
# SELF TEST
# =============================================================================

def self_test() -> Dict[str, Any]:

    with tempfile.TemporaryDirectory(
        prefix="majd-dmail-core-test-"
    ) as temp_dir:

        database_path = (
            Path(
                temp_dir
            )
            / "core.sqlite3"
        )

        platform = MajdDmailCorePlatform(
            database_path
        )

        customer = platform.users.create_user(
            "customer@example.com",
            "StrongPassword123!",
            display_name="Customer",
        )

        assert (
            customer["status"]
            == UserStatus.PENDING.value
        )

        issued = platform.users.issue_email_verification(
            customer["id"]
        )

        verified = platform.users.verify_email(
            "customer@example.com",
            issued["code"],
        )

        assert (
            verified["status"]
            == UserStatus.ACTIVE.value
        )

        authenticated = platform.users.authenticate(
            "customer@example.com",
            "StrongPassword123!",
        )

        token = platform.users.create_session(
            authenticated["id"]
        )

        actor = platform.users.resolve_session(
            token
        )

        assert actor is not None
        assert (
            actor.id
            == authenticated["id"]
        )

        revoked = platform.users.revoke_session(
            token
        )

        assert revoked is True

        assert (
            platform.users.resolve_session(
                token
            )
            is None
        )

        reset = platform.users.issue_password_reset(
            "customer@example.com"
        )

        assert (
            reset["delivery_required"]
            is True
        )

        platform.users.reset_password(
            "customer@example.com",
            reset["code"],
            "AnotherStrongPassword456!",
        )

        platform.users.authenticate(
            "customer@example.com",
            "AnotherStrongPassword456!",
        )

        return {
            "ok": True,
            "project": PROJECT_NAME,
            "file": THIS_FILENAME,
            "version": VERSION,
            "tests": {
                "database": True,
                "pending_account": True,
                "email_verification": True,
                "activation": True,
                "authentication": True,
                "session_creation": True,
                "session_resolution": True,
                "logout_revocation": True,
                "password_reset": True,
            },
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

    subcommands.add_parser(
        "self-test"
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

        if command == "self-test":

            result = self_test()

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

            result = (
                platform.seed_owner_from_environment()
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
    raise SystemExit(
        main()
    )
