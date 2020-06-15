* add docs to existing codebase
* refactor existing codebase
* set up docker integration
    * how does app connect to db
    * set up volume for app, where to download pdfs
    * set up volumes for db, load script and store data
    * set up default pdf viewer
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
* program start, load database enums as environmental variables
    * separate files
    * constants for important names, after loaded into environ, getter functions
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