import sqlite3
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import sys
aqstr = ["账户","密码"]
def clear():
    for i in range(100):
        print('\n')
def self_inspection():
    conn = sqlite3.connect('Question_bank.db')
    Question_bank = conn.cursor()
    try:
        Question_bank.execute('''CREATE TABLE Question_bank
        (
         Question   TEXT    NOT NULL,
          a1    TEXT     NOT NULL,
          a2    TEXT        ,
          a3    TEXT        ,
          a4    TEXT        );''')
        conn.commit()
        conn.close()
    except:
        conn.commit()
        conn.close()
def login(driver,aqstr):
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div[1]/form/div[2]/input").send_keys(aqstr[0])
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div[1]/form/div[3]/input").send_keys(aqstr[1])
    while True:
        clear()
        Verification_Code = input("请输入验证码:")
        driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div[1]/form/div[4]/input[1]").send_keys(Verification_Code)
        driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div[1]/form/div[6]/button").click()
        time.sleep(0.5)
        try:
            s = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div[1]/form/div[1]").text
        except:
            break
        if s == "验证码错误！":
            print("验证码错误")
            driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div[1]/form/div[4]/img").click()
            driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div[1]/form/div[4]/input[1]").clear()
        elif s == "账号或密码错误！":
            print("账号或密码错误！,20后自动关闭")
            time.sleep(20)
            sys.exit()
    time.sleep(3)
    Choice(driver)
    time.sleep(2)
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    driver.find_element_by_xpath("/html/body/section/section/div[1]/div[4]/a").click()
    return driver
def Choice(driver):
    ul = driver.find_element_by_xpath("/html/body/div[2]/div[2]/table/tbody/tr/td/div[1]/div[3]")
    test = ul.find_elements_by_xpath("div")
    for i in range(len(test)):
        print (i+1,test[i].text)
    n = int(input("请选择课群:")) -1
    test[n].find_element_by_xpath("a[1]/img").click()
def Choice_Exams(driver):
    time.sleep(2)
    Choice,flage = 0,0
    while True:
        time.sleep(2)
        try:
            driver.find_element_by_xpath("/html/body/div[12]/div[3]/div/div/button").click()
            time.sleep(1)
            driver.refresh()
        except:
            break
    ul = driver.find_element_by_xpath("/html/body/section/section/div[2]/div[3]/ul")
    test = ul.find_elements_by_xpath("li")
    for i in range(len(test)):
        lista = test[i].text.split('\n')
        print(i + 1, lista[0], lista[13], lista[14])
    while True:
        while True:
            try:
                Choice = int(input('请选择需要的考试')) - 1
                break
            except:
                print('请输入数字')
        if Choice > len(test):
            print('请输入小于等于%d的数字' % (len(test)))
        else:
            Exams = test[Choice]
            break
    listb = test[Choice].text.split('\n')
    if listb[14] == '允许':
        try:
            Exams.find_element_by_id("start-exam").click()
        except:
            Exams.find_element_by_class_name("repeat").click()
        time.sleep(1)
        driver.find_element_by_id("dlgc-2").click()
        time.sleep(2)
        driver.find_element_by_xpath("//html/body/div/div[1]/div[2]/main/article/div[3]/button").click()
        time.sleep(1)
    else:
        print('不可重复的不建议使用')
        flage = 1
    return (Choice,flage)
def start_exams(driver):
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/article/div[3]/div/div/div[2]/button[2]").click()
    print('开始答题了')
    conn = sqlite3.connect('Question_bank.db')
    print('数据库链接')
    time.sleep(2)
    numb = driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/ul/li[2]/span").text.split(' ')
    Qnumb = int(numb[2])
    print(Qnumb)
    for i in range(Qnumb - 1):
        query(driver, conn)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/ul/li[4]/button").click()
    query(driver, conn)
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div[3]/div/button").click()
    driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div[3]/div/div/div/div[2]/button[2]").click()
    print("end")
    conn.close()
    return (Qnumb)
def study(driver, numb):
    print("开始获取题目")
    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/article/div[2]/button").click()
    conn = sqlite3.connect('Question_bank.db')
    print('数据库链接')
    time.sleep(2)
    for i in range(numb-1):
        Add(driver,conn)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/ul/li[3]/button").click()
    Add(driver, conn)
    driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div[1]/span").click()
    conn.close()
def Add(driver,conn):
    c = conn.cursor()
    Question = driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/div/div/div/h3/div").text
    q_sql = "select * from Question_bank where Question=?"
    values = c.execute(q_sql,[Question])
    flage = 1
    for j in values:
        print("ed")
        if j[0]!= '':
            flage = 0
    if flage == 1:
        sql = "INSERT INTO Question_bank(Question,a1,a2,a3,a4) VALUES(?,?,?,?,?)"
        a_t = driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/div/div/div/div[2]/div").text.split('：')
        b_t = list(a_t[1])
        ans = []
        a1,a2,a3,a4 = None,None,None,None
        for i in b_t:
            if i == 'A':
                temp = driver.find_element_by_xpath(
                    "/html/body/div/div[1]/div[2]/main/div/div/div/div[1]/ul/li[1]/div[2]").text.split('.')
                ans.append(temp[1])
                print(temp[1],i)
            if i == 'B':
                temp = driver.find_element_by_xpath(
                    "/html/body/div/div[1]/div[2]/main/div/div/div/div[1]/ul/li[2]/div[2]").text.split('.')
                ans.append(temp[1])
                print(temp[1],i)
            if i == 'C':
                temp = driver.find_element_by_xpath(
                    "/html/body/div/div[1]/div[2]/main/div/div/div/div[1]/ul/li[3]/div[2]").text.split('.')
                ans.append(temp[1])
                print(temp[1],i)
            if i == 'D':
                temp = driver.find_element_by_xpath(
                    "/html/body/div/div[1]/div[2]/main/div/div/div/div[1]/ul/li[4]/div[2]").text.split('.')
                ans.append(temp[1])
                print(temp[1],i)
        numb = 1
        for i in ans:
            if numb == 1:
                a1 = i
            if numb == 2:
                a2 = i
            if numb == 3:
                a3 = i
            if numb == 4:
                a4 = i
            numb += 1
        data = (Question, a1,a2,a3, a4)
        print([Question], [a1], [a2], [a3], [a4])
        sql = "INSERT INTO Question_bank(Question,a1,a2,a3,a4) VALUES(?,?,?,?,?)"
        c.execute(sql, data)
        print("save_ed")
        conn.commit()
def query(driver, conn):
    c = conn.cursor()
    flage = 1
    Question = driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/div/div/div/h3/div").text
    q_sql = "select * from Question_bank where Question=?"
    values = c.execute(q_sql, [Question])
    print(Question)
    for row in values:
        flage = 0
        question_answer(driver,row[1])
        question_answer(driver,row[2])
        question_answer(driver,row[3])
        question_answer(driver,row[4])
    else:
        print(" ")
    if (flage == 1):
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/div/div/div/div/ul/li[1]").click()
        print("返回为空自动选A")
def question_answer(driver, answer):
    time.sleep(0.1)
    temp = driver.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/main/div/div/div/div[1]/ul/li[1]/div[2]").text.split('.')
    if temp[1] == answer:
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/div/div/div/div/ul/li[1]/div[2]").click()
        print(answer)
        time.sleep(0.1)
    temp = driver.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/main/div/div/div/div[1]/ul/li[2]/div[2]").text.split('.')
    if temp[1] == answer:
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/div/div/div/div/ul/li[2]/div[2]").click()
        print(answer)
        time.sleep(0.1)
    try:
        temp = driver.find_element_by_xpath(
            "/html/body/div/div[1]/div[2]/main/div/div/div/div[1]/ul/li[3]/div[2]").text.split('.')
        if temp[1] == answer:
            driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/div/div/div/div/ul/li[3]/div[2]").click()
            print(answer)
            time.sleep(0.1)
    except:
        return
    try:
        temp = driver.find_element_by_xpath(
            "/html/body/div/div[1]/div[2]/main/div/div/div/div[1]/ul/li[4]/div[2]").text.split('.')
        if temp[1] == answer:
            driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/div/div/div/div/ul/li[4]/div[2]").click()
            print(answer)
            time.sleep(0.1)
    except:
        return
def Retrieve_list(driver,n):
    print("重定向中")
    time.sleep(2)
    article = driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/article")
    test = article.find_elements_by_xpath("div")
    test[n].find_element_by_xpath("div[5]/button[2]").click()
    test[n].find_element_by_xpath("div[5]/div/div/div[2]/button[2]").click()
def e_start_exams(driver):
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/article/div[3]/div/div/div[2]/button[2]").click()
    print('开始答题了')
    conn = sqlite3.connect('Question_bank.db')
    print('数据库链接')
    time.sleep(1)
    numb = driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/ul/li[2]/span").text.split(' ')
    Qnumb = int(numb[2])
    print(Qnumb)
    for i in range(Qnumb - 1):
        e_query(driver, conn)
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/ul/li[4]/button").click()
    e_query(driver, conn)
    time.sleep(1)
    print("end,能回答的都回答了,50000s后关闭")
    conn.close()
def e_query(driver, conn):
    c = conn.cursor()
    flage = 1
    Question = driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/div/div/div/h3/div").text
    q_sql = "select * from Question_bank where Question=?"
    values = c.execute(q_sql, [Question])
    print(Question)
    for row in values:
        flage = 0
        question_answer(driver,row[1])
        question_answer(driver,row[2])
        question_answer(driver,row[3])
        question_answer(driver,row[4])
    else:
        print("获取完毕")
    if (flage == 1):
        print("返回为空，不选")
def main():
    a=0
    try:
        driver = webdriver.Edge("msedgedriver.exe")
    except:
        print("请下载最新的msedgedriver到此文件所在目录")
        time.sleep(500)
    driver.get("https://www.yooc.me/login")
    self_inspection()
    time.sleep(3)
    #aqstr = open('anser.txt', 'r',encoding='utf-8').read().split('\n')
    driver = login(driver,aqstr)
    Choice,flage = Choice_Exams(driver)
    if flage == 1:
        mode = input("是否启用考试模式y/n")
        if mode =="y":
            e_start_exams(driver)
            time.sleep(50000)
        else:
            print("5s后退出")
            time.sleep(5)
    else:
        a = int(input("请输入循环次数"))
        numb = start_exams(driver)
        study(driver, numb)
        for i in range(a-1):
            time.sleep(1)
            Retrieve_list(driver,Choice)
            time.sleep(2)
            driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/main/article/div[3]/button").click()
            numb = start_exams(driver)
            study(driver, numb)
    driver.quit()
if __name__ == "__main__":
    main()