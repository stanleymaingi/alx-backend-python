# Unleashing Advanced Querying Power – ALX Airbnb Database Module

## Project Overview
This project is part of the **ALX Airbnb Database Module**, focused on **advanced SQL querying and optimization techniques**. The goal is to work with a simulated Airbnb database to gain hands-on experience in **writing complex queries, optimizing performance, and implementing indexing and partitioning**.

Through this project, learners develop skills essential for **large-scale applications** where **efficiency, scalability, and data-driven decisions** are critical.

---

## Learning Objectives
By completing this project, you will:

- **Master Advanced SQL:** Write complex queries using joins, subqueries, aggregations, and window functions.
- **Optimize Query Performance:** Use tools like `EXPLAIN` and `ANALYZE` to monitor and improve query execution.
- **Implement Indexing and Partitioning:** Improve database performance on large datasets.
- **Monitor and Refine Performance:** Continuously evaluate database health and refine schemas for efficiency.
- **Think Like a DBA:** Make informed decisions about schema design, relationships, and query optimization.

---

## Project Tasks

### Task 0: Write Complex Queries with Joins
**Objective:** Gain mastery of SQL joins by writing complex queries.

#### 1. INNER JOIN – Retrieve all bookings with respective users
```sql
SELECT
    bookings.id AS booking_id,
    bookings.start_date,
    bookings.end_date,
    users.id AS user_id,
    users.name,
    users.email
FROM bookings
INNER JOIN users
    ON bookings.user_id = users.id;
