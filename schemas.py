from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Category schemas
class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# Product schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


# Inventory schemas
class InventoryBase(BaseModel):
    product_id: int
    channel: str
    quantity: int
    reorder_level: int


class InventoryCreate(InventoryBase):
    pass


class Inventory(InventoryBase):
    id: int
    last_updated: Optional[datetime] = None

    class Config:
        orm_mode = True


class InventoryUpdate(BaseModel):
    quantity: int
    comment: Optional[str] = None


# Sale schemas
class SaleBase(BaseModel):
    product_id: int
    channel: str
    quantity: int
    price: float
    sale_date: datetime


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):
    id: int

    class Config:
        orm_mode = True
