from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("ChromeDriver 설치 시도...")
service = Service(ChromeDriverManager().install())
print("ChromeDriver 설치 완료")

print("Chrome 브라우저 시작 시도...")
driver = webdriver.Chrome(service=service)
print("Chrome 브라우저 시작 완료")

print("Google 접속 시도...")
driver.get("https://www.google.com")
print("Google 접속 완료")

print("브라우저 종료...")
driver.quit()
print("브라우저 종료 완료")