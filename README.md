# FifiGit
> NOTE: Before we get started, you need to generate [Personal Access Token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) to access the GitHub API. Generate one and add it to the **line 8** of the code.

This is a CLI to interact with the [GitHub GraphQL API](https://docs.github.com/en/graphql) and the [GitHub REST API](https://docs.github.com/en/rest) (not anymore, but worth a mention). The core of the program is build upon Python, mainly using the [requests](https://pypi.org/project/requests/) and the [argparse](https://docs.python.org/3/library/argparse.html) library. The `request` library is used to `GET` data from the API server and import it to the Python code, while the `argparse` library is used to build the Command Line Interface, using arguement flags.

Feel free to jump to the [Installation](#install) if you want to skip over the explanation.

## GitHub REST API (discarded)
GitHub REST API can be used to create calls to get the data you need to integrate with GitHub.

Trying out a basic command, we can look at the functionality of the API

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
If you add the `-i` (`INFO`) tag we see that the `Content-Type` is `application/json`. Which implies that the returned objectafter a `GET` command will be of `json` format, this makes it easier for us to access information due to the presence of key attributes.

Using the Access token we can access Information on all (not, technically)the Repos by running the following command for a specific username
```
curl -H “Authorization: token MYTOKEN” "https://api.github.com/search/repositories?q=user:MYUSERNAME"
```
This is all we need to know about the REST API to build our CLI.

## <a name="gql">GitHub GraphQL API</a>
This is the v4.0 API used by GitHub. [GraphQL](https://docs.github.com/en/graphql) uses one endpoint `query` rather than multiple endpoint REST uses. This reduces the number of `GET` calls in the program and thus makes it faster.

I stumbled upon the APIv4.0 while looking for ways to list the topics of a Repositary (Issue #1). 

To list out the topics of a particular Repo, only GraphQL can be used as it is a Preview Feature, introduced in API v4.0. So, I had to implement this in my `--repo` flag, as Listing out of Topics of a Repo was asked.

I integrated the entire `--repo` module with this API, so only one `GET` call was required. 

Over time the entire program has migrated from the RESP API to the GraphQL API. Increasing the speed and keeping the `GET` calls clean.

I have also integrated the `uinfo` module with GraphQL to reduce query calls over followers and following sections, which would cost 3 calls on REST API. This is the query template for the same.

More information about the migration and implementations in the [Workings](#time) section.

Do try out the [GitHub Explorer](https://docs.github.com/en/graphql/overview/explorer) to visualize the nodes and the edges of the GraphQL API in real time!

## <a name="form">Introduction to the CLI </a>
To get the information from the API servers we use `post` from the `requests` module to run a targetted query.

The returned object is a `json` type one, hence navigation is easier and faster using the key attributes provided.

The interactive interface is then built on these foundations, which was then made into an Unix Executable File to run it through the Terminal.

We use `argparse` to convert the executable file into a useful Command Line Interface. To find how it works we run the following

```
$ FifiGit --help
usage: FifiGit [-h] [-u | -ub | -r REPO | -la {DESC,ASC} | -ls {DESC,ASC} | -lc {DESC,ASC} | -lu {DESC,ASC} | -lp {DESC,ASC}] name

GitHub API interface

positional arguments:
  name                  Initiates the program for the given user

optional arguments:
  -h, --help            show this help message and exit
  -u, --uinfo           Display the User Info
  -ub, --uinfo_basic    Display the basic User Info only
  -r REPO, --repo REPO  Displays the Repo Info
  -la {DESC,ASC}, --alpha_list {DESC,ASC}
                        lists all the Repos in Alpha order.
  -ls {DESC,ASC}, --star_list {DESC,ASC}
                        lists all the Repos in Stargazers order.
  -lc {DESC,ASC}, --created_list {DESC,ASC}
                        lists all the Repos in DOC order.
  -lu {DESC,ASC}, --updated_list {DESC,ASC}
                        lists all the Repos in DOU order.
  -lp {DESC,ASC}, --pushed_list {DESC,ASC}
                        lists all the Repos in DOP order.

Enjoy the program! :)
```

These are the possible flags for the interface:

* `--help` - The above help menus is shown
* `--uinfo` - It takes the argument `name` and displays the UserInfo for the respective User.
* `--uinfo_basic` - It takes the argument `name` and displayes only the basic information for the User (no follower/following)
* `--repo` - It takes 2 arguments, `name` and `REPO` and searches for the repository by that name on the User's account. If found, it displays the basic information about it.
* `--alpha_list` - It takes the argument `name` and displays the list all the Repositories sorted Alphabetically. [in ASC or DESC order]
* `--star_list` - It takes the argument `name` and displays the list all the Repositories sorted by Stargazers. [in ASC or DESC order]
* `--created_list` - It takes the argument `name` and displays the list all the Repositories sorted by Date of Creation. [in ASC or DESC order]
* `--updated_list` - It takes the argument `name` and displays the list all the Repositories sorted by Date of Update. [in ASC or DESC order]
* `--pushed_list` - It takes the argument `name` and displays the list all the Repositories sorted by Date of Last Push. [in ASC or DESC order]

Workings of each flag explained in [this](#time) section.

These 4 arguments are grouped using the `add_mutually_exclusive_group()` instance, so only one of them can be activated at a single point. (Hence the `|` in the `help` menu)

The `help` menu is filled with the following statement

```py
parser = argparse.ArgumentParser(description = "GitHub API interface", epilog = "Enjoy the program! :)")
```

### Why in Python?
The reason I chose this language over something like C++ is beacuse of the easy http connection power it possesses. `GET` commands can be used in just a single line, and playing with `json` objects is simpler too.

But...

`GET` process in general is too slow for any language, and thus acts as the Rate Limiter Command in the program. The larger the data set (`google` having over 2000 repos), the more time it takes.

## <a name="time">The Workings </a>

The entire program was first built in the REST API format, and it used to interact with the server over multiple redundant calls using `GET`.

I first implemented the GraphQL API in the commit 5b8a0b608be2248e60d6bd7798f00ac2e07ca678. At the same time saving fundamentals used in the previous state were carried forward in the current module.

Going about the different tags and the general infrastructure of the code:

### General

The fundamental of the code is to use the `argparse` tags and make queries accordingly from the GitHub GraphQL API.

The advantage of GraphQL as discussed above is that it has a single endpoint, so one complex structured call can theoretically replace thousands of REST API calls and still do the more drilled job (sorting, listing, slicing, etc.).

The migration took in steadily over commits in search f absolute clean code with the best possible query time.

### `--uinfo` and `--uinfo_basic`

The query targetted for this tag is

```js
query ($user:String!) {
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

This is the initial rate limited (`100`) query, which generates the first `100` followers/following and the basic information the user.

We Iterate the following queries using the `cursor` element to generate the complete list:

```js
query ($user:String!, $curso:String!) {
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

And then the data is extracted from the resulting `json` object. A siilar query with limited aspects is run for `--uinfo_basic`.

### `--repo`

This is a basic search operation over a given `user` and Repo `name`. The following query is run:


```js
query ($user:String!, $repo:String!) {
    user(login: $user) {
        repositories(ownerAffiliations: OWNER) {
            totalCount
        }
    }
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

This throws an `Exception` if the Repo is not found, and return the Repo details if it is. Which are then displayed to the user.

### `--list`

This is the one tag where the utility of the GraphQL comes into picture.

There are 2 major differences here:
* `MAX_CAP` at the the number of Repos is removed. (it is `1000` using the REST API)
* there is no need of sorting or different calls for different parameter sorting.

Keeping that in mind, this is the main query used for listing:

```js
query ($user:String!, $str:String!, $str2:String!) {
    user(login: $user) {
        repositories(first: 10, ownerAffiliations: OWNER, orderBy: {field: $str, direction: $str2}) {
            totalCount
            nodes {
                name
                isFork
            }
            edges {
                cursor
            }
        }
    }
}
```
where `field` and `direction` are the parameter you chose to sort the list and the order in which you want them.

I am running the final query page wise, and hence using the `cursor` again to load the next page.

To save time over this operation, I append all the last element `cursor` in a list and just use them to make the <a name = "query"> query </a> to reload the page:

```js
query ($user:String!, $str:String!, $str2:String!, $curs:String!) {
    user(login: $user) {
        repositories(first: 10, ownerAffiliations: OWNER, orderBy: {field: $str, direction: $str2}, after: $curso) {
            nodes {
                name
                isFork
            }
            edges {
                cursor
            }
        }
    }
}
```

### Conclusion
Once we the results after running the respective Queries, they are in a similar but, distinct format.

For example, running the above [query](#query) for `--list`, in a specific iteration with the given variables:

```js
{
    "user": "Fifirex"
    "str": STARGAZERS
    "str2": DESC
    "curs": "Y3Vyc29yOnYyOpIAzhP2Lcc="
}
```
This is the output:
```js
{
  "data": {
    "user": {
      "repositories": {
        "nodes": [
          {
            "name": "my-first-rep",
            "isFork": false
          },
          {
            "name": "github-slideshow",
            "isFork": false
          }
        ],
        "edges": [
          {
            "cursor": "Y3Vyc29yOnYyOpIAzhP1MMU="
          },
          {
            "cursor": "Y3Vyc29yOnYyOpIAzhMJqqM="
          }
        ]
      }
    }
  }
}
```

If I store this in a container `result`, to navigate to a specific value (say, 2nd Repo `name`), I need to use:

```py
name = result["data"]["user"]["repositories"]["nodes"][1]["name"]

# name = "github-slideshow"
```

This is all about how the code works. I might've missed a couple of points about speed computations, Graph Tangling, pagination, etc. but those were the major issues (*learnings, perhaps?*) that were faced.

Let's get to the installation now!

## <a name="install">Get the Code! </a>

> NOTE : This is a Unix Executable File, which can be run only on Unix-like OS (Linux or MacOS). For using the file on Windows, you can extract the Python core and convert it to a .exe file, and add it to the PATH in a similar fashion. 

> NOTE : For API access, we need an access token (mentioned in Section 1). Generate one and add it to the **line 8** in the code.

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
