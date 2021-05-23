import requests
import time
from selenium import webdriver


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
    try:
        #検証
        print("START")
        driver_path = '/app/.chromedriver/bin/chromedriver'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--lang=ja-JP')
        #driverに設定 ※optionsを指定しないとheadlessにならないので注意
        # driver = webdriver.Chrome(options=options, executable_path=driver_path)

        # 開発用
        driver = webdriver.Chrome(
            '/Users/shunsukegoto/Desktop/DEVELOP/Weather_notice/chromedriver',
            
        )

        #お天気サイト
        driver.get('https://tenki.jp/')
        if not 'https://tenki.jp/' in driver.current_url:
            raise Exception
    except:
        driver.quit()
        return "SELENIUM ERROR CAN NOT ACCESS TO https://tenki.jp/"

    #対象地域検索
    try:
        print("SUCCESS ACCESS TO https://tenki.jp/")
        search_box = driver.find_element_by_id("keyword")
        time.sleep(5)
        search_box.click()
        time.sleep(5)
        search_box.send_keys('京田辺市')
        search_box.submit()
    except:
        driver.quit()
        return "CAN NOT SEARCH ON https://tenki.jp/"

    #検索結果の候補から選択
    try:
        kyotanabeshi = driver.find_element_by_xpath(
            '/html/body/div[2]/section/section[1]/div[2]/p[1]/a'
        )
        time.sleep(5)
        kyotanabeshi.click()
    except:
        driver.quit()
        return "CAN NOT CLICK SEARCH RESULT"

    #気温取得
    try:
        time.sleep(30)
        #最高気温取得
        temparcher = driver.find_element_by_xpath(
            '/html/body/div[3]/section/div[3]/section[2]/div[1]/div[2]/dl/dd[1]/span[1]'
        ).text
        #明日の天気情報
        weather_info = driver.find_element_by_xpath("/html/body/div[3]/section/div[3]/section[2]/div[1]/div[1]/p").text
        #最低気温
        temparcher_low = driver.find_element_by_xpath("/html/body/div[3]/section/div[3]/section[2]/div[1]/div[2]/dl/dd[3]/span[1]").text
        #午前中の降水確率
        rainy_parcent_morning = driver.find_element_by_xpath("/html/body/div[3]/section/div[3]/section[2]/div[2]/table/tbody/tr[2]/td[2]").text
        #午後の降水確率
        rainy_parcent_after = driver.find_element_by_xpath("/html/body/div[3]/section/div[3]/section[2]/div[2]/table/tbody/tr[2]/td[3]").text
    except:
        driver.quit()
        return "CAN NOT GET TEMPARCHER"

    #google検索画面へ
    try:
        print("気温: {temparcher}".format(temparcher=temparcher))
        driver.get('https://www.google.com/')
        search_box = driver.find_element_by_name("q")
        search_box.click()
        time.sleep(10)
        search_box.send_keys(temparcher + "度の服装")
        search_box.submit()
        result = driver.find_elements_by_css_selector("div.tF2Cxc a")
        result_link = result[0]
        
        time.sleep(10)
        result_link.click()
        time.sleep(10)
        url = driver.current_url

        result_str = """
        \n明日の天気：{weather_info}\n最高気温：{temparcher}\n最低気温：{temparcher_low}\n午前中の降水確率：{rainy_parcent_morning}\n午後の降水確率：{rainy_parcent_after}\nお天気ファッション情報：\n{url}
        """.format(
            weather_info=weather_info,
            temparcher=temparcher,
            temparcher_low=temparcher_low,
            rainy_parcent_morning=rainy_parcent_morning,
            rainy_parcent_after=rainy_parcent_after,
            url=url
            )

        return result_str
    except:
        print(temparcher + "度の服装")
        driver.quit()
        return "CAN NOT SEARCH ON GOOGLE"

    driver.quit()


def main():
    result_url = Selenium()
    Line_Message(result_url)

main()


# schedule.every().day.at("21:22").do(main())

# # タスク監視ループ
# while True:
#     # 当該時間にタスクがあれば実行
#     schedule.run_pending()
#     # 1秒スリープ
#     time.sleep(100)
