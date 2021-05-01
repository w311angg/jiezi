import requests
import re

plist=requests.get('http://floor.huluxia.com/post/list/ANDROID/2.1?start=0&count=10&cat_id=43&tag_id=0&sort_by=1').json()['posts']
posts=[]

for one in plist:
  if one['isRich']==0 and one['isAppPost']==0:
    pid=one['postID']
    title=one['title']
    title=re.sub('^【.*?】','',title)
    title=re.sub('^\[.*?\]','',title)
    resp=requests.get('http://floor.huluxia.com/post/detail/ANDROID/2.3?post_id='+str(pid)).json()
    content=resp['post']['detail']
    images=resp['post']['images']
    if not '<image>' in content:
      posts.append({'title':title,'content':content,'images':images})
