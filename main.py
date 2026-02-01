from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
# with open('index.html' ,'r') as html_file:
#     content = html_file.read()
#     soup = BeautifulSoup(content, 'lxml')
#
#     # features = soup.find_all('h3')
#     # for feature in features:
#     #     print(feature.text)
#     reasons =  soup.find_all('a' , class_ = 'card')
#     for reason in reasons:
#         print(reason.p.text)

html_text = requests.get('https://www.youtube.com/').text
soup = BeautifulSoup(html_text , 'lxml')
print(html_text[:2000])

jobs = soup.find_all('ytd-rich-item-renderer')
print(jobs)


with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        locale="en-US"
    )

    page = context.new_page()
    page.goto("https://www.youtube.com/watch?v=aircAruvnKk", wait_until="domcontentloaded")

    page.wait_for_selector("ytd-app", timeout=60000)

    # Trigger feed load
    page.mouse.wheel(0, 4000)
    page.wait_for_timeout(3000)

    videos = page.locator("ytd-comment-thread-renderer").all()
    print("Videos found:", len(videos))

    browser.close()
