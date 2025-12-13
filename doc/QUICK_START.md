# 🚀 CredMarket - Complete Setup Guide

## ✅ What's Been Created

Your **CredMarket** project is now fully set up with:

### Backend (Django)
- ✅ Custom User model with OTP verification
- ✅ Company whitelist system
- ✅ Product listings with categories
- ✅ Messaging system
- ✅ Full Django admin panel
- ✅ All models, views, and URLs configured

### Frontend (Modern UI)
- ✅ Beautiful responsive design with Tailwind CSS
- ✅ Interactive components with Alpine.js
- ✅ HTMX for dynamic updates
- ✅ Modern gradient designs
- ✅ Mobile-friendly layouts
- ✅ All pages: Home, Login, Signup, OTP, Listings, Messages, Profile

---

## 🎯 Quick Start (5 Minutes)

### Step 1: Navigate to Project
```powershell
cd "C:\Users\mahchi01\OneDrive - Cadence Design Systems Inc\Documents\Sourcecode\credmarket"
```

### Step 2: Create Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Create Environment File
```powershell
Copy-Item .env.example .env
```

### Step 5: Use SQLite for Quick Testing (No PostgreSQL needed!)
The project is configured for PostgreSQL, but for quick testing, let's use SQLite:

Edit `credmarket/settings.py` and replace the DATABASES section with:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Step 6: Run Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser (Admin)
```powershell
python manage.py createsuperuser
```
Enter your details when prompted.

### Step 8: Load Sample Data
```powershell
python manage.py shell
```

Then paste this:
```python
from listings.models import Category
from companies.models import Company

# Create Categories
categories = [
    {'name': 'Electronics', 'icon': 'fa-laptop', 'order': 1},
    {'name': 'Furniture', 'icon': 'fa-couch', 'order': 2},
    {'name': 'Vehicles', 'icon': 'fa-car', 'order': 3},
    {'name': 'Books', 'icon': 'fa-book', 'order': 4},
    {'name': 'Clothing', 'icon': 'fa-tshirt', 'order': 5},
    {'name': 'Home Appliances', 'icon': 'fa-blender', 'order': 6},
    {'name': 'Sports & Fitness', 'icon': 'fa-dumbbell', 'order': 7},
    {'name': 'Others', 'icon': 'fa-box', 'order': 8},
]

for cat in categories:
    Category.objects.get_or_create(
        name=cat['name'],
        defaults={'icon': cat['icon'], 'order': cat['order']}
    )

# Create FAANG + Top Indian Companies
companies = [
    {'name': 'Google', 'domain': 'google.com'},
    {'name': 'Amazon', 'domain': 'amazon.com'},
    {'name': 'Meta (Facebook)', 'domain': 'fb.com'},
    {'name': 'Apple', 'domain': 'apple.com'},
    {'name': 'Netflix', 'domain': 'netflix.com'},
    {'name': 'Microsoft', 'domain': 'microsoft.com'},
    {'name': 'Flipkart', 'domain': 'flipkart.com'},
    {'name': 'Paytm', 'domain': 'paytm.com'},
    {'name': 'Zomato', 'domain': 'zomato.com'},
    {'name': 'Swiggy', 'domain': 'swiggy.in'},
    {'name': 'Ola', 'domain': 'olacabs.com'},
    {'name': 'PhonePe', 'domain': 'phonepe.com'},
]

for company in companies:
    Company.objects.get_or_create(
        domain=company['domain'],
        defaults={'name': company['name'], 'status': 'approved'}
    )

print("✅ Sample data created!")
exit()
```

### Step 9: Run the Server! 🎉
```powershell
python manage.py runserver
```

Visit:
- **🏠 Main Site**: http://localhost:8000
- **👨‍💼 Admin Panel**: http://localhost:8000/admin

---

## 🎨 Features Implemented

### 1. Authentication System ✅
- Email-based signup (corporate emails only)
- OTP verification (6-digit code)
- Company domain validation
- Waitlist system for unapproved companies
- Login/Logout functionality

**Test it:**
1. Go to http://localhost:8000/accounts/signup/
2. Try signing up with `test@google.com`
3. OTP will be printed in console (check terminal)
4. Enter OTP to verify

### 2. Listing System ✅
- Create, Read, Update, Delete listings
- Multiple image uploads
- Category system
- Price negotiation flag
- Condition tracking
- Location-based filtering
- View counter
- Featured listings

**Test it:**
1. Login first
2. Click "Sell" button
3. Fill the form and upload images
4. View your listing on homepage

### 3. Messaging System ✅
- Private conversations
- Real-time-like chat interface
- Message read status
- Inbox with unread count

**Test it:**
1. Create a listing
2. Login with different account
3. Click "Contact Seller" on listing
4. Send messages back and forth

### 4. Admin Panel ✅
- Manage users and approve accounts
- Company whitelist management
- Listing moderation
- Bulk actions (approve users, feature listings)

**Access:** http://localhost:8000/admin

---

## 📁 Project Structure

```
credmarket/
├── credmarket/              # Main Django project
│   ├── settings.py         # Configuration
│   ├── urls.py             # URL routing
│   └── wsgi.py
├── accounts/                # User authentication
│   ├── models.py           # User, OTPVerification
│   ├── views.py            # Signup, login, verify OTP
│   ├── admin.py            # User admin panel
│   └── urls.py
├── companies/               # Company whitelist
│   ├── models.py           # Company model
│   └── admin.py            # Company management
├── listings/                # Product marketplace
│   ├── models.py           # Listing, Category, Images
│   ├── views.py            # CRUD operations
│   ├── admin.py            # Listing management
│   └── urls.py
├── messaging/               # Chat system
│   ├── models.py           # Conversation, Message
│   ├── views.py            # Inbox, chat
│   └── urls.py
├── templates/               # HTML templates
│   ├── base.html           # Main layout
│   ├── accounts/           # Auth pages
│   ├── listings/           # Listing pages
│   └── messaging/          # Chat pages
├── media/                   # User uploads (created when files uploaded)
├── requirements.txt
├── .env.example
└── manage.py
```

---

## 🎯 How to Use

### As Admin
1. Login to admin: http://localhost:8000/admin
2. Go to "Companies" → Add companies to whitelist
3. Review waitlisted users and approve them
4. Manage listings and categories

### As User
1. Signup with corporate email
2. Verify email with OTP
3. Browse listings or create your own
4. Message sellers
5. Buy/Sell items

---

## 🔧 Common Tasks

### Add New Category
```powershell
python manage.py shell
```
```python
from listings.models import Category
Category.objects.create(name='Gadgets', icon='fa-mobile', order=9)
exit()
```

### Approve Company Domain
Via admin panel or shell:
```python
from companies.models import Company
Company.objects.create(name='Infosys', domain='infosys.com', status='approved')
exit()
```

### Create Test Listing
Via admin panel or:
```python
from accounts.models import User
from listings.models import Listing, Category

user = User.objects.first()
cat = Category.objects.first()

Listing.objects.create(
    title='iPhone 13 Pro Max',
    description='Excellent condition, barely used',
    category=cat,
    seller=user,
    price=55000,
    condition='excellent',
    city='Bangalore',
    state='Karnataka',
    location='Koramangala'
)
exit()
```

---

## 🚀 Next Steps

### For Production Deployment:

1. **Database**: Switch to PostgreSQL
   - Install PostgreSQL
   - Update .env with database credentials
   - Run migrations again

2. **Email Service**: Setup SendGrid
   - Get API key from sendgrid.com
   - Update .env with SENDGRID_API_KEY
   - Change EMAIL_BACKEND in settings.py

3. **File Storage**: Setup Cloudinary
   - Sign up at cloudinary.com
   - Get credentials
   - Update .env

4. **Static Files**:
   ```powershell
   python manage.py collectstatic
   ```

5. **Deploy**: Railway, Render, or DigitalOcean
   - Set DEBUG=False
   - Update ALLOWED_HOSTS
   - Use gunicorn as WSGI server

---

## 🎨 UI Features

### Modern Design Elements
- ✅ Gradient backgrounds
- ✅ Smooth animations
- ✅ Card hover effects
- ✅ Responsive grid layouts
- ✅ Beautiful forms
- ✅ Icon integration
- ✅ Mobile-optimized

### Components Used
- Tailwind CSS for styling
- Font Awesome icons
- Alpine.js for interactivity
- HTMX for dynamic updates

---

## 🐛 Troubleshooting

### "No module named 'xyz'"
```powershell
pip install -r requirements.txt
```

### "Table doesn't exist"
```powershell
python manage.py migrate
```

### "Static files not loading"
- Run in DEBUG mode for development
- Or run: `python manage.py collectstatic`

### "Email not sending"
- Check console output (OTP is printed there in development)
- For production, configure SendGrid

---

## 📞 Support

### Admin Panel
- URL: http://localhost:8000/admin
- Manage everything from here

### Django Shell
```powershell
python manage.py shell
```
Use to inspect data, create test records

### Database Browser
For SQLite, use: https://sqlitebrowser.org/

---

## 🎉 You're All Set!

Your marketplace is ready to use! 

**Try these:**
1. ✅ Create an account with corporate email
2. ✅ Post a test listing
3. ✅ Browse the beautiful homepage
4. ✅ Send a message to yourself
5. ✅ Explore the admin panel

**Questions?** Just ask! 🚀
