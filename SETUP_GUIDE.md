# FIXXY — Quick Setup Guide

## 🚀 Quick Start (5 Steps)

### Step 1: MySQL Setup

```powershell
# Start MySQL
Start-Service -Name MySQL80

# Create database
mysql -u root -p
```

In MySQL console:
```sql
CREATE DATABASE fixxy_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

Import schema:
```powershell
cd "c:\Users\preetham\Documents\py pj"
mysql -u root -p fixxy_store < database\schema.sql
```

### Step 2: Backend Setup

```powershell
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
Copy-Item .env.example .env
```

Edit `.env` file and set your MySQL password:
```
MYSQL_PASSWORD=your_actual_mysql_password
SECRET_KEY=generate_with_python_secrets_module
```

Generate SECRET_KEY:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Run Backend

```powershell
# From backend directory
uvicorn app.main:app --reload
```

Backend runs at: **http://localhost:8000**

API docs at: **http://localhost:8000/docs**

### Step 4: Frontend Setup

Open a NEW terminal:

```powershell
cd "c:\Users\preetham\Documents\py pj\frontend"

# Install dependencies
npm install
```

### Step 5: Run Frontend

```powershell
# From frontend directory
npm run dev
```

Frontend runs at: **http://localhost:5173**

### Step 6: Open Browser

Open **Google Chrome** and go to:
```
http://localhost:5173
```

---

## 👤 Demo Login Credentials

### Admin Account
- Username: `admin`
- Password: `admin123`

### Customer Account  
- Username: `customer`
- Password: `customer123`

---

## ✅ Verification Checklist

- [ ] MySQL service running
- [ ] Database `fixxy_store` created and schema imported
- [ ] Backend `.env` file configured
- [ ] Backend running on port 8000
- [ ] Backend API docs accessible at /docs
- [ ] Frontend dependencies installed
- [ ] Frontend running on port 5173
- [ ] Can open http://localhost:5173 in Chrome
- [ ] Can login with admin credentials

---

## 🐛 Common Issues

### "Access denied for user 'root'"
→ Check MySQL password in backend `.env` file

### "Unknown database 'fixxy_store'"  
→ Run the schema.sql import command

### "Port 8000 already in use"
→ Stop other process or change port in uvicorn command

### "Cannot find module" (Frontend)
→ Run `npm install` in frontend directory

### CORS errors
→ Check backend is running and CORS_ORIGINS in `.env` includes `http://localhost:5173`

---

## 📊 Features to Test

1. **Login** - Use admin/admin123
2. **Dashboard** - View statistics
3. **Products** - Browse spare parts catalog
4. **Cart** - Add items to cart
5. **Checkout** - Place an order
6. **Orders** - View order history
7. **Admin** - Manage products, inventory, coupons

---

## 📞 Need Help?

Check:
1. This guide
2. Main README.md
3. Backend API docs at /docs
4. Browser console for errors
5. Terminal for backend errors

---

**🚗 FIXXY — Drive Better • Fix Smarter**
