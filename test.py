import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
#import chromedriver_binary
import json
from selenium.webdriver.common.by import By
# -*- coding: utf-8 -*-


def Line_Message(message):
    try:
        # LINE_NOTIFY_ACCESS
        url = "https://notify-api.line.me/api/notify"
        access_token = '8cnVVmdN0Bj82ZOtIrHtkFp5zNVj7RsQK1FEUFYYK57'
        access_token_2 = '0j5WeGgcygNfyNVjMP9wfJnBXa6GZy9xWm4ZRHQGuXT'
        headers = {'Authorization': 'Bearer ' + access_token}
        headers2 = {'Authorization': 'Bearer ' + access_token_2}

        # Line送信
        payload = {'message': message}
        payload2 = {'message': message}
        r = requests.post(url, headers=headers, params=payload,)
        f = requests.post(url, headers=headers2, params=payload2,)

        return payload

    except:
        return "ライン送信失敗"


def Selenium():
    # 検証
    print("START")
    driver_path = '/app/.chromedriver/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    # driverに設定 ※optionsを指定しないとheadlessにならないので注意
    driver = webdriver.Chrome(options=options)

    # chrome_service = fs.Service(
    #     executable_path='/Users/shunsukegoto/Desktop/DEVELOP/Weather_notice/chromedriver')

    # 気温取得
    try:

        url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json'
        r = requests.get(url)
        res_json = json.loads(r.text)
        print(res_json)
        weather_info = res_json[0]["timeSeries"][0]["areas"][0]["weathers"][1]
        temparcher_low = res_json[1]["timeSeries"][1]["areas"][0]["tempsMin"][1]
        temparcher = res_json[1]["timeSeries"][1]["areas"][0]["tempsMax"][1]
        table = str.maketrans({
            '\u3000': '',
            ' ': '',
            '\t': ''
        })
    except:
        return "CAN NOT GET API RESPONCE"

    try:
        weather_info = weather_info.translate(table)
        driver = webdriver.Chrome()
        print("気温: {temparcher}".format(temparcher=temparcher))

        print("check1")
        driver.get('https://www.google.com/')
        time.sleep(10)
        search_box = driver.find_element(By.NAME, "q")
        search_box.click()
        time.sleep(10)
        search_box.send_keys(temparcher + "度の服装")
        search_box.submit()
        result = driver.find_element(By.CSS_SELECTOR, "div.tF2Cxc a")
        result_link = result[0]

        time.sleep(5)
        result_link.click()
        time.sleep(5)
        url = driver.current_url

        result_str = """
        \n明日の天気：{weather_info}\n最高気温：{temparcher}\n最低気温：{temparcher_low}\nお天気ファッション情報：\n{url}
        """.format(
            weather_info=weather_info,
            temparcher=temparcher,
            temparcher_low=temparcher_low,
            url=url
        )

        return result_str
    except Exception as e:
        print(e)
        print(temparcher + "度の服装")
        driver.quit()
        return "CAN NOT SEARCH ON GOOGLE"

    driver.quit()


def main():
    result_url = Selenium()
    Line_Message(result_url)


main()
