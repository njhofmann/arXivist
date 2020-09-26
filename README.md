# arXivist
arXivist is a terminal environment allowing for the management of pre-print papers from sites such as arXiv on one's 
local machine. 

## Motivation
Most search engines for research papers I am aware of are GUI based, accessed only via a web browser. As far as
I am aware, an equivalent utility for terminal environments does not exist - this project aims to fill that gap. 

The goal is to provide a comparatively powerful, accessible, and easy to use search tool for finding, storing, and 
tagging research papers from pre-print sites, all from the comfort of the command line.

## Installation & Set Up
#### Pre-Requisites
arXivist requires the installation of the following: 

- Command line interface which can run Bash scripts
- Git to clone the repo
- [Docker](https://docs.docker.com/get-docker/)
- [Docker-Compose](https://docs.docker.com/compose/install/)

Linux distros or Mac systems shouldn't have any issues running Bash scripts. Windows users will
 likely need to install the [Windows Subsystem for Linux](https://hackernoon.com/how-to-install-bash-on-windows-10-lqb73yj3).

It is recommended trying some of the sample Docker and Docker-Compose examples to ensure the programs are configured correctly

TODO add gif example here

#### Non-Root Access

After installing Docker and Docker-Compose, ensure they can be run [without root access](https://docs.docker.com/engine/install/linux-postinstall/)
The start up script assumes non-root access to Docker and Docker-Compose.

#### Manual Configuration

Make sure the permissions on `start.sh` are set to be executable by the current use. Something like 
`chmod 774 start.sh` should suffice.

Under `.env`, ensure the `PROGRAM_MODE` is set to `prod` and not `dev`.  

Also under `.env`, change `HOST_SAVE_DIRC` to a directory where you would like download materials to be saved. 
 
Don't touch any other variable under `.env`! 
 
#### Start Up!

To start the program for the first time, simply run `start.sh build` to set up the Docker environment and enter the 
program! 

After being build for the first time, any subsequent attempts to enter the program can be done with `start.sh`! If the 
underlying Docker containers are removed or one fails to enter the program again, simply try rebuilding with 
`start.sh build` again!

#### Updating

In updating the program, it is assumed the program was installed with git - with a link to the remote Github repo under
the default `origin` name. In addition, that the local `master` branch has an upstream connection to the remote `master`
branch.

So to check for any updates directly from GitHub - run `start.sh update`. This will automatically pull down any updates 
on the remote master branch and rebuild the Docker environment.

#### Setting Up Shortcuts

After setting up the program for the first time, it is recommended adding the following [custom commands](https://dev.to/mollynem/4-simple-steps-for-custom-bash-commands-4c58) 
to one's Bash profile for ease of use. `{PATH_TO_PROJECT}` is the path to the directory where this project lives. 

```
alias arxivist={PATH_TO_PROJECT}/start.sh
alias arxivist-build={PATH_TO_PROJECT}/start.sh build
alias arxivist-update={PATH_TO_PROJECT}/start.sh update
```

Now you should be able to enter `arxivist` right into a new command line and enter the program!
 
## Accreditations
Special thanks to the team managing and hosting [arXiv](arxiv.org) and the [arXiv API](https://arxiv.org/help/api/index), 
which this project would be nothing without.

Category winner from HackWitUs 2019.
