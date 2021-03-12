import requests
import json
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
def mail():
    msg=MIMEText(str(云挂机回返),'plain','utf-8')
    msg['From']=formataddr(["jiezi",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To']=formataddr(["WG",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject']='云挂机需要手动签到'                # 邮件的主题，也可以说是标题
 
    server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接
    print('邮件已发送')

my_sender=os.getenv('sender')    # 发件人邮箱账号
my_pass = os.getenv('pass')              # 发件人邮箱密码
my_user=os.getenv('to')      # 收件人邮箱账号，我这边发送给自己
debug=0
密钥=os.getenv("key")
板块列表=json.loads(requests.get("https://api.bbs.lieyou888.com/category/list/ANDROID/1.0?_key="+密钥).text)
成功=0
失败=0
print('===开始板块签到===')
for i in 板块列表["categories"]:
  if i["categoryID"]!=0:
    板块签到回返=requests.get("https://api.bbs.lieyou888.com/user/signin/ANDROID/1.0?_key="+密钥+"&cat_id="+str(i["categoryID"])).text
    print(i["title"]+"："+json.loads(板块签到回返)["msg"])
    if json.loads(板块签到回返)["status"]==1:
      成功=成功+1
    else:
      失败=失败+1
print('签到成功'+str(成功)+'，签到失败'+str(失败))

print('\n===开始其他任务===')
成功=0
失败=0
状态=[]
if debug==0:
  for i in range(5):
    time.sleep(2)
    #保持活跃度以成功云挂机签到
    看社区=requests.get('https://api.bbs.lieyou888.com/post/list/ANDROID/1.1?_key='+密钥).json()
    print('看社区：'+看社区['msg'])
    状态.append(看社区['status'])
云挂机回返=requests.post("https://api.lieyou888.com/signin/create/ANDROID/1.0?_key="+密钥).json()
#云挂机回返['msg']=None
if 云挂机回返['msg']!=None:
  print("云挂机签到："+云挂机回返['msg'])
else:
  print("云挂机签到："+str(云挂机回返))
  mail()
状态.append(云挂机回返['status'])

一元签到=requests.get('https://api.market.lieyou888.com/sign/click/ANDROID/1.0?_key='+密钥).json()
print('一元签到：'+一元签到['msg'])
状态.append(一元签到['status'])

一言=requests.get('https://international.v1.hitokoto.cn/?c=i').json()['hitokoto']
print('一言：'+一言)
发帖=requests.post('https://api.bbs.lieyou888.com/post/create/ANDROID/1.0?_key='+密钥,data={'lng':0.0,'cat_id':2,'tag_id':'-1','detail':一言,'type':0,'title':一言,'lat':0.0}).json()
print('发帖：'+发帖['msg'])
状态.append(发帖['status'])
if 发帖['status']==1:
  帖子id=发帖['postID']
  删帖=requests.get('https://api.bbs.lieyou888.com/post/destroy/ANDROID/1.0?post_id='+str(帖子id)+'&_key='+密钥).json()
  print('删帖：'+删帖['msg'])
  状态.append(删帖['status'])

for i in range(3):
  分享=requests.get('https://api.market.lieyou888.com/task/perform/ANDROID/1.0?data_type=APP_SHARE&_key='+密钥).json()
  print('分享：'+分享['msg'])
  状态.append(分享['status'])

帖子=requests.get('https://api.bbs.lieyou888.com/post/list/ANDROID/1.1?cat_id=2').json()['posts']
for one in 帖子:
  点赞=requests.get('https://api.bbs.lieyou888.com/post/praise/ANDROID/1.1?post_id='+str(one['postID'])+'&_key='+密钥).json()
  print('点赞：'+点赞['msg'])
  状态.append(点赞['status'])

回复=requests.post('https://api.bbs.lieyou888.com/comment/create/ANDROID/1.0?_key='+密钥,data={'text':一言,'post_id':帖子[3]['postID'],'comment_id':0}).json()
print('回复：'+回复['msg'])
回复id=回复['commentID']
状态.append(回复['status'])
删回复=requests.get('https://api.bbs.lieyou888.com/comment/destroy/ANDROID/1.0?comment_id='+str(回复id)+'&_key='+密钥).json()
print('删回复：'+删回复['msg'])
状态.append(删回复['status'])

#登录游戏=requests.post('https://sdkapi.1yuan.cn/sdkapi/user/login/gameuser',data=os.getenv('login')).json()
#print('登录游戏：'+登录游戏['message'])
#if 登录游戏['code']==0:
#  状态.append(1)
#else:
#  状态.append(0)
#print(登录游戏)
#状态.append(登录游戏['data']['popupStatus'])

for one in 状态:
  if one==1:
    成功+=1
  else:
    失败+=1
print('操作成功'+str(成功)+'，操作失败'+str(失败)+'，失败操作：'+str(状态))

print('\n===开始领取一元任务奖励===')
成功=0
失败=0
状态=[]
一元任务=requests.get('https://api.market.lieyou888.com/task/daily/list/ANDROID/1.0?_key='+密钥).json()['list']
for one in 一元任务:
  id=one['id']
  返回=requests.get('https://api.market.lieyou888.com/task/receive/ANDROID/1.0?_key='+密钥+'&task_id='+str(id)).json()
  print(one['title']+'：'+返回['msg'])
  状态.append(返回['status'])
未完成=[]
for one in 一元任务:
  if one['finished']==0:
    未完成.append(one['title'])
for one in 状态:
  if one==1:
    成功+=1
  else:
    失败+=1
print('领取成功'+str(成功)+'，领取失败'+str(失败)+'，未完成任务：'+str(未完成))

#print('\n===个人信息汇总===')
#信息=requests.get('https://api.bbs.lieyou888.com/user/info/ANDROID/1.1?user_id='+os.getenv('id')+'&_key='+密钥).json()
#print('LV'+str(信息['level'])+'，经验值'+str(信息['exp']))
#挂机=requests.get('https://api.lieyou888.com/card/list/ANDROID/1.0?_key='+密钥).json()['freeTimeCard']
#print('免费'+挂机['formattedBalance'])
#一元=requests.get('https://api.market.lieyou888.com/point/account/ANDROID/1.0?_key='+密钥).json()['balance']
#print('一元积分'+str(一元))
