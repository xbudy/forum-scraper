from bs4 import BeautifulSoup
import requests

class scrap:
  def __init__(self,manually=False,st=1,end=2):
    self.totalPages=0
    self.all_ids=[]
    self.replies=[]
    self.PostsData=[]
    self.manually=manually
    self.st=int(st)
    self.end=int(end)

  def getTotalPages(self):
    params = (
        ('action', 'threads'),
        ('p', 1),
    )
    response = requests.get('http://cb.rayaheen.net/archive/api/index.php', headers=headers, params=params)
    total=response.json()['pages']['total']
    self.totalPages=int(total)
    return int(total)

  def getAllPostsId(self):
    ids=[]
    print('getting all pages ...')
    self.getTotalPages()
    print('done !')

    if self.manually==False:

      for p in range(1,self.totalPages+1):
        print('getting ids ..')
        print('page : {}'.format(p))
        params = (
            ('action', 'threads'),
            ('p', p),
        )
        response = requests.get('http://cb.rayaheen.net/archive/api/index.php', headers=headers, params=params)
        threads=response.json()['threads']
        for thread in threads:
          idd=thread['id']
          if idd not in ids:
            ids.append(idd)
    else:
      for p in range(self.st,self.end+1):
        print('getting ids ..')
        print('page : {}'.format(p))
        params = (
            ('action', 'threads'),
            ('p', p),
        )
        response = requests.get('http://cb.rayaheen.net/archive/api/index.php', headers=headers, params=params)
        threads=response.json()['threads']
        for thread in threads:
          idd=thread['id']
          if idd not in ids:
            ids.append(idd)
    self.all_ids=ids
    return self.all_ids

  def getData(self,post_id):
    params = (
        ('action', 'posts'),
        ('tid', post_id),
        ('pid', 'NaN'),
        ('p', '1'),
    )

    rs = requests.get('http://cb.rayaheen.net/archive/api/index.php', headers=headers, params=params)
    ##
    postJson=rs.json()
    postData={}
    replies=[]
    ##
    postData['id']=post_id
    ##
    postData['Post_link']='http://cb.rayaheen.net/archive/?action=posts&tid={}&p=1'.format(post_id)
    ##
    thread=postJson['thread']
    ##
    Post_publishing_date=thread['date']
    postData['Post_publishing_date']=Post_publishing_date
    ##
    Post_author=thread['userName']
    postData['Post_author']=Post_author
    ##
    Post_title=thread['title']
    postData['Post_title']=Post_title
    ##
    for post in postJson['posts']:
      replyData={}
      if post['isreply']==0:
        post_html=BeautifulSoup(post['msg'],'html.parser')
        postData['post_html']=post_html
        ##
        post_text=post_html.getText()
        postData['post_text']=post_text
      if post['isreply']==1:
        replyData['id']=post['uid']
        ##
        replyData['post_id']=postData['id']
        ##
        reply_publishing_date=post['date']
        replyData['reply_publishing_date']=reply_publishing_date
        ##
        reply_author=post['userName']
        replyData['reply_author']=reply_author
        ##
        reply_html=BeautifulSoup(post['msg'],'html.parser')
        replyData['reply_html']=reply_html
        ##
        reply_text=reply_html.getText()
        replyData['reply_text']=reply_text
        ##
        replies.append(replyData)
    return postData,replies
  def start(self):
    self.PostsData=[]
    self.replies=[]
    result={}
    for id_ in self.getAllPostsId():
      print('getting data for id {}'.format(id_))
      data=getData(id_)
      postData=data[0]
      self.PostsData.append(postData)
      self.replies+=data[1]
    result['postsData']=self.PostsData
    result['replies']=self.replies
    return result
  
