import requests
import re

plist=requests.get('http://floor.huluxia.com/post/list/ANDROID/2.1?start=0&count=1&cat_id=43&tag_id=0&sort_by=0').json()['posts']
posts=[]

for one in plist:
  if one['isRich']==0 and one['isAppPost']==0:
    pid=one['postID']
    title=one['title']
    title=re.sub('【.*?】','',title)
    re=requests.get('http://floor.huluxia.com/post/detail/ANDROID/2.3?post_id='+str(pid)).json()
    content=re['post']['detail']
    images=re['post']['images']
    posts.append({'title':title,'content':content,'images':images})
