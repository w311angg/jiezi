import requests
import json
import os
import time
import smtplib
import hlx
import random
from email.mime.text import MIMEText
from email.utils import formataddr

sendpost=os.getenv('sendpost')
#sendpost='true'

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

#一言=requests.get('https://international.v1.hitokoto.cn/?c=i').json()['hitokoto']
#print('一言：'+一言)
#状态.append(1)
def 发帖(count):
  #print(count)
  global 状态
  #print(hlx.posts)
  imgstr=''
  for one in hlx.posts[count]['images']:
    time.sleep(5)
    image=requests.get(one).content
    file={'file':image}
    re=requests.post('http://api.upload.lieyou888.com/upload/image?_key='+密钥,files=file).json()
    url=re['fid']
    imgstr+=url+','
  内容=hlx.posts[count]['content']
  标题='【资源分享】'+hlx.posts[count]['title']
  #内容='hhhhghhhhhhhhhh'
  #标题='hhhhghhhhhhhhhh'
  发=requests.post('https://api.bbs.lieyou888.com/post/create/ANDROID/1.0?_key='+密钥,data={'lng':0.0,'cat_id':92,'tag_id':'9202','detail':内容,'type':0,'title':标题,'images':imgstr,'lat':0.0}).json()
  print('发帖：'+发['msg'])
  if '需要审核' in 发['msg']:
    帖id=发['postID']
    with requests.get('https://api.bbs.lieyou888.com/postaudti/detail/ANDROID/1.0?post_id=%s&_key=%s'%(帖id,密钥)) as content:
      post=content.json()['post']
      发帖戳=post['createTime']
    在审核=True
    while 在审核:
      time.sleep(10)
      消息=requests.get('https://api.bbs.lieyou888.com/message/new/list/ANDROID/1.3?type_id=1&_key='+密钥).json()['datas']
      for i in 消息:
        消息戳=i['createTime']
        #print(消息戳,发帖戳,消息戳>发帖戳)
        if 消息戳>发帖戳:
          text=i['content']['text']
          #print(text)
          if 标题 in text:
            在审核=False
            if '不能通过审核。' in text:
              #print('不能通过审核。')
              发帖(count+1)
            elif '已通过审核。' in text:
              #print('已通过审核。')
              pass
  elif '发贴太快了' in 发['msg']:
    time.sleep(60*5)
    print('发帖：计时完毕')
    发帖(count)
  elif '帖子含违规内容' in 发['msg']:
    print('::group::帖子内容')
    print(hlx.posts[count]['content'])
    print('::endgroup::')
    time.sleep(60*5)
    print('发帖：计时完毕')
    发帖(count+1)
  状态.append(发['status'])
if sendpost=='true' or os.getenv('on')=='schedule':
  发帖(0)
#if 发帖['status']==1:
#  帖子id=发帖['postID']
#  删帖=requests.get('https://api.bbs.lieyou888.com/post/destroy/ANDROID/1.0?post_id='+str(帖子id)+'&_key='+密钥).json()
#  print('删帖：'+删帖['msg'])
#  状态.append(删帖['status'])

for i in range(3):
  分享=requests.get('https://api.market.lieyou888.com/task/perform/ANDROID/1.0?data_type=APP_SHARE&_key='+密钥).json()
  print('分享：'+分享['msg'])
  状态.append(分享['status'])

帖子=requests.get('https://api.bbs.lieyou888.com/post/list/ANDROID/1.1?cat_id=92&sort_by=0').json()['posts']
for one in 帖子:
  点赞=requests.get('https://api.bbs.lieyou888.com/post/praise/ANDROID/1.1?post_id='+str(one['postID'])+'&_key='+密钥).json()
  print('点赞：'+点赞['msg'])
  状态.append(点赞['status'])
  取赞=requests.get('https://api.bbs.lieyou888.com/post/praise/ANDROID/1.1?post_id='+str(one['postID'])+'&_key='+密钥).json()
  print('取赞：'+取赞['msg'])
  状态.append(取赞['status'])

for one in 帖子:
  回复数=one['commentCount']
  帖子id=one['postID']
  if 回复数>40:
    评论=requests.get('https://api.bbs.lieyou888.com/post/detail/ANDROID/1.2',params={'post_id':帖子id,'count':20,'start':20}).json()['comments']
    用户id=one['user']['userID']
  else:
    continue
  是楼主=True
  while 是楼主:
    随机评论=random.choice(评论)
    if 随机评论['user']['userID']!=用户id:
      评论内容=随机评论['text']
      是楼主=False
  回复=requests.post('https://api.bbs.lieyou888.com/comment/create/ANDROID/1.0?_key='+密钥,data={'text':评论内容,'post_id':帖子[3]['postID'],'comment_id':0}).json()
  print('回复：'+回复['msg'])
  回复id=回复['commentID']
  状态.append(回复['status'])
  if 回复['code']==200:
    break
#删回复=requests.get('https://api.bbs.lieyou888.com/comment/destroy/ANDROID/1.0?comment_id='+str(回复id)+'&_key='+密钥).json()
#print('删回复：'+删回复['msg'])
#状态.append(删回复['status'])

#登录游戏=requests.post('https://sdkapi.1yuan.cn/sdkapi/user/login/gameuser',data=os.getenv('login')).json()
#print('登录游戏：'+登录游戏['message'])
#if 登录游戏['code']==0:
#  状态.append(1)
#else:
#  状态.append(0)
#print(登录游戏)
#状态.append(登录游戏['data']['popupStatus'])

补签卡=requests.get('https://api.lieyou888.com/question/submit/ANDROID/1.0?content=%5B%7B%22optionIds%22%3A%5B267%5D%2C%22topicId%22%3A71%7D%2C%7B%22optionIds%22%3A%5B403%5D%2C%22topicId%22%3A105%7D%2C%7B%22optionIds%22%3A%5B382%5D%2C%22topicId%22%3A99%7D%2C%7B%22optionIds%22%3A%5B452%5D%2C%22topicId%22%3A117%7D%2C%7B%22optionIds%22%3A%5B142%5D%2C%22topicId%22%3A39%7D%2C%7B%22optionIds%22%3A%5B138%5D%2C%22topicId%22%3A38%7D%2C%7B%22optionIds%22%3A%5B355%5D%2C%22topicId%22%3A93%7D%2C%7B%22optionIds%22%3A%5B450%5D%2C%22topicId%22%3A116%7D%2C%7B%22optionIds%22%3A%5B320%5D%2C%22topicId%22%3A84%7D%2C%7B%22optionIds%22%3A%5B418%5D%2C%22topicId%22%3A108%7D%5D&_key='+密钥).json()
print('补签卡：'+补签卡['msg'])
if '已完成' in 补签卡['msg']:
  状态.append(1)
else:
  状态.append(0)

失败位置=[]
for one,count in zip(状态,range(len(状态))):
  if one==1:
    成功+=1
  else:
    失败+=1
    失败位置.append(count+1)
print('操作成功'+str(成功)+'，操作失败'+str(失败)+'，失败操作：'+str(失败位置))

print('\n===开始领取一元任务奖励===')
成功=0
失败=0
状态=[]
一元任务=requests.get('https://api.market.lieyou888.com/task/daily/list/ANDROID/1.0?_key='+密钥).json()['list']
for one in 一元任务:
  id=one['id']
  返回=requests.get('https://api.market.lieyou888.com/task/receive/ANDROID/1.0?_key='+密钥+'&task_id='+str(id)).json()
  print('%s (%s/%s)：%s'%(one['title'],one['completedQuantity'],one['targetQuantity'],返回['msg']))
  状态.append(返回['status'])
未完成=[]
for one in 一元任务:
  if one['finished']==0:
    未完成.append('%s (%s/%s)'%(one['title'],one['completedQuantity'],one['targetQuantity']))
一元成就=requests.get('https://api.market.lieyou888.com/task/growth/list/ANDROID/1.0?_key='+密钥).json()['list']
for one in 一元成就:
  id=one['id']
  返回=requests.get('https://api.market.lieyou888.com/task/receive/ANDROID/1.0?_key='+密钥+'&task_id='+str(id)).json()
  print('%s (%s/%s)：%s'%(one['title'],one['completedQuantity'],one['targetQuantity'],返回['msg']))
  状态.append(返回['status'])
for one in 一元成就:
  if one['finished']==0:
    未完成.append('%s (%s/%s)'%(one['title'],one['completedQuantity'],one['targetQuantity']))
for one in 状态:
  if one==1:
    成功+=1
  else:
    失败+=1
print('领取成功'+str(成功)+'，领取失败'+str(失败)+'，未完成任务：')
for one in 未完成:
  print(one)

#print('\n===个人信息汇总===')
#信息=requests.get('https://api.bbs.lieyou888.com/user/info/ANDROID/1.1?user_id='+os.getenv('id')+'&_key='+密钥).json()
#print('LV'+str(信息['level'])+'，经验值'+str(信息['exp']))
#挂机=requests.get('https://api.lieyou888.com/card/list/ANDROID/1.0?_key='+密钥).json()['freeTimeCard']
#print('免费'+挂机['formattedBalance'])
#一元=requests.get('https://api.market.lieyou888.com/point/account/ANDROID/1.0?_key='+密钥).json()['balance']
#print('一元积分'+str(一元))
