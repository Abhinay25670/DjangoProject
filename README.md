# PharmaTrack - Smart Medicine Stock & Expiry Manager

A comprehensive Django web application designed for small clinics and pharmacies to efficiently manage their medicine inventory, track expiry dates, and receive alerts for low stock items.

## 🎯 Problem Statement

Small clinics and pharmacies often rely on notebooks or spreadsheets to manage medicine stock, leading to:

- Missed reorders
- Expired medicines
- Wasted inventory and patient risk

## ✨ Key Features

### 🔐 Authentication System

- User registration and login
- Secure password management
- User-specific inventory isolation

### 📦 Medicine Management

- Add, edit, and delete medicines
- Comprehensive medicine details (name, batch, manufacturer, dates, quantity)
- Form validation and error handling

### 📋 Inventory Tracking

- Searchable and filterable medicine list
- Real-time stock monitoring
- Batch number tracking

### ⏰ Expiry Alerts

- Automatic expiry date monitoring
- Color-coded status indicators:
  - 🔴 Red: Expired medicines
  - 🟡 Yellow: Expiring within 30 days
  - 🟢 Green: Good condition

### 📉 Low Stock Alerts

- Configurable low stock thresholds
- Visual indicators for low stock items
- Proactive inventory management

### 📊 Dashboard Overview

- Real-time statistics cards
- Recent medicines list
- Alert summaries
- Quick action buttons

### 🎨 Modern UI

- Bootstrap 5 responsive design
- Mobile-friendly interface
- Intuitive navigation
- Professional styling

## 🛠️ Tech Stack

- **Backend**: Django 5.2.4
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL ready
- **Authentication**: Django's built-in auth system
- **Icons**: Bootstrap Icons

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd pharmatrack
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install django
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

### Step 8: Access the Application

- Main application: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 📱 Usage Guide

### 1. Registration & Login

- Visit the application and click "Register"
- Create your account with username, email, and password
- Login with your credentials

### 2. Dashboard

- View overview statistics
- See recent medicines
- Check alerts and notifications
- Access quick actions

### 3. Adding Medicines

- Click "Add Medicine" from dashboard or navigation
- Fill in all required fields:
  - Medicine name
  - Batch number
  - Manufacturer
  - Manufacturing date
  - Expiry date
  - Quantity
  - Low stock threshold
- Optional: Add description and price per unit

### 4. Managing Inventory

- View all medicines in the "Medicines" section
- Use search and filter options
- Edit or delete medicines as needed
- Monitor stock levels and expiry dates

### 5. Alerts

- Check the "Alerts" section for:
  - Expired medicines
  - Medicines expiring soon
  - Low stock items
- Take appropriate action based on alerts

## 🎨 UI Features

### Responsive Design

- Works on desktop, tablet, and mobile devices
- Bootstrap 5 grid system
- Touch-friendly interface

### Color-Coded Status

- **Red**: Expired medicines
- **Yellow**: Expiring soon (≤30 days)
- **Green**: Good condition
- **Blue**: Low stock alerts

### Interactive Elements

- Hover effects on cards and buttons
- Smooth transitions
- Loading states
- Form validation feedback

## 🔧 Configuration

### Database

The application uses SQLite by default. For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files

Static files are configured for development. For production:

```bash
python manage.py collectstatic
```

## 🔮 Future Enhancements

### Planned Features

- [ ] Email notifications for expiring medicines
- [ ] Export inventory to Excel/PDF
- [ ] QR/barcode scanning
- [ ] Medicine usage analytics
- [ ] Multi-location support
- [ ] API endpoints for mobile apps
- [ ] Advanced reporting
- [ ] Integration with suppliers

### Technical Improvements

- [ ] Unit and integration tests
- [ ] API documentation
- [ ] Performance optimization
- [ ] Caching implementation
- [ ] Background task processing

---

**PharmaTrack** - Making medicine inventory management simple and efficient! 💊✨
