-- ============================================================================
-- FIXXY — Car Spare Parts & Billing Management System
-- MySQL Database Schema
-- ============================================================================

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS coupons;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS settings;

-- ============================================================================
-- USERS TABLE
-- Stores customer and admin accounts
-- ============================================================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NULL,
    address TEXT NULL,
    role ENUM('customer', 'admin') NOT NULL DEFAULT 'customer',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- CATEGORIES TABLE
-- Product categories for organization
-- ============================================================================
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- PRODUCTS TABLE
-- Spare parts and water wash services
-- ============================================================================
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK(price >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK(stock >= 0),
    description TEXT NULL,
    sold INT NOT NULL DEFAULT 0 CHECK(sold >= 0),
    image_url VARCHAR(500) NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_name (name),
    INDEX idx_category (category),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- VEHICLES TABLE
-- Customer vehicle information
-- ============================================================================
CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year VARCHAR(10) NULL,
    registration_number VARCHAR(50) NULL,
    is_primary BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- COUPONS TABLE
-- Discount coupons
-- ============================================================================
CREATE TABLE coupons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    discount DECIMAL(5,2) NOT NULL CHECK(discount >= 0 AND discount <= 100),
    description TEXT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    valid_from DATETIME NULL,
    valid_until DATETIME NULL,
    usage_limit INT NULL,
    usage_count INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_code (code),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ORDERS TABLE
-- Customer orders and bills
-- ============================================================================
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_no VARCHAR(100) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    car_brand VARCHAR(100) NULL,
    car_model VARCHAR(100) NULL,
    car_year VARCHAR(10) NULL,
    subtotal DECIMAL(10,2) NOT NULL CHECK(subtotal >= 0),
    discount DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK(discount >= 0),
    gst DECIMAL(10,2) NOT NULL CHECK(gst >= 0),
    grand_total DECIMAL(10,2) NOT NULL CHECK(grand_total >= 0),
    coupon_code VARCHAR(50) NULL,
    payment_method VARCHAR(100) NOT NULL,
    status ENUM('pending', 'confirmed', 'processing', 'completed', 'cancelled') NOT NULL DEFAULT 'confirmed',
    notes TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_bill_no (bill_no),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ORDER_ITEMS TABLE
-- Individual items in each order
-- ============================================================================
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK(price >= 0),
    quantity INT NOT NULL CHECK(quantity > 0),
    total DECIMAL(10,2) NOT NULL CHECK(total >= 0),
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL,
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SETTINGS TABLE
-- Application configuration
-- ============================================================================
CREATE TABLE settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT NOT NULL,
    description TEXT NULL,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_setting_key (setting_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SEED DATA
-- ============================================================================

-- Insert default categories
INSERT INTO categories (name, description) VALUES
('Filters', 'Engine and cabin filters'),
('Brakes', 'Brake pads, rotors and components'),
('Engine Parts', 'Engine components and accessories'),
('Electrical', 'Electrical systems and components'),
('Transmission', 'Transmission and clutch parts'),
('Suspension', 'Suspension and steering components'),
('Accessories', 'Car accessories and add-ons'),
('Cooling', 'Cooling system components'),
('Water Wash', 'Car washing and detailing services');

-- Insert default admin user
-- Username: admin
-- Password: admin123
INSERT INTO users (username, password_hash, full_name, role, phone, address) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIwNoLtg3G', 'FIXXY Administrator', 'admin', '9876543210', 'FIXXY Headquarters');

-- Insert demo customer user
-- Username: customer
-- Password: customer123
INSERT INTO users (username, password_hash, full_name, role, phone, address) VALUES
('customer', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Demo Customer', 'customer', '9876543211', 'Customer Address, City');

-- Insert default spare parts
INSERT INTO products (name, category, price, stock, description, sold) VALUES
('Oil Filter', 'Filters', 450.00, 30, 'Engine oil filtration for optimal performance', 0),
('Air Filter', 'Filters', 650.00, 25, 'Cleans air entering the engine', 0),
('Brake Pads', 'Brakes', 1800.00, 18, 'Friction pads for safe braking', 0),
('Spark Plug', 'Engine Parts', 350.00, 50, 'Ignition component for combustion', 0),
('Battery', 'Electrical', 4500.00, 12, 'Automotive battery 12V', 0),
('Timing Belt', 'Engine Parts', 1200.00, 15, 'Engine timing belt', 0),
('Alternator', 'Electrical', 6500.00, 8, 'Charges battery while driving', 0),
('Water Pump', 'Engine Parts', 3200.00, 10, 'Engine coolant circulation pump', 0),
('Clutch Plate', 'Transmission', 2800.00, 11, 'Clutch assembly component', 0),
('Shock Absorber', 'Suspension', 2400.00, 16, 'Suspension damping component', 0),
('Headlight Bulb', 'Electrical', 550.00, 40, 'Replacement headlight bulb (H4/H7)', 0),
('Wiper Blades', 'Accessories', 700.00, 22, 'Windshield wiper blades (pair)', 0),
('Radiator', 'Cooling', 5200.00, 7, 'Engine cooling radiator', 0),
('Fuel Pump', 'Engine Parts', 3900.00, 9, 'Fuel delivery component', 0),
('Wheel Bearing', 'Suspension', 1450.00, 20, 'Wheel rotation bearing', 0),
('Cabin Air Filter', 'Filters', 800.00, 24, 'Filters air entering cabin', 0),
('Disc Rotor', 'Brakes', 2100.00, 13, 'Brake disc rotor', 0),
('Fuse Set', 'Electrical', 250.00, 60, 'Automotive replacement fuses', 0);

-- Insert water wash services
INSERT INTO products (name, category, price, stock, description, sold) VALUES
('Full Clean', 'Water Wash', 499.00, 99999, 'Exterior wash, wheel cleaning and basic interior wipe', 0),
('Foam Wash', 'Water Wash', 699.00, 99999, 'Snow foam pre-wash, rinse and microfiber dry', 0),
('Premium Foam + Wax', 'Water Wash', 999.00, 99999, 'Foam wash, wax finish and tyre shine', 0),
('Interior Deep Clean', 'Water Wash', 1299.00, 99999, 'Seats, mats, dashboard and interior vacuum', 0);

-- Insert default coupons
INSERT INTO coupons (code, discount, description, active) VALUES
('WELCOME10', 10.00, 'Welcome discount for new customers', TRUE),
('SERVICE5', 5.00, 'Service customer discount', TRUE),
('FIXXY15', 15.00, 'Special FIXXY discount', TRUE);

-- Insert default settings
INSERT INTO settings (setting_key, setting_value, description) VALUES
('shop_name', 'FIXXY Car Spares', 'Name of the shop'),
('shop_tagline', 'Drive Better • Fix Smarter', 'Shop tagline'),
('gst_rate', '18', 'GST rate percentage'),
('currency', 'INR', 'Currency code'),
('currency_symbol', '₹', 'Currency symbol'),
('phone', '+91 98765 43210', 'Shop contact phone'),
('email', 'contact@fixxy.com', 'Shop contact email'),
('address', 'FIXXY Headquarters, Automotive District', 'Shop address');

-- Insert default vehicle for demo customer
INSERT INTO vehicles (user_id, brand, model, year, is_primary) VALUES
(2, 'Toyota', 'Innova', '2020', TRUE);

-- ============================================================================
-- VIEWS
-- ============================================================================

-- View for low stock products
CREATE OR REPLACE VIEW low_stock_products AS
SELECT 
    id,
    name,
    category,
    price,
    stock,
    sold,
    description
FROM products
WHERE stock < 10 
  AND category != 'Water Wash'
  AND active = TRUE
ORDER BY stock ASC;

-- View for product sales statistics
CREATE OR REPLACE VIEW product_sales_stats AS
SELECT 
    p.id,
    p.name,
    p.category,
    p.price,
    p.stock,
    p.sold,
    COALESCE(SUM(oi.quantity), 0) AS total_orders,
    COALESCE(SUM(oi.total), 0) AS total_revenue
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
WHERE p.active = TRUE
GROUP BY p.id, p.name, p.category, p.price, p.stock, p.sold
ORDER BY total_revenue DESC;

-- ============================================================================
-- STORED PROCEDURES
-- ============================================================================

DELIMITER //

-- Procedure to place an order (with transaction safety)
CREATE PROCEDURE place_order(
    IN p_bill_no VARCHAR(100),
    IN p_user_id INT,
    IN p_customer_name VARCHAR(255),
    IN p_phone VARCHAR(50),
    IN p_address TEXT,
    IN p_car_brand VARCHAR(100),
    IN p_car_model VARCHAR(100),
    IN p_car_year VARCHAR(10),
    IN p_subtotal DECIMAL(10,2),
    IN p_discount DECIMAL(10,2),
    IN p_gst DECIMAL(10,2),
    IN p_grand_total DECIMAL(10,2),
    IN p_coupon_code VARCHAR(50),
    IN p_payment_method VARCHAR(100),
    OUT p_order_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_order_id = -1;
    END;

    START TRANSACTION;
    
    INSERT INTO orders (
        bill_no, user_id, customer_name, phone, address,
        car_brand, car_model, car_year,
        subtotal, discount, gst, grand_total,
        coupon_code, payment_method
    ) VALUES (
        p_bill_no, p_user_id, p_customer_name, p_phone, p_address,
        p_car_brand, p_car_model, p_car_year,
        p_subtotal, p_discount, p_gst, p_grand_total,
        p_coupon_code, p_payment_method
    );
    
    SET p_order_id = LAST_INSERT_ID();
    
    COMMIT;
END //

DELIMITER ;

-- ============================================================================
-- TRIGGERS
-- ============================================================================

DELIMITER //

-- Update product sold count when order item is inserted
CREATE TRIGGER after_order_item_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE products 
    SET sold = sold + NEW.quantity,
        stock = CASE 
            WHEN category != 'Water Wash' THEN stock - NEW.quantity
            ELSE stock
        END
    WHERE id = NEW.product_id;
END //

-- Prevent negative stock
CREATE TRIGGER before_product_stock_update
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
    IF NEW.stock < 0 AND NEW.category != 'Water Wash' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stock cannot be negative';
    END IF;
END //

DELIMITER ;

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Additional composite indexes
CREATE INDEX idx_products_category_active ON products(category, active);
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);
CREATE INDEX idx_order_items_product ON order_items(product_id, order_id);

-- Full-text search indexes
ALTER TABLE products ADD FULLTEXT INDEX idx_product_search (name, description);

-- ============================================================================
-- SCHEMA COMPLETE
-- Database: fixxy_store
-- Version: 1.0
-- Created for: FIXXY Car Spare Parts & Billing Management System
-- ============================================================================
