#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD-DMAIL
MAJD-DMAIL-AI-AUTOMATION-MASTERMIND-01.py

FILE 01: AI + AUTOMATION + MASTERMIND CORE

Rules:
- Owner is the highest authority.
- Files 01 and 02 are manually maintained.
- This file may design/build/repair ONLY primary files 03, 04 and 05.
- No primary file 06 or higher.
- Never hard-code secrets.
- Never report an external service LIVE until a real health check succeeds.
- Generated Python must pass syntax validation before it is written.
- Existing generated files are backed up before replacement.
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


PROJECT_NAME = "MAJD-DMAIL"
VERSION = "1.1.0"
OWNER_AUTHORITY = "SUPREME_OWNER"

THIS_FILENAME = "MAJD-DMAIL-AI-AUTOMATION-MASTERMIND-01.py"
PRIMARY_FILE_02 = "MAJD-DMAIL-CORE-PLATFORM-02.py"

MAX_PRIMARY_FILES = 5

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

for directory in (
    DATA_DIR,
    LOG_DIR,
    STATE_DIR,
    BACKUP_DIR,
    RUNTIME_DIR,
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


logger = logging.getLogger(
    "MAJD_DMAIL_MASTERMIND"
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


DOMAIN_PLATFORM_REQUIREMENTS: Dict[str, Any] = {

    "mission": (
        "Build and operate an AI-driven domain services platform "
        "with automation, verified integrations, security, "
        "billing and self-repair."
    ),

    "capabilities": [

        "domain_search",

        "domain_registration",

        "domain_renewal",

        "domain_transfer",

        "domain_lifecycle",

        "dns_management",

        "ssl_tls",

        "professional_paid_email",

        "customer_accounts",

        "owner_control",

        "pricing",

        "payments",

        "billing",

        "invoices",

        "subscriptions",

        "customer_support",

        "security",

        "audit",

        "monitoring",

        "notifications",

        "self_repair",
    ],

    "rules": [

        "Owner remains highest authority.",

        "No fake success.",

        (
            "Secrets must come from environment "
            "or secure secret storage."
        ),

        "External providers must use adapters.",

        (
            "External services are LIVE only after "
            "real health verification."
        ),

        (
            "Files 01 and 02 must never be "
            "overwritten automatically."
        ),

        (
            "Generated primary files are limited "
            "to 03, 04 and 05."
        ),

        "No primary file 06 or higher.",

        (
            "Financial operations must be "
            "idempotent."
        ),

        (
            "Ownership-sensitive operations require "
            "strong authorization."
        ),

        (
            "Every important action must "
            "be auditable."
        ),

        (
            "Generated code must be verified "
            "before acceptance."
        ),
    ],
}


DEFAULT_GENERATED_ARCHITECTURE: Dict[
    str,
    Dict[str, str],
] = {

    "03": {

        "filename":
            "MAJD-DMAIL-DOMAIN-INFRASTRUCTURE-03.py",

        "purpose": (
            "Registrar adapters, domain availability, "
            "registration, renewal, transfer, DNS, "
            "SSL/TLS and provider health."
        ),
    },

    "04": {

        "filename":
            "MAJD-DMAIL-COMMERCE-SECURITY-04.py",

        "purpose": (
            "Pricing, subscriptions, payments, invoices, "
            "paid email, security, authorization, audit "
            "and financial verification."
        ),
    },

    "05": {

        "filename":
            "MAJD-DMAIL-PLATFORM-RUNTIME-05.py",

        "purpose": (
            "Customer and owner runtime, unified API, "
            "AI support, monitoring, notifications "
            "and final orchestration."
        ),
    },
}


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
    details: Optional[
        Dict[str, Any]
    ] = None,
) -> None:

    payload = {

        "timestamp":
            utc_now(),

        "project":
            PROJECT_NAME,

        "source_file":
            THIS_FILENAME,

        "event_type":
            event_type,

        "status":
            status,

        "details":
            details or {},
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

    result: List[str] = []

    for path in ROOT.glob(
        "MAJD-DMAIL-*.py"
    ):

        if extract_primary_number(
            path.name
        ) is not None:

            result.append(
                path.name
            )

    return sorted(
        result
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
            "AI may generate only primary files 03, 04 and 05."
        )

    return number


def syntax_check_content(
    content: str,
) -> Tuple[
    bool,
    Optional[str],
]:

    try:

        ast.parse(
            content
        )

        return (
            True,
            None,
        )

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

            "ok":
                False,

            "file":
                path.name,

            "error":
                "missing",
        }

    try:

        content = path.read_text(
            encoding="utf-8"
        )

    except Exception as exc:

        return {

            "ok":
                False,

            "file":
                path.name,

            "error":
                repr(
                    exc
                ),
        }

    ok, error = syntax_check_content(
        content
    )

    return {

        "ok":
            ok,

        "file":
            path.name,

        "error":
            error,

        "sha256":
            sha256_text(
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

        re.IGNORECASE
        | re.DOTALL,
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

    target = BACKUP_DIR / (
        f"{path.name}.{stamp}.bak"
    )

    shutil.copy2(
        path,
        target,
    )

    audit(

        "BACKUP_CREATED",

        details={

            "source":
                path.name,

            "backup":
                str(
                    target.relative_to(
                        ROOT
                    )
                ),
        },
    )

    return target


DEFAULT_STATE: Dict[
    str,
    Any,
] = {

    "project":
        PROJECT_NAME,

    "version":
        VERSION,

    "owner_authority":
        OWNER_AUTHORITY,

    "phase":
        "BOOTSTRAP",

    "primary_file_limit":
        MAX_PRIMARY_FILES,

    "file_01":
        THIS_FILENAME,

    "file_02":
        PRIMARY_FILE_02,

    "created_at":
        None,

    "updated_at":
        None,

    "last_plan":
        None,

    "last_build":
        None,

    "last_verify":
        None,

    "last_repair":
        None,
}


def load_state() -> Dict[
    str,
    Any,
]:

    state = read_json(
        STATE_FILE,
        dict(
            DEFAULT_STATE
        ),
    )

    if not state.get(
        "created_at"
    ):

        state[
            "created_at"
        ] = utc_now()

    state[
        "updated_at"
    ] = utc_now()

    return state


def save_state(
    state: Dict[str, Any],
) -> None:

    state[
        "updated_at"
    ] = utc_now()

    atomic_write_json(
        STATE_FILE,
        state,
    )


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

            30,

            int(
                os.getenv(
                    "MAJD_AI_TIMEOUT",
                    "180",
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
                timeout=10,
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

                for item
                in payload.get(
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

                    name
                    == self.model

                    or name.startswith(
                        self.model.split(
                            ":"
                        )[0]
                        + ":"
                    )
                )

                for name
                in models
            )

            return {

                "ok":
                    True,

                "provider":
                    "ollama",

                "base_url":
                    self.base_url,

                "requested_model":
                    self.model,

                "requested_model_available":
                    requested_available,

                "available_models":
                    models,
            }

        except Exception as exc:

            return {

                "ok":
                    False,

                "provider":
                    "ollama",

                "base_url":
                    self.base_url,

                "requested_model":
                    self.model,

                "error":
                    repr(
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

                "model":
                    self.model,

                "prompt":
                    system_prompt.strip()
                    + "\n\n"
                    + user_prompt.strip(),

                "stream":
                    False,

                "options": {
                    "temperature":
                        0.1
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

                "ok":
                    bool(
                        text
                    ),

                "text":
                    text,

                "provider":
                    "ollama",

                "model":
                    self.model,
            }

        except urllib.error.HTTPError as exc:

            return {

                "ok":
                    False,

                "text":
                    "",

                "provider":
                    "ollama",

                "model":
                    self.model,

                "error":
                    (
                        f"HTTP {exc.code}: "
                        f"{exc.reason}"
                    ),
            }

        except Exception as exc:

            return {

                "ok":
                    False,

                "text":
                    "",

                "provider":
                    "ollama",

                "model":
                    self.model,

                "error":
                    repr(
                        exc
                    ),
            }


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

            "generated_at":
                utc_now(),

            "project":
                PROJECT_NAME,

            "primary_limit":
                MAX_PRIMARY_FILES,

            "manual_files": {

                "01":
                    THIS_FILENAME,

                "02":
                    PRIMARY_FILE_02,
            },

            "ai_files":
                DEFAULT_GENERATED_ARCHITECTURE,

            "requirements":
                DOMAIN_PLATFORM_REQUIREMENTS,

            "source":
                "embedded_safe_architecture",
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

            plan[
                "ai_planning"
            ] = {

                "used":
                    False,

                "reason":
                    "AI provider unavailable",

                "health":
                    health,
            }

            atomic_write_json(
                PLAN_FILE,
                plan,
            )

            return plan

        system_prompt = """
You are the architecture planner for MAJD-DMAIL.

Hard rules:
- Primary files are limited to 01 through 05.
- File 01 already exists.
- File 02 is manually maintained.
- You may design ONLY files 03, 04 and 05.
- Never design file 06 or higher.
- Keep exactly three generated primary files.
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
                                "...-03.py",
                            "purpose":
                                "...",
                        },

                        "04": {
                            "filename":
                                "...-04.py",
                            "purpose":
                                "...",
                        },

                        "05": {
                            "filename":
                                "...-05.py",
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

            plan[
                "ai_planning"
            ] = {

                "used":
                    False,

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

                re.IGNORECASE
                | re.DOTALL,
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

                if extract_primary_number(
                    filename
                ) != int(
                    key
                ):

                    raise ValueError(
                        f"Invalid filename for {key}: {filename}"
                    )

                if not purpose:

                    raise ValueError(
                        f"Missing purpose for {key}."
                    )

            plan[
                "ai_files"
            ] = files

            plan[
                "source"
            ] = (
                "ai_reviewed_architecture"
            )

            plan[
                "ai_planning"
            ] = {

                "used":
                    True,

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

                "used":
                    False,

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


class AutonomousBuilder:

    FORBIDDEN_PATTERNS = (

        r"\beval\s*\(",

        r"\bexec\s*\(",

        r"\bos\.system\s*\(",

        r"subprocess\.Popen\s*\(",
    )


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

                "ok":
                    False,

                "file":
                    filename,

                "number":
                    number,

                "error":
                    "syntax_error",

                "detail":
                    syntax_error,
            }

        hits = [

            pattern

            for pattern
            in self.FORBIDDEN_PATTERNS

            if re.search(
                pattern,
                content,
            )
        ]

        if hits:

            return {

                "ok":
                    False,

                "file":
                    filename,

                "number":
                    number,

                "error":
                    "forbidden_pattern",

                "patterns":
                    hits,
            }

        return {

            "ok":
                True,

            "file":
                filename,

            "number":
                number,

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
                "MajdCommerceSecurity",

            "05":
                "MajdPlatformRuntime",

        }[
            number
        ]

        lines = [

            "#!/usr/bin/env python3",

            "# -*- coding: utf-8 -*-",

            "",

            (
                f'"""MAJD-DMAIL | {filename} | '
                f'AI-GENERATED FILE {number} | '
                f'{purpose}"""'
            ),

            "",

            "from __future__ import annotations",

            "",

            "import datetime as dt",

            "import json",

            "from typing import Any, Dict",

            "",

            'PROJECT_NAME = "MAJD-DMAIL"',

            f'FILE_NUMBER = "{number}"',

            'VERSION = "1.0.0"',

            "",

            "def utc_now() -> str:",

            (
                "    return "
                "dt.datetime.now("
                "dt.timezone.utc"
                ").isoformat()"
            ),

            "",

            f"class {class_name}:",

            "",

            "    def __init__(self) -> None:",

            (
                "        self.started_at "
                "= utc_now()"
            ),

            "",

            (
                "    def health(self) "
                "-> Dict[str, Any]:"
            ),

            "        return {",

            '            "ok": True,',

            (
                '            "project": '
                'PROJECT_NAME,'
            ),

            (
                '            "file_number": '
                'FILE_NUMBER,'
            ),

            (
                '            "started_at": '
                'self.started_at,'
            ),

            (
                '            "external_services_verified": '
                'False,'
            ),

            "        }",

            "",

            "def main() -> int:",

            (
                f"    runtime = "
                f"{class_name}()"
            ),

            (
                "    print("
                "json.dumps("
                "runtime.health(), "
                "ensure_ascii=False, "
                "indent=2"
                ")"
                ")"
            ),

            "    return 0",

            "",

            (
                'if __name__ == "__main__":'
            ),

            (
                "    raise "
                "SystemExit(main())"
            ),

            "",
        ]

        return "\n".join(
            lines
        )


    def ai_generate_code(
        self,
        number: str,
        filename: str,
        purpose: str,
    ) -> Optional[str]:

        if not self.ai.health().get(
            "ok"
        ):

            return None

        system_prompt = f"""
You are the autonomous Python engineer for MAJD-DMAIL.

Generate ONLY the complete source code for:

File number: {number}
Filename: {filename}
Purpose: {purpose}

Rules:
- File 01 is the mastermind.
- File 02 is manually maintained.
- You are creating only primary file {number}.
- Never create or request primary file 06 or higher.
- Never hard-code secrets.
- Never use eval(), exec(), os.system(), or subprocess.Popen().
- External providers must use adapters.
- External services are not LIVE until real health checks succeed.
- Code must remain usable when optional external providers are absent.
- Include useful health/status behavior and a main() entry point.
- Return ONLY complete Python source code.
"""

        user_prompt = (

            "Implement this file as a production-oriented "
            "MAJD-DMAIL component.\n\n"

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
            result["text"]
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
You repair MAJD-DMAIL Python source.

Rules:
- Return ONLY corrected complete Python source.
- Do not create additional files.
- Do not hard-code secrets.
- Never use eval(), exec(), os.system(), or subprocess.Popen().
- Preserve the intended responsibility of the current primary file.
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

Return only the corrected complete Python source.
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
            result["text"]
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

        if path.exists() and not force:

            check = syntax_check_file(
                path
            )

            return {

                "ok":
                    bool(
                        check.get(
                            "ok"
                        )
                    ),

                "file":
                    filename,

                "action":
                    "existing_file_kept",

                "verification":
                    check,
            }

        audit(

            "BUILD_STARTED",

            details={

                "file":
                    filename,

                "number":
                    number,
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

            source = "safe_fallback"

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

            and repair_attempts < 2

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
                "safe_fallback_after_ai_rejection"
            )

            validation = self.validate_code(
                filename,
                code,
            )

        if not validation.get(
            "ok"
        ):

            audit(

                "BUILD_REJECTED",

                status="FAILED",

                details={

                    "file":
                        filename,

                    "validation":
                        validation,
                },
            )

            return {

                "ok":
                    False,

                "file":
                    filename,

                "validation":
                    validation,
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

            audit(

                "BUILD_POST_WRITE_FAILED",

                status="FAILED",

                details={

                    "file":
                        filename,

                    "verification":
                        final_check,
                },
            )

            return {

                "ok":
                    False,

                "file":
                    filename,

                "verification":
                    final_check,
            }

        audit(

            "BUILD_COMPLETED",

            details={

                "file":
                    filename,

                "source":
                    source,

                "repair_attempts":
                    repair_attempts,

                "sha256":
                    final_check.get(
                        "sha256"
                    ),
            },
        )

        return {

            "ok":
                True,

            "file":
                filename,

            "source":
                source,

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

                "ok":
                    False,

                "blocked":
                    True,

                "reason": (
                    f"{PRIMARY_FILE_02} "
                    "is required before AI "
                    "may build 03-05."
                ),
            }

        results: Dict[
            str,
            Any,
        ] = {}

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

            "ok":
                all(
                    item.get(
                        "ok"
                    )
                    for item
                    in results.values()
                ),

            "results":
                results,
        }


class ProjectVerifier:

    def verify_primary_policy(
        self,
    ) -> Dict[str, Any]:

        files = list_primary_files()

        return {

            "ok":
                True,

            "files":
                files,

            "limit":
                MAX_PRIMARY_FILES,
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

            for filename
            in list_primary_files()
        }

        return {

            "ok":
                all(
                    item.get(
                        "ok"
                    )
                    for item
                    in results.values()
                ),

            "files":
                results,
        }


    def full(
        self,
        ai: AIProvider,
    ) -> Dict[str, Any]:

        policy = self.verify_primary_policy()

        python = self.verify_python()

        ai_health = ai.health()

        report = {

            "timestamp":
                utc_now(),

            "project":
                PROJECT_NAME,

            "policy":
                policy,

            "python":
                python,

            "ai":
                ai_health,

            "core_ok":
                bool(
                    policy[
                        "ok"
                    ]
                    and
                    python[
                        "ok"
                    ]
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

        results: Dict[
            str,
            Any,
        ] = {}

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
                ] = {

                    "ok":
                        False,

                    "action":
                        "missing",

                    "file":
                        path.name,
                }

                continue

            check = syntax_check_file(
                path
            )

            if check.get(
                "ok"
            ):

                results[
                    number
                ] = {

                    "ok":
                        True,

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

            "ok":
                all(
                    item.get(
                        "ok"
                    )
                    for item
                    in results.values()
                ),

            "results":
                results,
        }


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

        self.verifier = ProjectVerifier()

        self.repair_engine = SelfRepairEngine(
            self.builder
        )


    def bootstrap(
        self,
    ) -> Dict[str, Any]:

        self.state[
            "phase"
        ] = "READY_FOR_FILE_02"

        save_state(
            self.state
        )

        result = {

            "ok":
                True,

            "project":
                PROJECT_NAME,

            "version":
                VERSION,

            "owner_authority":
                OWNER_AUTHORITY,

            "file_01":
                THIS_FILENAME,

            "next_manual_file":
                PRIMARY_FILE_02,

            "ai_generated_after_02": [
                "03",
                "04",
                "05",
            ],

            "primary_file_limit":
                MAX_PRIMARY_FILES,
        }

        audit(
            "BOOTSTRAP_COMPLETED",
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

            "version":
                VERSION,

            "phase":
                self.state.get(
                    "phase"
                ),

            "owner_authority":
                OWNER_AUTHORITY,

            "primary_file_limit":
                MAX_PRIMARY_FILES,

            "primary_files":
                list_primary_files(),

            "file_02_exists":
                (
                    ROOT
                    / PRIMARY_FILE_02
                ).exists(),

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
            "PLAN_CREATED",
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

            result = {

                "ok":
                    False,

                "blocked":
                    True,

                "reason": (
                    f"Create {PRIMARY_FILE_02} first. "
                    "File 01 will not generate "
                    "or overwrite file 02."
                ),
            }

            audit(

                "BUILD_BLOCKED_WAITING_FOR_FILE_02",

                status="FAILED",

                details=result,
            )

            return result

        plan = read_json(
            PLAN_FILE,
            None,
        )

        if not plan:

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
            ] = "GENERATED_CORE_READY"

        save_state(
            self.state
        )

        return result


    def verify(
        self,
    ) -> Dict[str, Any]:

        result = self.verifier.full(
            self.ai
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

            "ai_operational":
                result[
                    "ai_operational"
                ],
        }

        save_state(
            self.state
        )

        audit(
            "VERIFY_COMPLETED",
            details=self.state[
                "last_verify"
            ],
        )

        return result


    def repair(
        self,
    ) -> Dict[str, Any]:

        plan = read_json(
            PLAN_FILE,
            None,
        )

        if not plan:

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

            "REPAIR_COMPLETED",

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

        plan = read_json(
            PLAN_FILE,
            None,
        )

        if not plan:

            plan = self.plan(
                use_ai=True
            )

        initial = self.verify()

        build_result = None

        repair_result = None

        if (
            ROOT
            / PRIMARY_FILE_02
        ).exists():

            missing = [

                number

                for number
                in (
                    "03",
                    "04",
                    "05",
                )

                if not (
                    ROOT
                    / plan[
                        "ai_files"
                    ][
                        number
                    ][
                        "filename"
                    ]
                ).exists()
            ]

            if missing:

                build_result = self.builder.build_all(
                    plan,
                    force=False,
                )

            repair_result = self.repair_engine.repair(
                plan
            )

        final = self.verify()

        result = {

            "started_at":
                started_at,

            "finished_at":
                utc_now(),

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

            "final_verification":
                final,
        }

        audit(

            "AUTOMATION_CYCLE_COMPLETED",

            details={

                "core_ok":
                    final[
                        "core_ok"
                    ],

                "ai_operational":
                    final[
                        "ai_operational"
                    ],

                "file_02_exists":
                    result[
                        "file_02_exists"
                    ],
            },
        )

        return result


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


def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(

        prog=THIS_FILENAME,

        description=(
            "MAJD-DMAIL AI + Automation + Mastermind Core"
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
        default=300,
    )

    return parser


def run_loop(
    mastermind: MajdDmailMastermind,
    interval: int,
) -> int:

    interval = max(
        30,
        int(
            interval
        ),
    )

    audit(

        "AUTOMATION_LOOP_STARTED",

        details={
            "interval_seconds":
                interval
        },
    )

    try:

        while True:

            try:

                result = mastermind.cycle()

                print_json(

                    {

                        "cycle_completed":
                            utc_now(),

                        "core_ok":
                            result[
                                "final_verification"
                            ][
                                "core_ok"
                            ],

                        "ai_operational":
                            result[
                                "final_verification"
                            ][
                                "ai_operational"
                            ],
                    }
                )

            except Exception as exc:

                audit(

                    "AUTOMATION_LOOP_CYCLE_FAILED",

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

    except KeyboardInterrupt:

        audit(

            "AUTOMATION_LOOP_STOPPED",

            details={
                "reason":
                    "keyboard_interrupt"
            },
        )

        return 0


def main() -> int:

    parser = build_parser()

    args = parser.parse_args()

    mastermind = MajdDmailMastermind()

    command = (
        args.command
        or "status"
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
