import base64
import time
from urllib import parse
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

class person:
    def __init__(self,accountid,password,address='广东省广州市天河区迎福路靠近广东金融学院(广州校区)',token="",notifyType=1):
        self.accountid = accountid
        self.password = password
        self.address=address
        self.token=token
        self.notifyType=notifyType
        #打卡
        self.res=self.daka()
        print(self.res)
        #推送
        res2=self.notifybyXtuis()
        print(res2)
    # 打卡主方法
    def daka(self):
        date = time.strftime("%Y-%m-%d", time.localtime())
        self.log = '开始\n您的打卡地址为：'+self.address+'\n'

        self.log = self.log + '登录中\n'

        self.login() #登录

        if self.loginToken != None:
            output = self.post()
            self.log = self.log + date + output['msg'] + '\n'
            self.log = self.log  + '结束\n\n'
            output['detail'] = self.log
            return output
        else:
            self.log = self.log + '登录失败\n结束\n'
            resp = {'code': 515, 'msg': '登录失败'}
            resp['detail'] = self.log
            return resp

    #登录并提交打卡方法
    def post(self):
        UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 yiban_iOS/5.0.2'
        for i in range(3): #尝试3此打卡
            time.sleep(0.5)
            date = time.strftime("%Y-%m-%d", time.localtime())
            session = requests.Session()
            #第一次重定向
            header1={
            'Host': 'f.yiban.cn' ,
            'Authorization': 'Bearer '+self.loginToken ,
            'AppVersion': '5.0.2' ,
            'Accept-Encoding': 'gzip, deflate' ,
            'Accept-Language': 'zh-cn' ,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' ,
            'loginToken': self.loginToken ,
            'User-Agent':  UA,
            'Connection': 'keep-alive' ,
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'client=iOS; loginToken='+self.loginToken
            }
            url_1='http://f.yiban.cn/iapp378946'
            try:
                a = session.get(url=url_1,headers=header1,allow_redirects=False)
                if "Location" not in a.headers :
                    self.log=self.log+'易班服务器异常\n'
                    yb_result = {'code': 404, 'msg': '易班服务器异常'}
                    return yb_result
            except Exception:
                self.log=self.log+'第一次重定向出错\n'
                continue
            #第二次重定向
            url_2 = a.headers['Location']
            header2={
            'Host': 'f.yiban.cn' ,
            'AppVersion': '5.0.2' ,
            'Accept-Encoding': 'gzip, deflate' ,
            'Accept-Language': 'zh-cn' ,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' ,
            'loginToken': self.loginToken ,
            'User-Agent':  UA,
            'Connection': 'keep-alive' ,
            'Upgrade-Insecure-Requests': '1'
            }
            try:
                b = session.get(url=url_2, headers=header2,allow_redirects=False)
                if "Location" not in b.headers:
                    self.log=self.log+'loginToken错误\n'
                    yb_result= {'code': 555, 'msg': 'loginToken错误，请修改'}
                    return yb_result
            except Exception:
                self.log=self.log+'第二次重定向出错\n'
                continue

            #跳转到易广金 得到cookie
            url_3=b.headers['Location']
            header3={
            'Host': 'ygj.gduf.edu.cn' ,
            'AppVersion': '5.0.2' ,
            'Accept-Encoding': 'gzip, deflate' ,
            'Accept-Language': 'zh-cn' ,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' ,
            'loginToken': self.loginToken ,
            'User-Agent':  UA,
            'Connection': 'keep-alive' ,
            'Upgrade-Insecure-Requests': '1'
            }
            try:
                c = session.get(url=url_3,headers=header3, allow_redirects=False)
                # 拿到StudentID
                studentID = c.headers['Location'].split('=')[1]
                session.get(url=url_3, headers=header3)
            except Exception:
                self.log=self.log+'第三次重定向出错\n'
                continue


            #检查绑定
            url_bind = "https://ygj.gduf.edu.cn/Handler/device.ashx?flag=checkBindDevice"
            session.get(url=url_bind, headers=header3)

            #检查打卡记录 （暂不检测）
            #url_check='https://ygj.gduf.edu.cn/Handler/health.ashx?flag=getHealth'
            #check_header={
            #'Host': 'ygj.gduf.edu.cn' ,
            #'Accept': '*/*' ,
            #'X-Requested-With': 'XMLHttpRequest' ,
            #'Accept-Language': 'zh-cn' ,
            #'Accept-Encoding': 'gzip, deflate, br' ,
            #'Content-Type': 'application/x-www-form-urlencoded' ,
            #'Origin': 'https://ygj.gduf.edu.cn' ,
            #'User-Agent': UA,
            #'Connection': 'keep-alive' ,
            #}
            #check_data={
            #    'studentID':studentID,
            #    'date':date
            #}
            #check=session.post(url=url_check,headers=check_header,data=check_data).json()

            #判断今日是否已打卡
            if True:
                #打卡
                url_save = "https://ygj.gduf.edu.cn/Handler/health.ashx?flag=save"
                save_headers={
                'Host': 'ygj.gduf.edu.cn' ,
                'Accept': '*/*' ,
                'X-Requested-With': 'XMLHttpRequest' ,
                'Accept-Language': 'zh-cn' ,
                'Accept-Encoding': 'gzip, deflate, br' ,
                'Content-Type': 'application/x-www-form-urlencoded' ,
                'Origin': 'https://ygj.gduf.edu.cn' ,
                'User-Agent': UA,
                'Connection': 'keep-alive' ,
                }
                data_yb_save = {
                          "studentID": studentID,
                          "date":date,
                          "health": "体温37.3℃以下（正常）",
                          "address": self.address,
                          "isTouch": "否",
                          "isPatient": "不是"}
                try:
                    yb_result = session.post(url=url_save, headers=save_headers, data=data_yb_save).json()
                    return yb_result
                except Exception:
                    self.log=self.log+'提交失败！\n'
                    yb_result ={'code':411,'msg':"提交失败"}
                    return yb_result
            #else:
                #yb_result = {'code': 0, 'msg': "今日已打卡"}
                #return yb_result
        return {'code':404,'msg':"打卡失败了"}

    #登录接口方法
    def login(self):
        for i in range(3):
            try:
                LOGINURL = f'https://mobile.yiban.cn/api/v4/passport/login?mobile={self.accountid}&password={self.doCrypto()}&ct=2&identify=1'
                reqHeaders = {"Origin": "https://c.uyiban.com",
                "User-Agent": "Yiban-Pro",
                "AppVersion": "5.0"}
                loginRequest = requests.post(LOGINURL, headers=reqHeaders).json()
                #登录成功后获取
                if loginRequest is not None and str(loginRequest["response"]) == "100":
                    loginToken = loginRequest["data"]["access_token"]
                    name=loginRequest['data']['user']['name']
                    #print(name,'登录成功')
                    self.log=self.log+name+'登录成功\n'
                    self.loginToken=loginToken
                    break
                else:
                    #print('密码错误')
                    self.log=self.log+'密码错误\n'
            except Exception :
                #print('登陆异常正在重试')
                self.log=self.log+'登陆异常正在重试\n'
                time.sleep(0.5)
        #print('登录异常')
        self.log=self.log+'登录异常\n'
        self.loginToken = None



    #登录加密方法
    def doCrypto(self):
            """
            v4接口
            密码加密
            Rsa,base64
            """
            PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
            MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzA
            Ajffez4G4A/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegIC
            XC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx+WasvbS0HuYpF8+
            KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bP
            A9/I5kwfyZ/mM5m8+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7/2vgq7kw2qSmR
            AGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOp
            d2rEpX0/8YE0dRXxukrM7i+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/
            7QT4SZrnRBEo++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/h
            mfJYekb3GEV+10xLOvpe/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNU
            AYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg/IVv6HkFE
            uCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbR
            ZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ==
            -----END PUBLIC KEY-----
            '''
            encrypt = PKCS1_v1_5.new(RSA.importKey(PUBLIC_KEY))
            Sencrypt = base64.b64encode(encrypt.encrypt(bytes(self.password, encoding="utf8")))
            return parse.quote(Sencrypt.decode("utf-8"))

    #通过sever酱来提醒（此方法已暂停维护）
    #def notifybySeverJ(sendKey='', notifyType=0, code=0, desp=''):
    #    """
    #    sendKey：Sever酱的sendkey，具体在 Sever酱网站获取 https://sct.ftqq.com/sendkey
    #    notifyType：提醒类型，0不提醒，1仅失败，2全部提醒
    #    code：打卡状态码，0为成功，其他为失败
    #   """
    #   if len(sendKey) == 0 or notifyType == 0:
    #        print("未输入key或无需提醒")
    #        return 1
    #
    #    if code == 0 and notifyType == 2:
    #        requests.get(url="https://sctapi.ftqq.com/" + sendKey + ".send?title=" + 'Clock%20success')
    #    elif code != 0:
    #        requests.get(url="https://sctapi.ftqq.com/" + sendKey + ".send?title=" + 'Clock%20failed')
    #    return 0
    #微信提示方法
    def notifybyXtuis(self):
        """
        sendKey：虾推啥的token，具体在虾推啥获取 http://www.xtuis.cn/
        notifyType：提醒类型，0不提醒，1仅失败，2全部提醒
        code：打卡状态码，0为成功，其他为失败
        """
        code=self.res['code']
        desp=self.log
        if len(self.token) == 0 or self.notifyType == 0:
            return {"code":1,"msg":"未输入key或无需提醒"}

        if code == 0 and self.notifyType == 2:
            mydata = {
                'text': '打卡成功!',
                'desp': desp
            }
            return   requests.post('http://wx.xtuis.cn/' + self.token + '.send', data=mydata).text

        elif code != 0:
            mydata = {
                'text': '打卡失败！',
                'desp': desp
            }
            return requests.post('http://wx.xtuis.cn/' + self.token + '.send', data=mydata).text

