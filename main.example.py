from drive import GoogleDriveClient
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']

if (__name__=="__main__"):
    client = GoogleDriveClient('credentials.json', 'token.pickle', SCOPES)

    """
        Example 1: Export specific google docs into HTML
    """
    file_id = 'FILE_ID_THAT_YOU_WANT_TO_EXPORT'
    html_file = client.export_file(file_id, 'text/html')
    html_file = html_file.decode('utf-8')

    # These 2 following lines is just additional to beautify and fix the html error
    html_file = BeautifulSoup(html_file, features="lxml")
    html_file = html_file.prettify()

    """
        Example 2: Listing 'user' files (files created by, opened by, or shared directly with the user)
    """
    corpora = 'user' # change this as your requirement. See here: https://developers.google.com/drive/api/v3/reference/files/list
    drive_id = 'THE_DESIRED_GOOGLE_DRIVE_ID'
    list_of_files = client.list_files(corpora, drive_id)

    """
        Example 3: Make a copy of a file
    """
    options = {
        'name': 'FILE_COPY',
        'parentFolderId': 'THE_DESIRED_PARENT_FOLDER'
    }
    file_id = 'THE_FILE_ID_YOU_WANT_TO_COPY'
    result = client.copy_file(file_id, options)
    print(result)