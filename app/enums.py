from enum import StrEnum


class CheckStatus(StrEnum):
    """Enumeration of possible service health states."""

    PASSING = "passing"
    FAILING = "failing"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"
