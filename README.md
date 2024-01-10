# pyomie

<p align="center">
  <a href="https://github.com/luuuis/pyomie/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/luuuis/pyomie/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://pyomie.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/pyomie.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/luuuis/pyomie">
    <img src="https://img.shields.io/codecov/c/github/luuuis/pyomie.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
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

The pyomie CLI returns a JSON payload for the given date.

````bash

 Usage: pyomie [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ adjustment           Fetch the OMIE adjustment mechanism data (2022-06-14 to 2023-12-31).                                                   │
│ spot                 Fetch the OMIE spot price data.                                                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

% pyomie spot
{"url": "https://www.omie.es/sites/default/files/dados/AGNO_2024/MES_01/TXT/INT_PBC_EV_H_1_10_01_2024_10_01_2024.TXT", "market_date": "2024-01-10", "header": "OMIE - Mercado de electricidad;Fecha Emisi\u00f3n :09/01/2024 - 13:10;;10/01/2024;Precio del mercado diario (EUR/MWh);;;;", "energy_total_es_pt": [33005.5, 30609.6, 29673.1, 29433.3, 29493.8, 29369.5, 31232.4, 36220.8, 39727.3, 41284.4, 42226.1, 42185.7, 42251.7, 42160.6, 41797.1, 41219.1, 40821.6, 41578.7, 43373.7, 44486.4, 45074.3, 43880.7, 39901.2, 35825.1], "energy_purchases_es": [14628.1, 13674.3, 13832.3, 14050.3, 14062.1, 13841.5, 14289.4, 17225.7, 19236.0, 19694.4, 19849.2, 19668.8, 19607.8, 19551.7, 19261.9, 18695.1, 18415.8, 18823.5, 19866.3, 20247.3, 20542.4, 19997.9, 17416.4, 14973.3], "energy_purchases_pt": [6274.2, 5780.5, 5345.9, 5046.5, 5116.3, 4834.2, 4925.7, 5445.5, 6180.0, 6959.3, 7402.3, 7520.7, 7651.2, 7547.3, 7510.1, 7612.3, 7650.8, 7833.7, 8032.9, 8405.5, 8580.9, 8364.2, 7929.4, 7319.4], "energy_sales_es": [13248.9, 12414.6, 12403.0, 12285.2, 12320.0, 12333.3, 12810.1, 15109.1, 16851.2, 17993.2, 19014.1, 19565.1, 19661.6, 19862.2, 19666.6, 19220.4, 18791.2, 18706.2, 19458.3, 19875.6, 19968.0, 19536.6, 17623.9, 16414.0], "energy_sales_pt": [6203.4, 5590.2, 5325.2, 5361.6, 5407.0, 5659.1, 7544.0, 8701.1, 9703.8, 9799.5, 9376.4, 8974.4, 8595.9, 8586.8, 8455.4, 8637.0, 8825.4, 9501.0, 9990.9, 10327.2, 10085.5, 9058.3, 8204.9, 6907.3], "energy_es_pt": [20902.3, 19454.8, 19178.2, 19096.8, 19178.4, 18675.7, 19215.1, 22671.2, 25416.0, 26653.7, 27251.5, 27189.5, 27259.0, 27099.0, 26772.0, 26307.4, 26066.6, 26657.2, 27899.2, 28652.8, 29123.3, 28362.1, 25345.8, 22292.7], "energy_export_es_to_pt": [70.8, 190.3, 20.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 412.1], "energy_import_es_from_pt": [0.0, 0.0, 0.0, 315.1, 290.7, 824.9, 2618.3, 3255.6, 3523.8, 2840.2, 1974.1, 1453.7, 944.7, 1039.5, 945.3, 1024.7, 1174.6, 1667.3, 1958.0, 1921.7, 1504.6, 694.1, 275.5, 0.0], "spot_price_es": [92.33, 90.12, 87.01, 85.8, 85.0, 86.3, 95.0, 103.94, 121.4, 121.4, 105.38, 102.97, 99.99, 98.5, 94.76, 94.73, 99.37, 102.7, 111.29, 121.4, 120.0, 107.71, 101.32, 92.68], "spot_price_pt": [92.33, 90.12, 87.01, 85.8, 85.0, 86.3, 95.0, 103.94, 121.4, 121.4, 105.38, 102.97, 99.99, 98.5, 94.76, 94.73, 99.37, 102.7, 111.29, 121.4, 120.0, 107.71, 101.32, 92.68]}```
````

The output is a JSON payload that may be used by other tooling.

```bash

% pyomie spot 2023-01-01 | jq -c '.header, .spot_price_pt'
"OMIE - Mercado de electricidad;Fecha Emisión :31/12/2022 - 13:24;;01/01/2023;Precio del mercado diario (EUR/MWh);;;;"
[0,0,0,0,0,0,0,0,0,0,0,0,0,0.1,0.1,0.01,1,4.16,15.1,19.51,24.61,40.07,40.07,16]
```

You can also `pipx run pyomie` to [run the CLI from a temporary virtual environment](https://pipx.pypa.io/stable/#walkthrough-installing-a-package-and-its-applications-with-pipx).

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

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
