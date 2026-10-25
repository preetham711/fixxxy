# FIXXY Quick Setup Guide

## Prerequisites Checklist

- [ ] Python 3.7+ installed
- [ ] MySQL Server installed and running
- [ ] pip package manager available

## Quick Setup (5 Minutes)

### 1. Install Python Dependencies
```bash
cd fixxy-flask
pip install -r requirements.txt
```

### 2. Configure MySQL

Edit `app/config.py` (lines 10-14):
```python
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "YOUR_MYSQL_PASSWORD"  # Change this!
MYSQL_DATABASE = "fixxy_store"
```

### 3. Create Database

**Option A - Command Line:**
```bash
mysql -u root -p < database/schema.sql
```

**Option B - MySQL Workbench:**
1. Open MySQL Workbench
2. Connect to your MySQL server
3. File → Open SQL Script → Select `database/schema.sql`
4. Execute (⚡ Lightning icon)

### 4. Verify Database

```bash
mysql -u root -p
```
```sql
USE fixxy_store;
SHOW TABLES;
SELECT COUNT(*) FROM products;  -- Should show 22 products
SELECT * FROM users WHERE role='admin';  -- Should show admin user
EXIT;
```

### 5. Run the Application

```bash
python run.py
```

You should see:
```
======================================================================
FIXXY — Car Spare Parts & Billing Management System
======================================================================

Starting Flask development server...

  Local:   http://127.0.0.1:5000
  Network: http://0.0.0.0:5000

Press CTRL+C to quit
======================================================================
```

### 6. Open in Browser

Open Google Chrome and go to: **http://127.0.0.1:5000**

### 7. Login

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Or create a new customer account** using the "Create New Account" button.

## Test the System

### Customer Test:
1. Register new account
2. Browse "Find Parts"
3. Add 3-4 items to cart
4. Go to "Cart & Billing"
5. Apply coupon: `WELCOME10`
6. Click "Proceed to Checkout"
7. Fill details and place order
8. View invoice

### Admin Test:
1. Login as admin
2. View Dashboard
3. Go to Products → Add new product
4. Check Inventory for low stock
5. View Orders
6. Create a new coupon
7. Export reports to CSV

## Common Issues

### Issue 1: "Access denied for user 'root'"
**Fix:** Update password in `app/config.py` line 13

### Issue 2: "Unknown database 'fixxy_store'"
**Fix:** Run the SQL script: `mysql -u root -p < database/schema.sql`

### Issue 3: "ModuleNotFoundError: No module named 'flask'"
**Fix:** Run: `pip install -r requirements.txt`

### Issue 4: "Port 5000 is already in use"
**Fix:** Edit `run.py` line 19: change `port=5000` to `port=5001`

### Issue 5: MySQL not running
**Fix Windows:** Start MySQL service from Services app
**Fix:** Check status: `mysql --version` and verify it responds

## File Checklist

Verify these files exist:
```
✓ run.py
✓ requirements.txt
✓ database/schema.sql
✓ app/config.py
✓ app/__init__.py
✓ app/database.py
✓ app/routes/customer.py
✓ app/routes/admin.py
✓ app/templates/layout.html
✓ app/static/css/style.css
```

## Default Data Included

- 1 admin user (admin/admin123)
- 18 spare parts products
- 4 water wash services
- 3 active coupons (WELCOME10, SERVICE5, SUMMER15)
- 9 categories

## Next Steps

1. Change admin password (Settings page)
2. Add your own products
3. Configure shop name (Settings)
4. Adjust GST rate if needed (Settings)
5. Test the complete order flow
6. Explore admin reports

## Support

If you encounter issues:
1. Check error messages in terminal
2. Verify MySQL is running
3. Confirm all prerequisites are installed
4. Review README.md for detailed documentation

---
**Ready to start!** Run `python run.py` and open http://127.0.0.1:5000
