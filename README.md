# CredMarket - India's Trusted Marketplace

A verified marketplace platform exclusively for corporate employees, ensuring a spam-free and trustworthy buying/selling experience.

## 🎯 Features

- **Corporate Email Verification**: Only verified corporate employees can register
- **Company Whitelist**: Admin-managed list of approved companies (FAANG, listed companies)
- **Spam-Free Listings**: Quality over quantity approach
- **In-App Messaging**: Secure communication between buyers and sellers
- **Category System**: Comprehensive product categories similar to OLX
- **Admin Dashboard**: Manage companies, waitlist, and user verification

## 🛠️ Tech Stack

- **Backend**: Django 5.0
- **Frontend**: Django Templates + HTMX + Tailwind CSS
- **Database**: PostgreSQL
- **Authentication**: Django OTP
- **Email**: SendGrid
- **File Storage**: Cloudinary
- **Deployment**: Railway/Render/DigitalOcean

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL 14+
- pip and virtualenv

## 🚀 Quick Start

### 1. Clone and Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE credmarket_db;
\q
```

### 3. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
# Update DB_PASSWORD, SECRET_KEY, SENDGRID_API_KEY, etc.
```

### 4. Run Migrations

```bash
cd credmarket
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 6. Load Initial Data (Optional)

```bash
# Load sample categories and companies
python manage.py loaddata initial_data.json
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit:
- **Main Site**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 📁 Project Structure

```
credmarket/
├── credmarket/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # User authentication & profiles
│   ├── models.py
│   ├── views.py
│   └── forms.py
├── companies/               # Company whitelist management
│   ├── models.py
│   └── admin.py
├── listings/                # Product listings
│   ├── models.py
│   ├── views.py
│   └── forms.py
├── messaging/               # Buyer-seller communication
│   ├── models.py
│   └── views.py
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
└── media/                   # User uploads
```

## 🔐 Authentication Flow

1. User enters corporate email
2. System validates email domain against whitelist
3. If approved → OTP sent to email
4. If not in whitelist → Added to waitlist
5. Admin reviews waitlist and approves companies
6. User verifies OTP and completes registration

## 👨‍💼 Admin Features

- Add/remove companies from whitelist
- Review and approve waitlisted users
- Manage product categories
- Monitor listings and users
- View analytics dashboard

## 🌟 Roadmap

### Phase 1 (Current)
- [x] Project setup
- [ ] Authentication with OTP
- [ ] Company whitelist system
- [ ] Basic listing CRUD
- [ ] Admin panel

### Phase 2
- [ ] In-app messaging
- [ ] Advanced search & filters
- [ ] Image optimization
- [ ] Email notifications

### Phase 3
- [ ] Promoted listings
- [ ] Ad placements
- [ ] Analytics dashboard
- [ ] Mobile optimization

## 📝 License

Proprietary - All rights reserved

## 🤝 Contributing

This is a private project. Contact the owner for collaboration opportunities.

---

Built with ❤️ for India's corporate professionals
