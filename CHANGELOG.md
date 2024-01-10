# CHANGELOG



## v0.1.1 (2024-01-09)

### Chore

* chore: use forked python-semantic-release running on Python 3.12 ([`1d3ba5f`](https://github.com/luuuis/pyomie/commit/1d3ba5fe2a5b243b1b263a04f4ca28b04089ce9c))

### Ci

* ci: use luuuis/python-semantic-release running on Python 3.12 (#7) ([`2aba05e`](https://github.com/luuuis/pyomie/commit/2aba05e473ecb9405b00eb5fd02f3b0bbab9985c))

* ci: use GitHub setup python action to ensure correct version ([`d0a2dea`](https://github.com/luuuis/pyomie/commit/d0a2dea8946f82e0b36251644809a638ba168503))

* ci: use forked upload-to-gh-release with Python 3.12

upstream uses Python 3.10, which this project does not support any more. ([`92b1e44`](https://github.com/luuuis/pyomie/commit/92b1e4486582c02b11be6ca86b5fc862566c9f95))

### Fix

* fix: rework lib to add static typing info (#6)

This is a breaking change but not applying semver since we&#39;re still in 0.x.

* fix: reworked the whole lib, use NamedTuple for returned data
* ci: python &gt;= 3.11 ([`1527fc1`](https://github.com/luuuis/pyomie/commit/1527fc12b532f0ba6fb5af6991698dfbed43f7bb))


## v0.1.0 (2024-01-07)

### Ci

* ci: include ci and chore in release notes (#4) ([`7796dfd`](https://github.com/luuuis/pyomie/commit/7796dfd22904f82b3db05a473321cd4336116e21))

### Feature

* feat: adds ability to fetch marginal and (historical) adjustment prices (#5)

* feat: adds ability to fetch marginal price and adjustment price (historical)

* includes a CLI with the ability to output either in JSON or the (unparsed) CSV response

* adds tests for CLI and two main entry points, diffs the response

* ci: set minimum python version to 3.10 ([`41a4b38`](https://github.com/luuuis/pyomie/commit/41a4b386cd77c7d72e5b633d051cb4da75c7cc5d))


## v0.0.0 (2024-01-04)

### Chore

* chore: prep for v0.0.1 (#1)

* chore: initial commit by @browniebroke/pypackage-template

* docs: add @luuuis as a contributor ([`2edc411`](https://github.com/luuuis/pyomie/commit/2edc411a176d877a64cf03749ed92423c15b5b86))

### Ci

* ci: remove CHANGELOG.md.j2 in favour of the built-in template (#3) ([`362d6e3`](https://github.com/luuuis/pyomie/commit/362d6e366d4e917a0130ef6106555b10fe150728))

* ci: adds poetry.lock (#2) ([`1ac64fe`](https://github.com/luuuis/pyomie/commit/1ac64fe11d65ecac892dfef7b13deb8e23f06a16))

### Unknown

* Initial commit ([`b450379`](https://github.com/luuuis/pyomie/commit/b450379baa88e9ed9534a7ee839d1f57b629533c))

