import requests
import sys

# setup owner name , access_token, and headers 
# access_token = input(" Enter the Acess Token: ")
access_token ='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' 
user = input(" Enter the name: ")
auth = {'Authorization':"token "+access_token}

url = f"https://api.github.com/users/{user}"
response = requests.get(url, headers = auth)
if response:
    data = response.json()
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

def info2 (url):
    listData = []
    for pnum in range(1,600):
        urlN = url + f"&page={pnum}"
        point = requests.get(urlN, headers = auth).json()['items']
        if(point == []):
            # repos.append(None)
            break
        else:
            listData.append(point)
    return listData

def invalid (ch):
    while (ch!= "y" and ch!= "Y" and ch!= "n" and ch!="N"):
        print(" Invalid")
        ch = input(" Enter the choice again (y/n): ")
    return ch

# test = info2(f"https://api.github.com/search/repositories?q=user:{user}")
# print (len(test))

# all_repo_names=[]
# for page in test:
#     for repo in page:
#         try:
#             all_repo_names.append(repo['full_name'].split("/")[1])
#         except:
#             pass
    
# print (all_repo_names)

# test = requests.get("https://api.github.com/search/repositories?q=user:Aeroscythe", headers=auth)
# print (test.json()['items'])

print (" =============================")
print ("           USER INFO")
print (" =============================")
print (" Username: " + user)
print (" Name : " + (data['name'] if data['name'] != None else "NULL"))
print (" Avatar URL : " + data['avatar_url'])
print (" GitHub Hnadle : " + data['url'])
print (" Email : " + (data['email'] if data['email'] != None else "NULL"))
print (" BioData : " + (data['bio'] if data['bio'] != None else "NULL"))

print (" Followers : [" + str(data['followers']) + "]")
if (data['followers'] != 0):
    followers = info (f"https://api.github.com/users/{user}/followers")
    for page in followers:
        for cont in page:
            try:
                print (" * " + cont['login'])
            except:
                pass

print (" Following : [" + str(data['following']) + "]")
if (data['followers'] != 0):
    following = info (f"https://api.github.com/users/{user}/following")
    for page in following:
        for cont in page:
            try:
                print (" * " + cont['login'])
            except:
                pass

resp = input(" Enquire about Repos? (y/n): ")
resp = invalid(resp)
while (resp!='n' and resp!='N'):
    flag = 0
    name = input (" Enter the repo name : ")
    repos = info2 (f"https://api.github.com/search/repositories?q=user:{user}&per_page=100")
    for page in repos:
        for cont in page:
            if(cont['full_name'].split("/")[1] == name):
                print (" Private : " + ("True" if cont['private'] else "False"))
                print (" Fork Count : " + str(cont['forks_count']))
                print (" Stargazers Count : " + str(cont['stargazers_count']))
                print (" Watchers Count : " + str(cont['watchers_count']))
                print (" License : " + (cont['license'] if cont['license'] != None else "NULL"))
                flag = 1
            else:
                pass
    if (flag == 0):
        print (" Repo not found")
    resp = input(" Continue? (y/n): ")
    resp = invalid(resp)

print(" Thank You")

