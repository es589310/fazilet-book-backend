"""
Production-ready ImageKit utilities for Dostum Kitab
Handles image uploads, optimization, and fallbacks
"""

import os
import logging
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from typing import Dict, Optional, Union

logger = logging.getLogger(__name__)

class ImageKitManager:
    """Production ImageKit manager with error handling and fallbacks"""
    
    def __init__(self):
        self.enabled = getattr(settings, 'IMAGEKIT_ENABLED', False)
        self.public_key = getattr(settings, 'IMAGEKIT_PUBLIC_KEY', '')
        self.private_key = getattr(settings, 'IMAGEKIT_PRIVATE_KEY', '')
        self.url_endpoint = getattr(settings, 'IMAGEKIT_URL_ENDPOINT', '')
        self.folder = getattr(settings, 'IMAGEKIT_FOLDER', 'dostumkitab')
        
        if self.enabled and not all([self.public_key, self.private_key, self.url_endpoint]):
            logger.warning("ImageKit enabled but missing required configuration")
            self.enabled = False
    
    def upload_image(self, image_file: UploadedFile, folder_path: str = 'general', 
                    filename: Optional[str] = None) -> Dict[str, Union[str, bool, int]]:
        """
        Upload image to ImageKit with production error handling
        
        Args:
            image_file: Django UploadedFile instance
            folder_path: Folder path in ImageKit
            filename: Custom filename (optional)
            
        Returns:
            Dict with upload result
        """
        if not self.enabled:
            return self._fallback_upload(image_file, folder_path, filename)
        
        try:
            # Import ImageKit only when needed
            from imagekitio import ImageKit
            from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
            
            # Initialize ImageKit
            imagekit = ImageKit(
                private_key=self.private_key,
                public_key=self.public_key,
                url_endpoint=self.url_endpoint
            )
            
            # Prepare upload options
            if not filename:
                filename = f"{folder_path}_{image_file.name}"
            
            options = UploadFileRequestOptions(
                use_unique_file_name=True,
                folder=f"{self.folder}/{folder_path}",
                response_fields=["is_private_file", "tags", "custom_coordinates", "custom_metadata"]
            )
            
            # Upload file
            upload = imagekit.upload_file(
                file=image_file,
                file_name=filename,
                options=options
            )
            
            if upload.response_metadata.http_status_code == 200:
                result = upload.response_metadata.raw
                return {
                    'success': True,
                    'url': result.get('url', ''),
                    'file_id': result.get('fileId', ''),
                    'filename': result.get('name', filename),
                    'size': result.get('size', 0),
                    'width': result.get('width', 0),
                    'height': result.get('height', 0)
                }
            else:
                logger.error(f"ImageKit upload failed: {upload.response_metadata.raw}")
                return {
                    'success': False,
                    'error': 'ImageKit upload failed'
                }
                
        except ImportError:
            logger.warning("ImageKit library not installed, using fallback")
            return self._fallback_upload(image_file, folder_path, filename)
        except Exception as e:
            logger.error(f"ImageKit upload error: {str(e)}")
            return {
                'success': False,
                'error': 'Upload failed'
            }
    
    def _fallback_upload(self, image_file: UploadedFile, folder_path: str, 
                         filename: Optional[str] = None) -> Dict[str, Union[str, bool, int]]:
        """
        Fallback upload method when ImageKit is not available
        Saves to local media directory
        """
        try:
            if not filename:
                filename = f"{folder_path}_{image_file.name}"
            
            # Create directory if it doesn't exist
            media_path = os.path.join(settings.MEDIA_ROOT, folder_path)
            os.makedirs(media_path, exist_ok=True)
            
            # Save file locally
            file_path = os.path.join(media_path, filename)
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # Return local file info
            return {
                'success': True,
                'url': f"{settings.MEDIA_URL}{folder_path}/{filename}",
                'file_id': f"local_{filename}",
                'filename': filename,
                'size': image_file.size,
                'width': 0,  # Local files don't have dimensions
                'height': 0
            }
            
        except Exception as e:
            logger.error(f"Fallback upload error: {str(e)}")
            return {
                'success': False,
                'error': 'Local upload failed'
            }
    
    def optimize_image_url(self, filename: str, width: Optional[int] = None, 
                          height: Optional[int] = None, quality: int = 80) -> str:
        """
        Generate optimized image URL from ImageKit
        
        Args:
            filename: Image filename
            width: Target width
            height: Target height
            quality: Image quality (1-100)
            
        Returns:
            Optimized image URL
        """
        if not self.enabled:
            return f"{settings.MEDIA_URL}general/{filename}"
        
        try:
            # Build transformation parameters
        transformations = []
        
        if width:
            transformations.append(f"w-{width}")
        if height:
            transformations.append(f"h-{height}")
        
        transformations.append(f"q-{quality}")
            
            # Construct URL
            if transformations:
                transform_str = ",".join(transformations)
                return f"{self.url_endpoint}{self.folder}/{filename}?tr={transform_str}"
            else:
                return f"{self.url_endpoint}{self.folder}/{filename}"
                
        except Exception as e:
            logger.error(f"ImageKit URL generation error: {str(e)}")
            return f"{settings.MEDIA_URL}general/{filename}"
    
    def delete_image(self, file_id: str) -> bool:
        """
        Delete image from ImageKit
        
        Args:
            file_id: ImageKit file ID
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.warning("ImageKit not enabled, cannot delete image")
            return False
        
        try:
            from imagekitio import ImageKit
            
            imagekit = ImageKit(
                private_key=self.private_key,
                public_key=self.public_key,
                url_endpoint=self.url_endpoint
            )
            
            result = imagekit.delete_file(file_id)
            return result.response_metadata.http_status_code == 200
            
        except ImportError:
            logger.warning("ImageKit library not installed")
            return False
    except Exception as e:
            logger.error(f"ImageKit delete error: {str(e)}")
            return False
    
    def get_image_info(self, file_id: str) -> Optional[Dict]:
        """
        Get image information from ImageKit
        
        Args:
            file_id: ImageKit file ID
            
        Returns:
            Image info dict or None
        """
        if not self.enabled:
            return None
        
        try:
            from imagekitio import ImageKit
            
            imagekit = ImageKit(
                private_key=self.private_key,
                public_key=self.public_key,
                url_endpoint=self.url_endpoint
            )
            
            result = imagekit.get_file_details(file_id)
            if result.response_metadata.http_status_code == 200:
                return result.response_metadata.raw
            return None
            
        except ImportError:
            logger.warning("ImageKit library not installed")
            return None
    except Exception as e:
            logger.error(f"ImageKit info error: {str(e)}")
            return None

# Global instance
imagekit_manager = ImageKitManager()

# Convenience functions
def upload_image(image_file: UploadedFile, folder_path: str = 'general', 
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
    return imagekit_manager.get_image_info(file_id) 