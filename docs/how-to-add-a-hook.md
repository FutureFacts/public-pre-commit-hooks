# How to add a new custom pre-commit hook

The recipe is quite simple. It requires a few things:

- **Create a new branch.**
- An CLI executable python script.
  - Add it to `./pre_commit_hooks/your_script.py`
  - See `./pre_commit_hooks/check_sqlfluff.py` for inspiration.
- Make sure it can be run after installing `poetry install`
  - Place all the script's dependencies in `pyproject.toml`
- Preferably make the python script available as a script.
  - Add a CLI script entry in `[tool.poetry.scripts]` in `pyproject.toml`
- Add your new hook or all new hooks that can be run based on your new script in: `.pre-commit-hooks.yaml`
  - The `entry` of the hook should connect to the script you've made.
  - Fill in all other hook fields
    - `id`: Unique identifier. Use lowercase letters, numbers and dashes.
    - `name`: Short name.
    - `description`: One line description.
    - `entry`: the command to run.
    - `language`: python
      - If your script is also a python script.
    - `types`: list of filetypes you want to pass to your hook.
  - For complete list of possible arguments: <https://pre-commit.com/#new-hooks>
- Test your script.
  - Locally by calling the python script directly: `python ./pre_commit_hooks/your_script.py`
  - Locally via Poetry: `poetry run your_script`
    - This is what you've put in `[tool.poetry.scripts]`
  - Locally via pre-commit: `pre-commit try-repo . your-script-hook --files ./your-test-file`
    - This is where you test the hook that you've put in `.pre-commit-hooks.yaml`
- **Create a PR to the `main` branch**
  - Preferably, ask for a review.
