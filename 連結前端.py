from flask import Flask, render_template, request
import catchsinglewebsitesdata
import read_result
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
abc = "輸出內容!!"
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.values['send'] == '送出':
            print("in")
            print(request.values['user'])
            name = request.values['user']  # name為輸入的網址
            print(name)
            import newdcard_crawler
            newdcard_crawler.getdata(name)  # 傳入網址，會儲存一個csv檔
            import testers
            testers.getresult()  # 會存一個last.csv檔
            import popular_comment
            popular_comment.getdata(name)
            name2 = read_result.rr(2)  # catchsinglewebsitesdata.getdata(name) #name2為丟網址給catchsinglewebsitesdata #總留言
            name3 = read_result.rr(3)  # positive
            name4 = read_result.rr(4)  # negative
            name5 = read_result.rr(5)  # titles
            name6 = read_result.rr(6)  # 正面評論數
            name7 = read_result.rr(7)  # 負面評論數
            name8 = read_result.rr(8)  # 熱門回應
            return render_template('customer.html', **locals())
    return render_template('customer.html', name="")


if __name__ == '__main__':
    app.run()
