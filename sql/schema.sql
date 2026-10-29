-- Reference schema for a PostgreSQL implementation of the same model.
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(40) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(40) NOT NULL,
    product VARCHAR(150) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
    country VARCHAR(80) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date);

CREATE OR REPLACE VIEW daily_sales AS
SELECT order_date,
       COUNT(DISTINCT order_id) AS order_count,
       SUM(quantity) AS units_sold,
       ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY order_date;
