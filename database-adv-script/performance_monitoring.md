# Performance Monitoring Report

## Objective
Monitor and refine the performance of frequently used queries in the Airbnb database.  
We focus on analyzing execution plans, identifying bottlenecks, and implementing improvements.

---

## 1. Query 1: Total Bookings per User

**Query:**
```sql
SELECT 
    u.user_id,
    u.name,
    COUNT(b.booking_id) AS total_bookings
FROM Users u
LEFT JOIN Booking b
    ON u.user_id = b.user_id
GROUP BY u.user_id, u.name;
