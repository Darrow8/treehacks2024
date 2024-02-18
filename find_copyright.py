from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
from googleapiclient.errors import HttpError
CLIENT_SECRETS_FILE = "/Users/darrowhartman/Desktop/repos/treehacks2024/client_secrets.json" #os.path.join(os.getcwd(),)
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
REDIRECT_URI = 'http://localhost:8000'
TOKEN_NAME = 'token.json'
def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_NAME):
        creds = Credentials.from_authorized_user_file(TOKEN_NAME, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            flow.redirect_uri = REDIRECT_URI
            creds = flow.run_console()
        # Save the credentials for the next run
        with open(TOKEN_NAME, 'w') as token:
            token.write(creds.to_json())
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

def upload_video(file_path, title, description, category_id, keywords):
    youtube = get_authenticated_service()
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': keywords,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': 'unlisted'
        }
    }
   
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    
    response = None
    try:
        print('Uploading file...')
        status, response = insert_request.next_chunk()
        if 'id' in response:
            print('Video id "%s" was successfully uploaded.' % response['id'])
        else:
            exit('The upload failed with an unexpected response: %s' % response)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    return response


if __name__ == '__main__':
    file_path = 'VideoA.mp4' 
    title = 'Video A'
    description = 'Testing'
    category_id = '22'  # https://developers.google.com/youtube/v3/docs/videoCategories/list
    keywords = ['barbie', 'oppenheimer']

    upload_status = upload_video(file_path, title, description, category_id, keywords)
    print(upload_status)
