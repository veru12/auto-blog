# 구글 블로거 API 발행 함수 정의
def post_to_blogger(post_title, post_content):
    try:
        creds_json = os.environ.get("GOOGLE_TOKEN_JSON")
        blog_id = os.environ.get("BLOG_ID")
        
        import json
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        creds_info = json.loads(creds_json)
        creds = Credentials.from_authorized_user_info(creds_info)
        service = build('blogger', 'v3', credentials=creds)
        
        # 게시물 데이터 구성
        body = {
            'title': post_title,
            'content': post_content
        }
        
        # 블로그에 포스팅 전송
        posts = service.posts()
        request = posts.insert(blogId=blog_id, body=body)
        request.execute()
        print("🎉 구글 블로거 발행 성공!")
    except Exception as e:
        print(f"❌ 발행 중 에러 발생: {e}")
        raise e

# 함수 호출
post_to_blogger(keyword, post_content)
