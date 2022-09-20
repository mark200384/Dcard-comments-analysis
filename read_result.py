import csv
import pandas as pd
from builtins import str


def rr(choice):
    f_read = open(r'last.csv')
    source_data = pd.read_csv(f_read)
    if choice == 2:  # 內文
        Text = source_data.loc[0]['content']
        return Text
    elif choice == 3:  # 正面回應
        Positive3 = []
        Positive2 = []
        Positive1 = []
        Positive_str = ""
        for i in range(len(source_data)):
            if source_data.loc[i]['sentiment'] == 3:
                Positive3.append(source_data.loc[i]['text'])
            elif source_data.loc[i]['sentiment'] == 2:
                Positive2.append(source_data.loc[i]['text'])
            elif source_data.loc[i]['sentiment'] == 1:
                Positive1.append(source_data.loc[i]['text'])
        temp = "\n".join(Positive3)
        Positive_str = temp
        temp = "\n".join(Positive2)
        Positive_str += temp
        temp = "\n".join(Positive1)
        Positive_str += temp

        return Positive_str
    elif choice == 4:  # 負面回應
        Negative3 = []
        Negative2 = []
        Negative1 = []
        Negative_str = ""
        for i in range(len(source_data)):
            if source_data.loc[i]['sentiment'] == -3:
                Negative3.append(source_data.loc[i]['text'])
            elif source_data.loc[i]['sentiment'] == -2:
                Negative2.append(source_data.loc[i]['text'])
            elif source_data.loc[i]['sentiment'] == -1:
                Negative1.append(source_data.loc[i]['text'])
        temp = "\n".join(Negative3)
        Negative_str = temp
        temp = "\n".join(Negative2)
        Negative_str += temp
        temp = "\n".join(Negative1)
        Negative_str += temp
        return Negative_str
    elif choice == 5:
        title = source_data.loc[0]['titles']
        heartcount = source_data.loc[0]['heartcount']
        comment = source_data.loc[0]['commentCount']
        from builtins import str
        heartcount = str(heartcount)
        comment = str(comment)
        # print("type(heartcount)", type(heartcount))
        # print(heartcount)
        # print("type(comment)", type(comment))
        # print(comment)
        str = "title:" + title + ",愛心數:" + str(heartcount)[0:-2] + ",留言數:" + str(comment)[0:-2]

        return str
    elif choice == 6:
        Positive = []
        for i in range(len(source_data)):
            if source_data.loc[i]['sentiment'] > 0:
                Positive.append(source_data.loc[i]['text'])
        plen = len(Positive)
        # print("plen", plen)
        return plen
    elif choice == 7:
        Negative = []
        for i in range(len(source_data)):
            if source_data.loc[i]['sentiment'] < 0:
                Negative.append(source_data.loc[i]['text'])
        nlen = len(Negative)
        # print("nlen", nlen)
        return nlen
    elif choice == 8:
        popular = []
        f_p = open(r"popular.csv")
        popular_data = pd.read_csv(f_p)
        from builtins import str
        for i in range(len(popular_data)):
            text = str(i+1) + ". " + popular_data.loc[i]['popular']
            popular.append(text)
        temp = "\n".join(popular)
        Popular_str = temp
        # print("Popular", Popular_str)
        return Popular_str
