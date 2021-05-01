import requests
import re

plist=requests.get('http://floor.huluxia.com/post/list/ANDROID/2.1?start=0&count=10&cat_id=43&tag_id=0&sort_by=2').json()['posts']
posts=[]

for one in plist:
  if one['isAppPost']==0:
    pid=one['postID']
    title=one['title']
    title=re.sub('^【.*?】','',title)
    title=re.sub('^\[.*?\]','',title)
    resp=requests.get('http://floor.huluxia.com/post/detail/ANDROID/2.3?post_id='+str(pid)).json()
    content=resp['post']['detail']
    images=resp['post']['images']
    posts.append({'title':title,'content':content,'images':images})
