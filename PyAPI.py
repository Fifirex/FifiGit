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
while (resp!= "n" and resp!= "y" and resp!= "N" and resp!= "Y"):
    print(" Invalid")
    resp = input(" Enter the choice again (y/n): ")
if (resp == "n" or resp == "N"):
    sys.exit(" Thank you")
else:
    name = input (" Enter the repo name : ")
    repos = info (f"https://api.github.com/users/{user}/repos")
    for page in repos:
        for cont in page:
            if(cont['full_name'].split("/")[1] == name):
                print (" Private : " + ("True" if cont['private'] else "False"))
                print (" Fork Count : " + str(cont['forks_count']))
                print (" Stargazers Count : " + str(cont['stargazers_count']))
                print (" Watchers Count : " + str(cont['watchers_count']))
            else:
                pass


# repos = info (f"https://api.github.com/users/{user}/repos")

# all_repo_names=[]
# for page in repos:
#     for repo in page:
#         try:
#             all_repo_names.append(repo['full_name'].split("/")[1])
#         except:
#             pass

# print (all_repo_names)
# print (len(all_repo_names))

# response = requests.get ('https://api.github.com/users/Fifirex/repos?page=2').json()
# print (response)

