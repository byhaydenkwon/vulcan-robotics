# Development and Git Practices

Let's document some good practices!

## Commits
* Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/), preferably with the relevant [VSCode extension](https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits). Use the following scopes:
  * `driver` for driver controls.
  * `auto` for match autonomous code.
  * `odom` for odometry-related changes.
  * `compat` for changes in the VEX V5 API.
  * `config` for changes to things like ports, motor torques and speeds, etc.
  * `intake`, `drivetrain`, etc. for specific mechanisms.
  * `preauto` for changes to pre-match code (including display).
  * `logging` for logging-related changes.
* Keep commits atomic.
  * One feature, one commit. One fix, one commit. Etc.
* Keep commits working.
  * Especially on the `main` and `dev` branches.
  * On other branches, at least look out for the obvious stuff even if you can't test. 
* Keep commits formatted.
  * Use the [ruff linter](https://docs.astral.sh/ruff/linter/) with the settings in [pyproject.toml](pyproject.toml). It's recommended to turn on format on save in your editor settings, but at least format before a commit.

## Branching

* The `main` branch should always have code that works and can be relied upon in a competitive match.
  * All previously working features and mechanisms should continue working.
    * Unless there's a build change that stopped it from working, in which case it should be fixed as soon as possible.
  * Code shouldn't cause errors.
  * Code shouldn't break rules.
    * Unless there's a rules change that caused it, in which case it should be fixed as soon as possible.
  * Code should do all these things consistently and with regard for edge cases.
  * Code should **be tested** (meaning the entire robot as a whole).
  * Merge into `main` only from `dev`, and always include a merge commit.
  * **Never commit directly to `main`.**
* The `dev` branch should have code that *should* work (and has been feature-tested) but has not necessarily been tested with the full system for all edge cases.
  * This is the branch that feature or fix branches should merge into for testing.
  * Small changes that don't require branches should be made here.
* Use `feature/`, `fix/`, and `refactor/` for other branch names.
  * Always go into and from `dev`.
  * Rebase regularly to avoid big merge conflicts.
## Tagging/Versioning
* TBD with notebook versioning.

## Import Order
1. Standard library imports.
2. `from vex import *`.
3. Imports from other external libraries.
4. Imports from `utils/`.
5. Imports from `mechanisms/`.
6. *(main.py only)* Imports from `control/`.

Each numbered group should be separated by a line. Use `from some_file import SomeClass` for all internal files. Do not use wildcard imports at all unless it's `from vex import *`.
