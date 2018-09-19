#https://praw.readthedocs.io/en/latest/
import csv
import praw
import time
from praw.models import MoreComments
reddit = praw.Reddit(client_id='Vl96qzbnmzWwtg',
                     client_secret='fGxf3KaWkmr_V7p0G9Zg6OAj4ro',
                     user_agent='skincare-edgretsae:1:1 (by /u/jsnkwok)')
#client id info... https://praw.readthedocs.io/en/latest/getting_started/authentication.html#oauth
#PRAW THROTTLE: https://github.com/eleweek/SearchingReddit/blob/master/download_whole_subreddit.py

print(reddit.read_only)  # Output: True! yes. 
subreddit = 'malefashionadvice'
#documentation for https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

#RECURSIVE FUNCTION: pulls out the comments from each response, so its a direct response. Is breadth first> 
def findallcomments(comment_object):
    allreplies = []
    #comment_count= 1
    for sub_comment in comment_object.replies:
        try: #wrap it into a 
            allreplies.append(sub_comment.body) #pulls out the BODY class
            try:
                sub_replies = findallcomments(sub_comment) #put in the OBJECT
            except:
                pass
            allreplies = allreplies+sub_replies
        except:
            pass
    return allreplies #need to append through the comment. how do i keep track? of the responses? 
    #return a list 
    #return a LIST of COMMENTS... then i can iterate through it and 


#controversial, gilded hot new rising top
with open('2018_0919_redditdump.csv', 'w') as csvfile:
    fieldnames = ['title', 'score','commentno','replyno','id','url','redditor','comment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'title': 'Baked', 'commentno':1,'replyno':1,'score': '1234','id': 'someid1123','url': 'wwwredditdotcom','redditor':'jsnkwok','comment': 'Beans'})
    print("..wrote the title, now writing Reddit posts...")

    threadno = 1
    commentno = 1
    #for submission in reddit.subreddit('SkincareAddiction/').hot(limit=999):

    #try .hot .top. .new .rising .contraversial 
    
    #1HOT 
    for submission in reddit.subreddit(subreddit).hot(limit=None):
        
        commentcount = 0 
        for top_level_comment in submission.comments: #https://praw.readthedocs.io/en/latest/tutorials/comments.html
            commentlist = [] #restart the list. only created it to append the subcomments. 
            try:
                redditor = top_level_comment.author
                comment = top_level_comment.body
                #commentlist.append(top_level_comment.body)
                ### UGLY REDUNDANT CODE
                try:
                    #print(top_level_comment.body)
                    commentcount += 1
                    writer.writerow({'title': submission.title, 'score': submission.score, 'commentno':commentcount,'replyno':replyno,'id': submission.id,'url': submission.url,'redditor':redditor,'comment': comment})
                    print("Thread %r // Comment %r // Replyno %r", threadno, commentno, replyno)
                    commentno += 1
                    replyno += 1
                except:
                    pass

                #USE IF WANT ALL REPLIES 
                #sub_comment_list = findallcomments(top_level_comment) #AGAIN, pass the OBJECT! We will print out via top_level_comment.body 
                #commentlist += sub_comment_list

                #USE IF ONLY USE 2nD LEVEL
                replyno = 0
                for sub_comment in top_level_comment.replies:
                    #commentlist.append(sub_comment.body)
                    comment = sub_comment.body     
                    redditor = sub_comment.author       
                    #for comment in commentlist: #removed forloop b/c.. i dont like 
                    try:
                        #print(top_level_comment.body)
                        commentcount += 1
                        writer.writerow({'title': submission.title, 'score': submission.score, 'commentno':commentcount,'replyno':replyno,'id': submission.id,'url': submission.url,'redditor':redditor,'comment': comment})
                        print("Thread %r // Comment %r // Replyno %r", threadno, commentno, replyno)
                        commentno += 1
                        replyno += 1
                    except:
                        pass
            except:
                pass
        threadno += 1
    #2TOP 
    for submission in reddit.subreddit(subreddit).top(limit=None):
        commentcount = 0 
        for top_level_comment in submission.comments: #https://praw.readthedocs.io/en/latest/tutorials/comments.html
            commentlist = [] #restart the list. only created it to append the subcomments. 
            try:
                commentlist.append(top_level_comment.body)
                #USE IF WANT ALL REPLIES 
                #sub_comment_list = findallcomments(top_level_comment) #AGAIN, pass the OBJECT! We will print out via top_level_comment.body 
                #commentlist += sub_comment_list

                #USE IF ONLY USE 2nD LEVEL
                for sub_comment in top_level_comment.replies:
                    commentlist.append(sub_comment.body)
                replyno = 0
                for comment in commentlist:
                    try:
                        #print(top_level_comment.body)
                        commentcount += 1
                        writer.writerow({'title': submission.title, 'score': submission.score, 'commentno':commentcount,'replyno':replyno,'id': submission.id,'url': submission.url,'comment': comment})
                        print("Thread %r // Comment %r // Replyno %r", threadno, commentno, replyno)
                        commentno += 1
                        replyno += 1
                    except:
                        pass
            except:
                pass
        threadno += 1
    #3RISING 
    for submission in reddit.subreddit(subreddit).rising(limit=None):
        commentcount = 0 
        for top_level_comment in submission.comments: #https://praw.readthedocs.io/en/latest/tutorials/comments.html
            commentlist = [] #restart the list. only created it to append the subcomments. 
            try:
                commentlist.append(top_level_comment.body)
                #USE IF WANT ALL REPLIES 
                #sub_comment_list = findallcomments(top_level_comment) #AGAIN, pass the OBJECT! We will print out via top_level_comment.body 
                #commentlist += sub_comment_list

                #USE IF ONLY USE 2nD LEVEL
                for sub_comment in top_level_comment.replies:
                    commentlist.append(sub_comment.body)
                replyno = 0
                for comment in commentlist:
                    try:
                        #print(top_level_comment.body)
                        commentcount += 1
                        writer.writerow({'title': submission.title, 'score': submission.score, 'commentno':commentcount,'replyno':replyno,'id': submission.id,'url': submission.url,'comment': comment})
                        print("Thread %r // Comment %r // Replyno %r", threadno, commentno, replyno)
                        commentno += 1
                        replyno += 1
                    except:
                        pass
            except:
                pass
        threadno += 1
    #4NEW
    for submission in reddit.subreddit(subreddit).new(limit=None):
        commentcount = 0 
        for top_level_comment in submission.comments: #https://praw.readthedocs.io/en/latest/tutorials/comments.html
            commentlist = [] #restart the list. only created it to append the subcomments. 
            try:
                commentlist.append(top_level_comment.body)
                #USE IF WANT ALL REPLIES 
                #sub_comment_list = findallcomments(top_level_comment) #AGAIN, pass the OBJECT! We will print out via top_level_comment.body 
                #commentlist += sub_comment_list

                #USE IF ONLY USE 2nD LEVEL
                for sub_comment in top_level_comment.replies:
                    commentlist.append(sub_comment.body)
                replyno = 0
                for comment in commentlist:
                    try:
                        #print(top_level_comment.body)
                        commentcount += 1
                        writer.writerow({'title': submission.title, 'score': submission.score, 'commentno':commentcount,'replyno':replyno,'id': submission.id,'url': submission.url,'comment': comment})
                        print("Thread %r // Comment %r // Replyno %r", threadno, commentno, replyno)
                        commentno += 1
                        replyno += 1
                    except:
                        pass
            except:
                pass
        threadno += 1
    

    #top_level_comments = list(submission.comments)#
    #all_comments = submission.comments.list()
    #print(top_level_comments)
    #print("-------")