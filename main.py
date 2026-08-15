import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            # GitHub 서버 환경 에러 방지를 위해 콘솔 기반 인증으로 변경
            creds = flow.run_console()
            
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('blogger', 'v3', credentials=creds)

def post_blog(title, content):
    service = get_service()
    blog_id = '742283761812618877' # 본인의 블로그 ID 숫자
    
    body = {
        'title': title,
        'content': content
    }
    
    posts = service.posts()
    request = posts.insert(blogId=blog_id, body=body)
    response = request.execute()
    print(f"포스팅 성공: {response['url']}")

if __name__ == '__main__':
    post_blog("자동 포스팅 테스트", "이 글은 자동으로 작성된 글입니다.")
