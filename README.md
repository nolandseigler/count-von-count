# count-von-count
Finds the largest number in a pdf document. Supports a test endpoint or upload your own file.

## Prerequisites

1. Make
1. curl
1. pdf file
1. docker or poetry with python 3.12 installed

Make is used for easy command running. If you do not have make installed you can copy and paste the commands into your terminal

To exercise the counter you will need a pdf file. The application was developed using this file: `https://www.saffm.hq.af.mil/Portals/84/documents/FY25/FY25%20Air%20Force%20Working%20Capital%20Fund.pdf?ver=sHG_i4Lg0IGZBCHxgPY01g%3d%3d`.

## Setup
For a quick setup using the file above run:
```
make download-test
```


## Run Docker

The simplest way to run this is in docker run:

```
make run-docker
```

## Run Local Host

This step requires poetry and python 3.12 or greater installed and on path.

Run

```
make install
make dev
```

## Use the app

### Test Mode

1. This url http://127.0.0.1:8000/api/v1/count/test will use the hardcoded test pdf to return the count response.
1. You may also upload your own pdf. This example uses the same test file.

```
make test-upload
```

