import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from openai import OpenAI
import re
from datetime import datetime
import sys

def get_theme_by_day():
    day_index = datetime.now().weekday()
    themes = {
        0: "금리 인하/인상 시기 자산 관리 및 예적금 재테크",
        1: "주식 시장 트렌드 분석 및 유망 섹터 투자 전략",
        2: "부동산 시장 동향 및 내 집 마련 청약 가이드",
        3: "직장인을 위한 연말정산 및 절세 꿀팁",
        4: "신용카드 혜택 비교 및 앱테크 실전 가이드",
        5: "초보자를 위한 가상화폐 및 디지털 자산 기초",
        6: "은퇴 준비를 위한 노후 연금 및 펀드 설계"
    }
    return themes.get(day_index, "생활 속 유용한 금융 상식 및 재테크")

def generate_blog_post():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    current_year = datetime.now().strftime("%Y")
    
    default_theme = get_theme_by_day()
    
    theme = default_theme
    if sys.stdin.isatty():
        try:
            user_input = input(f"오늘의 금융 블로그 주제를 직접 입력하시겠습니까? (엔터 치면 기본 주제 '{default_theme}'로 자동 진행): ").strip()
            if user_input:
                theme = user_input
        except EOFError:
            pass
    
    image_url = "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=1200&q=80"
    
    prompt_content = f"너는 월 수백만 원을 버는 전문 금융/경제 블로거야. {current_year}년 최신 경제 트렌드를 반영해 아주 알기 쉽고 신뢰성 높은 블로그 글을 써줘.\n" \
                     f"- 주제: {theme}\n" \
                     "- 절대 ```html 이나 ``` 같은 마크다운 기호를 출력하지 마. 오직 순수 HTML 태그만 시작부터 끝까지 작성해.\n" \
                     "- 독자가 검색해서 들어올 만한 정보 위주로, 서론-본론(3개 단락)-결론 구조로 작성해.\n" \
                     f"- 가장 첫 줄에 제목 <h1>을 쓰고, 바로 아래에 <div style='margin:20px 0;'><img src='{image_url}' width='100%' style='border-radius:8px;' alt='{theme} 관련 금융 경제 이미지'></div>를 넣어줘.\n" \
                     "- 소제목은 <h2>, 내용은 <p>, 리스트는 <ul><li>를 사용해.\n" \
                     "- 본문 중간(2단락과 3단락 사이)에 광고가 들어갈 깔끔한 빈 박스(<div style='background:#fcfcfc; border:1px dashed #ccc; padding:20px; text-align:center; color:#888; margin:20px 0;'>[광고 영역]</div>)를 하나 넣어줘.\n" \
                     "- 핵심 요약 박스(<div style='background:#f9f9f9; border-left:4px solid #28a745; padding:15px; margin:20px 0;'>)를 반드시 포함해.\n" \
                     "- 글 중간에 '관련 포스팅'이라는 문구를 넣고, 이전 금융 글들을 추천하는 내부 링크용 문구를 자연스럽게 삽입해.\n" \
                     "- 글의 마지막에는 '실전 자산관리 체크리스트' 3가지를 넣고, 그 아래에 아주 작은 회색 글씨로 금융 정보 제공 목적의 면책 조항(<p style='font-size:12px; color:#aaa; margin-top:30px;'>※ 본 포스팅은 일반적인 금융 정보를 제공하기 위한 것이며, 투자 권유나 법적 책임을 지지 않습니다. 최종 투자 결정은 본인에게 있습니다.</p>)을 추가해줘."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "너는 HTML 전문 금융 블로거야. 절대 ```html 이나 markdown 백틱을 포함하지 마세요. 순수 HTML 코드만 반환하세요."},
                  {"role": "user", "content": prompt_content}]
    )
    
    html_content = response.choices[0].message.content.strip()
    
    # [핵심] 찌꺼기 마크다운 기호(```html, ``` 등)를 완벽하게 강제로 제거하는 코드
    html_content = re.sub(r'^```html\s*', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'^```\s*', '', html_content, flags=re.IGNORECASE)
    html_content = html_content.replace('```', '').strip()
    
    match = re.search(r'<h1>(.*?)</h1>', html_content)
    title = match.group(1) if match else f"{theme} - {current_year}년 필수 금융 정보"
    
    return title, html_content

def send_email():
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    blog_email = os.environ.get("BLOG_EMAIL")
    
    title, html_content = generate_blog_post()
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = blog_email
    msg['Subject'] = title
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    with smtplib.SMTP_SSL("smtp.naver.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, blog_email, msg.as_string())
    print("성공! 깔끔하게 마크다운이 제거된 금융 포스팅 완료.")

if __name__ == "__main__":
    send_email()
