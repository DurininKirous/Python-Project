from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ServiceCheckBase(BaseModel):
    name: str
    description: str | None = None
    status: str


class ServiceCheckCreate(ServiceCheckBase):
    pass


class ServiceCheckUpdate(BaseModel):
    description: str | None = None
    status: str | None = None


class ServiceCheckRead(ServiceCheckBase):
    id: int
    last_checked_at: datetime

    model_config = ConfigDict(from_attributes=True)
