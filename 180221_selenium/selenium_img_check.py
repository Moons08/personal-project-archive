from selenium import webdriver
import time
import pandas as pd
import pygsheets

#check
def check_element(driver, selector):
    try:
        driver.find_element_by_css_selector(selector)
        return True
    except:
        return False

#build DF
df = pd.DataFrame(columns=["label"])
df['label'] = ['Joy', 'Sorrow', 'Anger', 'Surprise', 'Exposed', 'Blurred', 'Headwear', 'confidence']

for i in range(0, 10): #사진 갯수

    #open browser
    driver = webdriver.Chrome()
    driver.get('https://cloud.google.com/vision/')
    iframe = driver.find_element_by_css_selector("#vision_demo_section iframe")

    #check element
    sec, limit_sec = 0, 10
    doing = True
    while doing:
        sec += 1
        time.sleep(1)
        selector = '#vision_demo_section iframe'
        # after loading
        if check_element(driver, selector):
            # choice iframe
            driver.switch_to_frame(iframe)
            # file upload
            file_path = "/home/mk/documents/dev/personal-project-archive/180221_selenium/screenshot_element{}.png".format(i)
            driver.find_element_by_css_selector("#input").send_keys(file_path)
            doing = False

        if sec + 1 > limit_sec:
            print('error')
            driver.close()
            break;

    #timer reset
    sec = 0
    doing = True
    while doing:
        sec += 1
        time.sleep(1)
        selector = '#card div.face.style-scope.vs-faces > div #text'
        if check_element(driver, selector):
            score = driver.find_elements_by_css_selector('#card div.face.style-scope.vs-faces > div #text')
            conf = driver.find_elements_by_css_selector('#card div.conf-score.style-scope.vs-faces')
            doing = False

        if sec + 1 > limit_sec:
            print('error')
            driver.close()
            break;

    # 컬럼 생성
    df['text{}'.format(i)] = 0

    # 새 컬럼에 데이터 추가
    for idx, val in enumerate(score):
        a = val.text
        if idx > 6:
            continue
        else:
            if a == 'Very Unlikely': a = 0
            elif a == 'Unlikely': a = 1
            elif a == 'Possible': a = 2
            elif a == 'Likely': a = 3
            elif a == 'Very Likely': a = 4

            df.iat[idx, i+1] = a

    #confidence 추가
    df.iat[7, i+1] = float(conf[0].text.strip('%'))
    print('{}'.format(i))
    # 한 사이클 돌 때마다 닫음 (새로고침 불가)
    driver.close()

print(df)

# google spread sheet에 저장
gc = pygsheets.authorize(outh_file='client_secret.json')
sh = gc.open('sele')
sheet1 = sh.sheet1

# index type change (int -> str)
df.index = df.index.map(str)
# save
sheet1.set_dataframe(df, 'A1', copy_index=True) # (df, cell_start)

# csv 파일로 export하기
sheet1.export(pygsheets.ExportType.CSV, filename="sheet1.csv")
