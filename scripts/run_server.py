import os
import subprocess
import sys
import time

def run_django_server():
    """Django development server-ini işə salır"""
    
    print("Django development server işə salınır...")
    print("Port: 8000")
    print("URL: http://127.0.0.1:8000/")
    print("Admin Panel: http://127.0.0.1:8000/admin/")
    print("API Base: http://127.0.0.1:8000/api/")
    print("\nServer-i dayandırmaq üçün Ctrl+C basın\n")
    
    try:
        # Collectstatic (production üçün)
        if not os.environ.get('DEBUG', 'True').lower() == 'true':
            print("Static fayllar toplanır...")
            subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        
        # Server-i işə sal
        subprocess.run([sys.executable, 'manage.py', 'runserver', '8000'], check=True)
        
    except KeyboardInterrupt:
        print("\n\nServer dayandırıldı.")
    except subprocess.CalledProcessError as e:
        print(f"Server xətası: {e}")
        print("\nXəta həlli üçün yoxlayın:")
        print("1. Virtual environment aktivdir?")
        print("2. Bütün paketlər quraşdırılıb?")
        print("3. Database əlaqəsi düzgündür?")
        print("4. Migration faylları tətbiq edilib?")

if __name__ == "__main__":
    run_django_server()
