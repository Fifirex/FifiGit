# KOSS-Selections-API
This is a CLI to interact with the [GitHub REST API](https://docs.github.com/en/rest). The core of the program is build upon Python, mainly using the [requests](https://pypi.org/project/requests/) library. The library is used to `GET` data from the API server and import it to the Python code.

Feel free to jump to the [Installation](#install) if you want to skip over the explanation.

## GitHub REST API
GitHub REST API can be used to create calls to get the data you need to integrate with GitHub.

Trying out a basic command, we can look at the basic functionality of the API

```
$ curl https://api.github.com/Fifirex

> {
> "login": "Fifirex",
> "id": 75205458,
> "node_id": "MDQ6VXNlcjc1MjA1NDU4",
> "url": "https://api.github.com/users/Fifirex",
> ...
> }
```

If you add the `-i` tag we see that the `Content-Type` is `application/json`.

This can be usd to access Basic information and Public Repositaries on GitHub. To access Private Repos and more info on the user, we can generate a [Personal Access Token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) with valid scopes to access the respective data.

So we can access all the Repos by using the following command for a specific username

```
curl -H “Authorization: token MYTOKEN” https://api.github.com/search/repositories?q=user:MYUSERNAME
```

This is all we need to know about the API to build our CLI.

## Building the CLI
To get the information from the API servers we use `GET` from the `requests` module.

For example, for a given `user` we use

```
auth = {'Authorization':"token " + Token_Name}
data = requests.get (f"https://api.github.com/users/{user}", headers = auth).json()
```

`data` is the response `json` object, through which the data is extracted using the key attributes.

The interactive interface is then built on these foundations, which was then made into an Unix Executable File to run it through the Terminal.

## Let's talk _Python_
The reason I chose this language over something like C++ is beacuse of the easy http connection power it possesses. `GET` commands can be used in just a single line, and playing with `json` objects is simpler too.

But...

`GET` process in general is too slow for any language, and thus acts as the Rate Limiter Command in the program. The larger the data set (`google` having over 2000 repos), the more time it takes.

This time delay was reduced by pre loading Repositaries, and increasing the `per_page` to its maximum (`100`). I have also added a `WARNING` flag if the repo count exceeds `50`, and the user can chose to list out the names (not recommended) if they want to.

## <a name="install">Get the Code! </a>

> Note : This is a Unix Executable File, which can be run only on Unix-like OS (Linux or MacOS). For using the file on Windows, you can extract the Python core and convert it to a .exe file, and add it to the PATH in a similar fashion. 

> Note : For API access, we need an access token (mentioned in Section 1). Generate one and add it to the **line 7** in the code. 

First, we need th code. Clone the repository into a Directory of your choice using

```
git clone https://github.com/Fifirex/KOSS-Selections-API.git
```

Once we have the executable file, just typing `./FifiGit` while in the Directory will run the program. To make it a true CLI, we need meddle with the `PATH`.

First, make a temporary `bin` which will then be added to the `PATH`

```
$ mkdir -p ~/bin
$ cp FifiGit ~/bin
$ export PATH=$PATH":$HOME/bin"
```

This creates a copy of the file in the `PATH` and now you can run it by just,

```
$ FifiGit
> 
> Enter the name:
> ...
```

Pretty neat, eh?

To go a step further, where we can run this command from anywhere in the system and don't have to `PATH` it again and again, we can change the `~/.bash_profile` to `echo` the above commands everytime Terminal is run.

To do that, we edit the `~/.bash_profile`

```
$ open -e .bash_profile
```

This opens the file in TextEdit, now just add the following line at the end of the file

```
export PATH=$PATH":$HOME/bin"
```
Go to the home directory and source `.bash_profile` to update the changes.

```
$ cd ~
$ source .bash_profile
```

and **Voilà!**

now you can run the file from anywhere on the system by just typing `FifiGit` on your Terminal.
