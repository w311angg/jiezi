import requests
import json
import os
密钥=os.getenv("key")
板块列表=json.loads(requests.get("https://api.bbs.lieyou888.com/category/list/ANDROID/1.0?_key="+密钥).text)
成功=0
失败=0
for i in 板块列表["categories"]:
  if i["categoryID"]!=0:
    板块签到回返=requests.get("https://api.bbs.lieyou888.com/user/signin/ANDROID/1.0?_key="+密钥+"&cat_id="+str(i["categoryID"])).text
    print(i["title"]+"："+板块签到回返)
    if json.loads(板块签到回返)["status"]==1:
      成功=成功+1
    else:
      失败=失败+1
状态=[]
云挂机回返=requests.post("https://api.lieyou888.com/signin/create/ANDROID/1.0?_key="+密钥)
print("云挂机："+云挂机回返.text)
状态.append(云挂机回返.json()['status'])

一元签到=requests.get('https://api.market.lieyou888.com/sign/click/ANDROID/1.0?_key='+密钥).json()
print('一元签到：'+一元签到)
状态.append(一元签到['status'])

发帖=requests.post('https://api.bbs.lieyou888.com/post/create/ANDROID/1.0?_key='+密钥,data={'lng':0.0,'cat_id':2,'tag_id':'-1','detail':'水鸭子好看吗','type':0,'title':'你这个漂亮的小水鸭','lat':0.0}).json()
print('发帖：'+发帖)

分享=requests.get('https://api.market.lieyou888.com/task/perform/ANDROID/1.0?data_type=APP_SHARE&_key='+密钥)
print('分享：'+分享)

帖子=requests.get('https://api.bbs.lieyou888.com/post/list/ANDROID/1.1?cat_id=2').json()['posts']
for one in 帖子:
  点赞=requests.get('https://api.bbs.lieyou888.com/post/praise/ANDROID/1.1?post_id='+one['postID']+'&_key='+密钥)
  print('点赞：'+点赞)

一元任务=requests.get('https://api.market.lieyou888.com/task/daily/list/ANDROID/1.0?_key='+密钥).json()['list']
for one in 一元任务:
  id=one['id']
  返回=requests.get('https://api.market.lieyou888.com/task/receive/ANDROID/1.0?_key='+密钥+'&task_id='+id).json()
  print(one['title']+'：'+返回)
  状态.append(返回['status'])

print(str(成功)+" succeeded, "+str(失败)+" failed.")
