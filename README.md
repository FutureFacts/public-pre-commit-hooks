# Future Facts' Public Pre-commit Hooks

Some public pre-commit hooks that Future Facts shares with the world.

## Hooks

### check-sqlfluff-format

Formats all files via `sqlfluff format` CLI command.

This hook requires you to have a `.sqlfluff` file in the root of your repo to configure `sqlfluff` tool.

### check-sqlfluff-parse

Checks if all files can be parsed via `sqlfluff parse` CLI command.

This hook requires you to have a `.sqlfluff` file in the root of your repo to configure `sqlfluff` tool.

## How to use

Just add one or both of these hooks to your repo.

```yml
repos:
  - repo: https://github.com/FutureFacts/public-pre-commit-hooks
    rev: v1.0.1
    hooks:
      - id: check-sqlfluff-parse
      - id: check-sqlfluff-format
```

## Contributing

If you would like to create a new pre-commit hook. If you are a Future Facts employee feel free to do so.
If you are from outside the company you can create a fork and then a pull-request from your fork.

Getting started with this repo is easy:

- clone
- `poetry install`
- `pre-commit install`
  - Not added as a dev dependency.

Read the [how-to-add-a-hook.md](docs/how-to-add-a-hook.md) document to see how you can add a new hook.

## Why a custom check-sqlfluff hook

This pre-commit hook is a more lightweight simple variant of the standard `sqlfluff-fix` and `sqlfluff-lint` hooks provided by SQLFluff: <https://docs.sqlfluff.com/en/latest/production/pre_commit.html>
The reason this new hook has been build is the following

- In an existing codebase a lot of the SQL code might not be without linting/formatting violations.
  - So doing `sqlfluff-lint` will cause too many violations.
- Auto formatting is different then auto-fixing.
  - `sqlfluff-fix` attempt to fix all rule violations.
  - The command line `sqlfluff format` only fixes a stable set of of formatting violations.
    - <https://docs.sqlfluff.com/en/stable/reference/cli.html#sqlfluff-format>
  - I've observed that `sqlfluff fix` CLI or the pre-commit hook `sqlfluff-fix` can cause SQL code to not be 'backwards-compatible' after the fix.
    - Some fixes changed the column order of tables or views or renamed column names. These changes can be harmful in an existing codebase.
- The default SQLFluff pre-commit hooks don't check for parseability.
  - The CLI `sqlfluff parse` can check if a file can be parsed by `sqlfluff`.
  - This check is quite helpful and can catch a lot of syntax errors.

This custom SQLfluff pre-commit hook works without any setup and runs `sqlfluff` as if you are using it as a command-line tool.
This makes it very easy to verify issues manually if you also have `sqlfluff` installed locally.

Read more on SQLFluff: <https://github.com/FutureFacts/knowledge-base/blob/main/tooling/sqlfluff.md>
