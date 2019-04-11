[![open-gov-lic](https://img.shields.io/badge/License-OGL-blue.svg)](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

# bayesint

This repository includes the Python code for calculating Bayesian credible interval of ratios of independent beta distributions. It has been used in [*Methods for calculating credible intervals for ratios of beta distributions with application to relative risks of premature death during the second plague pandemic*](https://doi.org/10.1371/journal.pone.0211633)

## Getting Started

### Prerequisites

* [Python 2.7+](www.python.org)

### Installation

Clone the repository then run

```python
python setup.py install
```

## Usage

To get the relative risk of a contingency table given by

|       | +       | _             | Total   |
|-------|---------|---------------|---------|
| +     | P = 56  | M- P          | M = 366 |
| -     | C = 126 | N - C         | N = 354 |
| Total | C + P   | N - C + M - P | N + M   |

run

```python
from bayesint import rel_risk
rel_risk(56, 126, 366, 354)
# 236/549
```

and to obtain the equal-tailed quantile interval for the data given in the contingency table run

```python
from bayesint import eqt_int_frac
eqt_int_frac(56, 126, 366, 354, (0, 0, 0, 0), "risk", 0.05, "estim")
# (236/549, 0.184135819539239, 0.667343920284484)
```

## Authors

Maria Bekker-Nielsen Dunbar and Tom Finnie

## Contributing

This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct.

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## License

Public Health England 2017

This project is licensed under the Open Government License, see [LICENSE](LICENSE) for details
