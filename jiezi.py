import requests
import json
import os
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
print(云挂机回返)
print("云挂机签到："+云挂机回返['msg'])
状态.append(云挂机回返['status'])

一元签到=requests.get('https://api.market.lieyou888.com/sign/click/ANDROID/1.0?_key='+密钥).json()
print('一元签到：'+一元签到['msg'])
状态.append(一元签到['status'])

一言=requests.get('https://v1.hitokoto.cn/').json()['hitokoto']
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
