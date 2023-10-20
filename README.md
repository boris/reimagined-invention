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

 **Author -> Book** should be a many-to-many relationship as multiple authors can
share the ownership of a book.

For example, authors A and B wrote the book X. When listing all the books
written by author A, book X must appear in the results. Likewise when
listing the books written by author B.

If we want to use a one-to-one relationship, the book X should only be
returned as part of the results if we search by "the books written by author
A **and** author B" working together.

See [PR/3](https://github.com/boris/reimagined-invention/pull/3) for
documentation about v0.1.0 release.

## Usage
Create an empty `.env_vars` file. If you want to take advantage of the Makefile,
update it with the following content:
```
CF_TUNNEL=some_token
MYSQL_ROOT_PASSWORD=some_password
```
Create a `config.yaml` out of `config.yaml.example` and update the values. Then:
```
flask --app app --debug db migrate
flask --app app --debug db upgrade
flask --app app --debug run
```

## Sample DB
Sample DB has been added. On mysql create a new DB and restore using the dump.

## Suggestions
- Use [Cloudflare Tunnels](https://www.cloudflare.com/products/tunnel/)
