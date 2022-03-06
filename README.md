## Demand Forecasting and Markdown Pricing

## Problem statement
A retailer would like to decide weekly pricing of their products. He/she generally plans pricing for each quarter and would like to achieve following:
- Clear-out at least x% (say 60%) of total inventory
- Achieve total margin across all products (i.e., selling price - cost price)
Following are a few things to consider while deciding pricing of products.
- There shouldn’t be much difference in the pricing from one week to another.
- A particular price selected applies for all the products in the group.
- Shopkeeper must cater posed weekly demand to customers if inventory is available

## Tasks
- Develop a model that can help shopkeeper to identify their pricing for a quarter (13 weeks in the provided example)
- Model must suggest a pricing (price-point) that will be applied across all the products to achieve highest possible margin considering inventory clearance (say 60%)
- Max Price change from one week to next is 20 units
- A single price-point for a week that applies to all the products as they belong to same group
- Algorithmic details to solve the model and provide insights on complexity of model in scaling to larger number of products/weeks.

## Schema description
- product_id: 
    + unique product ID
- price: 
    + historical price in a week
- week: 
    + week in a quarter
- group: 
    + product group that a product belongs to (only one group in this case)
- demand: 
    + inventory sold during week at given price point
- selling_price: 
    + selling price of one unit of product in a week at a price-point
- total_inventory: 
    + Inventory available for each product at the start of the quarter. Same value is repeated for all possible weeks & price-points of a product. You can filter inventory available for a product by taking distinct values of columns product_id & total_inventory.
- cost_price: 
    + cost price of one unit of product in a week at a price-point