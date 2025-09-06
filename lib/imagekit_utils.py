"""
Production-ready ImageKit utilities for Dostum Kitab
Handles image uploads, optimization, and fallbacks
"""

import requests
import os
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from typing import Dict, Optional, Union

class ImageKitManager:
    def __init__(self):
        self.public_key = getattr(settings, 'IMAGEKIT_PUBLIC_KEY', '')
        self.private_key = getattr(settings, 'IMAGEKIT_PRIVATE_KEY', '')
        self.url_endpoint = getattr(settings, 'IMAGEKIT_URL_ENDPOINT', '')
        self.folder = getattr(settings, 'IMAGEKIT_FOLDER', 'dostumkitab')
    
    def upload_image(self, image_file, folder_path=None, filename=None):
        """
        Şəkli ImageKit-ə yükləyir
        """
        if folder_path is None:
            folder_path = self.folder
        
        if filename is None:
            filename = os.path.basename(image_file.name)
        
        # ImageKit API endpoint
        upload_url = "https://upload.imagekit.io/api/v1/files/upload"
        
        # Şəkil məlumatları
        files = {'file': image_file}
        data = {
            'fileName': filename,
            'folder': folder_path,
            'useUniqueFileName': 'true',
            'tags': 'kitab,bookstore',
            'responseFields': 'isPrivateFile,metadata'
        }
        
        # Authentication
        auth = (self.private_key, '')
        
        try:
            response = requests.post(upload_url, files=files, data=data, auth=auth)
            response.raise_for_status()
            
            result = response.json()
            return {
                'success': True,
                'url': result.get('url'),
                'file_id': result.get('fileId'),
                'filename': result.get('name'),
                'size': result.get('size'),
                'width': result.get('width'),
                'height': result.get('height')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_image_url(self, filename, transformation=None):
        """
        Şəklin URL-ni qaytarır
        """
        base_url = f"{self.url_endpoint}{filename}"
        
        if transformation:
            # Transformation parametrlərini əlavə edir
            base_url += f"?tr={transformation}"
        
        return base_url
    
    def delete_image(self, file_id):
        """
        Şəkli ImageKit-dən silir
        """
        delete_url = "https://api.imagekit.io/v1/files/" + file_id
        
        headers = {
            'Authorization': f'Basic {self.private_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.delete(delete_url, headers=headers)
            response.raise_for_status()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def optimize_image_url(self, filename, width=None, height=None, quality=80, format='auto'):
        """
        Optimizasiya edilmiş şəklin URL-ni qaytarır
        """
        transformations = []
        
        if width:
            transformations.append(f"w-{width}")
        if height:
            transformations.append(f"h-{height}")
        
        transformations.append(f"q-{quality}")
        transformations.append(f"f-{format}")
        
        transformation_string = ",".join(transformations)
        return self.get_image_url(filename, transformation_string)

# Global instance
imagekit_manager = ImageKitManager()

def get_imagekit_url(image_field):
    """
    Django ImageField-dan ImageKit URL-ni qaytarır
    """
    try:
        if not image_field:
            return None
        
        # Əgər ImageField-ın path-i varsa, onu istifadə et
        if hasattr(image_field, 'path') and os.path.exists(image_field.path):
            # Şəkli ImageKit-ə yüklə
            result = upload_logo_to_imagekit(image_field)
            if result['success']:
                return result['url']
        
        # Əgər ImageField-ın url-i varsa, onu istifadə et
        if hasattr(image_field, 'url'):
            return image_field.url
            
        return None
    except Exception as e:
        print(f"ImageKit URL alma xətası: {str(e)}")
        return None

def upload_logo_to_imagekit(image_file, folder_name='site'):
    """
    Logo faylını ImageKit-ə yükləyir
    """
    try:
        # ImageKit API endpoint
        upload_url = "https://api.imagekit.io/v1/files/upload"
        
        # API key-lər
        private_key = settings.IMAGEKIT_PRIVATE_KEY
        public_key = settings.IMAGEKIT_PUBLIC_KEY
        
        # Fayl adını al
        file_name = os.path.basename(image_file.name)
        
        # Faylı oxu
        with open(image_file.path, 'rb') as f:
            files = {'file': (file_name, f, 'image/png')}
            
            data = {
                'fileName': file_name,
                'folder': folder_name,
                'useUniqueFileName': True,
                'tags': ['logo', 'site'],
                'responseFields': ['url', 'fileId', 'name']
            }
            
            headers = {
                'Authorization': f'Basic {private_key}'
            }
            
            # ImageKit-ə yüklə
            response = requests.post(upload_url, files=files, data=data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'url': result.get('url'),
                    'file_id': result.get('fileId'),
                    'file_name': result.get('name')
                }
            else:
                return {
                    'success': False,
                    'error': f'ImageKit API xətası: {response.status_code}'
                }
                
    except Exception as e:
        return {
            'success': False,
            'error': f'Logo yükləmə xətası: {str(e)}'
        }

def delete_logo_from_imagekit(file_id):
    """
    ImageKit-dən logo faylını silir
    """
    try:
        delete_url = f"https://api.imagekit.io/v1/files/{file_id}"
        
        headers = {
            'Authorization': f'Basic {settings.IMAGEKIT_PRIVATE_KEY}'
        }
        
        response = requests.delete(delete_url, headers=headers)
        
        if response.status_code == 200:
            return {'success': True}
        else:
            return {
                'success': False,
                'error': f'ImageKit silmə xətası: {response.status_code}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': f'Logo silmə xətası: {str(e)}'
        }

# Convenience functions
def upload_image(image_file, folder_path: str = 'general', 
                filename: Optional[str] = None) -> Dict[str, Union[str, bool, int]]:
    """Convenience function for image upload"""
    return imagekit_manager.upload_image(image_file, folder_path, filename)

def optimize_image_url(filename: str, width: Optional[int] = None, 
                      height: Optional[int] = None, quality: int = 80) -> str:
    """Convenience function for image URL optimization"""
    return imagekit_manager.optimize_image_url(filename, width, height, quality)

def delete_image(file_id: str) -> bool:
    """Convenience function for image deletion"""
    return imagekit_manager.delete_image(file_id)

def get_image_info(file_id: str) -> Optional[Dict]:
    """Convenience function for getting image info"""
    return imagekit_manager.get_image_url(file_id)

# Create global instance
imagekit_manager = ImageKitManager() 