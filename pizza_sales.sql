use internship;
select * from pizza_sales;
select sum(total_price) AS TOTAL_REVENUE from pizza_sales;

select sum(total_price)/count(Distinct order_id)
AS AVERAGE_ORDER_VALUE 
from pizza_sales;

select sum(quantity) AS TOTAL_PIZZAS_SOLD from pizza_sales;

 select COUNT(Distinct order_id) AS TOTAL_ORDERS from pizza_sales;
 
select CAST(sum(quantity) 
AS FLOAT)/count(Distinct order_id) 
AS AVERAGE_PIZZAS_PER_ORDER 
from pizza_sales;

select sum(total_price) AS TOTAL_REVENUE,
COUNT(Distinct order_id) AS TOTAL_ORDERS,
sum(quantity) AS TOTAL_PIZZAS_SOLD,
sum(total_price)/count(Distinct order_id) AS AVERAGE_ORDER_VALUE,
CAST(sum(quantity) AS FLOAT)/count(Distinct order_id) AS AVERAGE_PIZZAS_PER_ORDER
from pizza_sales;

SELECT
DAYNAME(STR_TO_DATE(order_date, '%Y-%m-%d')) AS DAY_NAME,
COUNT(DISTINCT order_id) AS TOTAL_ORDERS
FROM pizza_sales
GROUP BY DAY_NAME
ORDER BY FIELD(DAY_NAME,
'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');

SELECT
 MONTH(STR_TO_DATE(order_date, '%Y-%m-%d')) AS MONTH_NO,
 MONTHNAME(STR_TO_DATE(order_date, '%Y-%m-%d')) AS MONTH_NAME,
 COUNT(DISTINCT order_id) AS TOTAL_ORDERS
 FROM pizza_sales
 GROUP BY MONTH_NO, MONTH_NAME
 ORDER BY MONTH_NO;
 
 select
pizza_category,
sum(total_price) AS TOTAL_SALES,
sum(total_price)*100.0/
(select sum(total_price) from pizza_sales) AS REVENUE_PERCENTAGE
from pizza_sales
GROUP BY pizza_category
ORDER BY REVENUE_PERCENTAGE DESC;

select
pizza_size,
sum(total_price) AS TOTAL_SALES,
sum(total_price)*100.0/
(select sum(total_price) from pizza_sales) AS REVENUE_PERCENTAGE
from pizza_sales
GROUP BY pizza_size
ORDER BY REVENUE_PERCENTAGE DESC;

select pizza_category,
sum(quantity) AS TOTAL_PIZZAS_SOLD
from pizza_sales
GROUP BY pizza_category
ORDER BY TOTAL_PIZZAS_SOLD DESC;

SELECT pizza_name,
SUM(total_price) AS REVENUE
FROM pizza_sales
GROUP BY pizza_name
ORDER BY REVENUE DESC
 LIMIT 5;
 
 SELECT pizza_name,
 SUM(quantity) AS QUANTITY_SOLD
 FROM pizza_sales
 GROUP BY pizza_name
 ORDER BY QUANTITY_SOLD DESC
 LIMIT 5;
 
 SELECT pizza_name,
COUNT(DISTINCT order_id) AS TOTAL_ORDERS
FROM pizza_sales
GROUP BY pizza_name
ORDER BY TOTAL_ORDERS DESC
LIMIT 5;

SELECT pizza_name,
SUM(total_price) AS REVENUE
FROM pizza_sales
GROUP BY pizza_name
ORDER BY REVENUE ASC
LIMIT 5;

SELECT pizza_name,
SUM(quantity) AS QUANTITY_SOLD
FROM pizza_sales
GROUP BY pizza_name
ORDER BY QUANTITY_SOLD ASC
LIMIT 5;

SELECT pizza_name,
COUNT(DISTINCT order_id) AS TOTAL_ORDERS
FROM pizza_sales
GROUP BY pizza_name
ORDER BY TOTAL_ORDERS ASC
LIMIT 5;