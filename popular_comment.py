from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import math


# In[2]:
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
    browser = webdriver.Chrome()
    browser.get(url1)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    article = json.loads(soup.text)
    # print(article)
    content = article['content']
    content = content.encode('cp950', 'ignore')
    content = content.decode('cp950')
    comment_count = article['commentCount']  # 留言數量
    title = article['title']
    # print(title)
    forumAlias = article['forumAlias']
    gender = article['gender']
    # print(comment_count)
    # In[3]:

    heart = 0  # 愛心數
    for i in article['reactions']:
        if i['id'] == '286f599c-f86a-4932-82f0-f5a06f1eca03':
            heart += i['count']

    # In[4]:

    total_comment = []

    for i in range(0, math.ceil(comment_count / 100)):
        url2 = url1 + '/comments?limit=100&after=' + str(100 * i)
        browser.get(url2)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        rejs = json.loads(soup.text)
        for j in rejs:
            if j['hidden'] != True:
                total_comment.append(j['content'])

    popular_comment = []
    popular_heart = []
    url3 = url1 + '/comments?limit=3&popular=true'
    browser.get(url3)
    # print(url3)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    rejs = json.loads(soup.text)
    for j in rejs:
        popular_comment.append(j['content'])
        popular_heart.append(j['likeCount'])

    browser.quit()
    import pandas as pd
    import re
    test = pd.DataFrame(data=total_comment, columns={'text'})
    test.loc[0, 'content'] = content
    for i in range(0, len(test)):
        test['text'][i] = test['text'][i].encode('cp950', 'ignore')
        test['text'][i] = test['text'][i].decode('cp950')

    popular = pd.DataFrame(data=popular_comment, columns={'popular'})
    for i in range(len(popular_comment)):
        popular['popular'][i] = popular['popular'][i].encode('cp950', 'ignore')
        popular['popular'][i] = popular['popular'][i].decode('cp950')
    popular_like = pd.DataFrame(data=popular_heart, columns={'popular_like'})

    temp = ""
    for i in range(len(test)):
        # temp = "".join([x for x in test.loc[i]['text'] if not  x.isdigit()])
        # test.loc[i]['text'] = temp
        test.loc[i]['text'] = re.sub(r'[\n\r]', '', test.loc[i]['text'])

    # print(test.loc[3]['text'])
    test['sentiment'] = ''
    test['heartcount'] = ''
    test['commentCount'] = ''
    test['commentCount'][0] = comment_count - 2
    test['heartcount'][0] = heart
    test['titles'] = ''
    test['forumAlias'] = ''
    test['gender'] = ''
    title = title.encode('cp950', 'ignore')
    title = title.decode('cp950')
    test['titles'][0] = title
    test['forumAlias'][0] = forumAlias
    test['gender'][0] = gender

    popular['popular_like'] = popular_like['popular_like']
    popular.to_csv('popular.csv', encoding='cp950', index=False)

    for i in range(0, len(test)):
        if len(test.loc[i, 'text']) == 0:
            test = test.drop(index=i)
    test = test[['content', 'text', 'sentiment', 'heartcount', 'commentCount', 'titles', 'forumAlias', 'gender']]
    test.to_csv('okokok.csv', encoding='cp950', index=False)


#     test = test.drop(["commentCount", "heartcount"], axis=1)
#     print(test)
#     return test

# getdata(str(input("please input an URL:")))
