# Partition Performance Report

## Objective
The goal of this task was to implement **table partitioning** on the `Booking` table to optimize query performance, particularly for queries filtering by `start_date`. The original `Booking` table contained a large number of rows, causing slow query execution.

---

## Implementation
1. Created a new partitioned table `Booking_Partitioned` using **RANGE partitioning** on the `start_date` column.
2. Created yearly partitions (`Booking_2024`, `Booking_2025`, `Booking_2026`) to divide the data logically.
3. Migrated existing data into the partitioned table.
4. Added indexes on `user_id`, `property_id`, and `start_date` columns in the partitioned table.

---

## Test Queries
**Query 1: Fetch bookings in 2025**
```sql
EXPLAIN ANALYZE
SELECT *
FROM Booking_Partitioned
WHERE start_date BETWEEN '2025-01-01' AND '2025-12-31';
