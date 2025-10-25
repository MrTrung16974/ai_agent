from pydantic import BaseModel, Field, PositiveFloat


class ItemBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=500)
    price: PositiveFloat


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: PositiveFloat | None = None


class ItemInDBBase(ItemBase):
    id: int

    class Config:
        from_attributes = True


class Item(ItemInDBBase):
    pass
