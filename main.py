from fastapi import FastAPI
from database.database import init_db
from routers.categories import router as categories_router
from routers.products import router as products_router
from routers.inventory import router as inventory_router
from routers.sales import router as sales_router

app = FastAPI(title="E-commerce Admin Dashboard API")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(categories_router)
app.include_router(products_router)
app.include_router(inventory_router)
app.include_router(sales_router)
