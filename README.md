# Overview

[fork] small cli tool to study using fl

*Free software: BSD license*

# Installation

```
cd flashcards
pip3 install -r requirements.txt
```

# Usage

## flash card
Let's suppose ``example.yaml`` is your file with information.

- normal mode
```
python3 cli.py example.yaml
```

- `-W` : writing mode (you can answer by writing and it will be saved)
```
python3 cli.py example.yaml -W
```

- `-S` : speaking mode (you can answer by speaking and it will be saved)
```
python3 cli.py example.yaml -S
```

## generate contents
- you can generate yaml file by speaking
```
python3 make_yaml.py english_phrase.yaml -S
```
