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
        0: "2026년 기준 금리 인하 수혜가 예상되는 고배당주 및 자산 관리 전략",
        1: "주식 시장 하락장 방어 및 인공지능(AI) 유망 섹터 집중 투자 분석",
        2: "부동산 시장의 새로운 대출 규제와 내 집 마련 실전 청약 전략",
        3: "직장인 필수 연말정산 환급금 극대화 및 합법적 절세 노하우",
        4: "고물가 시대 생활비 절약을 위한 신용카드 혜택 조합 및 앱테크 실전",
        5: "초보자를 위한 가상화폐 시장 트렌드 분석 및 디지털 자산 리스크 관리",
        6: "은퇴 후 안정적인 현금 흐름을 만드는 노후 연금 및 펀드 설계법"
    }
    return themes.get(day_index, "2026년 최신 경제 트렌드 및 실전 재테크 가이드")

def generate_blog_post():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    current_year = datetime.now().strftime("%Y")
    
    default_theme = get_theme_by_day()
    theme = default_theme
    
    if sys.stdin.isatty():
        try:
            user_input = input(f"오늘의 경제 블로그 주제를 직접 입력하시겠습니까? (엔터 치면 기본 주제 '{default_theme}' 자동 진행): ").strip()
            if user_input:
                theme = user_input
        except EOFError:
            pass
    
    # 3. DALL-E 3를 이용해 본문 내용과 연관된 맞춤형 썸네일 이미지 자동 생성
    print("DALL-E 3로 맞춤형 고품질 이미지를 생성 중입니다...")
    image_prompt = f"A professional, clean, modern financial and economic concept vector illustration representing '{theme}', high resolution, bright lighting, suitable for a financial blog banner."
    
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
        print(f"이미지 생성 중 오류 발생, 기본 이미지로 대체합니다: {e}")
        image_url = "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=1200&q=80"

    # 2 & 5. 페르소나 강화 및 SEO 최적화 (2000자 이상, 키워드 밀도, 전문적이면서 친근한 톤)
    prompt_content = f"""너는 경제 전문 블로그를 운영하며 월 수백만 원의 수익을 올리는 파워 블로거야. 
20{current_year}년 최신 경제 데이터를 바탕으로 독자의 체류 시간을 늘릴 수 있도록 아주 깊이 있고 풍부한 글을 작성해줘.

- 메인 주제: {theme}
- 글자 수 조건: 본문 내용이 공백 포함 **2000자 이상**이 되도록 상세하고 길게 서술해줘. 대충 쓰지 말고 전문적이고 유용한 정보를 아낌없이 담아줘.
- 페르소나/말투: 독자의 고민에 깊이 공감해주면서도, 데이터를 바탕으로 명확한 솔루션을 제시하는 친근하고 신뢰감 가는 어조(~해요, ~랍니다 체)를 사용해.
- SEO 최적화: 검색 포털 상단 노출을 위해 본문 전반에 걸쳐 관련 핵심 키워드를 자연스럽게 여러 번 반복해줘.
- 마크다운 제한: 절대 ```html 이나 ``` 같은 마크다운 백틱을 출력하지 마. 오직 순수 HTML 태그만 시작부터 끝까지 작성해.
- 구조:
  1. 가장 첫 줄에 검색 유입용 매력적인 제목 <h1>을 작성해.
  2. 바로 아래에 <div style='margin:20px 0;'><img src='{image_url}' width='100%' style='border-radius:8px;' alt='{theme} 관련 경제 이미지'></div>를 넣어줘.
  3. 서론: 독자의 현실적인 고민 환기 및 흥미 유발 (P <p> 태그 사용)
  4. 본론 1, 2, 3: 소제목 <h2>를 활용해 핵심 내용을 깊이 있게 3가지 단계로 나누어 상세히 설명 (<p>, <ul><li> 태그 활용)
  5. 중간 광고 박스: 본론 2와 3 사이에 <div style='background:#fcfcfc; border:1px dashed #ccc; padding:20px; text-align:center; color:#888; margin:20px 0;'>[수익형 광고 삽입 영역]</div> 추가
  6. 핵심 요약 박스: <div style='background:#f9f9f9; border-left:4px solid #28a745; padding:15px; margin:20px 0;'> 형태의 요약 정리 포함
  7. 관련 포스팅 추천 문구: 이전 관련 재테크 포스팅을 읽어보도록 유도하는 내부 링크 유도 문구 삽입
  8. 결론 및 실전 체크리스트: '실전 자산관리 체크리스트' 3가지를 정리하고, 마지막에 아주 작은 회색 글씨로 금융 면책 조항(<p style='font-size:12px; color:#aaa; margin-top:30px;'>※ 본 포스팅은 일반적인 금융 정보를 제공하기 위한 것이며, 투자 권유나 법적 책임을 지지 않습니다. 최종 투자 결정은 본인에게 있습니다.</p>)을 추가해줘."""

    print("OpenAI GPT 모델이 고품질 블로그 글을 작성 중입니다...")
    response = client.chat.completions.create(
        model="gpt-4o",  # 더 똑똑한 모델로 고품질 글 생성
        messages=[
            {"role": "system", "content": "너는 HTML 전문 경제 블로거야. 절대 백틱을 쓰지 말고 순수 HTML만 반환해."},
            {"role": "user", "content": prompt_content}
        ],
        temperature=0.7,
    )
    
    html_content = response.choices[0].message.content.strip()
    
    # 혹시 모를 마크다운 찌꺼기 제거
    html_content = re.sub(r'^```html\s*', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'^```\s*', '', html_content, flags=re.IGNORECASE)
    html_content = html_content.replace('```', '').strip()
    
    match = re.search(r'<h1>(.*?)</h1>', html_content)
    title = match.group(1) if match else f"{theme} - {current_year}년 필수 재테크 가이드"
    
    return title, html_content

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
    msg['Subject'] = f"[블로그 발행완료] {title}"
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    with smtplib.SMTP_SSL("smtp.naver.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, blog_email, msg.as_string())
    print("성공! DALL-E 3 이미지와 2000자 분량의 최적화된 블로그 포스팅이 메일로 전송되었습니다.")

if __name__ == "__main__":
    send_email()
