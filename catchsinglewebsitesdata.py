# 載入使用的套件
import requests
import math
import pandas as pd
import re

def findid(url):
    i = len(url) - 1
    counter = 0
    while (url[i] != '/'):
        counter += 1
        i -= 1
    pos = len(url) - counter
    id = 'https://www.dcard.tw/service/api/v2/posts/'
    for i in range(pos, len(url)):
        id += url[i]
    return id


def getdata(url):
    url1 = findid(url)  # api get

    resp = requests.get(url1)
    print(url1)
    print(resp)
    article = resp.json()
    comment_count = article['commentCount']  # 留言數量

    heart = 0  # 愛心數
    for i in article['reactions']:
        if i['id'] == '286f599c-f86a-4932-82f0-f5a06f1eca03':
            heart += i['count']


    total_comment = []

    for i in range(0, math.ceil(comment_count / 100)):
        url2 = url1 + '/comments?limit=100&after=' + str(100 * i)
        resp = requests.get(url2)
        rejs = resp.json()
        for j in rejs:
            if j['hidden'] != True and 'https' not in j['content']:
                total_comment.append(j['content'])
    #print(total_comment)

    test = pd.DataFrame(data=total_comment, columns={'text'})
    for i in range(0, len(test)):
        test['text'][i] = test['text'][i].encode('cp950', 'ignore')
        test['text'][i] = test['text'][i].decode('cp950')

    temp = ""
    for i in range(len(test)):
        # temp = "".join([x for x in test.loc[i]['text'] if not  x.isdigit()])
        # test.loc[i]['text'] = temp
        test.loc[i]['text'] = re.sub(r'[\n\r]', '', test.loc[i]['text'])

    #print(test.loc[3]['text'])
    test['commentCount'] = ''
    test['commentCount'][0] = comment_count - 2
    test['heartcount'] = ''
    test['heartcount'][0] = heart
    test.to_csv('dcard.csv', encoding='cp950')
    test = test.drop(["commentCount", "heartcount"], axis=1)
    print(test)
    return test #表格
################################################# 輸入網址
# network=str(input('please enter a URL:'))
# getdata(network)