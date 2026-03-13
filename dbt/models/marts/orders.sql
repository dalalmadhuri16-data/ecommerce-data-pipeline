-- Orders mart: order-level metrics
with source as (
    select * from {{ ref('stg_orders') }}
),

final as (
    select
        order_id,
        customer_id,
        product_id,
        quantity,
        price,
        quantity * price as revenue,
        order_date,
        status
    from source
    where status is not null
)

select * from final
