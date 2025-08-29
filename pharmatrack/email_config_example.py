# Email Configuration Examples for PharmaTrack

# ===========================================
# DEVELOPMENT SETUP (Current - Console Backend)
# ===========================================
# This prints emails to the console instead of sending them
# Perfect for development and testing

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@pharmatrack.com'

# ===========================================
# PRODUCTION SETUP - Gmail SMTP
# ===========================================
# To use Gmail SMTP, replace the console backend with this:

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-actual-email@gmail.com'  # Your Gmail address
# EMAIL_HOST_PASSWORD = 'your-app-password'        # Gmail App Password (not regular password)
# DEFAULT_FROM_EMAIL = 'your-actual-email@gmail.com'

# ===========================================
# GMAIL SETUP INSTRUCTIONS:
# ===========================================
# 1. Enable 2-Factor Authentication on your Gmail account
# 2. Generate an App Password:
#    - Go to Google Account settings
#    - Security → 2-Step Verification → App passwords
#    - Generate password for "Mail"
# 3. Use the generated App Password (not your regular Gmail password)
# 4. Replace 'your-actual-email@gmail.com' with your Gmail address
# 5. Replace 'your-app-password' with the generated App Password

# ===========================================
# PRODUCTION SETUP - Other Email Providers
# ===========================================

# For Outlook/Hotmail:
# EMAIL_HOST = 'smtp-mail.outlook.com'
# EMAIL_PORT = 587

# For Yahoo:
# EMAIL_HOST = 'smtp.mail.yahoo.com'
# EMAIL_PORT = 587

# For SendGrid:
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
