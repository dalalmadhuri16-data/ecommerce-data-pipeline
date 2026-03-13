-- Products mart: product-level metrics
with source as (
    select * from {{ ref('stg_orders') }}
),

product_metrics as (
    select
        product_id,
        count(distinct order_id)                    as total_orders,
        sum(quantity)                               as total_units_sold,
        sum(quantity * price)                       as total_revenue,
        avg(price)                                  as avg_selling_price,
        min(order_date)                             as first_sale_date,
        max(order_date)                             as last_sale_date
    from source
    group by product_id
),

final as (
    select
        product_id,
        total_orders,
        total_units_sold,
        round(total_revenue, 2)                     as total_revenue,
        round(avg_selling_price, 2)                 as avg_selling_price,
        first_sale_date,
        last_sale_date,
        case
            when total_units_sold >= 1000 then 'bestseller'
            when total_units_sold >= 500  then 'popular'
            when total_units_sold >= 100  then 'normal'
            else 'slow-mover'
        end                                         as product_category
    from product_metrics
)

select * from final
