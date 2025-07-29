import os
import sys
import django
from datetime import date, datetime, timedelta
from decimal import Decimal

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitab_backend.settings')
django.setup()

from django.contrib.auth.models import User
from books.models import Category, Author, Publisher, Book, BookReview
from users.models import UserProfile, Address
from orders.models import Cart, CartItem, Order, OrderItem

def create_sample_data():
    """Sample data yaradır"""
    
    print("Sample data yaradılır...")
    
    # 1. Superuser yarat (əgər yoxdursa)
    if not User.objects.filter(is_superuser=True).exists():
        print("Superuser yaradılır...")
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@kitabsat.az',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print("✅ Superuser yaradıldı: admin / admin123")
    else:
        admin_user = User.objects.filter(is_superuser=True).first()
        print("✅ Superuser mövcuddur")
    
    # 2. Test istifadəçiləri yarat
    print("\nTest istifadəçiləri yaradılır...")
    test_users = [
        {
            'username': 'ali_mammadov',
            'email': 'ali@example.com',
            'first_name': 'Əli',
            'last_name': 'Məmmədov',
            'password': 'test123'
        },
        {
            'username': 'leyla_hasanova',
            'email': 'leyla@example.com',
            'first_name': 'Leyla',
            'last_name': 'Həsənova',
            'password': 'test123'
        },
        {
            'username': 'rashad_aliyev',
            'email': 'rashad@example.com',
            'first_name': 'Rəşad',
            'last_name': 'Əliyev',
            'password': 'test123'
        }
    ]
    
    created_users = []
    for user_data in test_users:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"✅ İstifadəçi yaradıldı: {user.username}")
        created_users.append(user)
    
    # 3. Kateqoriyalar yarat
    print("\nKateqoriyalar yaradılır...")
    categories_data = [
        {'name': 'Dini Kitablar', 'slug': 'dini-kitablar', 'description': 'İslami və digər dini kitablar'},
        {'name': 'Uşaqlar üçün Kitablar', 'slug': 'usaqlar-ucun-kitablar', 'description': 'Uşaq ədəbiyyatı və təhsil kitabları'},
        {'name': 'Fəlsəfi Kitablar', 'slug': 'felsefe-kitablari', 'description': 'Fəlsəfə və düşüncə kitabları'},
        {'name': 'Tarixi Kitablar', 'slug': 'tarixi-kitablar', 'description': 'Tarix və bioqrafiya kitabları'},
        {'name': 'Elmi Kitablar', 'slug': 'elmi-kitablar', 'description': 'Elm və texnologiya kitabları'},
        {'name': 'Ədəbiyyat', 'slug': 'edebiyyat', 'description': 'Roman, hekayə və şeir kitabları'},
        {'name': 'Biznes Kitabları', 'slug': 'biznes-kitablari', 'description': 'İdarəetmə və biznes kitabları'},
        {'name': 'Psixologiya', 'slug': 'psixologiya', 'description': 'Psixologiya və özünü inkişaf kitabları'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f"✅ Kateqoriya yaradıldı: {category.name}")
        categories.append(category)
    
    # 4. Müəlliflər yarat
    print("\nMüəlliflər yaradılır...")
    authors_data = [
        {'name': 'Antoine de Saint-Exupéry', 'nationality': 'Fransız', 'birth_date': date(1900, 6, 29)},
        {'name': 'George Orwell', 'nationality': 'İngilis', 'birth_date': date(1903, 6, 25)},
        {'name': 'Paulo Coelho', 'nationality': 'Braziliyalı', 'birth_date': date(1947, 8, 24)},
        {'name': 'Fyodor Dostoyevski', 'nationality': 'Rus', 'birth_date': date(1821, 11, 11)},
        {'name': 'J.K. Rowling', 'nationality': 'İngilis', 'birth_date': date(1965, 7, 31)},
        {'name': 'Frank Herbert', 'nationality': 'Amerika', 'birth_date': date(1920, 10, 8)},
        {'name': 'Gabriel García Márquez', 'nationality': 'Kolumbiyalı', 'birth_date': date(1927, 3, 6)},
        {'name': 'Yuval Noah Harari', 'nationality': 'İsrail', 'birth_date': date(1976, 2, 24)},
        {'name': 'James Clear', 'nationality': 'Amerika', 'birth_date': date(1986, 1, 2)},
        {'name': 'Nizami Gəncəvi', 'nationality': 'Azərbaycan', 'birth_date': date(1141, 1, 1)},
    ]
    
    authors = []
    for author_data in authors_data:
        author, created = Author.objects.get_or_create(
            name=author_data['name'],
            defaults=author_data
        )
        if created:
            print(f"✅ Müəllif yaradıldı: {author.name}")
        authors.append(author)
    
    # 5. Nəşriyyatlar yarat
    print("\nNəşriyyatlar yaradılır...")
    publishers_data = [
        {'name': 'Qanun Nəşriyyatı', 'address': 'Bakı, Azərbaycan', 'phone': '+994 12 123 45 67'},
        {'name': 'Yazıçı Nəşriyyatı', 'address': 'Bakı, Azərbaycan', 'phone': '+994 12 234 56 78'},
        {'name': 'Elm Nəşriyyatı', 'address': 'Bakı, Azərbaycan', 'phone': '+994 12 345 67 89'},
        {'name': 'Penguin Books', 'address': 'London, UK', 'phone': '+44 20 1234 5678'},
        {'name': 'HarperCollins', 'address': 'New York, USA', 'phone': '+1 212 123 4567'},
    ]
    
    publishers = []
    for pub_data in publishers_data:
        publisher, created = Publisher.objects.get_or_create(
            name=pub_data['name'],
            defaults=pub_data
        )
        if created:
            print(f"✅ Nəşriyyat yaradıldı: {publisher.name}")
        publishers.append(publisher)
    
    # 6. Kitablar yarat
    print("\nKitablar yaradılır...")
    books_data = [
        {
            'title': 'Kiçik Şahzadə',
            'slug': 'kicik-shahzade',
            'category': categories[5],  # Ədəbiyyat
            'publisher': publishers[3],  # Penguin Books
            'authors': [authors[0]],  # Antoine de Saint-Exupéry
            'description': 'Dünyada ən çox oxunan kitablardan biri. Uşaq və böyüklər üçün fəlsəfi hekayə.',
            'language': 'az',
            'pages': 120,
            'publication_date': date(2020, 1, 15),
            'price': Decimal('15.99'),
            'original_price': Decimal('19.99'),
            'stock_quantity': 50,
            'is_featured': True,
            'is_bestseller': True,
        },
        {
            'title': '1984',
            'slug': '1984',
            'category': categories[5],  # Ədəbiyyat
            'publisher': publishers[3],  # Penguin Books
            'authors': [authors[1]],  # George Orwell
            'description': 'Distopik ədəbiyyatın şah əsəri. Totalitar rejimin tənqidi.',
            'language': 'az',
            'pages': 350,
            'publication_date': date(2019, 5, 20),
            'price': Decimal('12.99'),
            'original_price': Decimal('16.99'),
            'stock_quantity': 30,
            'is_featured': True,
            'is_bestseller': True,
        },
        {
            'title': 'Alxemik',
            'slug': 'alxemik',
            'category': categories[2],  # Fəlsəfi Kitablar
            'publisher': publishers[4],  # HarperCollins
            'authors': [authors[2]],  # Paulo Coelho
            'description': 'Ruhani səyahət və özünü kəşf etmə haqqında fəlsəfi roman.',
            'language': 'az',
            'pages': 200,
            'publication_date': date(2021, 3, 10),
            'price': Decimal('14.99'),
            'original_price': Decimal('18.99'),
            'stock_quantity': 40,
            'is_featured': True,
        },
        {
            'title': 'Cinayət və Cəza',
            'slug': 'cinayet-ve-ceza',
            'category': categories[5],  # Ədəbiyyat
            'publisher': publishers[0],  # Qanun Nəşriyyatı
            'authors': [authors[3]],  # Fyodor Dostoyevski
            'description': 'Rus ədəbiyyatının klassik əsəri. Psixoloji roman.',
            'language': 'az',
            'pages': 600,
            'publication_date': date(2020, 8, 5),
            'price': Decimal('13.99'),
            'original_price': Decimal('17.99'),
            'stock_quantity': 25,
            'is_bestseller': True,
        },
        {
            'title': 'Harri Potter və Fəlsəfə Daşı',
            'slug': 'harri-potter-felsefe-dashi',
            'category': categories[1],  # Uşaqlar üçün Kitablar
            'publisher': publishers[1],  # Yazıçı Nəşriyyatı
            'authors': [authors[4]],  # J.K. Rowling
            'description': 'Məşhur sehrli dünya haqqında fantastik roman seriyasının ilk kitabı.',
            'language': 'az',
            'pages': 400,
            'publication_date': date(2021, 6, 1),
            'price': Decimal('16.99'),
            'original_price': Decimal('21.99'),
            'stock_quantity': 60,
            'is_featured': True,
            'is_new': True,
        },
        {
            'title': 'Dune',
            'slug': 'dune',
            'category': categories[4],  # Elmi Kitablar
            'publisher': publishers[4],  # HarperCollins
            'authors': [authors[5]],  # Frank Herbert
            'description': 'Elmi-fantastik ədəbiyyatın şah əsəri.',
            'language': 'en',
            'pages': 800,
            'publication_date': date(2020, 12, 15),
            'price': Decimal('19.99'),
            'original_price': Decimal('25.99'),
            'stock_quantity': 20,
            'is_new': True,
        },
        {
            'title': 'Yüz İl Tənhalıq',
            'slug': 'yuz-il-tenhaliq',
            'category': categories[5],  # Ədəbiyyat
            'publisher': publishers[0],  # Qanun Nəşriyyatı
            'authors': [authors[6]],  # Gabriel García Márquez
            'description': 'Maqik realizm janrının şah əsəri.',
            'language': 'az',
            'pages': 450,
            'publication_date': date(2019, 11, 20),
            'price': Decimal('15.99'),
            'original_price': Decimal('19.99'),
            'stock_quantity': 35,
        },
        {
            'title': 'Sapiens',
            'slug': 'sapiens',
            'category': categories[3],  # Tarixi Kitablar
            'publisher': publishers[2],  # Elm Nəşriyyatı
            'authors': [authors[7]],  # Yuval Noah Harari
            'description': 'İnsanlığın tarixi haqqında məşhur kitab.',
            'language': 'az',
            'pages': 500,
            'publication_date': date(2021, 1, 10),
            'price': Decimal('17.99'),
            'original_price': Decimal('22.99'),
            'stock_quantity': 45,
            'is_bestseller': True,
        },
        {
            'title': 'Atomic Habits',
            'slug': 'atomic-habits',
            'category': categories[7],  # Psixologiya
            'publisher': publishers[4],  # HarperCollins
            'authors': [authors[8]],  # James Clear
            'description': 'Kiçik dəyişikliklərlə böyük nəticələr əldə etmək.',
            'language': 'az',
            'pages': 320,
            'publication_date': date(2021, 4, 5),
            'price': Decimal('14.99'),
            'original_price': Decimal('18.99'),
            'stock_quantity': 55,
            'is_featured': True,
            'is_new': True,
        },
        {
            'title': 'Xəmsə',
            'slug': 'xemse',
            'category': categories[5],  # Ədəbiyyat
            'publisher': publishers[1],  # Yazıçı Nəşriyyatı
            'authors': [authors[9]],  # Nizami Gəncəvi
            'description': 'Azərbaycan ədəbiyyatının klassik əsəri.',
            'language': 'az',
            'pages': 600,
            'publication_date': date(2020, 10, 1),
            'price': Decimal('22.99'),
            'original_price': Decimal('29.99'),
            'stock_quantity': 30,
            'is_featured': True,
        },
    ]
    
    books = []
    for book_data in books_data:
        authors_list = book_data.pop('authors')
        book, created = Book.objects.get_or_create(
            slug=book_data['slug'],
            defaults=book_data
        )
        if created:
            book.authors.set(authors_list)
            print(f"✅ Kitab yaradıldı: {book.title}")
        books.append(book)
    
    # 7. Kitab rəyləri yarat
    print("\nKitab rəyləri yaradılır...")
    import random
    
    review_comments = [
        "Çox gözəl kitab, hər kəsə tövsiyə edirəm!",
        "Maraqlı və öyrədici idi.",
        "Klassik əsər, mütləq oxunmalıdır.",
        "Çox bəyəndim, təkrar oxuyacağam.",
        "Müəllifin yazı tərzi çox gözəldir.",
        "Bu kitab həyatıma çox təsir etdi.",
        "Oxumaq üçün ideal kitab.",
        "Hər yaşdan insana uyğundur.",
    ]
    
    for book in books[:5]:  # İlk 5 kitab üçün rəy yarat
        for user in created_users:
            if random.choice([True, False]):  # 50% ehtimal
                review, created = BookReview.objects.get_or_create(
                    book=book,
                    user=user,
                    defaults={
                        'rating': random.randint(4, 5),
                        'comment': random.choice(review_comments)
                    }
                )
                if created:
                    print(f"✅ Rəy yaradıldı: {book.title} - {user.username}")
    
    # 8. İstifadəçi ünvanları yarat
    print("\nİstifadəçi ünvanları yaradılır...")
    for user in created_users:
        address, created = Address.objects.get_or_create(
            user=user,
            title="Ev ünvanı",
            defaults={
                'address_type': 'home',
                'full_address': f"{user.first_name} {user.last_name} evi, Bakı şəhəri",
                'city': 'Bakı',
                'district': 'Nəsimi',
                'postal_code': 'AZ1000',
                'phone': '+994 50 123 45 67',
                'is_default': True,
            }
        )
        if created:
            print(f"✅ Ünvan yaradıldı: {user.username}")
    
    print("\n🎉 Sample data yaradılması tamamlandı!")
    print("\nYaradılan məlumatlar:")
    print(f"- Kateqoriyalar: {Category.objects.count()}")
    print(f"- Müəlliflər: {Author.objects.count()}")
    print(f"- Nəşriyyatlar: {Publisher.objects.count()}")
    print(f"- Kitablar: {Book.objects.count()}")
    print(f"- İstifadəçilər: {User.objects.count()}")
    print(f"- Rəylər: {BookReview.objects.count()}")
    print(f"- Ünvanlar: {Address.objects.count()}")
    
    print("\nTest hesabları:")
    print("- Admin: admin / admin123")
    print("- Test istifadəçi 1: ali_mammadov / test123")
    print("- Test istifadəçi 2: leyla_hasanova / test123")
    print("- Test istifadəçi 3: rashad_aliyev / test123")
    
    print("\nDjango admin panel: http://127.0.0.1:8000/admin/")
    print("API base URL: http://127.0.0.1:8000/api/")

if __name__ == "__main__":
    create_sample_data()
