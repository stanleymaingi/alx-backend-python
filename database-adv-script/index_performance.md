-- File: database_index.sql

-- Index on Booking.user_id to speed up user-booking joins
CREATE INDEX idx_booking_user ON Booking(user_id);

-- Index on Booking.start_date to optimize queries filtered by date
CREATE INDEX idx_booking_start_date ON Booking(start_date);

-- Index on Booking.property_id to optimize joins with Property
CREATE INDEX idx_booking_property ON Booking(property_id);

-- Index on Review.property_id to optimize joins with Property
CREATE INDEX idx_review_property ON Review(property_id);

-- Optional: Index on Users.email for authentication lookups
CREATE INDEX idx_users_email ON Users(email);
