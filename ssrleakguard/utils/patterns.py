import re

# Common secret patterns with validators


def validate_jwt(token: str) -> bool:
    """Validate JWT structure"""
    parts = token.split(".")
    return len(parts) == 3 and all(len(p) > 0 for p in parts)


def validate_aws_key(key: str) -> bool:
    """Validate AWS access key format"""
    return len(key) == 20 and key.isupper()


def validate_aws_secret(secret: str) -> bool:
    """Validate AWS secret key format"""
    return len(secret) == 40


SECRET_PATTERNS = {
    "jwt_token": {
        "pattern": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
        "description": "JSON Web Token (JWT)",
        "severity": "high",
        "validator": validate_jwt,
    },
    "api_key_generic": {
        "pattern": r"(?i)(api[_-]?key|apikey|access[_-]?key)[\"\']?\s*[:=]\s*[\"\']?([a-z0-9_\-]{16,})",
        "description": "Generic API Key",
        "severity": "high",
    },
    "bearer_token": {
        "pattern": r"Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*",
        "description": "Bearer Token",
        "severity": "high",
    },
    "aws_access_key": {
        "pattern": r"AKIA[0-9A-Z]{16}",
        "description": "AWS Access Key ID",
        "severity": "critical",
        "validator": validate_aws_key,
    },
    "aws_secret_key": {
        "pattern": r"(?i)aws[_-]?secret[_-]?access[_-]?key[\"\']?\s*[:=]\s*[\"\']?([a-z0-9/+=]{40})",
        "description": "AWS Secret Access Key",
        "severity": "critical",
        "validator": validate_aws_secret,
    },
    "github_token": {
        "pattern": r"ghp_[a-zA-Z0-9]{36}",
        "description": "GitHub Personal Access Token",
        "severity": "critical",
    },
    "slack_token": {
        "pattern": r"xox[baprs]-[0-9]{10,12}-[0-9]{10,12}-[a-zA-Z0-9]{24,32}",
        "description": "Slack Token",
        "severity": "high",
    },
    "private_key": {
        "pattern": r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
        "description": "Private Key",
        "severity": "critical",
    },
    "database_connection": {
        "pattern": r"(?i)(mongodb|mysql|postgres|postgresql)://[^\s\"\'<>]+",
        "description": "Database Connection String",
        "severity": "high",
    },
    "email_address": {
        "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "description": "Email Address",
        "severity": "medium",
    },
    "phone_number": {
        "pattern": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b",
        "description": "Phone Number",
        "severity": "medium",
    },
    "session_id": {
        "pattern": r"(?i)(session[_-]?id|sessionid|sess)[\"\']?\s*[:=]\s*[\"\']?([a-f0-9]{32,})",
        "description": "Session ID",
        "severity": "high",
    },
}