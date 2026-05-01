CREATE OR REPLACE VIEW final_dataset AS
SELECT 
    sku,
    barcode, 
    product_name,
    product_type,
    inventory,
    quantity,
    revenue,
    cost,
    price,

    -- metric
    CASE WHEN price = 0 THEN 0 ELSE 1 - cost / price END AS margin,
    quantity * (price - cost) AS profit,
    CASE WHEN inventory = 0 THEN 0 ELSE quantity / inventory END AS sell_through,

    quantity / 4 AS avg_monthly_sales,

    -- percentile theo nhóm
    NTILE(4) OVER (PARTITION BY product_type ORDER BY quantity / 4) AS sales_quartile

FROM dataset;