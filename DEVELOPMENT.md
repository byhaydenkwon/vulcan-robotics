# Development and Git Practices

## Strange Setup Workarounds
*This section is Linux-only.*  

This is less than ideal, but it'll work. Basically,
```
pros build-compile-commands
```
really, really doesn't want to work on its own. The best workaround I've found is to install [Bear](https://github.com/rizsotto/Bear) and use `bear -- pros make all`; however, this leads to issues with the standard library headers not being recognized. To set this up correctly, there is a bit of strangeness we must work with.

The workaround is to put paths in `.clangd`, like so:
```
CompileFlags:
  Add:
    - -I/home/undonepotato/.config/VSCodium/User/globalStorage/sigbots.pros/install/pros-toolchain-linux/arm-none-eabi/include/c++/13.3.1
    - -I/home/undonepotato/.config/VSCodium/User/globalStorage/sigbots.pros/install/pros-toolchain-linux/arm-none-eabi/include/c++/13.3.1/arm-none-eabi
```
In general, your path will be:
```
~/.config/VSCode/User/globalStorage/sigbots.pros/install/pros-toolchain-linux/arm-none-eabi/include/c++/(your version number)
```
Replace `~` with your home path and `(your version number)` with the version number you find in that directory, then add this to `.clangd.disabled`:
```
CompileFlags:
  Add:
    -I(your path here)
    -I(your path here)/arm-none-eabi
```

Rename the file to `.clangd`, and you should be ready to go. Do not commit this file to version control.


## Commits
* Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/), preferably with the relevant [VSCode extension](https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits). Use the following scopes:
  * `driver` for driver controls.
  * `auto` for match autonomous code.
  * `odom` for odometry-related changes.
  * `compat` for changes in the VEX V5 API.
  * `config` for changes to things like ports, motor torques and speeds, etc.
  * `scoring`, `drivetrain`, etc. for specific mechanisms.
  * `preauto` for changes to pre-match code (including display).
  * `logging` for logging-related changes.
* Keep commits atomic.
  * One feature, one commit. One fix, one commit. Etc.
* Keep commits working.
  * Especially on the `main` and `dev` branches.
  * On other branches, at least look out for the obvious stuff even if you can't test. 
* Keep commits formatted.
  * For Python: use the [ruff linter](https://docs.astral.sh/ruff/linter/) with the settings in [pyproject.toml](pyproject.toml). It's recommended to turn on format on save in your editor settings, but at least format before a commit.
  * For C++: Use [clangd](https://clangd.llvm.org), for example with the VSCode extension. It should recognize the project's .clang-format.

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
