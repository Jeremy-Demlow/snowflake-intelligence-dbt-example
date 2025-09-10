{{ config(materialized='view') }}

SELECT
    id,
    blng_account_c,
    blng_invoice_date_c,
    blng_start_date_c,
    blng_end_date_c,
    blng_total_amount_c,
    blng_tax_amount_c,
    blng_product_c,
    blng_unit_price_c,
    blng_quantity_c,
    blng_subtotal_c,
    blng_invoice_status_c

FROM {{ source('acme_raw', 'invoices') }}
