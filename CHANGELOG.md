# Changelog:


## Unreleased
+ Migrated to Github Actions for CI.
+ Removed support for Python 3.7 and below.
+ Added pyproject.toml
+ Added pre-commit config.
+ Purged all IP, deleted git history, make project public.
+ Moved dependencies to pyproject.toml
+ Switched from `green` to `pytest` for test runner.
+ Moved to a `src` dir structure like all my other projects.
+ Linted project.
+ Ran `black` on entire project.
+ Updated `README.md`.
+ Added type annotations to most everything.
+ Made `Die` a dataclass and started migrating API to use that instead of tuples.
+ Tests were migrated from `unittest` to `pytest`.
+ Migrated the die "state" strings to an enum.
+ Removed some dead/unused code.
+ Refactored a `count_by_state` function and cleaned things up a bit.


## 0.1.3 / 2017-03-15
+ Documentation is now automagically built on every tag and uploaded to
  the internal documentation server.
+ Significant overhaul of docstrings for formatting and content.


## 0.1.2 / 2017-02-17
+ Fixed CI to search for .zip files.


## 0.1.1 / 2017-02-17
+ Updated CI for auto-deploy (!2)


## 0.1.0 / 2016-04-17
+ Initial Release


## 0.0.1 / 2016-04-17
+ Project Creation (from GDWCalc.gdw)
