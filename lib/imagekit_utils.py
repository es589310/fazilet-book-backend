import os
import requests
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib.parse

class ImageKitManager:
    def __init__(self):
        self.public_key = settings.IMAGEKIT_PUBLIC_KEY
        self.private_key = settings.IMAGEKIT_PRIVATE_KEY
        self.url_endpoint = settings.IMAGEKIT_URL_ENDPOINT
        self.folder = settings.IMAGEKIT_FOLDER
    
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