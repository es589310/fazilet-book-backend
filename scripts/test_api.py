import requests
import json

def test_api_endpoints():
    """API endpoints-ləri test edir"""
    
    base_url = "http://127.0.0.1:8000/api"
    
    print("API Endpoints test edilir...")
    print(f"Base URL: {base_url}")
    
    # Test endpoints
    endpoints = [
        ("GET", "/books/categories/", "Kateqoriyalar"),
        ("GET", "/books/", "Kitablar siyahısı"),
        ("GET", "/books/featured/", "Seçilmiş kitablar"),
        ("GET", "/books/bestsellers/", "Bestseller kitablar"),
        ("GET", "/books/new/", "Yeni kitablar"),
        ("GET", "/books/stats/", "Kitab statistikaları"),
    ]
    
    print("\n" + "="*50)
    
    for method, endpoint, description in endpoints:
        try:
            url = base_url + endpoint
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'results' in data:
                    count = len(data['results'])
                    print(f"✅ {description}: {count} nəticə")
                elif isinstance(data, list):
                    count = len(data)
                    print(f"✅ {description}: {count} nəticə")
                else:
                    print(f"✅ {description}: OK")
            else:
                print(f"❌ {description}: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {description}: Server əlaqə xətası")
        except requests.exceptions.Timeout:
            print(f"❌ {description}: Timeout xətası")
        except Exception as e:
            print(f"❌ {description}: {str(e)}")
    
    print("\n" + "="*50)
    
    # Test authentication endpoints
    print("\nAuthentication endpoints test edilir...")
    
    # Test registration
    try:
        register_data = {
            "username": "test_user_api",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "test123456",
            "password_confirm": "test123456"
        }
        
        response = requests.post(
            f"{base_url}/auth/register/",
            json=register_data,
            timeout=10
        )
        
        if response.status_code == 201:
            print("✅ Qeydiyyat: OK")
        elif response.status_code == 400:
            print("⚠️  Qeydiyyat: İstifadəçi mövcuddur")
        else:
            print(f"❌ Qeydiyyat: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Qeydiyyat: {str(e)}")
    
    # Test login
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(
            f"{base_url}/auth/login/",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Giriş: OK")
        else:
            print(f"❌ Giriş: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Giriş: {str(e)}")
    
    print("\n🎉 API test tamamlandı!")
    print("\nAPI Documentation:")
    print("- Books: http://127.0.0.1:8000/api/books/")
    print("- Auth: http://127.0.0.1:8000/api/auth/")
    print("- Orders: http://127.0.0.1:8000/api/orders/")

if __name__ == "__main__":
    test_api_endpoints()
