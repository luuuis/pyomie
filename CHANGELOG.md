# CHANGELOG


## v1.1.3 (2025-11-07)

### Bug Fixes

- Typerargument.make_metavar() takes 1 positional argument but 2 were given
  ([#29](https://github.com/luuuis/pyomie/pull/29),
  [`63f3ce5`](https://github.com/luuuis/pyomie/commit/63f3ce54e68d4f57a423e0c628a24b27a3f1313c))


## v1.1.2 (2025-11-07)

### Bug Fixes

- Typerargument.make_metavar() takes 1 positional argument but 2 were given
  ([#28](https://github.com/luuuis/pyomie/pull/28),
  [`60f6f3f`](https://github.com/luuuis/pyomie/commit/60f6f3f7a0e26705dbaccd209310971b6039f760))

fix: pin click version <8.2.0


## v1.1.1 (2025-11-07)

### Bug Fixes

- Raise Exception for HTTP errors, no longer return None
  ([#27](https://github.com/luuuis/pyomie/pull/27),
  [`a72e96b`](https://github.com/luuuis/pyomie/commit/a72e96bebb80c5b206947ed01d4fcd9d3e1ec0c6))

### Chores

- Improvements to README ([#26](https://github.com/luuuis/pyomie/pull/26),
  [`e949e22`](https://github.com/luuuis/pyomie/commit/e949e22d663c06f4437b24aff4af8d722dcae930))


## v1.1.0 (2025-11-05)

### Chores

- Downgrade typer version for Home Assistant compatibility
  ([#24](https://github.com/luuuis/pyomie/pull/24),
  [`667cb9f`](https://github.com/luuuis/pyomie/commit/667cb9fe227a8dada34f4d24799cee407e2d3878))

### Features

- Add lib logging and --verbose option ([#25](https://github.com/luuuis/pyomie/pull/25),
  [`9c86fe0`](https://github.com/luuuis/pyomie/commit/9c86fe0048922f81bf21465c79cca9576f6dddce))


## v1.0.2 (2025-11-02)

### Bug Fixes

- "secondary flag is not valid for non-boolean flag"
  ([#23](https://github.com/luuuis/pyomie/pull/23),
  [`904d106`](https://github.com/luuuis/pyomie/commit/904d1061602108d39375782b476d48dc0f0823f8))


## v1.0.1 (2025-10-02)

### Bug Fixes

- Reintroduced util.localize_quarter_hourly_data ([#21](https://github.com/luuuis/pyomie/pull/21),
  [`0b42859`](https://github.com/luuuis/pyomie/commit/0b4285927cbe2a50d52645e8521c4ee35b49f88a))

### Documentation

- Update README for v1.0.0 ([#20](https://github.com/luuuis/pyomie/pull/20),
  [`63786af`](https://github.com/luuuis/pyomie/commit/63786af5abd04bb7f8e602f14cd4331639657bab))

docs: update README for v1.x


## v1.0.0 (2025-10-01)

### Chores

- **build**: Skip commitlint on main ([#19](https://github.com/luuuis/pyomie/pull/19),
  [`3cb8144`](https://github.com/luuuis/pyomie/commit/3cb8144ff5a7e4c64a7cd08d36ce2d54faa9c20c))

chore: skip commitlint on main

### Features

- Omie quarter-hourly pricing support ([#18](https://github.com/luuuis/pyomie/pull/18),
  [`45ee162`](https://github.com/luuuis/pyomie/commit/45ee162de0d21627e75729faa97565f933eef6bc))

* fix: remove references to MIBEL adjustment price

* chore: set poetry in .tool-versions

* chore: remove unused util

* chore: unignore CLI test

BREAKING CHANGE: removed support for dates prior to 2025-10-01. prices are now reported on a
  quarter-hourly basis, with 96 data points for each day (or 92 or 100 in DST start/end). energy
  flows are reported as MW per 15-minute interval. SpotData property names have thus changed and
  clients must update their code accordingly.

BREAKING CHANGE: removes support MIBEL adjustment pricing

### Breaking Changes

- Removed support for dates prior to 2025-10-01. prices are now reported on a quarter-hourly basis,
  with 96 data points for each day (or 92 or 100 in DST start/end). energy flows are reported as MW
  per 15-minute interval. SpotData property names have thus changed and clients must update their
  code accordingly.

- Removes support MIBEL adjustment pricing


## v0.1.3 (2025-08-20)

### Bug Fixes

- Amend license name so PyPI recognises it ([#15](https://github.com/luuuis/pyomie/pull/15),
  [`5021d9a`](https://github.com/luuuis/pyomie/commit/5021d9a572bde7673aa84f256cb8f638e9bb2c9e))

* chore: add pre-commit as dev dependency

* fix: amend the license name so PyPI recognises it


## v0.1.2 (2025-08-07)

### Bug Fixes

- Compatibility with latest HA dependencies
  ([`6db5f67`](https://github.com/luuuis/pyomie/commit/6db5f67aa9d07aa193db1b41a13d8fcd10f920ee))

### Chores

- Remove hacktoberfest ([#11](https://github.com/luuuis/pyomie/pull/11),
  [`018ee68`](https://github.com/luuuis/pyomie/commit/018ee688afbd98df7275397f8658c13351faca6f))

- Removed CHANGELOG.md.j2 override
  ([`c40c629`](https://github.com/luuuis/pyomie/commit/c40c629209a814e02f310771e880e422563bc187))

- Use project email
  ([`61ccbbd`](https://github.com/luuuis/pyomie/commit/61ccbbd225d0a387aab8a3eebaa3eacd30be9ce0))

- **deps**: Upgrade dependencies ([#10](https://github.com/luuuis/pyomie/pull/10),
  [`12bde01`](https://github.com/luuuis/pyomie/commit/12bde0140a0a6b695f1490a61c32a490686eb4b0))

- **deps**: Upgrade dependencies ([#12](https://github.com/luuuis/pyomie/pull/12),
  [`1cd9d98`](https://github.com/luuuis/pyomie/commit/1cd9d987a8cb6555c681d46d5f069948bb3ab645))

- **deps**: Upgrade dependencies ([#13](https://github.com/luuuis/pyomie/pull/13),
  [`8879bb8`](https://github.com/luuuis/pyomie/commit/8879bb85f62d06988225df0209a27bda30f137f8))

* chore(deps): upgrade dependencies

* chore(deps): pin click<8.2.0 due to a bug in typer

- **deps**: Upgrade dependencies ([#14](https://github.com/luuuis/pyomie/pull/14),
  [`eb04aa3`](https://github.com/luuuis/pyomie/commit/eb04aa36cd7b056f67aa5921523c32402b8e1aab))

* chore: update to typer ^0.12.0

* chore: upgrade to python-semantic-release@v9

- **deps**: Upgrade dependencies ([#9](https://github.com/luuuis/pyomie/pull/9),
  [`270eb14`](https://github.com/luuuis/pyomie/commit/270eb146450df2b3e6c472d8218ec95ba5dec1a8))

### Documentation

- Removed shell completion support, tweaked CHANGELOG generation
  ([#8](https://github.com/luuuis/pyomie/pull/8),
  [`22fc333`](https://github.com/luuuis/pyomie/commit/22fc333a170a1eb8087a0809c2fd06e024e52082))

* chore: removes shell completion support, adds Usage section to README.md

* chore: added PyPI downloads badge


## v0.1.1 (2024-01-09)

### Bug Fixes

- Rework lib to add static typing info ([#6](https://github.com/luuuis/pyomie/pull/6),
  [`1527fc1`](https://github.com/luuuis/pyomie/commit/1527fc12b532f0ba6fb5af6991698dfbed43f7bb))

This is a breaking change but not applying semver since we're still in 0.x.

* fix: reworked the whole lib, use NamedTuple for returned data * ci: python >= 3.11

### Chores

- Use forked python-semantic-release running on Python 3.12
  ([`1d3ba5f`](https://github.com/luuuis/pyomie/commit/1d3ba5fe2a5b243b1b263a04f4ca28b04089ce9c))

### Continuous Integration

- Use forked upload-to-gh-release with Python 3.12
  ([`92b1e44`](https://github.com/luuuis/pyomie/commit/92b1e4486582c02b11be6ca86b5fc862566c9f95))

upstream uses Python 3.10, which this project does not support any more.

- Use GitHub setup python action to ensure correct version
  ([`d0a2dea`](https://github.com/luuuis/pyomie/commit/d0a2dea8946f82e0b36251644809a638ba168503))

- Use luuuis/python-semantic-release running on Python 3.12
  ([#7](https://github.com/luuuis/pyomie/pull/7),
  [`2aba05e`](https://github.com/luuuis/pyomie/commit/2aba05e473ecb9405b00eb5fd02f3b0bbab9985c))


## v0.1.0 (2024-01-07)

### Continuous Integration

- Include ci and chore in release notes ([#4](https://github.com/luuuis/pyomie/pull/4),
  [`7796dfd`](https://github.com/luuuis/pyomie/commit/7796dfd22904f82b3db05a473321cd4336116e21))

### Features

- Adds ability to fetch marginal and (historical) adjustment prices
  ([#5](https://github.com/luuuis/pyomie/pull/5),
  [`41a4b38`](https://github.com/luuuis/pyomie/commit/41a4b386cd77c7d72e5b633d051cb4da75c7cc5d))

* feat: adds ability to fetch marginal price and adjustment price (historical)

* includes a CLI with the ability to output either in JSON or the (unparsed) CSV response

* adds tests for CLI and two main entry points, diffs the response

* ci: set minimum python version to 3.10


## v0.0.0 (2024-01-04)

### Chores

- Prep for v0.0.1 ([#1](https://github.com/luuuis/pyomie/pull/1),
  [`2edc411`](https://github.com/luuuis/pyomie/commit/2edc411a176d877a64cf03749ed92423c15b5b86))

* chore: initial commit by @browniebroke/pypackage-template

* docs: add @luuuis as a contributor

### Continuous Integration

- Adds poetry.lock ([#2](https://github.com/luuuis/pyomie/pull/2),
  [`1ac64fe`](https://github.com/luuuis/pyomie/commit/1ac64fe11d65ecac892dfef7b13deb8e23f06a16))

- Remove CHANGELOG.md.j2 in favour of the built-in template
  ([#3](https://github.com/luuuis/pyomie/pull/3),
  [`362d6e3`](https://github.com/luuuis/pyomie/commit/362d6e366d4e917a0130ef6106555b10fe150728))
