import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from openai import OpenAI
import re
from datetime import datetime
import urllib.request
import json
import urllib.parse
import sys

# 1. 네이버 오픈 API 등을 활용하거나 트렌드 키워드를 자동으로 가져오는 함수
def get_latest_economic_issue():
    # 기본 fallback 주제 (뉴스 크롤링 실패 시 대체용)
    default_theme = "20th Century Fox 경제 트렌드 및 자산 관리 전략"
    
    # 2026년 기준 실시간 금융/경제 주요 키워드 리스트 중 요일별/랜덤 조합 또는 최신 트렌드 반영
    # 여기서는 GPT에게 최신 경제 이슈를 반영한 매력적인 주제를 스스로 브리핑하도록 요청할 수 있습니다.
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 경제 트렌드 분석가야. 현재 시점(2026년)에 직장인과 투자자들이 가장 관심을 가질 만한 시급하고 트렌디한 경제/재테크 블로그 주제 딱 1가지만 골라서 제목 형태로 짧게 만들어줘. 다른 부가 설명 없이 주제 문구만 딱 말해줘."},
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
    
    # 실시간 이슈 주제 자동 선정
    theme = get_latest_economic_issue()
    
    # DALL-E 3 맞춤형 썸네일 이미지 생성
    print("DALL-E 3로 맞춤형 일러스트 썸네일 생성 중...")
    image_prompt = f"A professional, clean, modern financial concept vector illustration for '{theme}', high resolution, bright lighting."
    
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

    # SEO 최적화 및 페르소나 반영 본문 프롬프트 (2000자 이상)
    prompt_content = f"""너는 경제 전문 블로그를 운영하며 월 수백만 원의 수익을 올리는 파워 블로거야. 
{current_year}년 최신 경제 트렌드와 데이터를 바탕으로 독자의 체류 시간을 늘릴 수 있도록 아주 깊이 있고 풍부한 글을 작성해줘.

- 메인 주제 (실시간 이슈): {theme}
- 글자 수 조건: 본문 내용이 공백 포함 **2000자 이상**이 되도록 상세하고 길게 서술해줘.
- 페르소나/말투: 독자의 고민에 깊이 공감해주면서도 명확한 솔루션을 제시하는 친근하고 신뢰감 가는 어조(~해요, ~랍니다 체) 사용.
- 마크다운 제한: 절대 ```html 이나 ``` 같은 마크다운 백틱을 출력하지 마. 오직 순수 HTML 태그만 작성해.
- 구조:
  1. 가장 첫 줄에 검색 유입용 매력적인 제목 <h1> 작성.
  2. 바로 아래에 <div style='margin:20px 0;'><img src='{image_url}' width='100%' style='border-radius:8px;' alt='{theme} 관련 이미지'></div> 삽입.
  3. 서론: 독자의 현실적인 고민 환기 (<p> 태그)
  4. 본론 1, 2, 3: 소제목 <h2>를 활용해 핵심 내용을 3단계로 나누어 상세 설명.
  5. 중간 광고 박스: 본론 2와 3 사이에 <div style='background:#fcfcfc; border:1px dashed #ccc; padding:20px; text-align:center; color:#888; margin:20px 0;'>[수익형 광고 삽입 영역 존]</div> 추가.
  6. 핵심 요약 박스: <div style='background:#f9f9f9; border-left:4px solid #28a745; padding:15px; margin:20px 0;'> 형태의 요약 포함.
  7. 관련 포스팅 추천 문구 및 결론, '실전 자산관리 체크리스트' 3가지, 마지막 면책 조항(<p style='font-size:12px; color:#aaa; margin-top:30px;'>※ 본 포스팅은 일반적인 금융 정보를 제공하기 위한 것이며, 투자 권유나 법적 책임을 지지 않습니다.</p>) 추가."""

    print("GPT-4o 모델이 고품질 블로그 글을 작성 중입니다...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 HTML 전문 경제 블로거야. 절대 백틱을 쓰지 말고 순수 HTML만 반환해."},
            {"role": "user", "content": prompt_content}
        ],
        temperature=0.7,
    )
    
    html_content = response.choices[0].message.content.strip()
    html_content = re.sub(r'^```html\s*', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'^```\s*', '', html_content, flags=re.IGNORECASE)
    html_content = html_content.replace('```', '').strip()
    
    match = re.search(r'<h1>(.*?)</h1>', html_content)
    title = match.group(1) if match else f"{theme} - {current_year}년 필수 재테크 가이드"
    
    return title, html_content

# 2. 텔레그램 알림 발송 함수
def send_telegram_alert(title):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("텔레그램 토큰 또는 챗 ID가 설정되지 않아 알림을 건너뜁니다.")
        return

    message = f"📢 [블로그 포스팅 생성 완료!]\n\n제목: {title}\n\n네이버 메일함에서 확인하세요!"
    url = f"[https://api.telegram.org/bot](https://api.telegram.org/bot){bot_token}/sendMessage"
    
    data = urllib.parse.urlencode({'chat_id': chat_id, 'text': message}).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req) as response:
            print("텔레그램 알림 전송 성공!")
    except Exception as e:
        print(f"텔레그램 알림 전송 실패: {e}")

def send_email():
    sender_email = "Venthes123@naver.com"
    sender_password = os.environ.get("SENDER_PASSWORD")
    blog_email = "Venthes123@naver.com"
    
    if not sender_password:
        raise ValueError("GitHub Secrets에 SENDER_PASSWORD가 설정되지 않았습니다!")

    title, html_content = generate_blog_post()
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = blog_email
    msg['Subject'] = f"[자동발행] {title}"
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    with smtplib.SMTP_SSL("smtp.naver.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, blog_email, msg.as_string())
    print("성공! 메일 전송 완료.")
    
    # 메일 전송 성공 시 텔레그램 알림 호출
    send_telegram_alert(title)

if __name__ == "__main__":
    send_email()
