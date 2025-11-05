# pyomie

<p align="center">
  <a href="https://github.com/luuuis/pyomie/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/luuuis/pyomie/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">
  </a>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/pyomie/">
    <img src="https://img.shields.io/pypi/v/pyomie.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <a href="https://pypi.org/project/pyomie/">
    <img src="https://img.shields.io/pypi/dm/pyomie" alt="pypy downloads">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/pyomie.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/pyomie.svg?style=flat-square" alt="License">
</p>

---

**Documentation**: <a href="https://pyomie.readthedocs.io" target="_blank">https://pyomie.readthedocs.io </a>

**Source Code**: <a href="https://github.com/luuuis/pyomie" target="_blank">https://github.com/luuuis/pyomie </a>

---

A command-line interface and asynchronous client library for OMIE - Spain and Portugal electricity market data.

## Installation

Install this via pip (or your favourite package manager):

`pip install pyomie`

## Usage

The pyomie CLI allows querying day-ahead market data for a given date.

```bash
% pyomie --help

 Usage: pyomie [OPTIONS] [DATE]

 Fetch the OMIE spot price data.

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   date      [DATE]  Date to fetch in YYYY-MM-DD format [default: today's date]                                                                                                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --csv              Print the CSV as returned by OMIE, without parsing.                                                                                                                                                                                                      │
│ --verbose          Verbose mode.                                                                                                                                                                                                                                            │
│ --help             Show this message and exit.                                                                                                                                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

By default, the output is a JSON payload that may be used by other tooling.

```bash

% pyomie 2025-10-02 | jq -c '{date: .market_date, average_pt:(.pt_spot_price|add/length)}'
{"date":"2025-10-02","average_pt":86.3228125}
```

You can also `pipx run pyomie` to [run the CLI from a temporary virtual environment](https://pipx.pypa.io/stable/#walkthrough-installing-a-package-and-its-applications-with-pipx).

## Contributors ✨

Thanks to these contributors ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/luuuis"><img src="https://avatars.githubusercontent.com/u/161006?v=4?s=80" width="80px;" alt="Luis Miranda"/><br /><sub><b>Luis Miranda</b></sub></a><br /><a href="https://github.com/luuuis/pyomie/commits?author=luuuis" title="Code">💻</a> <a href="#ideas-luuuis" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/luuuis/pyomie/commits?author=luuuis" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
