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

## Usage
```
flask --app app --debug run
flask --app app --debug db migrate
flask --app app --debug db upgrade
```
