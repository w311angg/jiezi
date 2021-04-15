import requests

plist=requests.get('http://floor.huluxia.com/post/list/ANDROID/2.1?start=0&count=1&cat_id=43&tag_id=0&sort_by=0').json()['posts']
posts=[]

for one in plist:
  if one['isRich']==0 and one['isAppPost']==0:
    pid=one['postID']
    title=one['title'].replace('【资源分享】','')
    content=requests.get('http://floor.huluxia.com/post/detail/ANDROID/2.3?post_id='+str(pid)).json()['post']['detail']
    posts.append({'title':title,'content':content})
