# AutoEd API

## Actors

| Actor Name | Description |
| - | - |
| editor | An instructor, TA, etc. Any user that is responsible for editing questions. Editors are an authenticated user group. |
| everyone | Any individual attempting to view the public site. Unauthenticated. |

## /question

### Description

Enables access to questions within AutoEd. Reading from this endpoint returns the question data and question template associated with a specific question. A question's ID (qid) is used to read data from a specific question.

### Access

| Actor | Allowed Operations |
| - | - |
| editor | Create, Read, Update, Delete |
| everyone | Read |

## /template

Enables access to AutoEd's Question Templates. Reading from this endpoint returns stringified HTML template data and stringified Python 3 code for auto-marking. A Question Template's ID (tid) is used to read data on a specific endpoint.

### Access

| Actor | Allowed Operations |
| - | - |
| editor | Create, Read, Update, Delete |

## /answer

Enables access to AutoEd's Answer endpoint. This endpoint serves as a location for answer submission.

### Access

| Actor | Allowed Operations |
| - | - |
| editor | Create |
| everyone | Create |
