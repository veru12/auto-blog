import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 구글 블로그 API 권한 설정
SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_service():
    creds = None
    # 1. token.pickle 파일이 있으면 기존 인증 정보를 불러옵니다.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # 2. 유효한 인증 정보가 없거나 만료된 경우
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 주의: GitHub Actions 서버에서는 이 부분이 실행되면 브라우저를 띄울 수 없어 에러가 납니다.
            # 로컬(내 PC)에서 미리 token.pickle을 생성해서 깃허브 시크릿에 등록하거나 포함해야 합니다.
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # 인증된 토큰 정보를 파일로 저장
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('blogger', 'v3', credentials=creds)

def post_blog(title, content):
    service = get_service()
    # 본인의 블로그 ID (블로그 주소의 고유 ID) 입력 필요
    blog_id = 'YOUR_BLOG_ID' 
    
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
