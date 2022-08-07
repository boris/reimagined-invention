# Reimagined Invention
New generation of [the book inventoy](https://books.lenore.me).

## Requirements:
- Python 3.9.10 in a venv `reimagined-invention`

## Design patterns
This project will be developed usign a [functional
structure](https://exploreflask.com/en/latest/blueprints.html#functional-structure)
to organize the files of the project according to what they do. This means that
templates are grouped together in one directory, static in another and views in
a third (copy/paste from Flask documentation).

### DB relationships:

 _Author -> Book_ should be a many-to-many relationship as multiple authors can
share the ownership of a book.

For example, authors A and B wrote the book X. When listing all the books
written by author A, book X must appear in the results. Likewise when
listing the books written by author B.

If we want to use a one-to-one relationship, the book X should only be
returned as part of the results if we search by "the books written by author
A **and** author B" working together.

## Usage
```
flask --app app --debug run
flask --app app --debug db migrate
flask --app app --debug db upgrade
```
