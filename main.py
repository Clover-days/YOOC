# coding=utf-8
import json
import requests
import time
from PIL import Image
from io import BytesIO
import base64
import re
import csv
Account_password=open('password.txt', 'r').read().split('\n')
Headers ={
    'Host': 'www.yooc.me',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3835.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.yooc.me/login',
}
submit_data ={}
answer_data ={}
score=0
def csv_pretreatment(name):
    with open(name + '.csv', 'a+', newline='', encoding='utf-8-sig') as f:
        f.seek(0, 0)
        print(f)
        writer = csv.writer(f)
        reader = csv.reader(f)
        for rows in reader:
            print('open:' + name + '.csv')
            f.close()
            break
        else:
            print(0)
            writer.writerow(['ID', 'subjectId', 'title', 'answer'])
            f.close()

def login():
    c_url = "https://www.yooc.me/login"
    cookie = requests.utils.dict_from_cookiejar(requests.get(c_url, headers=Headers).cookies)
    while True:
        captcha_key=get_captcha(cookie)
        data = {
            'email': Account_password[0],
            'password': Account_password[1],
            'rid': captcha_key,
            'remember': 'true'
        }
        login_url = 'https://www.yooc.me/yiban_account/login_ajax'
        Headers['X-CSRFToken']=cookie['csrftoken']
        r = requests.post(login_url, headers=Headers, data=data, cookies=cookie)
        if '"success": true'in r.text:
            print('这里是输出你的cookie:',requests.utils.dict_from_cookiejar(r.cookies))#这里是输出你的cookie
            return requests.utils.dict_from_cookiejar(r.cookies)
        elif'"value": "验证码错误！"'in r.text:
            print("验证码错误！")
            print("正在重新尝试")
        else:
            print(r.text)
            raise Exception("未知错误")

def get_captcha(cookie):
    captcha_url = "https://www.yooc.me/group/get_captcha?_=%d" % int(time.time() * 100)
    captcha_json = requests.get(captcha_url, cookies=cookie, headers=Headers).json()
    captcha_img=Image.open(BytesIO(requests.get(captcha_json['img']).content))
    try:
        import ddddocr
        ocr = ddddocr.DdddOcr()
        captcha_str = ocr.classification(captcha_img).upper()
        print(captcha_str)
    except:
        captcha_img.show()
        captcha_str=input("请输入验证码:")
    return captcha_json['key']
def get_examid(cookie,group_choice,exam_list_choose):
    Headers['Host']= 'www.yooc.me'
    group_url ='https://www.yooc.me/group/joined'
    group = requests.get(group_url,headers=Headers,cookies=cookie).json()
    if  group_choice == -1:
        for i in range(group['total']):
            print(i, group['items'][i]['title'])
        group_choice = int(input("请选择课群:"))
    group_id =group['items'][group_choice]['url'].split('/')[2]
    set_cookie_url= 'https://exambackend.yooc.me/api/exam/user/check'
    set_cookie_data={
        'userId':cookie['user_id'],
        'groupId':group_id
    }
    Headers['Host']='exambackend.yooc.me'
    Headers['Set-Cookie'] = requests.get(set_cookie_url,headers=Headers,cookies=cookie,data=set_cookie_data).headers['Set-Cookie']
    exam_list='https://exambackend.yooc.me/api/exam/list/get?userId=%d&groupId=%d'%(int(cookie['user_id']),int(group_id))
    Headers['Origin']='https://exam.yooc.me'
    exam_data = requests.get(exam_list,headers=Headers).json()
    if  exam_list_choose == -1:
        n = 0
        status = ['未知情况', '未开考', '开始考试', '考试中', '重做']
        for i in exam_data['data']:
            print(n, i['name'], '反复练习%r' % bool(i['canRepeat']), 'examId:%d' % i['examId'],
                  'examuserId: %d' % i['examuserId'], 'status: %s' % status[i['status']])
            n = n + 1
        exam_list_choose = int(input("请选择考试:"))
    return_data=exam_data['data'][exam_list_choose]
    return return_data,group_choice,exam_list_choose

def Pretreatment(cookie,exam_id,examuserId,status):
    url = ['https://exambackend.yooc.me/api/exam/repeat/action', 'https://exambackend.yooc.me/api/exam/start/action']
    if status==4:#重做
        repeat_data={
            'examuserId': examuserId,
            'examId': exam_id
        }
        repeat = requests.post(url[0],headers=Headers,cookies=cookie,data=repeat_data)
        print(repeat.json())
        start_data={
            'userId': int(cookie['user_id']),
            'examId': exam_id
        }
        start=requests.post(url[1],headers=Headers,cookies=cookie,data=start_data)
        print(start.json())
    elif status==3:#考试中
        return
    elif status==2:#开始考试
        data={
            'userId': int(cookie['user_id']),
            'examId': exam_id
        }
        r= requests.post(url[1],headers=Headers,cookies=cookie,data=data)
        print(r.json())
    elif status==1:#未开考
        raise Exception("未开考")
    else: #未知考试模式
        raise Exception("未知考试模式:%r",status)

def get_exam(cookie,exam_id):
    exam_setting_get_url = 'https://exambackend.yooc.me/api/exam/setting/get?examId=%d&userId=%d'%(int(exam_id),int(cookie['user_id']))
    try:
        examuserid = requests.get(exam_setting_get_url,headers=Headers,cookies=cookie).json()['data']['examuserId']
    except:
        print(requests.get(exam_setting_get_url, headers=Headers, cookies=cookie).json())
        raise Exception("未知错误")
    submit_data['examuserId']=examuserid
    url = 'https://exambackend.yooc.me/api/exam/paper/get?examuserId=%d'%examuserid
    r = requests.get(url,headers=Headers,cookies=cookie)
    return r.json()['data']

def exam_answer(exam_data,name):
    global score
    with open(name + '.csv', 'a+', newline='', encoding='utf-8-sig') as f:
        f.seek(0, 0)
        print(f)
        writer = csv.writer(f)

        reader = csv.reader(f)
        for i in exam_data:
            for j in i['subjects']:
                score=int(j['points'])+score
                answer =[]
                n = 0
                answer_numb=re.compile(r'\d+').findall(str(base64.b64decode(j['answer'][::-1]),'utf-8'))
                for a in answer_numb:
                    answer.append(j['option'][int(a[0])][0])
                    n=n+1
                answer_data.update({str(j['subjectId']):[{'1':answer_numb},1]})
                witer(j['subjectId'], j['title'][0][:-2],answer,writer,reader)
                f.seek(0, 0)

def exam_submit(cookie):
    global score
    url = 'https://exambackend.yooc.me/api/exam/submit/action'
    submit_data['score'] = str(base64.b64encode(bytes(str(score)+'yooc@admin', encoding='utf-8')),'utf-8')[::-1]
    submit_data['answer'] = json.dumps(re.sub("'",'\"',str(answer_data)))
    r =requests.post(url,headers=Headers,cookies=cookie,data=submit_data)
    print(r.json())
    submit_data.clear()
    answer_data.clear()
    score=0

def witer(subjectId,title,answer,writer,reader):
    ID = ''
    for rows in reader:
        ID=rows[0]
        if rows[1] == str(subjectId):
            print('已存在',[rows[0].encode('utf-8').decode('utf-8-sig')]+rows[1:])
            break
    else:
        try:
            ID = int(ID.encode('utf-8').decode('utf-8-sig'))
        except:
            ID = 0
        ID=ID+1
        print('存入',[ID,subjectId,title]+answer)
        writer.writerow([ID,subjectId,title]+answer)

def main():
    cookie=login()
    return_data,group_choice,exam_list_choose= get_examid(cookie,-1,-1)
    csv_pretreatment(return_data['name'])
    if bool(return_data['canRepeat']):
        n = int(input("请输入循环次数："))
        for i in range(n):
            try:
                return_data, group_choice, exam_list_choose = get_examid(cookie,group_choice,exam_list_choose)
                Pretreatment(cookie,return_data['examId'],return_data['examuserId'],return_data['status'])
                exam_data = get_exam(cookie,return_data['examId'])
                exam_answer(exam_data,return_data['name'])
                time.sleep(3)
                print(i)
                exam_submit(cookie)
                time.sleep(30)
            except:
                print("error")
                time.sleep(300)
                cookie=login()
    else:
        Pretreatment(cookie, return_data['examId'],return_data['examuserId'],return_data['status'])
        exam_data = get_exam(cookie, return_data['examId'])
        exam_answer(exam_data,return_data['name'])
        s=input("是否交卷y/n:")
        while(True):
            if s=="y":
                exam_submit(cookie)
                break
            elif s=='n':
                break

if __name__=="__main__":
    main()
