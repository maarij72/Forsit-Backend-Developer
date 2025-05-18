E-commerce Admin Dashboard Backend (FastAPI)
============================================

This project provides a backend API built with **FastAPI** (Python) and **PostgreSQL** to support an e-commerce admin dashboard. 

Database Schema
---------------

The API uses a normalized relational schema in a PostgreSQL database (ecommerce\_db). The key tables are:

*   **categories**: Stores product categories.
    
    *   Columns: id (PK), name
        
*   **products**: Stores product details.
    
    *   Columns: id (PK), name, description, price, category\_id (FK to categories)
        
*   **inventory**: Tracks stock levels for each product per sales channel.
    
    *   Columns: id (PK), product\_id (FK to products), channel, quantity, reorder\_level, last\_updated
        
*   **inventory\_history**: Logs inventory changes over time.
    
    *   Columns: id (PK), inventory\_id (FK to inventory), change\_qty, timestamp, comment
        
*   **sales**: Records individual sales transactions.
    
    *   Columns: id (PK), product\_id (FK to products), channel, quantity, price, sale\_date
        

### Indexing

*   All foreign keys are indexed for performance.
    
*   A B-tree index on sales.sale\_date enables efficient time-range queries.
    
*   Additional indexes on product\_id and other frequently queried fields optimize performance.
    

API Endpoints
-------------

The API provides the following endpoints (no authentication required):

### Categories

*   **GET /categories**
    
    *   Lists all categories.
        
*   **POST /categories**
    
    *   Creates a new category.
        
    *   Body: { "name": "" }
        

### Products

*   **GET /products**
    
    *   Lists products with pagination support.
        
    *   Query params: skip, limit
        
*   **GET /products/{product\_id}**
    
    *   Retrieves a product by its ID.
        
*   **POST /products**
    
    *   Creates a new product.
        
    *   Body: { "name": "", "description": "", "price": , "category\_id": }
        
    *   Returns the created product.
        

### Inventory

*   **GET /inventory**
    
    *   Lists inventory items.
        
    *   Optional query filters: product\_id, channel
        
*   **GET /inventory/{inventory\_id}**
    
    *   Retrieves an inventory item by ID.
        
*   **GET /inventory/stock/low-stock**
    
    *   Lists items where quantity ≤ reorder\_level.
        
*   **POST /inventory**
    
    *   Creates a new inventory record.
        
    *   Body: { "product\_id": , "channel": "", "quantity": , "reorder\_level": }
        
*   **PUT /inventory/{inventory\_id}**
    
    *   Updates inventory quantity and logs the change in inventory\_history.
        
    *   Body: { "quantity": , "comment": "" }
        

### Sales

*   **GET /sales**
    
    *   Lists sales records with filtering support.
        
    *   Query params: product\_id, category\_id, channel, start\_date, end\_date (ISO date strings)
        
    *   Returns sales records with all fields.
        
*   **GET /sales/revenue**
    
    *   Retrieves aggregated revenue data.
        
    *   Query params:
        
        *   start\_date, end\_date (date range filter)
            
        *   product\_id, category\_id, channel (optional filters)
            
        *   group\_by: One of day, week, month, year (default: day)
            
    *   Returns: List of { "period": "YYYY-MM-DD", "revenue": } (sum of price \* quantity per period)
        
*   **GET /sales/compare**
    
    *   Compares revenue across two time ranges.
        
    *   Query params: start1, end1, start2, end2 (required), plus optional product\_id, category\_id, channel
        
    *   Returns: JSON with two lists: "range1" and "range2", each containing daily revenue data.