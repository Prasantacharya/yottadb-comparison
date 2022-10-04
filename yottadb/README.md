How to build:

`docker pull yottadb/yottadb-debian:latest-master`

How to run:

`docker run -it --rm -v $(pwd)/db:/data yottadb/yottadb-debian:latest-master`

you will then be in a TTY where you can run `python3 test.py`