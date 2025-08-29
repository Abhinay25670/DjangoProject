# 🚀 Quick Deploy Guide - PharmaTrack

## 🎯 Easiest Deployment Options

### Option 1: Railway (Recommended - 5 minutes)

1. **Sign up at [Railway.app](https://railway.app)**
2. **Connect your GitHub repository**
3. **Add these environment variables:**
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```
4. **Deploy automatically!**

**✅ Done!** Your app will be live at `https://your-app-name.railway.app`

---

### Option 2: Heroku (10 minutes)

1. **Install Heroku CLI**
2. **Run these commands:**
   ```bash
   heroku create your-pharmatrack-app
   heroku addons:create heroku-postgresql:hobby-dev
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set EMAIL_HOST_USER=your-email@gmail.com
   heroku config:set EMAIL_HOST_PASSWORD=your-app-password
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

**✅ Done!** Your app will be live at `https://your-pharmatrack-app.herokuapp.com`

---

### Option 3: DigitalOcean App Platform (15 minutes)

1. **Sign up at [DigitalOcean](https://digitalocean.com)**
2. **Create new app from GitHub**
3. **Configure:**
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn pharmatrack.wsgi:application`
4. **Add environment variables in dashboard**
5. **Deploy**

**✅ Done!** Your app will be live at `https://your-app-name.ondigitalocean.app`

---

## 🔧 Before Deploying

### 1. Update Email Settings

Edit `pharmatrack/settings.py` and replace:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### 2. Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Test Locally

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

---

## 📧 Email Setup (Gmail)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password:**
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Use the App Password** (not your regular Gmail password)

---

## 🎉 After Deployment

1. **Visit your app URL**
2. **Register a new account**
3. **Check email verification** (emails will be sent to your configured email)
4. **Login and start using PharmaTrack!**

---

## 🔍 Troubleshooting

### Common Issues:

**❌ "Failed to send verification email"**

- Check email credentials in settings
- Verify Gmail App Password is correct
- Ensure 2FA is enabled on Gmail

**❌ "Static files not loading"**

- Run: `python manage.py collectstatic --noinput`

**❌ "Database connection error"**

- Check DATABASE_URL format
- Ensure database service is running

**❌ "Permission denied"**

- Check file permissions
- Ensure proper ownership

---

## 💰 Cost Comparison

| Platform     | Free Tier | Paid Plans  | Best For     |
| ------------ | --------- | ----------- | ------------ |
| Railway      | ✅ Yes    | $5/month    | Beginners    |
| Heroku       | ❌ No     | $7/month    | Easy setup   |
| DigitalOcean | ❌ No     | $5/month    | Performance  |
| VPS          | ❌ No     | $2.50/month | Full control |

---

## 🆘 Need Help?

1. **Check the full [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**
2. **Review platform-specific documentation**
3. **Check application logs**
4. **Test locally first**

---

**🎯 Recommended:** Start with **Railway** - it's the easiest and has a generous free tier!

Happy deploying! 🚀
