# arXivist
arXivist is a terminal environment allowing for the management of pre-print papers from arXiv on a local machine. 

## Motivation
Most search engines for research papers I am aware of are GUI based, usually accessed only via a web browser. As far as
I am aware, an equivalent utility for terminals does not exist. This project aims to fill that gap as a comprehensive, 
easily set up utility for finding, storing, and tagging research papers from pre-print sites, from the 
comfort of the command line.

## Installation
arXivist is built on top of Bash, Docker, and Docker-Compose - any system that has these installed should be 
able to build and enter the utility simply by running `start.sh`. I assume any Linux or Mac system shouldn't have any 
issues, but assume Windows users will likely need to install the Windows Subsystem for Linux to run the Bash scripts.

Make sure the permissions on the Bash scripts are set to be executable, and that the current user has non-root access to 
Docker (don't recommend running the utility as sudo).  
 
A more detailed installation guide will be made in the future.
 
## Accreditations
Special thanks to the team managing and hosting [arXiv](arxiv.org) and the [arXiv API](https://arxiv.org/help/api/index), 
which this project would be nothing without.

Category winner from HackWitUs 2019.