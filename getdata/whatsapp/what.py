from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

#driver=webdriver.Chrome()
driver.get('https://web.whatsapp.com')

name = input('Enter the name of the user or group :')
msg = input('Enter your message')
count=int(input('Enter the count'))

input('Enter anything after scanning QR Code')

user=driver.find_element_by_xpath('//span[@title="{}"]'.format(name))
user.click()

msg_box=driver.find_element_by_class_name('input.container')
for i in range(count):
    msg_box.send_keys(msg)
    button=driver.find_element_by_class_name('compose-btn-send')
    button.click()
