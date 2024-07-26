# Project Name

## Overview

This project uses FastAPI for building a web application with a GraphQL API. 

## Sample Queries

Queries all tables in the database

```
query AllCases {
  allCases {
    id
    number
    jurisdiction
  }
  allDocuments {
    status
    text
    title
  }
  allPeople {
    name
    contactInfo
  }
}
```

Creates a case

```
mutation AddCase($number: String!, $jurisdiction: String!) {
  addCase(number: $number, jurisdiction: $jurisdiction) {
    id
    number
  }
}
```

Add a document to a case

```
mutation AddDocument(
  $caseId: String!
  $text: String!
  $title: String!
  $type: String!
  $status: String!
) {
  addDocument(
    caseId: $caseId
    text: $text
    title: $title
    type: $type
    status: $status
  ) {
    id
  }
}
```

Gets a case and the documents

```
query getCase($caseId: String) {
  getCase(caseId: $caseId) {
    id
    number
    documents {
      id
      text
      title
    }
    jurisdiction
  }
}
```

## Makefile Targets

To start the project

Create a virtual environment

```sh
virtualenv venv
source venv/bin/activate 
```


The `Makefile` in this project helps to streamline common tasks such as running the application, running tests, cleaning up files, and installing dependencies.

`make install`  To install all necessary dependencies

`make run`      To run the web application

`make browse`   To open the GUI to test the API

`make dev`      To install the dependencies for development

`make tests`    To run the tests



### Variables

- `APP_MODULE`: Specifies the module path for the FastAPI application, default is `app.main:app`.
- `HOST`: The host address for the FastAPI application, default is `0.0.0.0`.
- `PORT`: The port for the FastAPI application, default is `8000`.
- `ENV_FILE`: The environment file containing environment variables, default is `.env`.
- `PROJECT_DIR`: The directory where the project is located, default is the current working directory.


