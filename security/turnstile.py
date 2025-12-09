import requests
from config import settings

def verify_turnstile(token: str, ip: str = None) -> bool:
    """verify cloudflare token"""
    
    if not token:
        return False
    
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    
    data = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token
    }
    
    if ip:
        data["remoteip"] = ip
    
    try:
        response = requests.post(url, json=data, timeout=5)
        result = response.json()
        print(f"Turnstile API response: {result}")
        return result.get("success", False)
    except Exception as e:
        print(f"Turnstile verification error: {e}")
        return False