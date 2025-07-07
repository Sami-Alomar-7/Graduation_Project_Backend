import clamd
import os
import logging
from django.conf import settings
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class VirusScanner:
    """
    Virus scanning utility using ClamAV
    """
    
    def __init__(self):
        self.cd = None
        self._connect()
    
    def _connect(self):
        """Connect to ClamAV daemon"""
        try:
            # Try Unix socket first (Linux/Mac)
            self.cd = clamd.ClamdUnixSocket()
            self.cd.ping()
        except:
            try:
                # Try TCP socket (Windows or remote)
                self.cd = clamd.ClamdNetworkSocket(
                    host=getattr(settings, 'CLAMD_HOST', 'localhost'),
                    port=getattr(settings, 'CLAMD_PORT', 3310)
                )
                self.cd.ping()
            except Exception as e:
                logger.warning(f"Could not connect to ClamAV: {e}")
                self.cd = None
    
    def scan_file(self, file_path):
        """
        Scan a file for viruses
        
        Args:
            file_path: Path to the file to scan
            
        Returns:
            dict: {'clean': bool, 'result': str, 'error': str}
        """
        if not self.cd:
            logger.warning("ClamAV not available, skipping virus scan")
            return {
                'clean': True,
                'result': 'ClamAV not available',
                'error': None
            }
        
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    'clean': False,
                    'result': 'File not found',
                    'error': 'File does not exist'
                }
            
            # Scan the file
            scan_result = self.cd.instream(open(file_path, 'rb'))
            
            if scan_result['stream'][0] == 'FOUND':
                return {
                    'clean': False,
                    'result': f"Virus detected: {scan_result['stream'][1]}",
                    'error': None
                }
            elif scan_result['stream'][0] == 'OK':
                return {
                    'clean': True,
                    'result': 'File is clean',
                    'error': None
                }
            else:
                return {
                    'clean': False,
                    'result': f"Unknown scan result: {scan_result}",
                    'error': None
                }
                
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")
            return {
                'clean': False,
                'result': 'Scan failed',
                'error': str(e)
            }
    
    def scan_django_file(self, django_file):
        """
        Scan a Django uploaded file for viruses
        
        Args:
            django_file: Django UploadedFile object
            
        Returns:
            dict: {'clean': bool, 'result': str, 'error': str}
        """
        try:
            # Save to temporary file for scanning
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in django_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            # Scan the temporary file
            result = self.scan_file(temp_file_path)
            
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
            
            return result
            
        except Exception as e:
            logger.error(f"Error scanning Django file: {e}")
            return {
                'clean': False,
                'result': 'Scan failed',
                'error': str(e)
            }

# Global virus scanner instance
virus_scanner = VirusScanner() 