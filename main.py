import os
import openai
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# 1. OpenAI API 설정
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 2. 블로그에 사용할 키워드 및 프롬프트 설정
keyword = "2026년 무작자 소액대출 조건 및 금리 비교 가이드"
prompt = f"금융 전문 기자처럼 객관적이고 정확하며 신뢰감 있는 어조로 블로그 포스팅을 작성해줘."

# 3. OpenAI API를 이용해 글 생성 요청
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"주제: '{keyword}'에 대해 구글 블로그에 올릴 고품질 포스팅을 작성해줘. HTML 태그(h2, h3, p 등)를 활용해서 가독성 좋게 만들어줘."}
    ]
)

post_content = response.choices[0].message.content
print("금융 AI 글 생성 완료!")

# 4. 구글 블로거 API 발행 함수 정의
def post_to_blogger(post_title, post_content):
    try:
        creds_json = os.environ.get("GOOGLE_TOKEN_JSON")
        blog_id = os.environ.get("BLOG_ID")
        
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

# 5. 함수 호출 (keyword 변수가 정의되어 있으므로 에러가 나지 않습니다)
post_to_blogger(keyword, post_content)
