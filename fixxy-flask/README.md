# FIXXY — Car Spare Parts & Billing Management System

A complete Python Flask web application for automotive spare parts shop management with customer billing, inventory tracking, order management, and administrative controls.

## 🚀 Features

### Customer Features
- **User Registration & Authentication** - Secure login with password hashing
- **Product Catalogue** - Browse spare parts with search and category filtering
- **Shopping Cart** - Add/update/remove items with live total calculation
- **Coupon System** - Apply discount coupons at checkout
- **Water Wash Services** - Book car wash packages
- **Checkout & Billing** - Complete order placement with GST calculation
- **Order History** - View past orders and invoices
- **Vehicle Management** - Save vehicle details for faster checkout
- **Invoice Generation** - Printable/downloadable invoices

### Admin Features
- **Dashboard** - Real-time statistics and key metrics
- **Product Management** - Add, edit, delete products
- **Inventory Control** - Track stock levels and low stock alerts
- **Order Management** - View all orders and customer details
- **Customer Management** - View registered customers and their order history
- **Coupon Management** - Create and manage discount coupons
- **Reports & Analytics** - Sales reports, category-wise analysis, CSV export
- **Settings** - Configure GST rate and shop information

## 🛠 Technology Stack

- **Backend**: Python 3.x + Flask
- **Frontend**: Jinja2 Templates + HTML + CSS
- **Database**: MySQL
- **Authentication**: PBKDF2-SHA256 password hashing
- **Session Management**: Flask-Session

## 📋 Prerequisites

Before running FIXXY, ensure you have:

1. **Python 3.7 or higher**
   ```bash
   python --version
   ```

2. **MySQL Server** (running on localhost:3306)
   - Download from https://dev.mysql.com/downloads/mysql/
   - Ensure MySQL service is running

3. **pip** (Python package manager)
   ```bash
   pip --version
   ```

## 🔧 Installation & Setup

### Step 1: Clone or Extract the Project
```bash
cd fixxy-flask
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- Flask==3.0.0
- Flask-Session==0.5.0
- mysql-connector-python==8.2.0

### Step 3: Configure Database

1. **Update MySQL credentials** in `app/config.py`:
   ```python
   MYSQL_USER = "root"
   MYSQL_PASSWORD = "your_mysql_password"
   ```

2. **Create the database**:
   - Option A: Run the SQL script manually:
     ```bash
     mysql -u root -p < database/schema.sql
     ```
   
   - Option B: Use MySQL Workbench:
     - Open `database/schema.sql`
     - Execute the script

3. **Verify database creation**:
   ```bash
   mysql -u root -p
   USE fixxy_store;
   SHOW TABLES;
   ```

### Step 4: Run the Application
```bash
python run.py
```

The application will start on:
- **Local**: http://127.0.0.1:5000
- **Network**: http://0.0.0.0:5000

Open **Google Chrome** and navigate to http://127.0.0.1:5000

## 👤 Default Admin Login

After database setup, use these credentials to login as admin:

- **Username**: `admin`
- **Password**: `admin123`

**⚠️ Important**: Change the admin password in production!

## 📚 Usage Guide

### For Customers:

1. **Register** - Create a new account from the login page
2. **Browse Parts** - Search and filter spare parts by category
3. **Add to Cart** - Select quantity and add items to cart
4. **Apply Coupons** - Enter coupon codes for discounts (try: WELCOME10)
5. **Checkout** - Fill in customer and vehicle details
6. **Place Order** - Choose payment method and confirm
7. **View Invoice** - Print or save your bill

### For Admins:

1. **Login** as admin
2. **Dashboard** - Monitor sales, stock, and orders
3. **Products** - Add new products or update existing ones
4. **Inventory** - Update stock levels
5. **Orders** - View all customer orders
6. **Coupons** - Create promotional discount codes
7. **Reports** - Export data and view analytics
8. **Settings** - Configure GST rate and shop name

## 🗂 Project Structure

```
fixxy-flask/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config.py             # Configuration settings
│   ├── database.py           # Database utilities
│   ├── auth_utils.py         # Authentication helpers
│   ├── utils.py              # Utility functions
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py           # Landing page routes
│   │   ├── auth.py           # Login/registration routes
│   │   ├── customer.py       # Customer routes
│   │   └── admin.py          # Admin routes
│   ├── templates/
│   │   ├── base.html         # Base template
│   │   ├── layout.html       # Layout with sidebar
│   │   ├── auth/             # Authentication templates
│   │   ├── customer/         # Customer pages
│   │   └── admin/            # Admin pages
│   └── static/
│       └── css/
│           └── style.css     # Professional styling
├── database/
│   └── schema.sql            # Database schema
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🎨 Design

FIXXY features a modern, professional automotive-themed interface with:
- Clean dark theme with orange accents
- Responsive layout for desktop, tablet, and mobile
- Professional typography and spacing
- Intuitive navigation with sidebar menu
- Card-based dashboard widgets
- Professional invoice templates

## 💾 Database Schema

The application uses MySQL with the following main tables:

- **users** - Customer and admin accounts
- **products** - Spare parts and services
- **categories** - Product categories
- **orders** - Customer orders
- **order_items** - Individual items in orders
- **coupons** - Discount codes
- **vehicles** - Customer vehicle information
- **settings** - Application configuration

## 🔒 Security Features

- **Password Hashing**: PBKDF2-SHA256 with 180,000 iterations
- **Session Management**: Secure server-side sessions
- **SQL Injection Protection**: Parameterized queries
- **CSRF Protection**: Built-in Flask protection
- **Role-Based Access**: Customer and admin roles
- **Admin Route Protection**: Decorator-based authorization

## 🛡 Database Transactions

Order placement uses atomic transactions to ensure:
- Stock validation before order creation
- All-or-nothing order processing
- Automatic rollback on any failure
- Concurrent stock update handling

## 🧪 Testing the Application

### Test Customer Flow:
1. Register a new account
2. Add a vehicle (e.g., Toyota Innova 2020)
3. Browse spare parts
4. Add 3-4 products to cart
5. Apply coupon code: `WELCOME10`
6. Complete checkout
7. View order and print invoice

### Test Admin Flow:
1. Login as admin
2. Check dashboard statistics
3. Add a new product
4. Update stock for low-stock items
5. View customer orders
6. Create a new coupon (e.g., SUMMER15 for 15% off)
7. Export reports

## 📊 Sample Data

The database includes:
- **18 pre-loaded spare parts** across 8 categories
- **4 water wash service packages**
- **3 default coupon codes**:
  - `WELCOME10` - 10% discount
  - `SERVICE5` - 5% discount
  - `SUMMER15` - 15% discount

## ⚙️ Configuration

Edit `app/config.py` to customize:
- MySQL connection settings
- GST rate (default 18%)
- Payment methods
- Application name and tagline

## 🐛 Troubleshooting

### Issue: Cannot connect to MySQL
**Solution**: 
- Verify MySQL is running: `mysql --version`
- Check credentials in `app/config.py`
- Ensure MySQL port 3306 is not blocked

### Issue: Database tables not created
**Solution**:
- Manually run: `mysql -u root -p < database/schema.sql`
- Verify database exists: `SHOW DATABASES;`

### Issue: ModuleNotFoundError
**Solution**:
- Reinstall dependencies: `pip install -r requirements.txt`
- Use virtual environment

### Issue: Port 5000 already in use
**Solution**:
- Change port in `run.py`: `app.run(port=5001)`
- Or stop the conflicting service

## 📝 Notes

- This is a local development project for educational purposes
- Payment processing is simulated (no real transactions)
- The admin password should be changed in production
- Session data is stored in filesystem (not suitable for production scale)

## 🔄 Migrating from Tkinter Version

This Flask application is a complete rebuild of the original Tkinter application with:
- Web-based interface instead of desktop GUI
- Modern responsive design
- Same business logic and features
- Enhanced admin controls
- Better scalability

## 📖 Further Development

Potential enhancements:
- Email notifications for orders
- SMS integration for order status
- PDF invoice generation (using ReportLab)
- Image upload for products
- Advanced search with filters
- Customer reviews and ratings
- Multi-language support
- Real payment gateway integration

## 📄 License

This project is for educational purposes.

## 👨‍💻 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all prerequisites are installed
3. Review error messages in the terminal
4. Ensure MySQL service is running

---

**FIXXY** — Drive Better • Fix Smarter
