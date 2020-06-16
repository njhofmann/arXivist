* refactor existing codebase
    * unified env file
    * distinguish between program and user entries in console
    * rework mode loops
    * redo how command enums are done
* set up docker integration
    * set up volumes
    * postgres port
    * port to web
* fix search query, all option
* separate out IO from logic
* keyword args for search
* removal options
    * remove keyword
    * remove added paper
* clear previously displayed text
* dump / reload database
* keyword args
    * add keyword args to existing
    * add keyword args before saving
* add support for other pre-print repos
    * bioRxiv
    * chemRxiv
    * psyArxiv
    * socArxiv
* steps to publish as library or fully fledged app
    * versioning
* separate out io for testing and prod

1. docker
    1. get containers w/o volumes
    1. add volumes 
    1. set up env file
    1. get rid of db_init? container does that?
        1. postgres volume with setup? init creating tables if don't exist?

1. Redo init-db method