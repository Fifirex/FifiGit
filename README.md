# FifiGit
This is a CLI to interact with the [GitHub REST API](https://docs.github.com/en/rest) and the [GitHub GraphQL API](https://docs.github.com/en/graphql). The core of the program is build upon Python, mainly using the [requests](https://pypi.org/project/requests/) and the [argparse](https://docs.python.org/3/library/argparse.html) library. The `request` library is used to `GET` data from the API server and import it to the Python code, while the `argparse` library is used to build the Command Line Interface, using arguement flags.

Feel free to jump to the [Installation](#install) if you want to skip over the explanation.

## GitHub REST API
GitHub REST API can be used to create calls to get the data you need to integrate with GitHub.

Trying out a basic command, we can look at the functionality of the API

```cmd
$ curl https://api.github.com/Fifirex

> {
> "login": "Fifirex",
> "id": 75205458,
> "node_id": "MDQ6VXNlcjc1MjA1NDU4",
> "url": "https://api.github.com/users/Fifirex",
> ...
> }
```

If you add the `-i` (`INFO`) tag we see that the `Content-Type` is `application/json`. Which implies that the returned objectafter a `GET` command will be of `json` format, this makes it easier for us to access information due to the presence of key attributes.

This can be used to access User information and Public Repositaries from GitHub. To access Private Repos and more info on the user, we can generate a [Personal Access Token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) with valid scopes to access the respective data.

Using the Access token we can access Information on all the Repos by running the following command for a specific username

```cmd
curl -H “Authorization: token MYTOKEN” "https://api.github.com/search/repositories?q=user:MYUSERNAME"
```

This is all we need to know about the REST API to build our CLI.

## <a name="gql">GitHub GraphQL API</a>
This is the v4.0 API used by GitHub. [GraphQL](https://docs.github.com/en/graphql) uses one endpoint `query` rather than multiple endpoint REST uses. This reduces the number of `GET` calls in the program and thus makes it faster.

To list out the topics of a particular Repo, only GraphQL can be used as it is a Preview Feature, introduced in API v4.0. So, I had to implement this in my `--repo` flag, as Listing out of Topics of a Repo was asked. 

I integrated the entire `--repo` module with this API, so only one `GET` call was required, with the following query structure

```js
query ($repo: String!, $user: String!){
    repository(name: $repo, owner: $user) {
        licenseInfo {
            key
            name
            url
            spdxId
        }
        isFork
        isPrivate
        forks {
            totalCount
        }
        stargazers {
            totalCount
        }
        watchers {
            totalCount
        }
        repositoryTopics(first: 100) {
            nodes {
                topic {
                    name
                }
            }
        }
    }
}
```
I have also integrated the `uinfo` module with GraphQL to reduce query calls over followers and following sections, which would cost 3 calls on REST API. This is the query template for the same

```js
query ($user: String!){
  user(login: $user) {
    name
    avatarUrl
    url
    email
    bio
    followers(first: 100) {
      nodes {
        login
      }
      totalCount
      edges {
        cursor
      }
    }
    following(first: 100) {
      nodes {
        login
      }
      totalCount
      edges {
        cursor
      }
    }
  }
}
```
To counter the limitation over rate limitation of `100`, I used two more query templates using the `cursor` of the last call's last element. This iterates over all the followers/following users.

```js
query ($repo: String!, $curso: String!){
  user(login: $user) {
    followers(first: 100, after: $curso) {
      nodes {
        login
      }
      edges {
        cursor
      }
    }
  }
}
```

The reason I did not use this API throughout the CLI (mainly the `--list` and `--sort_list` sections) is that it has a [rate limitation](https://docs.github.com/en/graphql/overview/resource-limitations) over the `first` parameter of `100`. Hence, Repos more than `100` cannot be enquired in a single query, which limits the functionality by a factor of `10` (maximum count in REST API is `1000`).

[Substantial efforts](#time) were then made to make the REST API `GET` the most effective.

## <a name="form">Building the CLI </a>
To get the information from the API servers we use `GET` from the `requests` module.

For example, for a given `user` we use

```py
auth = {'Authorization':"token " + Token_Name}
data = requests.get (f"https://api.github.com/users/{user}", headers = auth).json()
```

`data` is the response `json` object, through which the data is extracted using the key attributes.

The interactive interface is then built on these foundations, which was then made into an Unix Executable File to run it through the Terminal.

We use `argparse` to convert the executable file into a useful Command Line Interface. To find how it works we run the following

```cmd
$ FifiGit --help
usage: FifiGit [-h] [-u | -ub | -r REPO | -l | -ls] name

GitHub API interface

positional arguments:
  name                  Initiates the program for the given user

optional arguments:
  -h, --help            show this help message and exit
  -u, --uinfo           Display the User Info
  -ub, --uinfo_basic    Display the basic User Info only
  -r REPO, --repo REPO  Displays the Repo Info
  -l, --list            Display all the Repo Names
  -ls, --sort_list      Display all the Repo Names sorted in Alpha

Enjoy the program! :)
```

These are the possible flags for the interface:

* `--help` - The above help menus is shown
* `--uinfo` - It takes the argument `name` and displays the UserInfo for the respective User.
* `--uinfo_basic` - It takes the argument `name` and displayes only the basic information for the User (no follower/following)
* `--repo` - It takes 2 arguments, `name` and `REPO` and searches for the repository by that name on the User's account. If found, it displays the basic information about it.
* `--list` - It takes the argument `name` and displays the list all the Repositories under the User Account.
* `--sort_list` - It takes the argument `name` and displays the list all the Repositories sorted Alphabetically.

Workings of each flag explained in [this](#time) section.

> Note: GitHub API restricts repo search results to the first `1000`, there is a warning thrown if `total_count > 1000`, as all the Repos cannot be listed or searched, in case of a huge Repo Base. 

These 4 arguments are grouped using the `add_mutually_exclusive_group()` instance, so only one of them can be activated at a single point. (Hence the `|` in the `help` menu)

The `help` menu is filled with the following statement

```py
parser = argparse.ArgumentParser(description = "GitHub API interface", epilog = "Enjoy the program! :)")
```

### Why in Python?
The reason I chose this language over something like C++ is beacuse of the easy http connection power it possesses. `GET` commands can be used in just a single line, and playing with `json` objects is simpler too.

But...

`GET` process in general is too slow for any language, and thus acts as the Rate Limiter Command in the program. The larger the data set (`google` having over 2000 repos), the more time it takes.

## <a name="time">Countering the Time delay </a>

The one major boost in speed was achieved after `--list` was made page-wise, where only 10 results are displayed at a time. A `goto` feature is also added to the flag for easier navigation.

This snippet shows how the time boost is acieved for a huge repo base like `google` ( `2006` owned repos)

```cmd
$ FifiGit google -l

 =============================
           REPO INFO
       unforked only  :)
 =============================

 Total count : [2006]
 Warning: API limits search to first 1000 results only (100 pages)

 Page: 1 of 100
 * material-design-icons
 * guava
 * material-design-lite
 * styleguide
 * leveldb
 * googletest
 * iosched
 * gson
 * python-fire
 * web-starter-kit

 Next Page? (y/n/goto(g)): 
```

The `--repo` tag has been modified a lot to reduce the time taken in searching the Repos. This was done by pre loading Repositaries, and increasing the `per_page` to its maximum (`100`) while searching. 

This implies that while searching on a full repo base (`1000 repos`), it would only take `10` `GET` commands in the worst case scenario. And by pre loading the pages and searching, the probability of hitting the worst case is reduced. 

The worst case scenario time was measured by searching a non-existent Repo at `google`

```cmd
$ FifiGit google -r hi

 =============================
           REPO INFO
       unforked only  :)
 =============================

 Total count : [2006]
 Warning: API limits search to first 1000 results only (1006 Repos will be missed)

 Proceed, dispite the Warning? (y/n): y

 Repo not found
 Hint: you must own the repo (not forked)
 Hint: the repos exceeded API limit, so it must've missed there

 Time Taken: 22.84958250471863 seconds
```

This time is the worst case time, and is a marvelous improvement over the previous times.

Another major improvement in the time delay was done by switching over to GraphQL for `--uinfo` and `--repo` modules, as they require less number of calls due to a single end point nature of the query. The query formats can be seen in the [GraphQL](#gql) section.

>WARNING: Using the --sort_list tag is a major hitting on your machine if the Repo base is huge. As the entire base must be sorted to display even a small portion of it. Use it only if absolutely necessary.

## <a name="install">Get the Code! </a>

> Note : This is a Unix Executable File, which can be run only on Unix-like OS (Linux or MacOS). For using the file on Windows, you can extract the Python core and convert it to a .exe file, and add it to the PATH in a similar fashion. 

> Note : For API access, we need an access token (mentioned in Section 1). Generate one and add it to the **line 7** in the code. 

First, we need th code. Clone the repository into a Directory of your choice using

```cmd
git clone https://github.com/Fifirex/KOSS-Selections-API.git
```

Once we have the executable file, just typing `./FifiGit` while in the Directory will run the program. To make it a true CLI, we need meddle with the `$PATH`.

First, make a temporary `bin` which will then be added to the `PATH`

```cmd
$ mkdir -p ~/bin
$ cp FifiGit ~/bin
$ export PATH=$PATH":$HOME/bin"
```

This creates a copy of the file in the `$PATH` and now you can run it by just,

```cmd
$ FifiGit Fifirex -u
> 
> ...
```

Pretty neat, eh?

To go a step further, where we can run this command from anywhere in the system and don't have to `PATH` it again and again, we can change the `~/.bash_profile` to `echo` the above commands everytime Terminal is run.

To do that, we edit the `~/.bash_profile`

```cmd
$ open -e .bash_profile
```

This opens the file in TextEdit, now just add the following line at the end of the file

```cmd
export PATH=$PATH":$HOME/bin"
```
Go to the home directory and source `.bash_profile` to update the changes.

```cmd
$ cd ~
$ source .bash_profile
```

and **Voilà!**

now you can run the file from anywhere on the system by just typing `FifiGit` with the [format](#form) mentioned above on your Terminal.
