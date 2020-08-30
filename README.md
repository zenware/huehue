# HueHue

Logo

[![tests](https://github.com/zenware/huehue/workflows/tests/badge.svg)](https://github.com/zenware/huehue/actions?workflow=tests)
[![Codecov](https://codecov.io/gh/zenware/huehue/branch/master/graph/badge.svg)](https://codecov.io/gh/zenware/huehue)
[![PyPI](https://img.shields.io/pypi/v/huehue.svg)](https://pypi.org/project/huehue/)
[![Read the Docs](https://readthedocs.org/projects/huehue/badge/)](https://huehue.readthedocs.io/)

This is a CLI and API Client for the Philips Hue lights written in Python.
I decided to write this project so I could add light control to some personal automation tasks.
It's a work in progress that started as a very terrible wrapper script and is slowly turning into something a bit nicer.

## Installing

Pipx might be the most convenient way to install Python CLI Tools Currently?
```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx completions
pipx install huehue
```

## Example Usage
Currently working out how I want the cli to work....
```
huehue bridge list  # List all the bridges on your network (probably there is only one)
huehue lights list  
```

## Notes

Attempting in some ways to follow the Google Python Style Guide, but probably going to give up and use black instead.
https://google.github.io/styleguide/pyguide.html
