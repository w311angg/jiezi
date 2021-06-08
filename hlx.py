import requests
import re
import time

plist=requests.get('http://floor.huluxia.com/post/list/ANDROID/2.1?start=0&count=100&cat_id=43&tag_id=0&sort_by=1').json()['posts']
posts=[]
ticks = time.time()*1000

for one in plist:
  print(ticks-one['createTime'],ticks,one['createTime'])
  if one['isRich']==0 and one['isAppPost']==0 and ticks-one['createTime']>10*60*60*1000:
    pid=one['postID']
    title=one['title']
    title=re.sub('^【.*?】','',title)
    title=re.sub('^\[.*?\]','',title)
    resp=requests.get('http://floor.huluxia.com/post/detail/ANDROID/2.3?post_id='+str(pid)).json()
    content=resp['post']['detail']
    images=resp['post']['images']
    if (not '<image>' in content) and (len(images)>=3):
      posts.append({'title':title,'content':content,'images':images})
