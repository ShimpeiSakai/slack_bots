import wikipedia
import urllib
import json

def weather():

    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city='
    # '130010'とすると東京の情報を取得してくれる
    # ここを変えれば任意の地域の天気情報を取得できる
    city_id = '130010'
    html = urllib.request.urlopen(url + city_id)
    jsonfile = json.loads(html.read().decode('utf-8'))
    title = jsonfile['title'] 
    telop = jsonfile['forecasts'][0]['telop']
    #telopが晴れだったら晴れのスラックのアイコンとか場合分け
    telop_icon = ''
    if telop.find('雪') > -1:    
        telop_icon = ':showman:'
    elif telop.find('雷') > -1:
        telop_icon = ':thinder_cloud_and_rain:'
    elif telop.find('晴') > -1:
        if telop.find('曇') > -1:
            telop_icon = ':partly_sunny:'
        elif telop.find('雨') > -1:
            telop_icon = ':partly_sunny_rain:'
        else:
            telop_icon = ':sunny:'
    elif telop.find('雨') > -1:
        telop_icon = ':umbrella:'
    elif telop.find('曇') > -1:
        telop_icon = ':cloud:'
    else:
        telop_icon = ':fire:'
    text = '`' + title + '`\n' + '今日の天気 : ' + '`' + telop + '`' + telop_icon + "\n"

    if telop in '曇':
        messages = 'どよんとしますね。'
    elif '晴れ' in telop:
        messages = 'いい天気になりそうですね'
    elif '雨' in telop:
        messages = '傘は持っていきましょうか。'
    else:
        messages = 'こんな感じですね。'

    print(text + messages)

something = "ポケモン"

def wikipediaSearch():
    search_text = something
    response_string = ""
    wikipedia.set_lang("ja")
    search_response = wikipedia.search(search_text)

    if not search_response:
        response_string = "その単語は登録されていません。"
        return response_string
    try:
        wiki_page = wikipedia.page(search_response[0])
    except Exception as e:
        response_string = "エラーが発生しました。\n{}\n{}".format(e.message, str(e))
        return response_string

    wiki_content = wiki_page.content

    response_string += wiki_content[0:wiki_content.find("。")] + "。\n"

    response_string += "リンクはこちら：" + wiki_page.url

    return print(response_string)

def twitter():
    import urllib.request
    from requests_oauthlib import OAuth1Session
    import datetime
    import requests, tweepy, os, key

    #apiを取得
    auth = tweepy.OAuthHandler(key.getConsumerKey(), key.getConsumerSecret())
    auth.set_access_token(key.getAccessToken(), key.getAccessSecret())
    api = tweepy.API(auth)

    #検索キーワードを設定する。
    #searchWord = "大阪桐蔭" #検索ワード１つ
    searchWord = ["金足農業","応援"] #検索ワード複数

    # twitter内を検索する
    for status in api.search(q=searchWord, lang='ja', result_type='recent', count=5): #qに検索したいワードを指定する。
        print("ユーザーID:" + status.user.name) #userIDを表示
        print("ユーザー名:" + status.user.screen_name) #ユーザー名を表示
        #time = status.created_at + datetime.timedelta(hours=9)
        print("投稿日時:" + str(status.created_at + datetime.timedelta(hours=9))) #投稿日時を表示
        print(status.text) #ツイートを表示
        print()

twitter()
