from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time
import traceback

queries = ["홍천 1박2일 KBS", "홍천 1박 2일 방송"]

def wait_for_page_load(driver, timeout=30):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

def find_news_titles(driver, timeout=30):
    selectors = [
        (By.CSS_SELECTOR, "a.tit_main"),
        (By.CSS_SELECTOR, ".tit_main"),
        (By.XPATH, "//a[contains(@class, 'tit_main')]"),
        (By.CLASS_NAME, "news_tit"),  # 추가 뉴스 제목용 선택자
    ]
    
    for selector in selectors:
        try:
            elements = WebDriverWait(driver, timeout).until(
                EC.visibility_of_all_elements_located(selector)
            )
            if elements:
                return elements
        except TimeoutException:
            print(f"선택자 {selector}로 요소를 찾지 못했습니다.")
    
    print("페이지 소스:")
    print(driver.page_source)
    raise TimeoutException("뉴스 제목을 찾을 수 없습니다.")

try:
    print("ChromeDriver 설치 시도...")
    service = Service(ChromeDriverManager().install())
    print("ChromeDriver 설치 완료")

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    print("Chrome 브라우저 시작 시도...")
    driver = webdriver.Chrome(service=service, options=options)
    print("Chrome 브라우저 시작 완료")

    for query in queries:
        print(f"\n현재 검색 키워드: {query}")

        try:
            print("다음 홈페이지 접속 시도...")
            driver.get('https://www.daum.net/')
            wait_for_page_load(driver)
            print("다음 홈페이지 접속 완료")

            print("검색창 찾기 시도...")
            search_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            print("검색창 찾기 완료")
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            wait_for_page_load(driver)
            print("검색어 입력 및 검색 완료")

            print("뉴스 탭 찾기 시도...")
            news_tab = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "뉴스")]'))
            )
            print("뉴스 탭 찾기 완료")
            news_tab.click()
            wait_for_page_load(driver)
            print("뉴스 탭 클릭 완료")

            print("뉴스 제목 찾기 시도...")
            news_titles = find_news_titles(driver)
            print(f"{len(news_titles)} 개의 뉴스 제목 찾음")

            for i, title in enumerate(news_titles[:5], 1):
                print(f"{i}. {title.text}")

            print("\n")
            time.sleep(5)

            # step6. 뉴스 제목 텍스트 추출
            print("모든 뉴스 제목 추출 시도...")
            news_titles = driver.find_elements(By.CLASS_NAME, "news_tit")
            print(f"총 {len(news_titles)}개의 뉴스 제목 추출")
            for i, title in enumerate(news_titles, 1):
                print(f"{i}. {title.text}")

        except Exception as e:
            print(f"키워드 '{query}' 처리 중 오류 발생: {str(e)}")
            traceback.print_exc()

except Exception as e:
    print(f"전체 실행 중 오류 발생: {str(e)}")
    traceback.print_exc()

finally:
    if 'driver' in locals():
        print("브라우저 종료 시도...")
        driver.quit()
        print("브라우저 종료 완료")