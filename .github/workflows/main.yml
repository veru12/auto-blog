import random
import os
import openai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# OpenAI API 설정
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 1. 고수익 분야별 키워드 및 페르소나(역할) 리스트 설정
high_revenue_topics = [
    {
        "category": "금융/대출",
        "keyword": "2026년 무직자 소액대출 조건 및 금리 비교 가이드",
        "prompt": "금융 전문 기자처럼 객관적이고 정확하며 신뢰감 있는 어조로 블로그 포스팅을 작성해줘."
    },
    {
        "category": "법률/세무",
        "keyword": "개인회생 신청 자격 및 변제금 줄이는 실무 팁",
        "prompt": "친절하고 전문적인 법률 상담가처럼 독자가 이해하기 쉽게 설명하는 블로그 글을 작성해줘."
    },
    {
        "category": "세무/환급",
        "keyword": "종합소득세 신고 기간 및 절세 방법 총정리",
        "prompt": "세무사이자 꼼꼼한 정보 전달자처럼 핵심만 짚어서 알기 쉽게 블로그 포스팅을 작성해줘."
    },
    {
        "category": "IT/테크/구독",
        "keyword": "속도 빠른 우수 VPN 추천 및 가격 비교 5가지",
        "prompt": "IT 테크 블로거처럼 실속 있고 객관적인 리뷰 형태의 블로그 글을 작성해줘."
    }
]

# 2. 실행할 때마다 고수익 분야 중 하나를 랜덤으로 선택
selected_topic = random.choice(high_revenue_topics)

print(f"선택된 고수익 분야: [{selected_topic['category']}] - {selected_topic['keyword']}")

# 3. OpenAI API를 이용해 글 생성 요청
response = openai.chat.completions.create(
    model="gpt-4o-mini",  # 가성비와 성능이 좋은 모델
    messages=[
        {"role": "system", "content": selected_topic["prompt"]},
        {"role": "user", "content": f"주제: '{selected_topic['keyword']}'에 대해 구글 블로그에 올릴 고품질 포스팅을 작성해줘. HTML 태그(h2, h3, p 등)를 활용해서 가독성 좋게 만들어줘."}
    ]
)

post_content = response.choices[0].message.content
print("AI 글 생성 완료!")

# (참고) 기존에 쓰시던 구글 블로그 API 발행 코드로 이어서 발행을 진행하시면 됩니다.
# post_to_blogger(selected_topic['keyword'], post_content)
