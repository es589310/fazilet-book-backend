# Sosial Media Linkləri Təlimatı

## 📱 Mövcud Funksionallıq

Bu layihədə sosial media linkləri Django admin panelindən idarə olunur və frontend-də navbar və footer-da avtomatik olaraq göstərilir.

## 🚀 Quraşdırma

### 1. Backend (Django)

- **Model**: `contact/models.py` - `SocialMediaLink` modeli
- **Admin**: `contact/admin.py` - Admin panel konfiqurasiyası
- **API**: `contact/views.py` - `get_social_media_links` endpoint
- **URL**: `/api/contact/social-links/`

### 2. Frontend (Next.js)

- **Komponent**: `components/social-media-icons.tsx`
- **Navbar**: `components/navigation-bar.tsx` - sağ tərəfdə
- **Footer**: `components/footer.tsx` - ayrı sütunda

## ⚙️ Admin Panelində İdarə Etmə

### Sosial Media Linkləri Əlavə Etmək:

1. Django admin panelinə daxil olun: `http://localhost:8000/admin/`
2. "Contact" bölməsində "Sosial media linkləri" seçin
3. "Sosial media linki əlavə et" düyməsinə klikləyin
4. Məlumatları doldurun:
   - **Platforma**: Facebook, Instagram, Twitter, YouTube, LinkedIn, Telegram
   - **Link**: Sosial media səhifəsinin URL-i
   - **İkon CSS sinifi**: (Boş buraxa bilərsiniz - avtomatik təyin olunacaq)
   - **Aktiv**: Linkin göstərilib-göstərilməməsi
   - **Sıra**: İkonların göstərilmə sırası

### Mövcud Linkləri Düzəltmək:

1. Admin panelində "Sosial media linkləri" siyahısına keçin
2. Düzəltmək istədiyiniz linkə klikləyin
3. Məlumatları yeniləyin və saxlayın

### Linkləri Deaktiv Etmək:

1. Admin panelində linki açın
2. "Aktiv" sahəsini işarəsiz edin
3. Saxlayın

## 🎨 Frontend İstifadəsi

### Sosial Media İkonları Komponenti:

```tsx
import SocialMediaIcons from './components/social-media-icons';

// Navbar üçün
<SocialMediaIcons variant="navbar" />

// Footer üçün
<SocialMediaIcons variant="footer" />
```

### Variantlar:

- **`navbar`**: Kiçik ikonlar, mavi hover effekti
- **`footer`**: Böyük ikonlar, ağ hover effekti

## 🔧 API Endpoint

### GET `/api/contact/social-links/`

**Response:**
```json
{
  "links": [
    {
      "platform": "facebook",
      "url": "https://facebook.com/dostumkitab",
      "icon_class": "fab fa-facebook-f",
      "is_active": true,
      "order": 1
    }
  ],
  "success": true
}
```

## 📱 Dəstəklənən Platformalar

- ✅ Facebook
- ✅ Instagram  
- ✅ Twitter
- ✅ YouTube
- ✅ LinkedIn
- ✅ Telegram

## 🎯 Xüsusiyyətlər

- **Avtomatik İkonlar**: Hər platforma üçün uyğun ikon avtomatik təyin olunur
- **Responsive Dizayn**: Navbar və footer-da fərqli ölçülər
- **Hover Effektləri**: İnteraktiv istifadəçi təcrübəsi
- **Admin İdarəetməsi**: Django admin panelindən tam idarə
- **API Avtomatik Yeniləmə**: Frontend avtomatik olaraq yenilənir

## 🚨 Diqqət

- Linklər `is_active = True` olduqda göstərilir
- `order` sahəsi ikonların göstərilmə sırasını təyin edir
- Platforma adı unikal olmalıdır (hər platforma üçün yalnız bir link)
- İkon CSS sinifi boş buraxıldıqda avtomatik təyin olunur

## 🔄 Yeniləmə

Sosial media linklərini dəyişdirdikdən sonra frontend avtomatik olaraq yenilənəcək. Əlavə cache təmizləmə tələb olunmur. 