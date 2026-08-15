import os
import openai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# OpenAI API 설정
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 금융 전문 고수익 키워드 및 페르소나 설정
keyword = "2026년 무직자 소액대출 조건 및 금리 비교 가이드"
prompt = "금융 전문 기자처럼 객관적이고 정확하며 신뢰감 있는 어조로 블로그 포스팅을 작성해줘."

print(f"선택된 금융 분야 키워드: {keyword}")

# OpenAI API를 이용해 글 생성 요청
response = openai.chat.completions.create(
    model="gpt-4o-mini",  # 가성비와 성능이 좋은 모델
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"주제: '{keyword}'에 대해 구글 블로그에 올릴 고품질 포스팅을 작성해줘. HTML 태그(h2, h3, p 등)를 활용해서 가독성 좋게 만들어줘."}
    ]
)

post_content = response.choices[0].message.content
print("금융 AI 글 생성 완료!")

# (참고) 기존에 쓰시던 구글 블로그 API 발행 코드로 이어서 발행을 진행하시면 됩니다.
# post_to_blogger(keyword, post_content)
