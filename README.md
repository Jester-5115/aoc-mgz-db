# Age of Empires II Recorded Game Database

Store and query recorded game metadata.

## Features

- Add by file, match, series, or csv (in parallel)
- Tag matches
- Supplement with Voobly player data
- Detect duplicates
- Detect player perspectives of the same match
- Detect incomplete matches
- CLI and API
- Compresses stored files (~5% of original size)

# Setup

- Install and configure a relational database supported by [SQLAlchemy](https://docs.sqlalchemy.org/en/latest/dialects/)
- Determine [database connection url](https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)
- Ensure SSH key pair connectivity to storage host

## Environmental Variables

Avoid passing credentials and connection information while using the CLI by setting the following environmental variables:

- `MGZ_DB`: database connection url
- `MGZ_STORE_HOST`: hostname of file storage (\[user@\]host\[:port\])
- `MGZ_STORE_PATH`: file system path for storage

Optional:

- `VOOBLY_KEY`: voobly api key
- `VOOBLY_USERNAME`: voobly username
- `VOOBLY_PASSWORD`: voobly password

# Relationship Diagram

![Relationship Diagram](/docs/schema.png?raw=true)

# Examples

## Adding

```bash
mgzdb add file rec.20181026-164339.mgz
mgzdb add match https://www.voobly.com/match/view/18916420
mgzdb add series "135406198-NAC2Q1 GrandFinal F1Re vs BacT.zip"
mgzdb add csv matchDump.csv
```

When adding a series, the filename is used as the series name. Optionally prepend the name with a Challonge match ID.

## Querying

```bash
mgzdb query file 1
mgzdb query match 1
mgzdb query series 1
mgzdb query summary
```

## Removing

```bash
mgzdb remove --file 1
mgzdb remove --match 1
mgzdb remove --series 1
```

## Tagging

```bash
mgzdb tag 1 drush
```
