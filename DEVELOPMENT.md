# Development and git Practices

Let's document some good practices!

## Commits
* Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/), preferably with the relevant [VSCode extension](https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits). Use the following scopes:
  * `driver` for driver controls.
  * `auto` for match autonomous code.
  * `odom` for odometry-related changes.
  * `compat` for changes in the VEX V5 API.
  * `config` for changes to things like ports, motor torques and speeds, etc.
  * `intake`, `hopper`, etc. for specific mechanisms.
  * `preauto` for changes to pre-match code.
* Keep commits atomic.
  * One feature, one commit. One fix, one commit. Etc.
* (Try to) keep commits working.
  * Especially on the `main` branch.
  * On other branches, at least look out for the obvious stuff even if you can't test. 
* Keep commits formatted.
  * Use the [ruff linter](https://docs.astral.sh/ruff/linter/) with the settings in [pyproject.toml](pyproject.toml). It's recommended to turn on format on save in your editor settings, but at least format before a commit.

## Branching

* The `main` branch should always have code that works.
  * All previously working features and mechanisms should continue working.
    * Unless there's a build change that stopped it from working.
  * Code shouldn't cause errors.
  * Code shouldn't break rules.
    * Unless there's a rules change that caused it.
  * Code should do all these things consistently and with regard for edge cases.
  * Code should **be tested**.
  * Merge into `main` only from `dev`, and always include a merge commit.
  * **Never commit directly to `main`.**
* The `dev` branch should have code that *should* work but is not necessarily tested.
  * This is the branch that feature or fix branches should merge into for testing.
  * Small changes that don't require branches should be made here.
* Use `feature/`, `fix/`, and `refactor/` for other branch names.
  * Always go into and from `dev`.
  * Rebase regularly to avoid big merge conflicts.
## Tagging/Versioning
* TBD with notebook versioning.