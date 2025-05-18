from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from database.database import get_db
import database.models as models, schemas

router = APIRouter()


@router.get("/sales", response_model=List[schemas.Sale])
def read_sales(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: int = None,
    category_id: int = None,
    channel: str = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Sale)
    # Filter by date
    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    # Filter by product
    if product_id:
        query = query.filter(models.Sale.product_id == product_id)
    # Filter by channel
    if channel:
        query = query.filter(models.Sale.channel == channel)
    # Filter by category (join through product)
    if category_id:
        query = query.join(models.Product).filter(
            models.Product.category_id == category_id
        )
    sales = query.all()
    return sales


@router.get("/sales/revenue")
def revenue(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: int = None,
    category_id: int = None,
    channel: str = None,
    group_by: str = Query("day", regex="^(day|week|month|year)$"),
    db: Session = Depends(get_db),
):
    # Determine grouping
    if group_by == "day":
        trunc_func = func.date_trunc("day", models.Sale.sale_date)
    elif group_by == "week":
        trunc_func = func.date_trunc("week", models.Sale.sale_date)
    elif group_by == "month":
        trunc_func = func.date_trunc("month", models.Sale.sale_date)
    elif group_by == "year":
        trunc_func = func.date_trunc("year", models.Sale.sale_date)
    else:
        raise HTTPException(status_code=400, detail="Invalid group_by parameter")

    query = db.query(
        trunc_func.label("period"),
        func.sum(models.Sale.quantity * models.Sale.price).label("revenue"),
    )

    # filters
    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(models.Sale.product_id == product_id)
    if channel:
        query = query.filter(models.Sale.channel == channel)
    if category_id:
        query = query.join(models.Product).filter(
            models.Product.category_id == category_id
        )

    query = query.group_by("period").order_by("period")
    results = query.all()
    # Format output
    data = []
    for period, revenue in results:
        data.append({"period": period.date().isoformat(), "revenue": float(revenue)})
    return data


@router.get("/sales/compare")
def compare(
    start1: datetime,
    end1: datetime,
    start2: datetime,
    end2: datetime,
    product_id: int = None,
    category_id: int = None,
    channel: str = None,
    db: Session = Depends(get_db),
):
    # Aggregate daily revenue for each range
    def get_daily_range(start_date, end_date):
        query = db.query(
            func.date_trunc("day", models.Sale.sale_date).label("day"),
            func.sum(models.Sale.quantity * models.Sale.price).label("revenue"),
        ).filter(models.Sale.sale_date >= start_date, models.Sale.sale_date <= end_date)

        if product_id:
            query = query.filter(models.Sale.product_id == product_id)
        if channel:
            query = query.filter(models.Sale.channel == channel)
        if category_id:
            query = query.join(models.Product).filter(
                models.Product.category_id == category_id
            )

        query = query.group_by("day").order_by("day")
        return query.all()

    range1 = get_daily_range(start1, end1)
    range2 = get_daily_range(start2, end2)

    data1 = [
        {"date": day.date().isoformat(), "revenue": float(rev)} for day, rev in range1
    ]
    data2 = [
        {"date": day.date().isoformat(), "revenue": float(rev)} for day, rev in range2
    ]
    return {"range1": data1, "range2": data2}
