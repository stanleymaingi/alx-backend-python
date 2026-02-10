-- File: subqueries.sql
-- ALX Airbnb Database: Practice Subqueries

-- ========================================================
-- 1. Non-correlated Subquery: Find properties where
--    the average rating is greater than 4.0
-- ========================================================
SELECT *
FROM Property
WHERE property_id IN (
    SELECT property_id
    FROM Review
    GROUP BY property_id
    HAVING AVG(rating) > 4.0
);

-- ========================================================
-- 2. Correlated Subquery: Find users who have made
--    more than 3 bookings
-- ========================================================
SELECT *
FROM Users u
WHERE (
    SELECT COUNT(*)
    FROM Booking b
    WHERE b.user_id = u.user_id
) > 3;
