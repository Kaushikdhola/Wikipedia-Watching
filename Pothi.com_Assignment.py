

import json
import time
import datetime
from sseclient import SSEClient as EventSource

url = 'https://stream.wikimedia.org/v2/stream/mediawiki.revision-create'
wiki={}
wiki_five_minutes={}
users={}
users_five_minutes={}
#Function to generate numbers of updated pages with specific domain for 1 minute 
def Updates_on_Domain_one_min():
    endTime = datetime.datetime.now() + datetime.timedelta(minutes=1)
    for event in EventSource(url):
       if datetime.datetime.now() >= endTime:
          break
       else: 
          pass
       if event.event == 'message':
          try:
             change = json.loads(event.data)
             
             #adds domain to the dictionary for the first time with value 0
             if wiki.get(change['meta']['domain']) is None:
                 wiki[change['meta']['domain']]=0
             else:
                 #adds how many number of pages updated in particular domain 
                 wiki[change['meta']['domain']]=wiki[change['meta']['domain']]+1
             
             #checks if data is related to en.wikipedia.org
             if(change['meta']['domain']=="en.wikipedia.org"):
                 
                 #checks if user is bot or not to exclude bots from report
                 if(change['performer']['user_is_bot']==False):
                     
                     #adds user name to the dictionary for the first time with user edit score
                     if(users.get(change['performer']['user_text']) is None):

                         #checks whether user_edit_count is available in performer sub-dictionary or not 
                         if 'user_edit_count' in change['performer'].keys(): 
                             users[change['performer']['user_text']]=change['performer']['user_edit_count']
                         else:
                             pass
                     else:
                         if(change['performer']['user_text'] in users.keys()):
                             
                             #compares user_edit_count if same user appears multiple time over given period of time
                             if(users[change['performer']['user_text']]<change['performer']['user_edit_count']):
                                 
                                 #updates user_edit_count if current user edit count is greater than previous user edit count 
                                 users[change['performer']['user_text']]=change['performer']['user_edit_count']
             else:   
                  pass 
          except ValueError:
             pass
       else:
          # print(change['performer'])
          print('{user} edited {title}'.format(**change))

#Function to generate numbers of updated pages with specific domain for 5 minutes
def Updates_on_Domain_five_min():
    endTime = datetime.datetime.now() + datetime.timedelta(minutes=5)
    for event in EventSource(url):
       if datetime.datetime.now() >= endTime:
          break
       else: 
          pass
       if event.event == 'message':
          try:
             change = json.loads(event.data)
             
             #adds domain to the dictionary for the first time with value 0
             if wiki_five_minutes.get(change['meta']['domain']) is None:
                 wiki_five_minutes[change['meta']['domain']]=0
             else:
                 #adds how many number of pages updated in particular domain 
                 wiki_five_minutes[change['meta']['domain']]=wiki_five_minutes[change['meta']['domain']]+1
             
             #checks if data is related to en.wikipedia.org
             if(change['meta']['domain']=="en.wikipedia.org"):
                 
                 #checks if user is bot or not to exclude bots from report
                 if(change['performer']['user_is_bot']==False):

                     #adds user name to the dictionary for the first time with user edit score
                     if(users_five_minutes.get(change['performer']['user_text']) is None):
                         
                         #checks whether user_edit_count is available in performer sub-dictionary or not 
                         if 'user_edit_count' in change['performer'].keys(): 
                             users_five_minutes[change['performer']['user_text']]=change['performer']['user_edit_count']
                         else:
                             pass
                     else:
                         if(change['performer']['user_text'] in users_five_minutes.keys()):

                             #compares user_edit_count if same user appears multiple time over given period of time
                             if(users_five_minutes[change['performer']['user_text']]<change['performer']['user_edit_count']):
                                 
                                 #updates user_edit_count if current user edit count is greater than previous user edit count 
                                 users_five_minutes[change['performer']['user_text']]=change['performer']['user_edit_count']
             else:   
                  pass
          except ValueError:
             pass
       else:
          print('{user} edited {title}'.format(**change))
#generating Domail Report
def domain_report():
    
    #sorting and displaying one minute domain report  
    domain_count=0
    domain_repost_dict=sorted(wiki.items(), key=lambda x: x[1], reverse=True)
    
    for i in domain_repost_dict:
      if(i[1]!=0):
         domain_count+=1    
    
    print("Total number of Wikipedia Domains Updated: "+str(domain_count))
    print("")
    for i in domain_repost_dict:
      if(i[1]!=0):
        print(i[0] +": "+ str(i[1]) +" pages updated")
    print("")


    #sorting and displaying one minute users data report  
    users_report_dict=sorted(users.items(), key=lambda x: x[1], reverse=True)
    print("Users who made changes to en.wikipedia.org ")
    print("")
    for i in users_report_dict:
      print(i[0] +": "+ str(i[1]))
    
    print("")
    print("Five Minutes Data")
    print("")

    #sorting and displaying five minute domain report 

    domain_count_five=0
    domain_repost_five_dict=sorted(wiki_five_minutes.items(), key=lambda x: x[1], reverse=True)
    
    for i in domain_repost_five_dict:
      if(i[1]!=0):
         domain_count_five+=1    
    
    print("Total number of Wikipedia Domains Updated: "+str(domain_count))
    print("")
    for i in domain_repost_five_dict:
      if(i[1]!=0):
        print(i[0] +": "+ str(i[1]) +" pages updated")
    print("")
    

    #sorting and displaying one minute users data report  
    
    users_report_five_dict=sorted(users_five_minutes.items(), key=lambda x: x[1], reverse=True)
    print("Users who made changes to en.wikipedia.org ")
    print("")
    for i in users_report_five_dict:
      print(i[0] +": "+ str(i[1]))
Updates_on_Domain_one_min()
Updates_on_Domain_five_min()
domain_report()