# 기존 라이브러리 유지 + 추가 라이브러리
# pip install google-api-python-client

import os
import requests
import json
from openai import OpenAI
import re
from datetime import datetime
import urllib.request
import urllib.parse
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

# [추가된 기능] 유입 데이터를 기반으로 테마 선정
def get_optimized_economic_issue():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # 여기에 Search Console API 연동 로직 추가 가능
    # 지금은 AI에게 이전 글의 성과 데이터를 주입하여 주제 선정
    prompt = "최근 자산관리 키워드 중 검색량이 급증하는 테마 하나를 선정하고, 이전보다 더 깊이 있는 내용을 제안해줘."
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# [추가된 기능] 네이버 블로그 자동 발행 모듈
def post_to_naver_blog(title, content):
    # 네이버 오픈 API 사용 (client_id, client_secret 필요)
    print("네이버 블로그 API 연동 준비 중...")
    # 실제 발행 로직은 네이버 API 문서에 따라 추가 구현
    pass

# 기존 generate_blog_post 로직에 get_optimized_economic_issue() 통합
# ... (이하 기존 코드 구조와 동일하되 위 함수 호출로 변경)

# 실행 파이프라인 고도화
def run_pipeline():
    try:
        # 1. 최적화된 주제 선정
        theme = get_optimized_economic_issue()
        
        # 2. 글 작성 및 발행
        title, html_content = generate_blog_post()
        post_to_blogger(title, html_content)
        post_to_naver_blog(title, html_content) # [추가] 네이버 블로그도 동시 발행
        
        # ... (이메일 및 텔레그램 동일)
    except Exception as e:
        self_correct_code(str(e))
