from pydantic import BaseModel, ConfigDict


class visionBase(BaseModel):
    """Base schema for vision."""

    name: str


class visionCreate(visionBase):
    """Schema for creating a vision."""

    pass


class visionResponse(visionBase):
    """Schema for vision response."""

    id: int

    model_config = ConfigDict(from_attributes=True)
