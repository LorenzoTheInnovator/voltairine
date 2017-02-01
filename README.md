# voltairine
Chat bot for Anarchism discord.

[![codecov](https://codecov.io/gh/gooseberrycollective/voltairine/branch/master/graph/badge.svg)](https://codecov.io/gh/gooseberrycollective/voltairine)
[![Build Status](https://travis-ci.org/gooseberrycollective/voltairine.svg?branch=master)](https://travis-ci.org/gooseberrycollective/voltairine)
![](https://reposs.herokuapp.com/?path=gooseberrycollective/voltairine)

# Commands

## Educational

| Command        | Function           |
| ------------- |:-------------:|
| !afaq         | Anarchist FAQ |
| !anarchism    | General Info      |
| !ancom        | Anarchist Communist Essential Readings      |
| !anfem        | Anarchist-Feminist Essential Readings      |
| !anti-civ     | Anti-Civ Essential Readings      |
| !bakunin      | Mikhail Bakunin Essential Readings      |
| !berkman      | Alexander Berkman Essential Readings       |
| !bonanno      | Bonanno Essential Readings      |
| !bookchin     | Bookchin Essential Readings      |
| !bookclub     | Our Bookclub      |
| !books        | Key Reading List      |
| !chomsky      | Noam Chomsky Essential Readings      |
| !durruti      | Durruti Essential Readings      |
| !feminism     | General Info      |
| !goldman      | Emma Goldman Essential Readings      |
| !kropotkin    | Peter Kropotkin Essential Readings      |
| !makhno       | Nestor Makhno Essential Readings      |
| !mutualism    | Mutalist Essential Readings      |
| !proudhon     | Pierre Proudhon Essential Readings      |
| !stirner      | Max Stirner Essential Readings      |

# Install

`pip install -r requirements.txt`

`touch volt_settings.toml`

example config:
```toml
token = "DISCORD_TOKEN"
[pyborg]
server = "localhost"
port = 2001
multiplex = true
learning = true
```
