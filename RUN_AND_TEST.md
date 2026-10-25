# 🚀 FIXXY - Run and Test Guide

## Quick Start - Let's Test Both Logins!

Follow these steps exactly to run and test the application.

---

## Step 1: Start MySQL (1 minute)

```powershell
# Check MySQL status
Get-Service -Name MySQL* | Select-Object Name, Status

# If not running, start it
Start-Service -Name MySQL80

# Verify it's running
Get-Service -Name MySQL80
```

✅ **Expected:** Status = Running

---

## Step 2: Verify Database (2 minutes)

```powershell
# Connect to MySQL
mysql -u root -p
# Enter your MySQL password when prompted
```

In MySQL console:
```sql
-- Check database exists
SHOW DATABASES LIKE 'fixxy_store';

-- Use database
USE fixxy_store;

-- Verify users exist
SELECT id, username, role, full_name FROM users;
```

✅ **Expected Output:**
```
+----+----------+----------+------------------------+
| id | username | role     | full_name              |
+----+----------+----------+------------------------+
|  1 | admin    | admin    | FIXXY Administrator    |
|  2 | customer | customer | Demo Customer          |
+----+----------+----------+------------------------+
```

If you see this, type `EXIT;` and continue.

**If database doesn't exist:**
```sql
CREATE DATABASE fixxy_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

Then import schema:
```powershell
cd "c:\Users\preetham\Documents\py pj"
mysql -u root -p fixxy_store < database\schema.sql
```

---

## Step 3: Start Backend Server (2 minutes)

Open **Terminal 1** (PowerShell):

```powershell
# Navigate to backend
cd "c:\Users\preetham\Documents\py pj\backend"

# Install dependencies (first time only)
pip install -r requirements.txt
```

**Configure .env file:**
```powershell
# Copy example
Copy-Item .env.example .env -Force

# Edit .env
notepad .env
```

**Edit these values in .env:**
```
MYSQL_PASSWORD=your_actual_mysql_password_here
SECRET_KEY=your-secret-key-generate-below
```

**Generate SECRET_KEY:**
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Copy the output and paste it as SECRET_KEY in .env

**Start the backend:**
```powershell
uvicorn app.main:app --reload
```

✅ **Expected Output:**
```
🚗 FIXXY API Starting...
Version: 1.0.0
Environment: Development
Database: fixxy_store @ localhost:3306
======================================================================
✅ Database connection successful
======================================================================
📚 API Documentation: http://localhost:8000/docs
======================================================================

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Test Backend:**
Open browser: http://localhost:8000/health

Should see:
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

✅ **Backend is ready!**

---

## Step 4: Start Frontend Server (2 minutes)

Open **NEW Terminal 2** (PowerShell):

```powershell
# Navigate to frontend
cd "c:\Users\preetham\Documents\py pj\frontend"

# Install dependencies (first time only)
npm install
```

**Start the frontend:**
```powershell
npm run dev
```

✅ **Expected Output:**
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

Browser should automatically open to: **http://localhost:5173**

You should see the **FIXXY login page**.

✅ **Frontend is ready!**

---

## Step 5: Test Customer Login ✅

### Test Customer Login
1. **Username:** `customer`
2. **Password:** `customer123`
3. **Click:** LOGIN

### ✅ Expected Behavior:
- Loading indicator appears
- URL changes to: `http://localhost:5173/dashboard`
- You see **Customer Dashboard** with:
  - "Welcome back, Demo Customer!"
  - Statistics cards (Spare Parts, Units Available, Wash Packages)
  - Customer menu items:
    - Dashboard (active)
    - Find Parts
    - Cart & Billing
    - Water Wash
    - Orders
  - NO admin menu items
  - NO "ADMIN" badge

### ✅ What You Should See:
```
================================
       FIXXY Dashboard
================================
Welcome back, Demo Customer!

Statistics:
[Spare Parts]  [Units Available]  [Wash Packages]
     18               500+              4

Quick Actions:
- Find Parts
- Water Wash
```

**If this works, the customer login is successful!** ✅

---

## Step 6: Test Admin Login ✅

### Logout First
1. **Click:** Logout button at bottom of sidebar
2. You return to login page

### Test Admin Login
1. **Username:** `admin`
2. **Password:** `admin123`
3. **Click:** LOGIN

### ✅ Expected Behavior:
- Loading indicator appears
- URL changes to: `http://localhost:5173/admin`
- You see **Admin Dashboard** with:
  - "Welcome back, FIXXY Administrator!"
  - **🔐 ADMIN** badge in top-right corner
  - Advanced statistics:
    - Total Products
    - Total Stock
    - Low Stock Items (red)
    - Total Orders
    - Total Revenue (₹)
  - Recent Orders table
  - Admin menu items:
    - ADMIN section
    - Dashboard (active)
    - Products
    - Inventory
    - Orders
    - Coupons
    - Settings
    - CUSTOMER VIEW section
    - Customer Dashboard link

### ✅ What You Should See:
```
================================
    Admin Dashboard    🔐 ADMIN
================================
Welcome back, FIXXY Administrator!

Statistics:
[Total Products] [Total Stock] [Low Stock] [Total Orders] [Total Revenue]
      18             500+           2            0            ₹0.00

Recent Orders:
(table showing orders, or "No orders yet")

Quick Actions:
- Add Product
- Update Stock
- Manage Coupons
```

**If this works, the admin login is successful!** ✅

---

## Step 7: Verify Role-Based Access

### Test 1: Admin Can't Access Customer URL Directly
1. While logged in as admin
2. Manually type in browser: `http://localhost:5173/dashboard`
3. ✅ **Expected:** Redirects back to `/admin`

### Test 2: Customer Can't Access Admin URL Directly
1. Logout from admin
2. Login as customer
3. Manually type in browser: `http://localhost:5173/admin`
4. ✅ **Expected:** Redirects to `/dashboard`

### Test 3: Unauthenticated Can't Access Protected Pages
1. Logout completely
2. Manually type: `http://localhost:5173/dashboard`
3. ✅ **Expected:** Redirects to `/login`

---

## Step 8: Browser Console Verification

Open **Chrome DevTools** (Press F12)

### Check localStorage After Login

**After logging in as admin:**
```javascript
// In Console tab, type:
localStorage.getItem('token')
// Should show JWT token

JSON.parse(localStorage.getItem('user'))
// Should show:
// {
//   id: 1,
//   username: "admin",
//   role: "admin",
//   full_name: "FIXXY Administrator"
// }
```

**After logging in as customer:**
```javascript
JSON.parse(localStorage.getItem('user'))
// Should show:
// {
//   id: 2,
//   username: "customer",
//   role: "customer",
//   full_name: "Demo Customer"
// }
```

### Check Network Requests

1. Open **Network tab** in DevTools
2. Filter by **XHR**
3. Login as admin
4. You should see:
   - `POST /api/auth/login` → Status 200
   - Response contains `access_token` and `user` object
   - `GET /api/products` → Status 200
   - `GET /api/orders/statistics/dashboard` → Status 200

---

## Step 9: Test Login Errors

### Test 1: Wrong Password
1. Logout
2. Username: `admin`
3. Password: `wrongpassword`
4. Click LOGIN
5. ✅ **Expected:** Error message "Incorrect username or password"

### Test 2: Wrong Username
1. Username: `wronguser`
2. Password: `admin123`
3. Click LOGIN
4. ✅ **Expected:** Error message "Incorrect username or password"

### Test 3: Empty Fields
1. Leave username empty
2. Click LOGIN
3. ✅ **Expected:** Browser validation error

---

## 🎯 Complete Test Checklist

Run through this checklist:

### Backend Tests
- [ ] MySQL service running
- [ ] Database `fixxy_store` exists
- [ ] Users table has admin and customer
- [ ] Backend starts without errors
- [ ] Health check returns healthy status
- [ ] API docs load at /docs

### Frontend Tests
- [ ] Frontend starts without errors
- [ ] Login page displays correctly
- [ ] FIXXY branding shows

### Customer Login Tests
- [ ] Can login with customer/customer123
- [ ] Redirects to /dashboard
- [ ] Shows "Welcome back, Demo Customer"
- [ ] Shows customer statistics
- [ ] Shows customer menu only
- [ ] Does NOT show admin menu
- [ ] Does NOT show ADMIN badge
- [ ] Can logout

### Admin Login Tests
- [ ] Can login with admin/admin123
- [ ] Redirects to /admin
- [ ] Shows "Welcome back, FIXXY Administrator"
- [ ] Shows 🔐 ADMIN badge
- [ ] Shows advanced statistics
- [ ] Shows Recent Orders table
- [ ] Shows admin menu
- [ ] Shows "Customer Dashboard" link
- [ ] Can logout

### Security Tests
- [ ] Wrong password shows error
- [ ] Wrong username shows error
- [ ] Customer cannot access /admin
- [ ] Admin cannot access /dashboard (redirects to /admin)
- [ ] Unauthenticated user redirects to /login
- [ ] Token stored in localStorage
- [ ] API calls include Authorization header

### Console Tests
- [ ] No CORS errors
- [ ] No JavaScript errors
- [ ] localStorage has token
- [ ] localStorage has user object
- [ ] User object has correct role

---

## 🐛 Troubleshooting

### Problem: "Login failed" error

**Check:**
1. Backend is running (Terminal 1)
2. Frontend is running (Terminal 2)
3. Check backend terminal for errors
4. Check browser console (F12) for errors

**Solution:**
```powershell
# Restart backend
cd backend
uvicorn app.main:app --reload

# Restart frontend (new terminal)
cd frontend
npm run dev
```

---

### Problem: "CORS error" in browser console

**Error message:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
1. Check backend `.env` file:
```
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

2. Restart backend server

---

### Problem: Login works but doesn't redirect

**Check:**
1. Browser console for errors
2. Network tab → Check /api/auth/login response
3. Check if token is saved: `localStorage.getItem('token')`

**Solution:**
```javascript
// Clear storage and try again
localStorage.clear()
location.reload()
```

---

### Problem: Admin sees customer dashboard

**Check:**
```javascript
// Check user role
JSON.parse(localStorage.getItem('user')).role
// Should be "admin"
```

**Solution:**
1. Logout completely
2. Clear localStorage: `localStorage.clear()`
3. Close all tabs
4. Open new tab
5. Login again as admin

---

### Problem: Database connection failed

**Check:**
```powershell
# Check MySQL service
Get-Service -Name MySQL80

# Test connection
mysql -u root -p
```

**Solution:**
1. Verify MySQL password in backend `.env`
2. Restart MySQL service:
```powershell
Restart-Service -Name MySQL80
```

---

## 📹 Step-by-Step Visual Guide

### What You Should See When Testing:

**1. Login Page:**
```
┌─────────────────────────────────────┐
│  FIXXY                              │
│  Drive Better • Fix Smarter         │
│                                     │
│  CAR SPARE PARTS & BILLING SYSTEM   │
│                                     │
│  Welcome back                       │
│  Sign in to continue                │
│                                     │
│  USERNAME: [___________]            │
│  PASSWORD: [___________]            │
│                                     │
│  [     LOGIN  →     ]              │
│  [Create new account]               │
│                                     │
│  Demo: admin / admin123             │
└─────────────────────────────────────┘
```

**2. Customer Dashboard:**
```
┌─────────┬───────────────────────────────────┐
│ FIXXY   │  Dashboard                        │
│         │  Welcome back, Demo Customer!     │
│ Dashboard│                                   │
│ Find Parts│ [Spare Parts] [Units] [Wash]    │
│ Cart    │      18         500+      4       │
│ Water Wash│                                  │
│ Orders  │  Quick Actions:                   │
│         │  [Find Parts →]  [Water Wash →]  │
│ Logout  │                                   │
└─────────┴───────────────────────────────────┘
```

**3. Admin Dashboard:**
```
┌─────────┬────────────────────────────────┐
│ FIXXY   │  Admin Dashboard    🔐 ADMIN   │
│ ADMIN   │  Welcome back, Administrator   │
│         │                                │
│ Dashboard│ [Products] [Stock] [Low] [Orders]│
│ Products│     18       500+     2      0   │
│ Inventory│                               │
│ Orders  │  Recent Orders:               │
│ Coupons │  (table or "No orders yet")   │
│ Settings│                               │
│         │  Quick Actions:               │
│ CUSTOMER│  [Add Product] [Update Stock] │
│ Dashboard│                              │
│         │                                │
│ Logout  │                                │
└─────────┴────────────────────────────────┘
```

---

## ✅ Success Criteria

You know everything works when:

✅ **Customer login (`customer`/`customer123`):**
- Redirects to `/dashboard`
- Shows customer name
- Shows customer menu
- No admin features visible

✅ **Admin login (`admin`/`admin123`):**
- Redirects to `/admin`
- Shows admin name
- Shows 🔐 ADMIN badge
- Shows admin menu
- Shows advanced statistics
- Shows recent orders table

✅ **Security:**
- Wrong credentials show error
- Customers can't access `/admin`
- Admins redirect from `/dashboard` to `/admin`
- Logged out users redirect to `/login`

---

## 🎉 If All Tests Pass

Congratulations! Your FIXXY application is working perfectly with:
- ✅ Customer login working
- ✅ Admin login working
- ✅ Role-based dashboards
- ✅ Proper routing
- ✅ Security implemented

**You can now build additional features!**

---

## 📞 Need Help?

**Backend not starting?**
→ Check CODE_DOCUMENTATION.md "Backend Documentation" section

**Frontend not loading?**
→ Check TEST_AND_VERIFY.md "Troubleshooting" section

**Login not working?**
→ Check browser console (F12) → Console tab for errors
→ Check backend terminal for errors

**Database issues?**
→ Run: `mysql -u root -p` and verify database exists

---

## 🚀 Quick Command Reference

```powershell
# Start MySQL
Start-Service -Name MySQL80

# Backend (Terminal 1)
cd "c:\Users\preetham\Documents\py pj\backend"
uvicorn app.main:app --reload

# Frontend (Terminal 2)
cd "c:\Users\preetham\Documents\py pj\frontend"
npm run dev

# Check MySQL
mysql -u root -p

# Test backend
curl http://localhost:8000/health
```

---

**🚗 FIXXY — Drive Better • Fix Smarter**

Follow this guide step-by-step, and both customer and admin logins will work perfectly!
