{{ config(materialized='table') }}

/*
NDR (Net Dollar Retention) calculation based on complex CTE logic
This model implements the exact NDR calculation pattern provided by the user
*/

WITH
cte_source AS (
    -- Base billing metrics data
    SELECT 
        parent_account_id,
        ndr_parent,
        month_id,
        billing_month,
        l3m_arr,
        size_segment,
        market_segment,
        trade_segment,
        product_category
    FROM {{ ref('stg_billing_metrics') }}
),

cte_sum_billing_year AS (
    -- Historical ARR for each NDR parent (billed tenant) as of each month
    SELECT
        ndr_parent,
        month_id,
        SUM(l3m_arr) AS l3m_arr
    FROM cte_source
    GROUP BY month_id, ndr_parent
),

cte_denominator AS (
    -- Total ARR for the comparable month in the last year
    SELECT
        cs1.ndr_parent,
        cs1.month_id,
        cs2.l3m_arr AS l3m_arr_previous_year
    FROM cte_sum_billing_year cs1
    LEFT JOIN cte_sum_billing_year cs2
    ON cs2.month_id = CAST(cs1.month_id AS int) - 100  -- Month ID is like 202508, subtract 100 for previous year 202408
    AND cs2.ndr_parent = cs1.ndr_parent
),

cte_ndr_numerator AS (
    -- Expansion for the current month for all tenants who had billings from last year in the similar month
    SELECT
        c1.ndr_parent,
        c1.month_id,
        c1.billing_month,
        SUM(c1.l3m_arr) AS l3m_arr_current
    FROM cte_source c1
    WHERE c1.ndr_parent IN (
        SELECT c2.ndr_parent
        FROM cte_source c2
        WHERE c2.month_id = (CAST(c1.month_id AS int) - 100)
        AND c2.l3m_arr > 0
    )
    GROUP BY c1.month_id, c1.ndr_parent, c1.billing_month
),

cte_ndr AS (
    -- Final NDR calculation
    SELECT
        ndr.ndr_parent,
        ndr.month_id,
        ndr.billing_month,
        ndr.l3m_arr_current,
        d.l3m_arr_previous_year,
        IFF(d.l3m_arr_previous_year > 0, 
            ROUND((ndr.l3m_arr_current / d.l3m_arr_previous_year) * 100, 2), 
            NULL) AS ndr_percentage,
        (ndr.l3m_arr_current - d.l3m_arr_previous_year) AS arr_expansion
    FROM cte_ndr_numerator ndr
    JOIN cte_denominator d
    ON d.month_id = ndr.month_id
    AND d.ndr_parent = ndr.ndr_parent
    ORDER BY ndr.month_id DESC
),

-- Join with segmentation data for detailed analysis
final AS (
    SELECT 
        a.*,
        -- Add segmentation dimensions from the first record for each ndr_parent
        seg.size_segment,
        seg.market_segment,
        seg.trade_segment,
        seg.product_category
    FROM cte_ndr a
    LEFT JOIN (
        SELECT DISTINCT
            ndr_parent,
            FIRST_VALUE(size_segment) OVER (PARTITION BY ndr_parent ORDER BY month_id DESC) AS size_segment,
            FIRST_VALUE(market_segment) OVER (PARTITION BY ndr_parent ORDER BY month_id DESC) AS market_segment,
            FIRST_VALUE(trade_segment) OVER (PARTITION BY ndr_parent ORDER BY month_id DESC) AS trade_segment,
            FIRST_VALUE(product_category) OVER (PARTITION BY ndr_parent ORDER BY month_id DESC) AS product_category
        FROM cte_source
    ) seg
    ON seg.ndr_parent = a.ndr_parent
    -- Filter future months as they are irrelevant
    WHERE a.billing_month < DATE_TRUNC('month', CURRENT_DATE())
)

SELECT * FROM final
