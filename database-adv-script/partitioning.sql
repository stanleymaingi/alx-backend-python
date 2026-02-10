-- ---------------------------------------------
-- Partitioning Booking table by start_date
-- ---------------------------------------------

-- Step 1: Create a new partitioned table
CREATE TABLE Booking_Partitioned (
    booking_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    property_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
) PARTITION BY RANGE (start_date);

-- Step 2: Create partitions for each year
CREATE TABLE Booking_2024 PARTITION OF Booking_Partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE Booking_2025 PARTITION OF Booking_Partitioned
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

CREATE TABLE Booking_2026 PARTITION OF Booking_Partitioned
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

-- Step 3: Migrate existing data from Booking into Booking_Partitioned
INSERT INTO Booking_Partitioned (booking_id, user_id, property_id, start_date, end_date)
SELECT booking_id, user_id, property_id, start_date, end_date
FROM Booking;

-- Step 4: Optional: drop old Booking table and rename
-- DROP TABLE Booking;
-- ALTER TABLE Booking_Partitioned RENAME TO Booking;

-- Step 5: Add indexes on partitioned table for optimization
CREATE INDEX idx_booking_partitioned_user ON Booking_Partitioned(user_id);
CREATE INDEX idx_booking_partitioned_property ON Booking_Partitioned(property_id);
CREATE INDEX idx_booking_partitioned_start_date ON Booking_Partitioned(start_date);
