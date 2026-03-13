-- Customers mart: customer-level metrics
with source as (
    select * from {{ ref('stg_orders') }}
),

customer_metrics as (
    select
        customer_id,
        count(distinct order_id)                    as total_orders,
        sum(quantity * price)                       as lifetime_value,
        avg(quantity * price)                       as avg_order_value,
        min(order_date)                             as first_order_date,
        max(order_date)                             as last_order_date,
        datediff('day', min(order_date),
                        max(order_date))            as customer_tenure_days
    from source
    group by customer_id
),

final as (
    select
        customer_id,
        total_orders,
        round(lifetime_value, 2)                    as lifetime_value,
        round(avg_order_value, 2)                   as avg_order_value,
        first_order_date,
        last_order_date,
        customer_tenure_days,
        case
            when lifetime_value >= 1000 then 'high'
            when lifetime_value >= 500  then 'medium'
            else 'low'
        end                                         as customer_segment
    from customer_metrics
)

select * from final
