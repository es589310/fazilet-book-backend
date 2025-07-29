import os
import subprocess
import sys

def create_migrations():
    """Django migration faylları yaradır"""
    
    print("Django migration faylları yaradılır...")
    
    apps = ['books', 'users', 'orders']
    
    for app in apps:
        print(f"\n{app} app üçün migration yaradılır...")
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'makemigrations', app
            ], capture_output=True, text=True, check=True)
            print(f"✅ {app} migration yaradıldı")
            if result.stdout:
                print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"❌ {app} migration xətası: {e}")
            if e.stderr:
                print(e.stderr)
    
    print("\nBütün migration faylları yaradılır...")
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'makemigrations'
        ], capture_output=True, text=True, check=True)
        print("✅ Ümumi migration yaradıldı")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ümumi migration xətası: {e}")
        if e.stderr:
            print(e.stderr)
    
    print("\nMigration faylları tətbiq edilir...")
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate'
        ], capture_output=True, text=True, check=True)
        print("✅ Migration faylları tətbiq edildi")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration tətbiqi xətası: {e}")
        if e.stderr:
            print(e.stderr)
    
    print("\n🎉 Database migration tamamlandı!")
    print("\nNövbəti addım: python scripts/create_sample_data.py")

if __name__ == "__main__":
    create_migrations()
