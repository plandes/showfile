# Invoke native applications to view files

[![PyPI][pypi-badge]][pypi-link]
[![Python 3.9][python39-badge]][python39-link]
[![Python 3.10][python310-badge]][python310-link]
[![Build Status][build-badge]][build-link]

Invoke native applications to view files.  On macOS, the default web browser
and Preview.app are used to view HTML and PDF files respectively.  On all other
operating systems the default web browser is used to view files.


## Usage

Create a [configuration file] with the dimensions of each of the screens you
work with and where you want Preview.app to be displayed.  You can validate
these configurations by having the application echo them back at you:

```bash
$ showfile config
```

Invoke the application to show the file and display it:

```bash
$ showfile show example.pdf
```


See the [configuration file] example.


## Obtaining

The easiest way to install the command line program is via the `pip` installer:
```bash
pip3 install zensols.showfile
```

Binaries are also available on [pypi].


## Documentation

See the [full documentation](https://plandes.github.io/showfile/index.html).
The [API reference](https://plandes.github.io/showfile/api.html) is also
available.


## Changelog

An extensive changelog is available [here](CHANGELOG.md).


## License

[MIT License](LICENSE.md)

Copyright (c) 2022 Paul Landes


<!-- links -->
[pypi]: https://pypi.org/project/zensols.showfile/
[pypi-link]: https://pypi.python.org/pypi/zensols.showfile
[pypi-badge]: https://img.shields.io/pypi/v/zensols.showfile.svg
[python39-badge]: https://img.shields.io/badge/python-3.9-blue.svg
[python39-link]: https://www.python.org/downloads/release/python-390
[python310-badge]: https://img.shields.io/badge/python-3.10-blue.svg
[python310-link]: https://www.python.org/downloads/release/python-310
[build-badge]: https://github.com/plandes/showfile/workflows/CI/badge.svg
[build-link]: https://github.com/plandes/showfile/actions

[configuration file]: test-resources/showfile.conf
