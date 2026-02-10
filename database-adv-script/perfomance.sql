-- File: perfomance.sql
-- Initial Query: Fetch all bookings with user, property, and payment details

-- Optimized version with indexes assumed on Booking(user_id), Booking(property_id), Payment(booking_id)

SELECT 
    b.booking_id,
    b.start_date,
    b.end_date,
    u.user_id,
    u.name AS user_name,
    u.email AS user_email,
    p.property_id,
    p.title AS property_title,
    p.location AS property_location,
    pay.payment_id,
    pay.amount AS payment_amount,
    pay.payment_date
FROM Booking b
-- Only INNER JOIN users and properties, LEFT JOIN payment (optional)
INNER JOIN Users u
    ON b.user_id = u.user_id
INNER JOIN Property p
    ON b.property_id = p.property_id
LEFT JOIN Payment pay
    ON b.booking_id = pay.booking_id;

-- Notes:
-- 1. Ensure indexes exist:
--    CREATE INDEX idx_booking_user ON Booking(user_id);
--    CREATE INDEX idx_booking_property ON Booking(property_id);
--    CREATE INDEX idx_payment_booking ON Payment(booking_id);
-- 2. Use EXPLAIN ANALYZE to check performance.
