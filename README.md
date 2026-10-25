# FIXXY — Car Spare Parts & Billing Management System

**Drive Better • Fix Smarter**

A modern, professional web-based car spare parts and billing management system. Built for automotive service centers, spare parts shops, and car maintenance businesses.

---

## 🚗 Features

### Customer Features
- **User Authentication**: Secure login and registration with PBKDF2 password hashing
- **Dashboard**: Overview of available parts, services, and quick actions
- **Spare Parts Catalogue**: Searchable, filterable product catalog with categories
- **Vehicle Management**: Store and manage vehicle details (brand, model, year)
- **Shopping Cart**: Add products, adjust quantities, real-time calculations
- **Water Wash Services**: Professional car wash packages
- **Coupon System**: Apply discount coupons at checkout
- **GST Calculations**: Automatic tax computation
- **Order Management**: View order history and details
- **Invoice Generation**: Professional printable/downloadable invoices

### Admin Features
- **Admin Dashboard**: Business metrics, statistics, and insights
- **Product Management**: Add, edit, delete products
- **Inventory Control**: Stock tracking, low-stock alerts
- **Order Management**: View and manage all customer orders
- **Customer Management**: View customer information and order history
- **Coupon Management**: Create and manage discount coupons
- **Reports**: Sales reports, inventory reports, CSV export
- **Settings**: Configure shop details, GST rates, business information

---

## 🛠 Technology Stack

### Frontend
- **React** 18+ with Vite
- **React Router** for navigation
- **Axios** for API communication
- **Modern CSS** with responsive design
- **Lucide React** for icons

### Backend
- **FastAPI** (Python 3.8+)
- **MySQL** database
- **Pydantic** for data validation
- **JWT** authentication
- **Python-Jose** for token handling
- **Passlib** with bcrypt for password hashing
- **CORS** middleware for local development

### Database
- **MySQL** 8.0+
- Relational schema with foreign keys
- Proper indexing for performance

---

## 📁 Project Structure

```
FIXXY/
├── frontend/                # React application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── layouts/        # Layout components
│   │   ├── services/       # API service layer
│   │   ├── hooks/          # Custom React hooks
│   │   ├── utils/          # Utility functions
│   │   ├── assets/         # Static assets
│   │   ├── App.jsx         # Root component
│   │   └── main.jsx        # Entry point
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── core/           # Core utilities (auth, config)
│   │   ├── database.py     # Database connection
│   │   └── main.py         # FastAPI application
│   ├── requirements.txt
│   └── .env.example
│
├── database/
│   └── schema.sql          # MySQL schema
│
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites

1. **Python 3.8+**
2. **Node.js 16+** and npm
3. **MySQL 8.0+**

### Step 1: Clone or Extract Project

Navigate to the project directory:
```powershell
cd "c:\Users\preetham\Documents\py pj"
```

### Step 2: MySQL Setup

1. **Start MySQL** (if not running):
   ```powershell
   # Check if MySQL is running
   Get-Service -Name MySQL*
   
   # Start if stopped
   Start-Service -Name MySQL80
   ```

2. **Create Database**:
   ```powershell
   mysql -u root -p
   ```
   
   In MySQL console:
   ```sql
   CREATE DATABASE fixxy_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   EXIT;
   ```

3. **Import Schema**:
   ```powershell
   mysql -u root -p fixxy_store < database\schema.sql
   ```

### Step 3: Backend Setup

1. **Navigate to backend**:
   ```powershell
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   
   Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
   
   Edit `.env` and set your MySQL password:
   ```
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_mysql_password_here
   MYSQL_DATABASE=fixxy_store
   
   SECRET_KEY=your-secret-key-here-generate-with-openssl
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   ```

   **Generate a secure SECRET_KEY**:
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Run backend server**:
   ```powershell
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

   Backend will be available at: **http://localhost:8000**
   
   API documentation: **http://localhost:8000/docs**

### Step 4: Frontend Setup

Open a **new terminal** window.

1. **Navigate to frontend**:
   ```powershell
   cd "c:\Users\preetham\Documents\py pj\frontend"
   ```

2. **Install dependencies**:
   ```powershell
   npm install
   ```

3. **Run development server**:
   ```powershell
   npm run dev
   ```

   Frontend will be available at: **http://localhost:5173**

### Step 5: Access Application

Open **Google Chrome** and navigate to:
```
http://localhost:5173
```

---

## 👤 Demo Accounts

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`

### Test Customer Account
- **Username**: `customer`
- **Password**: `customer123`

*Note: These are demo accounts for testing. Change passwords before production use.*

---

## 📝 Environment Variables

### Backend (.env)

```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=fixxy_store

# JWT Authentication
SECRET_KEY=your-secret-key-generate-with-openssl
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS (for local development)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

---

## 🔧 Usage Guide

### Customer Workflow

1. **Register/Login**: Create an account or login
2. **Browse Parts**: Search and filter spare parts by category
3. **Add to Cart**: Select products and add to cart
4. **Water Wash**: Choose car wash services
5. **Apply Coupon**: Enter coupon code for discounts
6. **Checkout**: Fill in vehicle and customer details
7. **Select Payment**: Choose payment method
8. **Place Order**: Confirm and generate invoice
9. **View Orders**: Check order history and download invoices

### Admin Workflow

1. **Login as Admin**: Use admin credentials
2. **Dashboard**: View business metrics
3. **Manage Products**: Add/edit/delete spare parts
4. **Inventory**: Update stock levels, view low-stock items
5. **Orders**: View and manage customer orders
6. **Customers**: View customer information
7. **Coupons**: Create and manage discount coupons
8. **Reports**: Generate sales and inventory reports
9. **Settings**: Configure shop details and GST rates

---

## 🗄 Database Schema

### Tables

- **users**: Customer and admin accounts
- **products**: Spare parts and water wash services
- **categories**: Product categories
- **coupons**: Discount coupons
- **orders**: Customer orders
- **order_items**: Individual items in orders
- **vehicles**: Customer vehicle information
- **settings**: Application settings (shop name, GST, etc.)

See `database/schema.sql` for complete schema.

---

## 🐛 Troubleshooting

### Backend won't start

**Error**: `Access denied for user 'root'@'localhost'`
- **Solution**: Check MySQL password in `.env` file

**Error**: `Unknown database 'fixxy_store'`
- **Solution**: Create database: `CREATE DATABASE fixxy_store;`

**Error**: `ModuleNotFoundError`
- **Solution**: Install dependencies: `pip install -r requirements.txt`

### Frontend won't start

**Error**: `Cannot find module`
- **Solution**: Run `npm install` in frontend directory

**Error**: `Network Error` when calling API
- **Solution**: Ensure backend is running on port 8000

### CORS Errors

- **Solution**: Check `CORS_ORIGINS` in backend `.env` file includes `http://localhost:5173`

### MySQL Connection Issues

1. Check MySQL service is running:
   ```powershell
   Get-Service -Name MySQL*
   ```

2. Test connection:
   ```powershell
   mysql -u root -p -e "SELECT 1;"
   ```

3. Check port 3306 is not blocked by firewall

---

## 🔒 Security Notes

### For Production Deployment

1. **Change default passwords** for admin and demo accounts
2. **Use strong SECRET_KEY** (generate with `secrets.token_urlsafe(32)`)
3. **Enable HTTPS** with SSL certificates
4. **Restrict CORS origins** to your production domain
5. **Use environment variables** for all sensitive data
6. **Never commit** `.env` file to version control
7. **Update dependencies** regularly for security patches
8. **Use MySQL user** with limited privileges (not root)
9. **Enable MySQL SSL** connections
10. **Implement rate limiting** on API endpoints

---

## 📊 API Documentation

Once the backend is running, visit:
```
http://localhost:8000/docs
```

This provides interactive Swagger/OpenAPI documentation for all API endpoints.

---

## 🏗 Building for Production

### Frontend

```powershell
cd frontend
npm run build
```

Build output will be in `frontend/dist/`.

Deploy to:
- Netlify
- Vercel
- Static hosting (Nginx, Apache)

### Backend

```powershell
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Deploy to:
- AWS (EC2, Elastic Beanstalk)
- Google Cloud Platform
- Heroku
- DigitalOcean
- VPS with Nginx reverse proxy

### Database

- Use managed MySQL service (AWS RDS, Google Cloud SQL)
- Set up automated backups
- Enable SSL connections
- Use connection pooling

---

## 🎨 Customization

### Branding

Edit frontend colors in `frontend/src/App.css`:
- Primary color: `#ff7918` (FIXXY Orange)
- Background: `#071a2d` (Dark blue)
- Accent: `#43c58a` (Green)

### Business Information

Login as admin and go to **Settings** to update:
- Shop name
- GST rate
- Currency
- Business details

### Product Categories

Categories are stored in the database. Admin can add categories when creating products.

---

## 📄 License

This is a demonstration project created for educational purposes.

---

## 👥 Credits

**Original Project**: FIXXY Car Spare Parts & Billing System (Python + Tkinter)

**Web Version**: Modern React + FastAPI + MySQL implementation

---

## 📞 Support

For issues or questions:
1. Check this README
2. Review API documentation at `/docs`
3. Check browser console for frontend errors
4. Check terminal for backend errors

---

## 🗺 Roadmap

Future enhancements:
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Multi-location support
- [ ] Supplier management
- [ ] Purchase order system
- [ ] Email notifications
- [ ] SMS notifications
- [ ] WhatsApp integration
- [ ] Payment gateway integration
- [ ] Mobile app (React Native)

---

**Built with ❤️ for automotive service excellence**

🚗 **FIXXY** — Drive Better • Fix Smarter
