from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum as SQLEnum, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .enums import CheckStatus


class Base(DeclarativeBase):
    pass


class ServiceCheck(Base):
    __tablename__ = "service_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[CheckStatus] = mapped_column(
        SQLEnum(CheckStatus, name="check_status", native_enum=False),
        nullable=False,
        default=CheckStatus.UNKNOWN,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    last_checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
