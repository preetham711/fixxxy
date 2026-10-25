-- FIXXY Car Spare Parts & Billing Management System
-- Database Schema for MySQL

DROP DATABASE IF EXISTS fixxy_store;
CREATE DATABASE fixxy_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE fixxy_store;

-- Users table (customers and admin)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'customer',
    phone VARCHAR(50) DEFAULT '',
    address TEXT DEFAULT '',
    created_at DATETIME NOT NULL,
    INDEX idx_username (username),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Products table (spare parts and water wash services)
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK(price >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK(stock >= 0),
    description TEXT,
    sold INT NOT NULL DEFAULT 0,
    active TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_name (name),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Categories table
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Coupons table
CREATE TABLE coupons (
    code VARCHAR(50) PRIMARY KEY,
    discount DECIMAL(5,2) NOT NULL CHECK(discount >= 0 AND discount <= 100),
    description TEXT,
    active TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Vehicles table
CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year VARCHAR(10) NOT NULL,
    registration_number VARCHAR(50) DEFAULT '',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Orders table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_no VARCHAR(100) NOT NULL UNIQUE,
    user_id INT,
    customer_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    car_brand VARCHAR(100) DEFAULT '',
    car_model VARCHAR(100) DEFAULT '',
    car_year VARCHAR(10) DEFAULT '',
    registration_number VARCHAR(50) DEFAULT '',
    subtotal DECIMAL(10,2) NOT NULL,
    discount DECIMAL(10,2) NOT NULL DEFAULT 0,
    gst DECIMAL(10,2) NOT NULL,
    grand_total DECIMAL(10,2) NOT NULL,
    coupon_code VARCHAR(50) DEFAULT '',
    payment_method VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'completed',
    created_at DATETIME NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_bill_no (bill_no),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Order items table
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE SET NULL,
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Settings table
CREATE TABLE settings (
    `key` VARCHAR(100) PRIMARY KEY,
    `value` TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default admin user (password: admin123)
-- Note: Password hash generated using PBKDF2-SHA256 with 180,000 iterations
-- If you need to change the password, run: python setup_database.py
-- Or generate a new hash with: python generate_password.py
INSERT INTO users (username, password_hash, full_name, role, phone, address, created_at) VALUES
('admin', 'fb6b0726a147cdb6f4abf30c745c033a$e997411df3276d24ef63f3f44e4352820c7721a0bd978571b7f23c54e5b107ef', 'FIXXY Administrator', 'admin', '1234567890', 'Admin Office', NOW());

-- Insert default categories
INSERT INTO categories (name, description) VALUES
('Filters', 'Air filters, oil filters, fuel filters'),
('Brakes', 'Brake pads, brake discs, brake fluid'),
('Engine Parts', 'Spark plugs, timing belts, pistons'),
('Electrical', 'Batteries, alternators, starters'),
('Suspension', 'Shock absorbers, springs, bushings'),
('Transmission', 'Clutch plates, gearbox parts'),
('Cooling', 'Radiators, coolant, thermostats'),
('Accessories', 'Wiper blades, bulbs, fuses'),
('Water Wash', 'Car wash and detailing services');

-- Insert default products
INSERT INTO products (name, category, price, stock, description, sold) VALUES
('Oil Filter', 'Filters', 450.00, 30, 'High-quality engine oil filtration', 0),
('Air Filter', 'Filters', 650.00, 25, 'Cleans air entering the engine', 0),
('Brake Pads', 'Brakes', 1800.00, 18, 'Premium friction pads for safe braking', 0),
('Spark Plug', 'Engine Parts', 350.00, 50, 'OEM quality ignition component', 0),
('Battery', 'Electrical', 4500.00, 12, 'Maintenance-free automotive battery', 0),
('Timing Belt', 'Engine Parts', 1200.00, 15, 'Durable engine timing belt', 0),
('Alternator', 'Electrical', 6500.00, 8, 'Charges battery while driving', 0),
('Water Pump', 'Engine Parts', 3200.00, 10, 'Engine coolant circulation pump', 0),
('Clutch Plate', 'Transmission', 2800.00, 11, 'Heavy-duty clutch assembly component', 0),
('Shock Absorber', 'Suspension', 2400.00, 16, 'Premium suspension damping component', 0),
('Headlight Bulb', 'Electrical', 550.00, 40, 'Bright halogen headlight bulb', 0),
('Wiper Blades', 'Accessories', 700.00, 22, 'All-weather windshield wiper blades', 0),
('Radiator', 'Cooling', 5200.00, 7, 'Aluminum engine cooling radiator', 0),
('Fuel Pump', 'Engine Parts', 3900.00, 9, 'High-pressure fuel delivery pump', 0),
('Wheel Bearing', 'Suspension', 1450.00, 20, 'Precision wheel rotation bearing', 0),
('Cabin Air Filter', 'Filters', 800.00, 24, 'Filters air entering cabin', 0),
('Disc Rotor', 'Brakes', 2100.00, 13, 'Ventilated brake disc rotor', 0),
('Fuse Set', 'Electrical', 250.00, 60, 'Automotive replacement fuse set', 0);

-- Insert water wash services
INSERT INTO products (name, category, price, stock, description, sold) VALUES
('Full Clean', 'Water Wash', 499.00, 99999, 'Exterior wash, wheel cleaning and basic interior wipe', 0),
('Foam Wash', 'Water Wash', 699.00, 99999, 'Snow foam pre-wash, rinse and microfiber dry', 0),
('Premium Foam + Wax', 'Water Wash', 999.00, 99999, 'Foam wash, wax finish and tyre shine', 0),
('Interior Deep Clean', 'Water Wash', 1299.00, 99999, 'Seats, mats, dashboard and interior vacuum', 0);

-- Insert default coupons
INSERT INTO coupons (code, discount, description, active) VALUES
('WELCOME10', 10.00, 'Welcome discount for new customers', 1),
('SERVICE5', 5.00, 'Service customer discount', 1),
('SUMMER15', 15.00, 'Summer season special offer', 1);

-- Insert default settings
INSERT INTO settings (`key`, `value`) VALUES
('shop_name', 'FIXXY Car Spares'),
('gst_rate', '18'),
('currency', 'INR'),
('currency_symbol', '₹');
