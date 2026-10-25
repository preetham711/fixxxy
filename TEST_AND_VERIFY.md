# FIXXY — Testing and Verification Guide

## ✅ Complete Testing Checklist

### Step 1: Verify Backend Setup

#### 1.1 Check MySQL Service
```powershell
# Check if MySQL is running
Get-Service -Name MySQL* | Select-Object Name, Status

# If not running, start it
Start-Service -Name MySQL80
```

✅ **Expected:** Status should be "Running"

#### 1.2 Verify Database
```powershell
mysql -u root -p
```

In MySQL console:
```sql
-- Check if database exists
SHOW DATABASES LIKE 'fixxy_store';

-- Check tables
USE fixxy_store;
SHOW TABLES;

-- Verify default data
SELECT username, role FROM users;
SELECT COUNT(*) FROM products;
SELECT code, discount FROM coupons;

EXIT;
```

✅ **Expected:**
- Database `fixxy_store` exists
- 8 tables created
- 2 users (admin, customer)
- ~22 products
- 3 coupons

#### 1.3 Test Backend API
```powershell
cd backend

# Activate virtual environment (if created)
.\venv\Scripts\Activate.ps1

# Run backend
uvicorn app.main:app --reload
```

✅ **Expected:**
- Server starts on http://localhost:8000
- No errors in console
- See "✅ Database connection successful"

#### 1.4 Test API Endpoints

Open browser: **http://localhost:8000/docs**

Test these endpoints:

1. **GET /health** → Should return `{"status": "healthy"}`
2. **POST /api/auth/login**
   - username: `admin`
   - password: `admin123`
   - Should return JWT token and user object
3. **GET /api/products** → Should return array of products

✅ **Expected:** All endpoints return 200 status with data

---

### Step 2: Verify Frontend Setup

#### 2.1 Install Dependencies
```powershell
# Open NEW terminal
cd frontend

npm install
```

✅ **Expected:**
- No errors during installation
- `node_modules` folder created
- `package-lock.json` created

#### 2.2 Start Frontend
```powershell
npm run dev
```

✅ **Expected:**
- Server starts on http://localhost:5173
- Automatically opens browser
- No errors in console

---

### Step 3: Test Authentication Flow

#### 3.1 Test Customer Login

1. **Open:** http://localhost:5173
2. **Enter:**
   - Username: `customer`
   - Password: `customer123`
3. **Click:** LOGIN

✅ **Expected:**
- Loading indicator appears
- Redirects to `/dashboard`
- Shows "Welcome back, Demo Customer!"
- Sidebar shows customer menu items
- Statistics load (Spare Parts, Units Available, etc.)

#### 3.2 Test Admin Login

1. **Click:** Logout
2. **Enter:**
   - Username: `admin`
   - Password: `admin123`
3. **Click:** LOGIN

✅ **Expected:**
- Redirects to `/admin`
- Shows "Welcome back, FIXXY Administrator!"
- Shows "🔐 ADMIN" badge
- Sidebar shows admin menu items
- Dashboard loads with statistics

#### 3.3 Test Invalid Login

1. **Enter:**
   - Username: `wronguser`
   - Password: `wrongpass`
2. **Click:** LOGIN

✅ **Expected:**
- Error message: "Incorrect username or password"
- Stays on login page
- Does NOT redirect

---

### Step 4: Test Registration

1. **Click:** "Create a new customer account"
2. **Fill form:**
   - Full Name: `Test User`
   - Username: `testuser`
   - Password: `test123456`
   - Confirm Password: `test123456`
3. **Click:** CREATE ACCOUNT

✅ **Expected:**
- Success message: "Account created successfully!"
- Redirects to login page
- Can login with new credentials

---

### Step 5: Browser Console Checks

#### 5.1 Check localStorage

Open Chrome DevTools (F12) → Console:

```javascript
// Check if token exists
localStorage.getItem('token')

// Check user data
JSON.parse(localStorage.getItem('user'))

// Should see:
// {
//   id: 1,
//   username: "admin",
//   role: "admin",
//   full_name: "FIXXY Administrator"
// }
```

✅ **Expected:** Token and user data present after login

#### 5.2 Check Network Requests

DevTools → Network tab → XHR filter:

After login, you should see:
- `POST /api/auth/login` → 200 OK
- `GET /api/products` → 200 OK
- `GET /api/orders/statistics/dashboard` → 200 OK (admin only)

✅ **Expected:** All requests return 200 status

#### 5.3 Check Console Errors

Look for:
- ❌ CORS errors
- ❌ 404 errors
- ❌ JavaScript errors

✅ **Expected:** No errors in console

---

### Step 6: Test Customer Dashboard Features

Login as customer (`customer` / `customer123`)

#### 6.1 Dashboard Statistics
- Shows "Spare Parts" count
- Shows "Units Available" count
- Shows "Wash Packages" count

✅ **Expected:** Numbers match database

#### 6.2 Navigation
- Click sidebar links
- All links should work (even if pages not built yet)

✅ **Expected:** Navigation works without errors

---

### Step 7: Test Admin Dashboard Features

Login as admin (`admin` / `admin123`)

#### 7.1 Admin Statistics
- Total Products
- Total Stock
- Low Stock Items
- Total Orders
- Total Revenue

✅ **Expected:** Displays correct statistics

#### 7.2 Recent Orders Table
- Shows recent orders (if any exist)
- Displays bill number, customer, total, status

✅ **Expected:** Table renders correctly

#### 7.3 Admin Navigation
- Dashboard (active)
- Products
- Inventory
- Orders
- Coupons
- Settings
- Customer Dashboard link

✅ **Expected:** All menu items visible

---

### Step 8: Test API Integration

#### 8.1 Test with Browser Console

Login as admin, then in Console:

```javascript
// Test get products
fetch('http://localhost:8000/api/products', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('token')
  }
})
.then(r => r.json())
.then(data => console.log('Products:', data))

// Test get orders
fetch('http://localhost:8000/api/orders', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('token')
  }
})
.then(r => r.json())
.then(data => console.log('Orders:', data))
```

✅ **Expected:** Returns data arrays

---

### Step 9: Test Error Handling

#### 9.1 Test Expired Token

In Console:
```javascript
// Clear token
localStorage.removeItem('token')

// Try to refresh page
location.reload()
```

✅ **Expected:** Redirects to login page

#### 9.2 Test Backend Offline

1. Stop backend server (Ctrl+C)
2. Try to login

✅ **Expected:**
- Error message appears
- Frontend handles gracefully

#### 9.3 Test Authorization

Login as customer, then try:
```javascript
// Try to access admin endpoint
fetch('http://localhost:8000/api/products', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('token'),
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({name: 'Test', category: 'Test', price: 100, stock: 10})
})
.then(r => r.json())
.then(data => console.log(data))
```

✅ **Expected:** Returns 403 Forbidden (customers can't create products)

---

### Step 10: Database Verification

After testing, check database changes:

```sql
USE fixxy_store;

-- Check new user was created
SELECT * FROM users WHERE username = 'testuser';

-- Check default data still exists
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM coupons;
```

✅ **Expected:**
- New user exists
- Default data intact

---

## 🐛 Troubleshooting Common Issues

### Issue 1: Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```powershell
cd backend
pip install -r requirements.txt
```

---

### Issue 2: MySQL connection fails

**Error:** `Access denied for user 'root'@'localhost'`

**Solution:**
1. Check `.env` file in backend folder
2. Verify `MYSQL_PASSWORD` matches your MySQL password
3. Test MySQL connection:
```powershell
mysql -u root -p
```

---

### Issue 3: CORS errors in browser

**Error:** `blocked by CORS policy`

**Solution:**
1. Check backend `.env` file:
```
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```
2. Restart backend server

---

### Issue 4: Frontend shows blank page

**Check:**
1. Browser console for errors
2. Network tab for failed requests
3. Backend is running on port 8000

**Solution:**
```powershell
# Restart both servers
# Terminal 1
cd backend
uvicorn app.main:app --reload

# Terminal 2
cd frontend
npm run dev
```

---

### Issue 5: Login doesn't redirect

**Check:**
1. Console for errors
2. Network tab → Response from `/api/auth/login`
3. localStorage after login

**Solution:**
- Clear browser cache and localStorage:
```javascript
localStorage.clear()
location.reload()
```

---

### Issue 6: Admin dashboard shows customer dashboard

**Solution:**
1. Logout completely
2. Clear localStorage:
```javascript
localStorage.clear()
```
3. Login again with admin credentials
4. Check redirect in Network tab

---

### Issue 7: Statistics show 0 for everything

**Check database:**
```sql
SELECT COUNT(*) FROM products;
```

**If 0, reimport schema:**
```powershell
mysql -u root -p fixxy_store < database\schema.sql
```

---

## ✅ Final Verification Checklist

- [ ] MySQL service running
- [ ] Database `fixxy_store` created with all tables
- [ ] Default users exist (admin, customer)
- [ ] Default products exist (22+)
- [ ] Backend starts without errors
- [ ] Backend health check passes
- [ ] API documentation accessible at /docs
- [ ] Frontend starts without errors
- [ ] Frontend opens in browser automatically
- [ ] Can login as customer
- [ ] Customer redirects to `/dashboard`
- [ ] Customer dashboard shows statistics
- [ ] Can logout
- [ ] Can login as admin
- [ ] Admin redirects to `/admin`
- [ ] Admin dashboard shows statistics
- [ ] Admin dashboard shows "ADMIN" badge
- [ ] Recent orders table renders
- [ ] Can register new user
- [ ] New user can login
- [ ] No CORS errors in console
- [ ] No JavaScript errors in console
- [ ] localStorage stores token and user
- [ ] API calls include Authorization header
- [ ] Unauthorized access returns 403
- [ ] Invalid login shows error message

---

## 📊 Success Criteria

**Backend:** ✅
- All API endpoints working
- Database connected
- Authentication functional
- Authorization working

**Frontend:** ✅
- Application loads
- Login working
- Registration working
- Role-based routing working
- Customer dashboard displays
- Admin dashboard displays
- API integration working

**Security:** ✅
- Passwords hashed
- JWT tokens working
- Authorization enforced
- No sensitive data exposed

---

## 🎯 What's Working Now

### ✅ Complete Features
1. User Registration
2. User Login (Customer & Admin)
3. JWT Authentication
4. Role-based Access Control
5. Customer Dashboard
6. Admin Dashboard
7. Product API (CRUD)
8. Order API (Create, Read)
9. Coupon API (Validate, CRUD)
10. Vehicle API (CRUD)
11. Settings API
12. Database with seed data
13. API Documentation

### 🔨 Pages to Build Next
1. Products Catalog (customer view)
2. Shopping Cart
3. Checkout Process
4. Order History
5. Water Wash Services
6. Admin Product Management
7. Admin Inventory Management
8. Admin Order Management
9. Admin Coupon Management
10. Admin Settings

---

## 📚 Quick Reference

### Default Credentials
```
Admin:
Username: admin
Password: admin123

Customer:
Username: customer
Password: customer123
```

### URLs
```
Frontend:   http://localhost:5173
Backend:    http://localhost:8000
API Docs:   http://localhost:8000/docs
Health:     http://localhost:8000/health
```

### Ports
```
Frontend:   5173
Backend:    8000
MySQL:      3306
```

---

## 🚀 Next Steps After Verification

1. **Build remaining pages** - Follow implementation guide
2. **Add more products** - Use admin API
3. **Test complete workflows** - End-to-end testing
4. **Add features** - Cart, checkout, orders
5. **Polish UI** - Responsive design, animations
6. **Deploy** - Production deployment

---

**🚗 FIXXY — Drive Better • Fix Smarter**

All core functionality is working! The application is ready for development of remaining features.
