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
云挂机回返=requests.get("https://api.lieyou888.com/signin/create/ANDROID/1.0?_key="+密钥,data='type=1').text
print("云挂机："+云挂机回返)
if json.loads(云挂机回返)["status"]==1:
  成功=成功+1
else:
  失败=失败+1
print(str(成功)+" succeeded, "+str(失败)+" failed.")
