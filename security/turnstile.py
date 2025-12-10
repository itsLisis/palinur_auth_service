import requests
from config import settings

def verify_turnstile(token: str, ip: str = None) -> bool:
    """verify cloudflare token"""
    
    if not token:
        print("Turnstile: No token provided")
        return False
    
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    
    data = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token
    }
    
    if ip:
        data["remoteip"] = ip
    
    try:
        print(f"Turnstile: Verifying token with IP: {ip}")
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        print(f"Turnstile API response: {result}")
        print(f"Turnstile token (first 20 chars): {token[:20]}...")
        return result.get("success", False)
    except Exception as e:
        print(f"Turnstile verification error: {e}")
        return False