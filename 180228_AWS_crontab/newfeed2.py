import datetime
import requests, json, time
from selenium import webdriver
from xvfbwrapper import Xvfb #use xvfbwrapper

date = datetime.date.today()

def send_slack(msg):

    webhook_URL = "https://hooks.slack.com/services/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"

    data = {
    "channel": "#random",
    "emoji": ":grinning:",
    "msg": msg,
    "username": "newsfeed",
    }

    payload = {
    "channel": data["channel"],
    "username": data["username"],
    "icon_emoji": data["emoji"],
    "text": data["msg"],
    }

    response = requests.post(webhook_URL,
                            data = json.dumps(payload),
                            )
    print(response)

def get_article(page):
    with Xvfb() as xvfb:
        display = xvfb
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

#send message
send_slack(str("today's headlines!"))
send_slack(str(date))
get_article(1)
