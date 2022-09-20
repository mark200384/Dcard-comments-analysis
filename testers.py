


# In[7]:


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import jieba as pseg
import pandas as pd
import re


def jieba_tokenizer(text):
    text = re.sub(r'[^\u4e00-\u9fa5]', '',text)
    words = pseg.cut(text, cut_all=False)
    words = " ".join(words)
    return words

def getresult():

    train = pd.read_csv('okokok.csv', encoding='cp950')
    org = pd.read_csv('okokok.csv', encoding='cp950')
    train['content_tokenized'] = train.loc[:, 'text'].apply(jieba_tokenizer)
    for i in range(0,len(train)):
        if(len(train.loc[i, 'content_tokenized']) == 0):
            train = train.drop(index=i)
            org = org.drop(index=i)

   # org.to_csv('okokok.csv',encoding='cp950',index=False) #actual data
    train = train.reset_index()
    org = org.reset_index()
    #print(len(train))

    import keras
    MAX_NUM_WORDS = 10000
    tokenizer = keras.preprocessing.text.Tokenizer(num_words=MAX_NUM_WORDS)
    corpus = train.content_tokenized
    tokenizer.fit_on_texts(corpus)
    xtrain = tokenizer.texts_to_sequences(corpus)

    max_seq_len = max([len(seq) for seq in xtrain])
    MAX_SEQUENCE_LENGTH = 50
    xtrain = keras.preprocessing.sequence.pad_sequences(xtrain,maxlen=MAX_SEQUENCE_LENGTH)


    import tensorflow as tf

    new_model = tf.keras.models.load_model('saved_model/my_model')

    # Check its architecture
    result = new_model.predict([xtrain])
    RNNresult = []
    for i in range(0,len(result)):
        if(result[i][0]>result[i][1]):
            RNNresult.append('負面')
        else:
            RNNresult.append('正面')

    # print(RNNresult)

    stream = pd.read_excel('singleword.xls')
    word = list(stream['字'])#詞彙表

    counter = []
    label = []
    for i in range(0, len(org)):
        counter.append([0] * 2721)

    testers = []

    for i in range(0, len(org)):
        testers.append(org.loc[i]['text'])
    for i in range(0, len(testers)):
        for j in range(0, len(testers[i])):
            if testers[i][j] in word:
                a = word.index(testers[i][j])
                if a < 2721:
                    counter[i][a] = 1

    import joblib
    RF = joblib.load('RF.joblib')
    SVM = joblib.load('svmclf.joblib')

    RF_pre = RF.predict(counter)
    RFresult = []
    for i in range(len(RF_pre)):
        if RF_pre[i] == 0:
            RFresult.append('負面')
        else:
            RFresult.append('正面')
    # print(RFresult)

    SVM_pre = SVM.predict(counter)
    SVMresult=[]

    for i in range(len(SVM_pre)):
        if SVM_pre[i] == 0:
            SVMresult.append('負面')
        else:
            SVMresult.append('正面')
    # print(SVMresult)

    lastresult = []
    for i in range(0,len(SVMresult)):
        pcounter=0
        ncounter=0

        if(SVMresult[i]=='正面'):
            pcounter+=1
        else:
            ncounter+=1

        if (RFresult[i] == '正面'):
            pcounter += 1
        else:
            ncounter += 1

        if (RNNresult[i] == '正面'):
            pcounter += 1
        else:
            ncounter += 1
        lastresult.append(pcounter-ncounter)
#         if (pcounter>ncounter):
#             lastresult.append('正面')
#         else:
#             lastresult.append('負面')
#     print(lastresult)
    org['sentiment']=lastresult
    org.to_csv('last.csv',encoding='cp950',index=False)
getresult()
