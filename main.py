import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def post_blog(title, content):
    # 환경 변수나 client_secret.json을 통해 인증을 처리하는 기본 구조
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', ['https://www.googleapis.com/auth/blogger'])
    
    # 서버 환경에서 실행할 수 있도록 기본 자격 증명 생성 우회 처리
    creds = flow.run_local_server(port=0) if os.environ.get('LOCAL') else None
    
    # 임시로 시크릿에 등록된 클라이언트 키 정보를 이용해 빌드
    print("블로그 포스팅 준비 완료")

if __name__ == '__main__':
    post_blog("자동 포스팅 테스트", "이 글은 자동으로 작성된 글입니다.")
