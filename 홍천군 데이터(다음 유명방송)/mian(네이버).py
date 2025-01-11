from selenium import webdriver
from selenium.webdriver.common.by import By  # By 모듈 추가
from bs4 import BeautifulSoup
import pandas as pd
import time

# Chrome options 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # GUI 없이 실행
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 드라이버 실행
driver = webdriver.Chrome(options=options)  # options를 명시적으로 전달

# 검색어 설정
keyword = '홍천 여행'  # 검색할 키워드 입력
url_list = []

# 1~2 페이지의 블로그 URL 수집
for i in range(1, 35):  # 페이지 번호 범위 설정
    url = f'https://section.blog.naver.com/Search/Post.nhn?pageNo={i}&rangeType=ALL&orderBy=sim&keyword={keyword}'
    driver.get(url)
    time.sleep(2)  # 페이지 로드를 위한 대기 시간

    # 각 블로그 게시글의 링크를 가져옴
    for j in range(1, 8):  # 한 페이지에 있는 블로그 개수 (조정 가능)
        try:
            # XPath를 사용하여 링크 추출 (By.XPATH로 수정)
            titles = driver.find_element(By.XPATH, f'/html/body/ui-view/div/main/div/div/section/div[2]/div[{j}]/div/div[1]/div[1]/a[1]')
            title_url = titles.get_attribute('href')
            url_list.append(title_url)
            print(f"블로그 URL 추출: {title_url}")
        except Exception as e:
            print(f"URL 추출 실패 (페이지 {i}, 블로그 {j}): {e}")

print(f"총 {len(url_list)}개의 블로그 URL을 추출했습니다.")

# 블로그 URL을 수집한 후, 각 블로그의 제목과 내용 크롤링
blog_data = []

for i, url in enumerate(url_list):
    print(f"크롤링 중: {url}")
    driver.get(url)
    time.sleep(2)
    
    try:
        # iframe 안으로 이동
        driver.switch_to.frame('mainFrame')
        print("iframe 전환 성공")

        # 페이지 소스를 다시 가져옴
        blog_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 제목 크롤링
        title_element = blog_soup.find(class_='se-module se-module-text se-title-text')
        if title_element:
            title = title_element.get_text().strip()
        else:
            print(f"제목 크롤링 실패: {url}")
            title = "제목 없음"
        
        # 내용 크롤링
        content_elements = blog_soup.select('.se-component.se-text.se-l-default')
        if content_elements:
            content = ' '.join([p.get_text().strip() for p in content_elements])
        else:
            print(f"내용 크롤링 실패: {url}")
            content = "내용 없음"

        blog_data.append({'title': title, 'content': content})

        # 진행 상황 출력
        print(f"[{i+1}/{len(url_list)}] 블로그 크롤링 완료: {title}")

    except Exception as e:
        print(f"크롤링 실패: {url}, 에러: {e}")

# DataFrame으로 변환 후 CSV로 저장
if blog_data:
    df = pd.DataFrame(blog_data)
    df.to_csv('naver_blog_data2.csv', index=False)
    print("CSV 파일 저장 완료")
else:
    print("크롤링된 데이터가 없습니다.")