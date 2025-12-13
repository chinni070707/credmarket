# Local Testing Guide - Test Before You Deploy

## 🎯 Why Test Locally?

**Problem**: Deploying to Render takes 3-5 minutes per deployment
**Solution**: Test everything locally first, then deploy once when everything works

## 🚀 Quick Local Testing Checklist

Before every commit, run these commands:

```powershell
# 1. Activate virtual environment
.\venv\Scripts\activate

# 2. Run migrations (if you changed models)
python manage.py makemigrations
python manage.py migrate

# 3. Collect static files (if you changed CSS/JS)
python manage.py collectstatic --no-input

# 4. Run the development server
python manage.py runserver

# 5. Open browser and test
# Visit: http://127.0.0.1:8000
```

## 📋 Detailed Testing Workflow

### 1. **Check for Code Errors**

```powershell
# Check for Python syntax errors
python manage.py check

# Check for migration issues
python manage.py makemigrations --dry-run --check
```

**Expected Output**: "No changes detected" or "System check identified no issues"

### 2. **Test Database Changes**

```powershell
# After changing models, create migrations
python manage.py makemigrations

# Apply migrations to local database
python manage.py migrate

# Verify migrations worked
python manage.py showmigrations
```

### 3. **Test Your Changes**

```powershell
# Start the development server
python manage.py runserver
```

**Then test in your browser:**
- Homepage: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin/
- Login: http://127.0.0.1:8000/accounts/login/
- Signup: http://127.0.0.1:8000/accounts/signup/

**What to test:**
- ✅ Pages load without errors
- ✅ Forms submit correctly
- ✅ Buttons work
- ✅ Images display
- ✅ Links navigate properly
- ✅ No 404 or 500 errors in terminal

### 4. **Check Logs for Errors**

While the server is running, watch the terminal for errors:

```
# Good output (no errors):
[13/Dec/2025 16:30:45] "GET / HTTP/1.1" 200 4523

# Bad output (error - fix this!):
[13/Dec/2025 16:30:45] "GET / HTTP/1.1" 500 4375
Internal Server Error: /
```

### 5. **Test Different Scenarios**

```powershell
# Test as anonymous user
# - Open incognito window
# - Try accessing pages without logging in

# Test as logged-in user
# - Create a test account
# - Login and test features

# Test with different data
# - Create listings
# - Upload images
# - Submit forms
```

## 🛠️ Common Local Testing Tasks

### **Before Changing Templates**

```powershell
# Make sure static files are up to date
python manage.py collectstatic --no-input

# Start server and view in browser
python manage.py runserver
```

### **Before Changing Models**

```powershell
# Check current state
python manage.py showmigrations

# Make your model changes in code...

# Create migration
python manage.py makemigrations

# Review the migration file
# Look in: listings/migrations/ or accounts/migrations/

# Apply migration
python manage.py migrate

# Test the changes work
python manage.py shell
>>> from listings.models import Listing
>>> Listing.objects.all()
```

### **Before Changing Views**

```powershell
# Add logging to your view:
import logging
logger = logging.getLogger(__name__)

def my_view(request):
    logger.info("Testing my view")
    # Your code...

# Start server with verbose logging
python manage.py runserver

# Watch terminal for your log messages
# Visit the page in browser
# Check terminal for "Testing my view"
```

### **Before Changing Settings**

```powershell
# Test settings changes locally first
# Edit credmarket/settings.py

# Restart server (Ctrl+C, then runserver again)
python manage.py runserver

# Check for errors on startup
```

## 🐛 Debug Common Issues Locally

### **500 Internal Server Error**

```powershell
# Check the terminal - you'll see full error details:
# Example:
# File "/path/to/file.py", line 45
#   return render(request, 'template.html', context)
# NameError: name 'context' is not defined

# Fix the error, save file
# Server auto-reloads, test again
```

### **Template Not Found**

```
# Error in terminal:
# django.template.exceptions.TemplateDoesNotExist: mytemplate.html

# Fix: Check template path
# Should be: templates/app_name/template.html
```

### **Import Errors**

```
# Error:
# ModuleNotFoundError: No module named 'django_ratelimit'

# Fix: Install missing package
pip install django-ratelimit

# Update requirements.txt
pip freeze > requirements.txt
```

### **Database Errors**

```powershell
# Reset local database (DEVELOPMENT ONLY!)
# WARNING: This deletes all data!

# Delete database
rm db.sqlite3

# Remove migration files (keep __init__.py)
rm listings/migrations/0*.py
rm accounts/migrations/0*.py
rm companies/migrations/0*.py

# Recreate everything
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## ✅ Pre-Commit Checklist

**Before every `git commit`, verify:**

```powershell
# 1. Code has no syntax errors
python manage.py check

# 2. Server runs without crashes
python manage.py runserver
# Press Ctrl+C to stop

# 3. Test the specific feature you changed
# - Open browser
# - Navigate to the changed page
# - Verify it works

# 4. Check for console errors
# - Open browser DevTools (F12)
# - Look for red errors in Console tab

# 5. If everything works locally, THEN commit
git add .
git commit -m "Your message"
git push origin main
```

## 🎨 Test Frontend Changes

### **CSS/Tailwind Changes**

```powershell
# 1. Make your CSS changes in templates

# 2. Hard refresh browser (Ctrl+Shift+R)
# This clears cache and shows fresh CSS

# 3. Check in different browsers
# - Chrome
# - Firefox
# - Edge

# 4. Check responsive design
# - Press F12 (DevTools)
# - Click device toolbar icon
# - Test mobile, tablet, desktop sizes
```

### **JavaScript Changes**

```powershell
# 1. Make JS changes in templates

# 2. Open browser DevTools (F12)

# 3. Check Console tab for errors
# - No errors = good!
# - Red errors = fix them!

# 4. Test the functionality
# - Click buttons
# - Submit forms
# - Watch for expected behavior
```

## 📊 Test with Production-Like Settings

### **Test with DEBUG=False Locally**

```powershell
# 1. Edit .env file
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# 2. Collect static files
python manage.py collectstatic --no-input

# 3. Run server
python manage.py runserver

# 4. Test - should work like production

# 5. IMPORTANT: Set back to DEBUG=True when done
DEBUG=True
```

## 🔍 Use Django Shell for Testing

```powershell
# Open Django shell
python manage.py shell

# Test queries
>>> from listings.models import Listing, Category
>>> Category.objects.all()
>>> Listing.objects.filter(status='active').count()

# Test creating objects
>>> from accounts.models import User
>>> user = User.objects.create_user(
...     email='test@example.com',
...     password='testpass123'
... )
>>> user.is_active
True

# Exit shell
>>> exit()
```

## 💡 Pro Tips

### **1. Use Git Branches for Experiments**

```powershell
# Create a test branch
git checkout -b test-new-feature

# Make changes, test locally
# If it works:
git checkout main
git merge test-new-feature
git push origin main

# If it doesn't work:
git checkout main
git branch -D test-new-feature  # Delete failed experiment
```

### **2. Use Django's Built-in Tests**

```powershell
# Run existing tests
python manage.py test

# This catches many issues before deployment!
```

### **3. Keep Multiple Terminal Windows Open**

```
Terminal 1: Development server (python manage.py runserver)
Terminal 2: Git commands (git add, git commit, git push)
Terminal 3: Testing commands (python manage.py shell, etc.)
```

### **4. Use Browser DevTools**

```
Press F12 in browser:
- Console: See JavaScript errors
- Network: See failed requests (404, 500)
- Elements: Inspect HTML/CSS
- Application: Check cookies, storage
```

## 🚫 Never Deploy Without Testing

### **Bad Workflow** ❌
```powershell
# Make changes
git add .
git commit -m "Changes"
git push origin main
# Wait 5 minutes
# Site broken!
# Fix, wait 5 more minutes...
```

### **Good Workflow** ✅
```powershell
# Make changes
python manage.py check                    # 2 seconds
python manage.py runserver                # 5 seconds
# Test in browser - everything works!     # 1 minute
git add .
git commit -m "Feature X working"
git push origin main                      # 5 minutes
# Site works perfectly!
```

## 📝 Sample Testing Session

```powershell
# 1. Start fresh
cd credmarket
.\venv\Scripts\activate

# 2. Check for issues
python manage.py check
# Output: System check identified no issues (0 silenced).

# 3. Apply any pending migrations
python manage.py migrate
# Output: No migrations to apply.

# 4. Start server
python manage.py runserver
# Output: Starting development server at http://127.0.0.1:8000/

# 5. Open browser to http://127.0.0.1:8000
# - Click around
# - Test login
# - Test signup
# - Create a listing
# - Everything works!

# 6. Stop server (Ctrl+C)

# 7. Commit and deploy
git add .
git commit -m "Add new feature - tested locally"
git push origin main

# 8. Done! Confident deployment because you tested first.
```

## 🎓 Learn More

```powershell
# Django management commands
python manage.py help

# Get help for specific command
python manage.py help migrate
python manage.py help runserver

# Django shell with enhanced features
pip install django-extensions
python manage.py shell_plus
```

---

**Remember**: 5 minutes testing locally saves 30 minutes debugging in production! 🚀
