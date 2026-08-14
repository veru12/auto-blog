import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# 블로그 ID와 인증 정보 경로 설정
BLOG_ID = '742203761012618877' # 블로그 주소 뒤에 나오는 번호
CLIENT_SECRET_FILE = 'client_secret.json'

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, ['https://www.googleapis.com/auth/blogger'])
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('blogger', 'v3', credentials=creds)

def post_blog(title, content):
    service = get_service()
    post = {'kind': 'blogger#post', 'title': title, 'content': content}
    service.posts().insert(blogId=BLOG_ID, body=post).execute()
    print("포스팅 완료!")

if __name__ == '__main__':
    post_blog("자동 포스팅 테스트", "이 글은 자동으로 작성된 글입니다.")
