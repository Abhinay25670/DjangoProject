#!/usr/bin/env python
"""
Test SendGrid API key directly
"""

import os
import requests

def test_sendgrid_api():
    api_key = "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"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Test API key by getting account info
    try:
        response = requests.get('https://api.sendgrid.com/v3/user/account', headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ SendGrid API key is valid!")
        else:
            print("❌ SendGrid API key is invalid or expired!")
            
    except Exception as e:
        print(f"❌ Error testing SendGrid API: {str(e)}")

if __name__ == '__main__':
    test_sendgrid_api()
