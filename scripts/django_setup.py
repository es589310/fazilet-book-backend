import os
import subprocess
import sys

def setup_django_project():
    """Django layihəsini quraşdır"""
    
    print("Django layihəsi quraşdırılır...")
    
    # Virtual environment yaradırıq
    print("1. Virtual environment yaradılır...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # Aktivasiya təlimatları
    print("\n2. Virtual environment aktivasiya edin:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Linux/Mac
        print("   source venv/bin/activate")
    
    print("\n3. Paketləri quraşdırın:")
    print("   pip install -r requirements.txt")
    
    print("\n4. Database migration:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    
    print("\n5. Superuser yaradın:")
    print("   python manage.py createsuperuser")
    
    print("\n6. Serveri işə salın:")
    print("   python manage.py runserver 8000")
    
    print("\nDjango backend 8000 portunda işləyəcək!")

if __name__ == "__main__":
    setup_django_project()
