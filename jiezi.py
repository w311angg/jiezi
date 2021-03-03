import requests
import json
import os
密钥=os.getenv("key")
板块列表=json.loads(requests.get("https://api.bbs.lieyou888.com/category/list/ANDROID/1.0?_key="+密钥).text)
成功=0
失败=0
print('\n===开始板块签到===')
for i in 板块列表["categories"]:
  if i["categoryID"]!=0:
    板块签到回返=requests.get("https://api.bbs.lieyou888.com/user/signin/ANDROID/1.0?_key="+密钥+"&cat_id="+str(i["categoryID"])).text
    print(i["title"]+"："+板块签到回返)
    if json.loads(板块签到回返)["status"]==1:
      成功=成功+1
    else:
      失败=失败+1
print('签到成功'+str(成功)+'，签到失败'+str(失败))

print('\n===开始其他任务===')
云挂机回返=requests.post("https://api.lieyou888.com/signin/create/ANDROID/1.0?_key="+密钥).text
print("云挂机签到："+云挂机回返)

一元签到=requests.get('https://api.market.lieyou888.com/sign/click/ANDROID/1.0?_key='+密钥).json()
print('一元签到：'+str(一元签到))

一言=requests.get('https://v1.hitokoto.cn/').json()['hitokoto']
发帖=requests.post('https://api.bbs.lieyou888.com/post/create/ANDROID/1.0?_key='+密钥,data={'lng':0.0,'cat_id':2,'tag_id':'-1','detail':一言,'type':0,'title':一言,'lat':0.0}).json()
print('发帖：'+str(发帖))

分享=requests.get('https://api.market.lieyou888.com/task/perform/ANDROID/1.0?data_type=APP_SHARE&_key='+密钥).json()
print('分享：'+str(分享))

帖子=requests.get('https://api.bbs.lieyou888.com/post/list/ANDROID/1.1?cat_id=2').json()['posts']
for one in 帖子:
  点赞=requests.get('https://api.bbs.lieyou888.com/post/praise/ANDROID/1.1?post_id='+str(one['postID'])+'&_key='+密钥).json()
  print('点赞：'+str(点赞))

回复=requests.post('https://api.bbs.lieyou888.com/comment/create/ANDROID/1.0?_key='+密钥,data={'text':一言,'post_id':帖子[3]['postID'],'comment_id':0}).json()
print('回复：'+str(回复))

print('\n===开始领取一元任务奖励===')
成功=0
失败=0
状态=[]
一元任务=requests.get('https://api.market.lieyou888.com/task/daily/list/ANDROID/1.0?_key='+密钥).json()['list']
for one in 一元任务:
  id=one['id']
  返回=requests.get('https://api.market.lieyou888.com/task/receive/ANDROID/1.0?_key='+密钥+'&task_id='+str(id)).json()
  print(one['title']+'：'+str(返回))
  状态.append(返回['status'])
for one in 状态:
  if one==1:
    成功+=1
  else:
    失败+=1
print('领取成功'+str(成功)+'，领取失败'+str(失败))
