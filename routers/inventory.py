from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
import database.models as models, schemas

router = APIRouter()


@router.post("/inventory", response_model=schemas.Inventory)
def create_inventory(item: schemas.InventoryCreate, db: Session = Depends(get_db)):
    # Check if product exists
    product = (
        db.query(models.Product).filter(models.Product.id == item.product_id).first()
    )
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")
    inv = models.Inventory(
        product_id=item.product_id,
        channel=item.channel,
        quantity=item.quantity,
        reorder_level=item.reorder_level,
    )
    db.add(inv)
    try:
        db.commit()
        db.refresh(inv)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Inventory entry already exists for this product and channel",
        )
    return inv


@router.get("/inventory", response_model=List[schemas.Inventory])
def read_inventory(
    product_id: int = None, channel: str = None, db: Session = Depends(get_db)
):
    query = db.query(models.Inventory)
    if product_id is not None:
        query = query.filter(models.Inventory.product_id == product_id)
    if channel is not None:
        query = query.filter(models.Inventory.channel == channel)
    items = query.all()
    return items


@router.get("/inventory/{inventory_id}", response_model=schemas.Inventory)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inv = db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()
    if inv is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return inv


@router.get("/inventory/stock/low-stock", response_model=List[schemas.Inventory])
def low_stock(db: Session = Depends(get_db)):
    items = (
        db.query(models.Inventory)
        .filter(models.Inventory.quantity <= models.Inventory.reorder_level)
        .all()
    )
    return items


@router.put("/inventory/{inventory_id}", response_model=schemas.Inventory)
def update_inventory(
    inventory_id: int,
    inv_update: schemas.InventoryUpdate,
    db: Session = Depends(get_db),
):
    inv = db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()
    if inv is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    old_qty = inv.quantity
    inv.quantity = inv_update.quantity
    # update last_updated handled by DB default on update
    # calculate change
    change = inv_update.quantity - old_qty
    # record history
    history = models.InventoryHistory(
        inventory_id=inventory_id, change_qty=change, comment=inv_update.comment
    )
    db.add(history)
    db.commit()
    db.refresh(inv)
    return inv
