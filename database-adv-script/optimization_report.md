# Database Query Optimization Report

## Project: ALX Airbnb Database
## Task: Optimize Complex Queries
## Author: [Your Name]
## Date: [Insert Date]

---

## 1. Objective

The goal of this task is to optimize a complex query that retrieves all bookings along with related user, property, and payment details. Optimization involves:

- Analyzing the query execution plan
- Identifying bottlenecks
- Applying indexing
- Refactoring joins to reduce unnecessary computations

---

## 2. Initial Query

The initial query used multiple joins:

```sql
SELECT 
    b.booking_id,
    b.start_date,
    b.end_date,
    u.user_id,
    u.name,
    u.email,
    p.property_id,
    p.title,
    p.location,
    pay.payment_id,
    pay.amount,
    pay.payment_date
FROM Booking b
INNER JOIN Users u
    ON b.user_id = u.user_id
INNER JOIN Property p
    ON b.property_id = p.property_id
LEFT JOIN Payment pay
    ON b.booking_id = pay.booking_id;
