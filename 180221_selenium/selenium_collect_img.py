import time
from selenium import webdriver
from PIL import Image as pil

# get to target
driver = webdriver.Chrome()
driver.get('https://www.youtube.com/watch?v=eAccyJ4bKuA')

# resizing
element = driver.find_element_by_css_selector('#movie_player')
location, size = element.location, element.size
left, top = location['x'], location['y']
right, bottom = left + size['width'], top + size['height']
area = (left, top, right, bottom)
time.sleep(5)
for i in range(10):
    time.sleep(1) # 1초마다 스샷
    driver.save_screenshot('screenshot.png') # save
    pil_im = pil.open('screenshot.png') # load
    pil_im = pil_im.crop(area) # resizing
    pil_im.save('screenshot_element{}.png'.format(i)) # 번호순 저장

driver.execute_script('alert("done")')
