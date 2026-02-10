-- File: aggregations_and_window_functions.sql
-- Purpose: Perform aggregations and window functions on Airbnb database

-- ===========================================================
-- Task 1: Total number of bookings made by each user
-- ===========================================================

SELECT 
    u.user_id,
    u.name,
    COUNT(b.booking_id) AS total_bookings
FROM Users u
LEFT JOIN Booking b
    ON u.user_id = b.user_id
GROUP BY u.user_id, u.name
ORDER BY total_bookings DESC;

-- ===========================================================
-- Task 2: Rank properties based on total number of bookings
-- ===========================================================

SELECT 
    p.property_id,
    p.title,
    COUNT(b.booking_id) AS total_bookings,
    RANK() OVER (ORDER BY COUNT(b.booking_id) DESC) AS property_rank
FROM Property p
LEFT JOIN Booking b
    ON p.property_id = b.property_id
GROUP BY p.property_id, p.title
ORDER BY property_rank ASC;
