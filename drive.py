from auth import get_credential, create_service

class GoogleDriveClient():
    """
    This is a class for Google Drive Client.

    Attributes:
        credential_files (str): Path for the credential file from Google Cloud Project
        token_file (str): Path for saving our token for automatic authentication
    """
    def __init__(self, credential_file, token_file, scopes):
        self.google_authorizer = get_credential(credential_file, token_file, scopes)
    
    def export_file(self, file_id, mime_type):
        """Returns the exported file that has specific mime_type"""

        drive = create_service('drive', 'v3', self.google_authorizer)

        result = drive.files().export(
            fileId = file_id,
            mimeType = mime_type
        ).execute()

        return result
    
    def get_file(self, file_id):
        """Returns the metadata of the specific file"""

        drive = create_service('drive', 'v3', self.google_authorizer)

        result = drive.files().get(
            fileId = file_id
        ).execute()

        return result
    
    def copy_file(self, file_id, options):
        """Returns the copy of the specific file"""

        drive = create_service('drive', 'v3', self.google_authorizer)

        result = drive.files().copy(
            fileId = file_id,
            enforceSingleParent = True,
            body = {
                "name": options['name'],
                "parents": [
                    options['parentFolderId'],
                ],
            }
        ).execute()

        return result

    def list_files(self, corpora_type, drive_id):
        """Returns the list of the files from specific drive_id"""

        data = {
            'corpora': corpora_type,
            'includeItemsFromAllDrives': True,
            'supportsAllDrives': True,
        }

        if (corpora_type == 'drive'):
            data['driveId'] = drive_id

        return self._paginate(data)

    def _paginate(self, data):
        """Helper function of the list_files function"""

        drive = create_service('drive', 'v3', self.google_authorizer)

        results = []
        should_paginate = True
        page_token = None

        while (should_paginate):
            data['pageToken'] = page_token

            result = drive.files().list(**data).execute()

            page_token = result['nextPageToken'] if ('nextPageToken' in result) else 0 
            
            should_paginate = isinstance(page_token, str)
            results.append(result['files'])
        
        return results