# 🚀 PharmaTrack Deployment Guide

This guide covers multiple deployment options for your PharmaTrack Django application.

## 📋 Prerequisites

- Python 3.8+ installed
- Git installed
- Domain name (optional but recommended)
- Email service configured (Gmail, SendGrid, etc.)

## 🌐 Deployment Options

### Option 1: Railway (Recommended - Easiest)

Railway is the easiest platform for Django deployment with automatic deployments.

#### Steps:

1. **Sign up at [Railway.app](https://railway.app)**
2. **Connect your GitHub repository**
3. **Add environment variables:**
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   DATABASE_URL=postgresql://user:pass@host:port/db
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```
4. **Deploy automatically**

**Cost:** Free tier available, then $5/month

---

### Option 2: Heroku (Popular Choice)

#### Steps:

1. **Install Heroku CLI**
2. **Create Heroku app:**
   ```bash
   heroku create your-pharmatrack-app
   ```
3. **Add PostgreSQL database:**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```
4. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```
5. **Deploy:**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

**Cost:** $7/month for basic plan

---

### Option 3: DigitalOcean App Platform

#### Steps:

1. **Sign up at [DigitalOcean](https://digitalocean.com)**
2. **Create new app from GitHub**
3. **Configure build settings:**
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn pharmatrack.wsgi:application`
4. **Add environment variables in dashboard**
5. **Deploy**

**Cost:** $5/month for basic plan

---

### Option 4: AWS EC2 (Advanced)

#### Steps:

1. **Launch EC2 instance (Ubuntu 20.04)**
2. **Connect via SSH and run setup script:**
   ```bash
   # Run the setup script
   chmod +x setup_aws.sh
   ./setup_aws.sh
   ```
3. **Configure domain and SSL**

**Cost:** ~$10-20/month depending on instance size

---

### Option 5: VPS (Virtual Private Server)

#### Popular VPS Providers:

- **DigitalOcean Droplets** ($5/month)
- **Linode** ($5/month)
- **Vultr** ($2.50/month)
- **Hetzner** (€3.29/month)

#### Steps:

1. **Create VPS instance**
2. **Follow the manual deployment guide below**

---

## 🔧 Manual Deployment Steps (VPS/EC2)

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib git -y

# Create project directory
sudo mkdir -p /var/www/pharmatrack
sudo chown $USER:$USER /var/www/pharmatrack
cd /var/www/pharmatrack
```

### 2. Clone and Setup Project

```bash
# Clone your repository
git clone https://github.com/yourusername/pharmatrack.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE pharmatrack;
CREATE USER pharmatrack_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE pharmatrack TO pharmatrack_user;
\q
```

### 4. Configure Production Settings

```bash
# Copy production settings
cp pharmatrack/production_settings.py pharmatrack/settings.py

# Edit settings with your configuration
nano pharmatrack/settings.py
```

### 5. Run Migrations and Collect Static Files

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 6. Configure Gunicorn

```bash
# Create Gunicorn service file
sudo nano /etc/systemd/system/pharmatrack.service
```

Add this content:

```ini
[Unit]
Description=PharmaTrack Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/pharmatrack
ExecStart=/var/www/pharmatrack/venv/bin/gunicorn --workers 3 --bind unix:/var/www/pharmatrack/pharmatrack.sock pharmatrack.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### 7. Configure Nginx

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/pharmatrack
```

Add this content:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/pharmatrack;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/pharmatrack/pharmatrack.sock;
    }
}
```

### 8. Enable Services

```bash
# Enable and start services
sudo systemctl enable pharmatrack
sudo systemctl start pharmatrack
sudo systemctl enable nginx
sudo systemctl restart nginx

# Enable site
sudo ln -s /etc/nginx/sites-available/pharmatrack /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 9. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## 🔐 Environment Variables

Create a `.env` file or set these environment variables:

```bash
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@localhost:5432/pharmatrack
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

---

## 📧 Email Configuration

### Gmail Setup:

1. Enable 2-Factor Authentication
2. Generate App Password
3. Use App Password in EMAIL_HOST_PASSWORD

### SendGrid (Recommended for Production):

1. Sign up at [SendGrid](https://sendgrid.com)
2. Create API key
3. Update settings:
   ```python
   EMAIL_HOST = 'smtp.sendgrid.net'
   EMAIL_PORT = 587
   EMAIL_HOST_USER = 'apikey'
   EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
   ```

---

## 🚀 Quick Deploy Commands

### For Railway:

```bash
# Just push to GitHub - Railway auto-deploys
git add .
git commit -m "Deploy to production"
git push origin main
```

### For Heroku:

```bash
git add .
git commit -m "Deploy to production"
git push heroku main
heroku run python manage.py migrate
```

### For VPS:

```bash
# On your server
cd /var/www/pharmatrack
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart pharmatrack
```

---

## 🔍 Troubleshooting

### Common Issues:

1. **Static files not loading:**

   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Database connection errors:**

   - Check DATABASE_URL format
   - Ensure PostgreSQL is running

3. **Email not sending:**

   - Verify email credentials
   - Check firewall settings
   - Test with console backend first

4. **Permission errors:**
   ```bash
   sudo chown -R www-data:www-data /var/www/pharmatrack
   sudo chmod -R 755 /var/www/pharmatrack
   ```

---

## 📊 Monitoring and Maintenance

### Log Files:

- Application logs: `/var/log/pharmatrack/`
- Nginx logs: `/var/log/nginx/`
- System logs: `journalctl -u pharmatrack`

### Backup Database:

```bash
pg_dump pharmatrack > backup_$(date +%Y%m%d).sql
```

### Update Application:

```bash
cd /var/www/pharmatrack
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart pharmatrack
```

---

## 💰 Cost Comparison

| Platform         | Monthly Cost | Difficulty         | Features                |
| ---------------- | ------------ | ------------------ | ----------------------- |
| Railway          | Free-$5      | ⭐ Easy            | Auto-deploy, PostgreSQL |
| Heroku           | $7+          | ⭐⭐ Medium        | Easy, but expensive     |
| DigitalOcean App | $5+          | ⭐⭐ Medium        | Good performance        |
| VPS (Manual)     | $2.50-$10    | ⭐⭐⭐ Hard        | Full control, cheapest  |
| AWS EC2          | $10-$20+     | ⭐⭐⭐⭐ Very Hard | Scalable, complex       |

---

## 🎯 Recommended Approach

**For beginners:** Start with **Railway** - it's the easiest and has a generous free tier.

**For production:** Use **DigitalOcean App Platform** or **VPS** for better control and lower costs.

**For scaling:** Consider **AWS** or **Google Cloud** for enterprise-level applications.

---

## 📞 Support

If you encounter issues during deployment:

1. Check the logs: `journalctl -u pharmatrack -f`
2. Verify environment variables
3. Test locally first
4. Check firewall and security groups
5. Ensure all dependencies are installed

Happy deploying! 🚀
