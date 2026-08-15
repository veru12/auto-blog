import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_service():
    # GitHub Secrets 환경 변수에서 인증 정보를 불러옵니다.
    creds = None
    token_json = os.environ.get('GOOGLE_TOKEN_JSON')
    
    if token_json:
        # 텍스트로 저장된 토큰 정보를 불러옴
        from io import StringIO
        import json
        creds = Credentials.from_authorized_user_info(json.loads(token_json), SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("Google 인증 토큰(GOOGLE_TOKEN_JSON)이 GitHub Secrets에 설정되지 않았습니다!")

    return build('blogger', 'v3', credentials=creds)

def post_blog(title, content):
    service = get_service()
    blog_id = '742283761812618877' # 본인 블로그 ID
    
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
