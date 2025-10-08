from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .enums import CheckStatus


class ServiceCheckBase(BaseModel):
    name: str
    description: str | None = None
    status: CheckStatus


class ServiceCheckCreate(ServiceCheckBase):
    pass


class ServiceCheckUpdate(BaseModel):
    description: str | None = None
    status: CheckStatus | None = None


class ServiceCheckRead(ServiceCheckBase):
    id: int
    created_at: datetime
    last_checked_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ServiceCheckSummary(BaseModel):
    total: int
    by_status: dict[CheckStatus, int]
    latest_check: datetime | None = None
