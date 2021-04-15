import requests

plist=requests.get('http://floor.huluxia.com/post/list/ANDROID/2.1?start=0&count=1&cat_id=43&tag_id=0&sort_by=0').json()['posts']
posts=[]

for one in plist:
  pid=one['postID']
  title=one['title']
  content=requests.get('http://floor.huluxia.com/post/detail/ANDROID/2.3?post_id='+str(pid))
  posts.append({'title':title,'content':content})
