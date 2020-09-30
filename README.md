# arXivist
arXivist is a command line interface allowing for the management of pre-print research papers and other publications 
from repositories such as arXiv on a local machine. 

![example](https://media.giphy.com/media/kKb6nsR38gzP2EAUke/giphy.gif)

## Motivation
Most search engines for research papers I am aware of are GUI based, accessed only via a web browser. As far as
I am aware, an equivalent utility for terminal environments does not exist - this project aims to fill that gap. 

The goal is to provide a comparatively powerful, accessible, and easy to use search tool for finding, storing, and 
tagging research papers from pre-publication repositories, all from the comfort of the command line on one's own 
computer.

## Installation & Set Up

#### Pre-Requisites
arXivist requires the installation of the following: 

- Command line interface which can run Bash scripts
- Git to clone the repo
- [Docker](https://docs.docker.com/get-docker/)
- [Docker-Compose](https://docs.docker.com/compose/install/)

This program was developed on Ubuntu, so other Linux distros or Mac systems shouldn't have any issues setting it up. 

Windows users will likely need to install the [Windows Subsystem for Linux](https://hackernoon.com/how-to-install-bash-on-windows-10-lqb73yj3).
and follow some [additional steps](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers) to get it setup.e

It is recommended trying some of the sample Docker and Docker-Compose examples to ensure the programs are configured correctly

#### Non-Root Access

After installing Docker and Docker-Compose, ensure they can be run [without root access](https://docs.docker.com/engine/install/linux-postinstall/)
The start up script assumes non-root access to Docker and Docker-Compose.

#### Manual Configuration

Make sure the permissions on `start.sh` are set to be executable by the current user. Something like 
`chmod 774 start.sh` should suffice.

Under `.env`, ensure the `PROGRAM_MODE` is set to `prod` and not `dev`.  

Also under `.env`, change `HOST_SAVE_DIRC` to a directory where you would like download materials to be saved. Aimed
at `~/Downloads` by default.
 
Don't touch any other variable under `.env`! 
 
#### Start Up!

To start the program for the first time, simply run `start.sh build` to set up the Docker environment and enter the 
program! This may take a moment to build.

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
alias arxivist-build='{PATH_TO_PROJECT}/start.sh build'
alias arxivist-update='{PATH_TO_PROJECT}/start.sh update'
```

Now you should be able to enter `arxivist` right into a new command line and enter the program!

#### Usage

How to use the application and what each command does should be very straightforwards from simply using the program. 
Command names are meant to be self explanatory with help commands also giving more detailed explanations.

Either way, a basic structure of the modes and commands making up the application are as follows:

- search mode
    - search for new materials to download
- view mode
    - search for previously downloaded materials to modify them
- suggest mode 
    - suggest papers based off of previously downloaded materials 

## Accreditations
Special thanks to the team managing and hosting [arXiv](arxiv.org) and the [arXiv API](https://arxiv.org/help/api/index), 
which this project would be nothing without.

Category winner from HackWitUs 2019.

## Planned Future Milestones
1. Better download setup?
1. Mass download / upload for previously downloaded papers.
1. View downloaded materials from within container
1. Integration with other pre-print sites such as bioRxiv
1. Fully separate out IO logic from input & print statements