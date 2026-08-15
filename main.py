import os
import pickle
from googleapiclient.discovery import build

def get_service():
    # 깃허브 서버에 저장되어 있는 인증 토큰 파일을 불러옵니다.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        return build('blogger', 'v3', credentials=creds)
    else:
        raise Exception("token.pickle 파일이 없습니다! 로컬에서 인증 후 업로드해야 합니다.")

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
