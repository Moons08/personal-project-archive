import datetime
import requests, json, time
from pyvirtualdisplay import Display
from selenium import webdriver

date = datetime.date.today()
def send_slack(msg):

    # 슬랙 웹훅 URL
    webhook_URL = "https://hooks.slack.com/services/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"

    # 데이터
    data = {
    "channel": "#random",
    "emoji": ":grinning:",
    "msg": msg,
    "username": "newsfeed",
    }

    # 페이로드 생성
    payload = {
    "channel": data["channel"],
    "username": data["username"],
    "icon_emoji": data["emoji"],
    "text": data["msg"],
    }

    # 전송

    response = requests.post(webhook_URL,
                            data = json.dumps(payload),
                            )

    # 결과

    print(response)

def get_article(page):
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Chrome()
    driver.get("http://news.naver.com/main/main.nhn?mode=LSD&mid =shm&sid1=105#&date="+str(date)+" 00:00:00&page=" + str(page))
    articles = driver.find_elements_by_css_selector('#section_body li')

    for article in articles:
        title = article.find_element_by_css_selector('dt:not(.photo) > a').text
        link = article.find_element_by_css_selector('dt:not(.photo) > a').get_attribute('href')

        data = "<{}|{}>".format(link, title)
        send_slack(data)

    driver.quit()
    display.stop()

#send message
send_slack(str("today's headlines!"))
send_slack(str(date))
get_article(1)

#https://api.slack.com/incoming-webhooks#adding_links
