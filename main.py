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

def get_latest_economic_issue():
    default_theme = "2026년 최신 경제 트렌드 및 자산 관리 전략"
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 경제 트렌드 분석가야. 현재 시점(2026년)에 맞는 가장 핫한 경제 이슈 주제 하나만 추천해줘."},
                {"role": "user", "content": "오늘자 핫한 경제 이슈 주제 추천해줘."}
            ],
            temperature=0.9
        )
        trending_theme = response.choices[0].message.content.strip().replace('"', '')
        print(f"추출된 실시간 경제 이슈 주제: {trending_theme}")
        return trending_theme
    except Exception as e:
        print(f"트렌드 주제 추출 중 오류 발생, 기본 주제 사용: {e}")
        return default_theme

def generate_blog_post():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    current_year = datetime.now().strftime("%Y")
    
    theme = get_latest_economic_issue()
    
    print("DALL-E 3로 맞춤형 일러스트 썸네일 생성 중...")
    image_prompt = f"A professional, clean, modern financial concept vector illustration representing {theme}, high quality"
    
    try:
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = image_response.data[0].url
    except Exception as e:
        print(f"이미지 생성 실패, 대체 이미지 사용: {e}")
        image_url = "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=1200&q=80"

    prompt_content = f"""너는 경제 전문 블로그를 운영하며 월 수백만 원의 수익을 올리는 파워 블로거야. {current_year}년 최신 경제 트렌드와 데이터를 바탕으로 독자의 체류 시간을 늘릴 수 있도록 아주 길고 상세하게 글을 작성해.
    - 메인 주제 (실시간 이슈): {theme}
    - 글자 수 조건: 본문 내용이 공백 포함 **2000자 이상**이 되도록 상세하고 길게 서술해줘.
    - 페르소나/말투: 독자의 고민에 깊이 공감해주면서도 명확한 솔루션을 제시하는 친근하고 신뢰감 가는 말투를 사용해.
    - 마크다운 제한: 절대 ```html 이나 ``` 같은 마크다운 백틱을 출력하지 마. 오직 순수 HTML 태그만 출력해.
    - 구조:
      1. 가장 첫 줄에 검색 유입용 매력적인 제목 <h1> 작성.
      2. 바로 아래에 <div style='margin:20px 0;'><img src='{image_url}' width='100%' style='border-radius:8px;' alt='금융 이미지'></div> 작성.
      3. 서론: 독자의 현실적인 고민 환기 (<p> 태그)
      4. 본론 1, 2, 3: 소제목 <h2>를 활용해 핵심 내용을 3단계로 나누어 상세 설명.
      5. 중간 광고 박스: 본론 2와 3 사이에 <div style='background:#fcfcfc; border:1px dashed #ccc; padding:20px; text-align:center; margin:20px 0;'>광고 영역</div> 반드시 삽입.
      6. 핵심 요약 박스: <div style='background:#f9f9f9; border-left:4px solid #28a745; padding:15px; margin:20px 0;'> 요약 </div> 반드시 포함.
      7. 관련 포스팅 추천 문구 및 결론, '실전 자산관리 체크리스트' 3가지, 마지막 면책 조항(<p style='font-size:12px; color:#777;'>본 포스팅은 투자 권유가 아니며...)으로 마무리."""

    print("GPT-4o 모델이 고품질 블로그 글을 작성 중입니다...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 HTML 전문 경제 블로거야. 절대 백틱을 쓰지 말고 순수 HTML만 작성해."},
            {"role": "user", "content": prompt_content}
        ],
        temperature=0.7,
    )

    html_content = response.choices[0].message.content.strip()
    html_content = re.sub(r'^```html\s*', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'^```\s*', '', html_content)
    html_content = html_content.replace('```', '').strip()

    match = re.search(r'<h1>(.*?)</h1>', html_content)
    title = match.group(1) if match else f"{theme} - {current_year}년 필수 재테크 가이드"

    return title, html_content

def post_to_blogger(title, content):
    blog_id = os.environ.get("BLOG_ID")
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    refresh_token = os.environ.get("REFRESH_TOKEN")

    if not all([blog_id, client_id, client_secret, refresh_token]):
        print("구글 블로그 API 인증 정보가 부족합니다. 블로그 발행을 건너뜁니다.")
        return

    token_url = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    token_res = requests.post(token_url, data=payload)
    access_token = token_res.json().get("access_token")

    if not access_token:
        print("구글 액세스 토큰 발급 실패:", token_res.text)
        return

    post_url = f"[https://www.googleapis.com/blogger/v3/blogs/](https://www.googleapis.com/blogger/v3/blogs/){blog_id}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "title": title,
        "content": content
    }

    res = requests.post(post_url, headers=headers, json=body)
    if res.status_code == 200:
        print("구글 블로그 포스팅 성공!")
    else:
        print("구글 블로그 포스팅 실패:", res.text)
        raise Exception(f"Blogger API Error: {res.text}")

def send_telegram_alert(title):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        return

    message = f"💰 [경제 블로그 포스팅 완료]\n\n제목: {title}"
    url = f"[https://api.telegram.org/bot](https://api.telegram.org/bot){bot_token}/sendMessage"
    data = urllib.parse.urlencode({'chat_id': chat_id, 'text': message}).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req) as response:
            pass
    except Exception as e:
        print(f"텔레그램 알림 전송 실패: {e}")

# AI 셀프 디버깅 및 코드 자가 수정 함수
def self_correct_code(error_message):
    print("AI가 에러를 감지하여 스스로 코드를 분석 및 수정합니다...")
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    with open(__file__, "r", encoding="utf-8") as f:
        current_code = f.read()

    prompt = f"""파이썬 블로그 자동화 스크립트 실행 중 다음과 같은 에러가 발생했다.
[에러 메시지]
{error_message}

[현재 main.py 코드]
{current_code}

위 에러를 해결할 수 있도록 수정된 전체 파이썬 코드를 작성해줘.
주의사항:
1. 마크다운 백틱(```python 등)을 절대 포함하지 말고, 오직 순수 파이썬 코드 텍스트만 출력해라.
2. 기능이 누락되지 않도록 기존 코드를 기반으로 에러만 정확히 수정해라."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    fixed_code = response.choices[0].message.content.strip()
    fixed_code = re.sub(r'^```python\s*', '', fixed_code, flags=re.IGNORECASE)
    fixed_code = re.sub(r'^```\s*', '', fixed_code)
    fixed_code = fixed_code.replace('```', '').strip()

    # GitHub API를 통해 리포지토리의 main.py 자동 업데이트
    github_token = os.environ.get("GH_PAT") # 깃허브 개인 액세스 토큰 필요
    repo_name = os.environ.get("GITHUB_REPOSITORY") # 깃허브 자동 제공 변수 (예: 계정명/저장소명)
    
    if not github_token or not repo_name:
        print("GitHub 토큰(GH_PAT)이 없어 코드를 자동 커밋하지 못했습니다.")
        return

    api_url = f"[https://api.github.com/repos/](https://api.github.com/repos/){repo_name}/contents/main.py"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    
    # 기존 파일의 SHA 값 가져오기
    res = requests.get(api_url, headers=headers)
    if res.status_code == 200:
        file_sha = res.json().get("sha")
    else:
        return

    encoded_content = base64.b64encode(fixed_code.encode("utf-8")).decode("utf-8")
    
    update_data = {
        "message": "AI Self-Correction: Fix runtime error automatically",
        "content": encoded_content,
        "sha": file_sha
    }
    
    update_res = requests.put(api_url, headers=headers, json=update_data)
    if update_res.status_code in [200, 201]:
        print("AI가 성공적으로 코드를 자가 수정하여 깃허브에 커밋했습니다!")
    else:
        print("코드 자가 커밋 실패:", update_res.text)

def run_pipeline():
    try:
        sender_email = "Venthes123@naver.com"
        sender_password = os.environ.get("SENDER_PASSWORD")
        blog_email = "Venthes123@naver.com"
        
        if not sender_password:
            raise ValueError("GitHub Secrets에 SENDER_PASSWORD가 설정되지 않았습니다!")

        title, html_content = generate_blog_post()
        
        # 1. 구글 블로그 발행
        post_to_blogger(title, html_content)
        
        # 2. 이메일 발송
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = blog_email
        msg['Subject'] = f"[자동발행] {title}"
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        with smtplib.SMTP_SSL("smtp.naver.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, blog_email, msg.as_string())
        print("성공: 이메일 전송 완료.")
        
        # 3. 텔레그램 알림 호출
        send_telegram_alert(title)
        
    except Exception as e:
        error_msg = str(e)
        print(f"실행 중 치명적 오류 발생: {error_msg}")
        # 오류 발생 시 AI 셀프 디버깅 작동
        self_correct_code(error_msg)

if __name__ == "__main__":
    run_pipeline()
