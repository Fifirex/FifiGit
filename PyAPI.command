#!/usr/local/bin/python3
import requests
import sys

# setup owner name , access_token, and headers 
user = input(" Enter the name: ")
access_token ='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' 
auth = {'Authorization':"Token "+access_token}

url = f"https://api.github.com/users/{user}"
data = requests.get(url, headers = auth).json()
if requests.get(url, headers = auth):
    data = requests.get(url, headers = auth).json()
else:
    sys.exit(" User not found") 

def info (url):
    listData = []
    for pnum in range(1,600):
        urlN = url + f"?page={pnum}"
        point = requests.get(urlN, headers = auth).json()
        if(point == []):  
            # repos.append(None)
            break
        else: 
            listData.append(point)
    return listData

print (" Here is some info on the user:")
print (" Username: " + user)
print (" Name : " + (data['name'] if data['name'] != None else "NULL"))
print (" Avatar URL : " + data['avatar_url'])
print (" GitHub Hnadle : " + data['url'])
print (" Email : " + (data['email'] if data['email'] != None else "NULL"))
print (" BioData : " + (data['bio'] if data['bio'] != None else "NULL"))

repos = info(f"https://api.github.com/users/{user}/repos")

all_repo_names=[]
for page in repos:
    for repo in page:
        try:
            all_repo_names.append(repo['full_name'].split("/")[1])
        except:
            pass

# print (all_repo_names)
# print (len(all_repo_names))

# response = requests.get ('https://api.github.com/users/Fifirex/repos?page=2').json()
# print (response)




