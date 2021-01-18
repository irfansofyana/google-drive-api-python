from auth import get_credentials, create_service
# from html_sanitizer import Sanitizer
# from htmllaundry import sanitize
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class GoogleDriveClient():
    def __init__(self, credential_files, token_file, scopes):
        self.google_authorizer = get_credentials(credential_files, token_file, scopes)
    
    def export_file(self, file_id, mime_type):
        drive = create_service('drive', 'v3', self.google_authorizer)

        results = drive.files().export(
            fileId=file_id,
            mimeType=mime_type
        ).execute()

        return results
    
    def get_file(self, file_id):
        drive = create_service('drive', 'v3', self.google_authorizer)

        results = drive.files().get(
            fileId=file_id
        ).execute()

        return results

    def list_files(self, drive_id):
        return self._paginate()

    # WIP
    def paginate(self, resource, data):
        drive = create_service('drive', 'v3', self.google_authorizer)
        return drive