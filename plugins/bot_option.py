from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from requests_oauthlib import OAuth1Session
import wikipedia, re, urllib, json, datetime, requests, tweepy, os
import urllib.request

CONSUMER_KEY = 'dSpYD00eJOMlV9ctzJkvLoQRn'
CONSUMER_SECRET = 'HVuVdnynvobUTYyshxTsdGDyy0CuqXQqJGLB0V0ZEi0tOCurqS'
ACCESS_TOKEN = '724714346341797888-MkCrVM9RyyvHp2ZtRy6dVjndzjoEpRh'
ACCESS_SECRET = 'JrXPvgMQKs7EbJEiQMo6e9dcwIN9n24mwAqjEcsZ8ZFat'

def getConsumerKey():
    return CONSUMER_KEY

def getConsumerSecret():
    return CONSUMER_SECRET

def getAccessToken():
    return ACCESS_TOKEN

def getAccessSecret():
    return ACCESS_SECRET

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？
# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない
@respond_to('メンション')
def mention_func(message):
    message.reply('私にメンションと言ってどうするのだ') 

@listen_to('こんばんわ')
def listen_func(message):
    message.reply('こんばんわ！')

@respond_to('こんにちは')
def hello(message):
    message.reply('こんにちは！')

@respond_to('おはよう')
def goodmoning(message):
    message.reply('おはようございます!')

@respond_to(r'天気|天候')
def weather(message):

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
    text = '`' + title + '`\n' + '今日の天気 : ' + telop + telop_icon + "\n"

    if '曇り' in telop:
        messages = 'どよんとしますね。'
    elif '晴れ' in telop:
        messages = 'いい天気になりそうですね'
    elif '雨' in telop:
        messages = '傘は持っていきましょうか。'
    else:
        messages = 'こんな感じですね。'

    message.send(text + messages) 

@respond_to(r'電車|遅延')
def train(message):
    import urllib3
    import json

    url = 'https://tetsudo.rti-giken.jp/free/delay.json'
    html = urllib.request.urlopen(url)
    jsonfile = json.loads(html.read().decode('utf-8'))

    for json in jsonfile:    
        name = json['name'] 
        company = json['company']
        text = company + name
    
    message.send('以下の電線が遅れています。\n```' + text + '```') 

@respond_to('wiki (.*)')
def wikipediaSearch(message, something):
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

    return message.send(response_string)


@respond_to('twitter (.*)')
def twitter(message, something):
    #apiを取得
    auth = tweepy.OAuthHandler(getConsumerKey(), getConsumerSecret())
    auth.set_access_token(getAccessToken(), getAccessSecret())
    api = tweepy.API(auth)

    #検索キーワードを設定する。
    #searchWord = "大阪桐蔭" #検索ワード１つ
    something = something.split(',')

    searchWord = [something] #検索ワード複数

    # twitter内を検索する
    for status in api.search(q=searchWord, lang='ja', result_type='recent', count=5): #qに検索したいワードを指定する。
        u_id = "ユーザーID:" + status.user.name #userIDを表示
        u_name = "ユーザー名:" + status.user.screen_name #ユーザー名を表示
        get_time = "投稿日時:" + str(status.created_at + datetime.timedelta(hours=9)) #投稿日時を表示
        text = status.text #ツイートを表示
        p = u_id + '\n' + u_name + '\n' + get_time + '\n' + text
        message.send('```' + p + '```')
    
