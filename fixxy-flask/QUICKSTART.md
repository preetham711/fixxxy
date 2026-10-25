# FIXXY Quick Start (3 Steps)

## Step 1: Install Dependencies (1 minute)
```bash
cd fixxy-flask
pip install -r requirements.txt
```

## Step 2: Setup Database (2 minutes)

**Option A - Automated (Recommended):**
```bash
python setup_database.py
```

**Option B - Manual:**
1. Update MySQL password in `app/config.py` line 13
2. Run: `mysql -u root -p < database/schema.sql`

## Step 3: Run Application (1 second)
```bash
python run.py
```

Open Chrome: **http://127.0.0.1:5000**

## Login
- **Admin**: username `admin` / password `admin123`
- **Or**: Click "Create New Account" for customer access

## That's It! 🎉

Test the system:
1. Browse spare parts
2. Add items to cart
3. Apply coupon: `WELCOME10`
4. Complete checkout
5. View your invoice

---

**Need Help?**
- Setup issues: Read `SETUP_GUIDE.md`
- Full documentation: Read `README.md`
- Testing guide: Read `TESTING_GUIDE.md`
