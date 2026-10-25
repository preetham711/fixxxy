# FIXXY Testing & Verification Guide

This guide helps you test all features of the FIXXY application.

## Initial Setup Test

### 1. Database Connection Test
```bash
python -c "from app.database import Database; print('✓ Database connected!' if Database.get_connection() else '✗ Connection failed')"
```

### 2. Verify Tables
```sql
mysql -u root -p fixxy_store -e "SHOW TABLES;"
```
Expected: 8 tables (users, products, categories, coupons, vehicles, orders, order_items, settings)

### 3. Check Sample Data
```sql
mysql -u root -p fixxy_store -e "SELECT COUNT(*) as product_count FROM products; SELECT COUNT(*) as coupon_count FROM coupons; SELECT username, role FROM users;"
```

## Feature Testing Checklist

### Authentication Tests

#### Test 1: Admin Login
- [ ] Go to http://127.0.0.1:5000
- [ ] Enter username: `admin`, password: `admin123`
- [ ] Should redirect to Admin Dashboard
- [ ] Verify admin menu items visible (Products, Inventory, Orders, etc.)

#### Test 2: Customer Registration
- [ ] Click "Create New Account"
- [ ] Fill in:
  - Full Name: Test Customer
  - Username: testuser
  - Phone: 9876543210
  - Password: test123
- [ ] Should create account and show success message
- [ ] Should redirect to login page

#### Test 3: Customer Login
- [ ] Login with username: `testuser`, password: `test123`
- [ ] Should redirect to Customer Dashboard
- [ ] Verify customer menu visible (Find Parts, Cart, Orders, etc.)

#### Test 4: Logout
- [ ] Click "Logout" in sidebar
- [ ] Should redirect to login page
- [ ] Should clear session

### Customer Flow Tests

#### Test 5: Browse Products
- [ ] Login as customer
- [ ] Click "Find Parts"
- [ ] Verify products display in grid
- [ ] Check product cards show:
  - Product name
  - Category
  - Price
  - Stock status
  - Description
  - Add to Cart button

#### Test 6: Search and Filter
- [ ] In "Find Parts", enter search: "filter"
- [ ] Should show only filter products (Oil Filter, Air Filter, Cabin Air Filter)
- [ ] Select category: "Brakes"
- [ ] Should show only brake products
- [ ] Click "Clear" - should show all products

#### Test 7: Add to Cart
- [ ] Click "Add to Cart" on "Oil Filter"
- [ ] Should show success message
- [ ] Cart badge should show "1" (or total quantity)
- [ ] Add 2 more different products
- [ ] Cart badge should update

#### Test 8: View and Manage Cart
- [ ] Click "Cart & Billing" in sidebar
- [ ] Verify all added products appear in table
- [ ] Change quantity of first product to 2
- [ ] Click "Update" - quantity should change, total should update
- [ ] Click "Remove" on one product - should be removed from cart

#### Test 9: Apply Coupon
- [ ] In Cart page, enter coupon: `WELCOME10`
- [ ] Click "Apply"
- [ ] Should show success message
- [ ] Discount should show 10% reduction
- [ ] Grand total should reflect discount

#### Test 10: Checkout Process
- [ ] Click "Proceed to Checkout"
- [ ] Fill in customer details:
  - Name: John Doe
  - Phone: 9876543210
  - Address: 123 Main Street, Mumbai
- [ ] Fill vehicle details:
  - Brand: Toyota
  - Model: Innova
  - Year: 2020
- [ ] Select payment method: UPI QR
- [ ] Click "CONFIRM & GENERATE BILL"
- [ ] Should redirect to invoice page

#### Test 11: Invoice Verification
- [ ] Verify invoice shows:
  - Bill number (starts with FX)
  - Customer details
  - Vehicle details
  - All ordered products with quantities
  - Subtotal, Discount, GST, Grand Total
  - Payment method
- [ ] Click "Print Invoice" - print dialog should open
- [ ] Go back to "My Orders" - order should appear in list

#### Test 12: Water Wash Services
- [ ] Click "Water Wash" in sidebar
- [ ] Verify 4 services displayed
- [ ] Click "Add package to cart" on "Foam Wash"
- [ ] Go to Cart - service should be in cart
- [ ] Complete checkout with water wash service

#### Test 13: Vehicle Management
- [ ] Click "My Vehicles" in sidebar
- [ ] Add a new vehicle:
  - Brand: Honda
  - Model: City
  - Year: 2021
  - Registration: MH12AB1234
- [ ] Vehicle should appear in the list
- [ ] Add another vehicle
- [ ] Both should be visible

### Admin Flow Tests

#### Test 14: Admin Dashboard
- [ ] Login as admin
- [ ] Verify dashboard shows:
  - Total Products count
  - Total Stock count
  - Low Stock Items count
  - Total Orders count
  - Total Revenue
  - Total Customers count
- [ ] Verify "Low Stock Alert" table appears if items < 10 stock
- [ ] Verify "Recent Orders" table shows orders

#### Test 15: Product Management
- [ ] Click "Products" in admin menu
- [ ] Verify products list appears
- [ ] Click "Add New Product"
- [ ] Fill in:
  - Name: Test Part
  - Category: Engine Parts
  - Price: 1500
  - Stock: 20
  - Description: Test description
- [ ] Click "Add Product"
- [ ] Product should appear in products list

#### Test 16: Edit Product
- [ ] In Products list, click "Edit" on "Test Part"
- [ ] Change price to 1600
- [ ] Change stock to 25
- [ ] Click "Update Product"
- [ ] Verify changes in products list

#### Test 17: Delete Product
- [ ] Click "Delete" on "Test Part"
- [ ] Confirm deletion
- [ ] Product should be marked inactive (hidden from customer view)

#### Test 18: Inventory Management
- [ ] Click "Inventory" in admin menu
- [ ] Verify all products listed with current stock
- [ ] Find a product with stock < 10 (should be highlighted in red)
- [ ] Update stock to 50
- [ ] Verify stock updated

#### Test 19: View Orders
- [ ] Click "Orders" in admin menu
- [ ] Verify all orders from all customers appear
- [ ] Click "View" on any order
- [ ] Verify full order details and invoice display

#### Test 20: Customer Management
- [ ] Click "Customers" in admin menu
- [ ] Verify list shows:
  - Customer names
  - Usernames
  - Phone numbers
  - Order count per customer
  - Total amount spent per customer

#### Test 21: Coupon Management
- [ ] Click "Coupons" in admin menu
- [ ] Create new coupon:
  - Code: TEST20
  - Discount: 20
  - Description: Test 20% discount
- [ ] Click "Save"
- [ ] Coupon should appear in list as "Active"
- [ ] Click "Toggle" to deactivate
- [ ] Status should change to "Inactive"
- [ ] Click "Toggle" again to reactivate

#### Test 22: Reports and Analytics
- [ ] Click "Reports" in admin menu
- [ ] Verify "Category-wise Sales" table
- [ ] Verify "Monthly Revenue" table
- [ ] Click "Export Products CSV"
- [ ] CSV file should download with all products
- [ ] Click "Export Orders CSV"
- [ ] CSV file should download with all orders

#### Test 23: Settings
- [ ] Click "Settings" in admin menu
- [ ] Change shop name to "FIXXY Premium Spares"
- [ ] Change GST rate to 15
- [ ] Click "Save Settings"
- [ ] Verify success message
- [ ] Place a new order and verify GST is calculated at 15%

### Security Tests

#### Test 24: Unauthorized Access
- [ ] Logout
- [ ] Try to access: http://127.0.0.1:5000/admin/dashboard
- [ ] Should redirect to login page with warning message

#### Test 25: Customer Cannot Access Admin
- [ ] Login as customer
- [ ] Try to access: http://127.0.0.1:5000/admin/products
- [ ] Should redirect to customer dashboard with error message

#### Test 26: Session Management
- [ ] Login as customer
- [ ] Close browser
- [ ] Open browser and go to site
- [ ] Should require login again (session expired)

### Edge Cases Tests

#### Test 27: Empty Cart Checkout
- [ ] Clear entire cart
- [ ] Try to click "Proceed to Checkout"
- [ ] Should show warning "Cart is empty"

#### Test 28: Out of Stock Product
- [ ] As admin, set a product stock to 0
- [ ] As customer, try to add that product to cart
- [ ] Should show "Out of stock" warning

#### Test 29: Invalid Coupon
- [ ] Add products to cart
- [ ] Enter coupon: `INVALID123`
- [ ] Click "Apply"
- [ ] Should show "Invalid or inactive coupon" error

#### Test 30: Stock Limit in Cart
- [ ] Add a product with stock = 5
- [ ] Try to set quantity to 10 in cart
- [ ] Should limit to maximum available stock (5)

### Performance Tests

#### Test 31: Multiple Products Load
- [ ] Go to "Find Parts"
- [ ] Verify all 18+ products load quickly
- [ ] No errors in browser console (F12)

#### Test 32: Database Transaction Test
- [ ] Add 5 products to cart
- [ ] Place order
- [ ] Verify:
  - Order created in database
  - All order items saved
  - Stock reduced for each product
  - If any step fails, entire order should rollback

## Expected Results Summary

### Successful Setup Indicators:
- ✓ All pages load without errors
- ✓ Images and CSS load properly
- ✓ Database queries execute successfully
- ✓ Cart calculations are accurate
- ✓ Orders save correctly
- ✓ Invoices display properly
- ✓ Admin functions work
- ✓ Authentication prevents unauthorized access

### Test Completion:
- Run all 32 tests
- Check off each passed test
- Note any failures with details
- Verify no errors in browser console
- Confirm no MySQL errors in terminal

## Troubleshooting Failed Tests

### If products don't display:
- Check `SELECT * FROM products WHERE active=1` in MySQL
- Verify images/CSS are loading (F12 → Network tab)

### If cart doesn't update:
- Check browser console for JavaScript errors
- Verify session is working: `flask_session/` folder exists

### If orders fail:
- Check MySQL user has INSERT, UPDATE permissions
- Verify transaction support: `SHOW ENGINES;` (InnoDB should be supported)

### If coupon doesn't apply:
- Verify coupon exists: `SELECT * FROM coupons WHERE code='WELCOME10'`
- Check active=1 for the coupon

## Success Criteria

All tests should pass with:
- ✓ No 404 errors
- ✓ No 500 errors  
- ✓ No database connection errors
- ✓ Calculations are mathematically correct
- ✓ Data persists correctly
- ✓ Security controls work as expected

---
**Testing Complete!** The FIXXY application is ready for use.
