# xTraktor

Structured data extractor for the modern world wide web.

## What is this?
Implementation of 3 approaches to structured data extraction:
- using [r̎͒̔̓̒e̊ͯ̎̔̏̾͆ͤ͆ͬg̃̏ͨͣ̑̑ͧ̆̓͐ͬͥ͂͗̍uͮͫ̽ͪ͆̆̈́̓͆l̒̀̔̾͛ͮ͗̊̓aͣͨͮ̐͋̏͛̉͋ͭ̏̓͑ͮ͌̄̽͑̚r͂̓ͫ͋ͯͪͧ̑͐͛ͪͮͮͨ̌̄̈ ͮ̾ͦ͂̌ͩͧ́̈́eͣ̀ͯͧ̿ͧ̂x̓͂̃̈́ͬͫ͗ͯ̔ͮ̂̃̅̓ͤͮ̈͑p̎ͭ̌ͤ̋͑ͮ̇̀͒ͫ̽̐̀̚rͪͭ̑̾̄ͫeͤͪ̽ͭ͊ͯ́̂̊ͧ͑ͩ̃͋ͥ͒̓̈́̑s̒ͨ̋̎̿͐͋ͥ̎s̏̅̽ͦ̐̈́ͣ͋̚i̽ͪ̊ͥͯ͆͛̋ͪo͌̊̈́̐̓͂͐͂͊͋̍́͆nͣ̀̽ͫ͆ͩ͒́̆ͦ̐͒̾sͤ̄̿̆͌](https://stackoverflow.com/a/1732454),
- using XPath,
- using RoadRunner-like implementation.

Usage demonstrated on sample pages from 3 websites: [overstock.com](https://www.overstock.com/), 
[rtvslo.si](https://www.rtvslo.si/) and [avto.net](https://www.avto.net/). We have gathered two
pages from each website.

This is the second assignment in the **Web information extraction and retrieval** course.

## Setup
**[Optional]** Create a virtualenv and activate it.
```
$ virtualenv --python=python3 --system-site-packages wiervenv
$ source wiervenv/bin/activate
```
  
Install required dependencies.
```
$ pip3 install -r requirements.txt
```
  
Install in dev mode.
```
$ python3 setup.py develop
```

## Running the parser
`implementation/` contains the implementations of regular-expressions-based (`regex.py`) 
and XPath-based (`xpath.py`) approaches. RoadRunner-like approach is **not implemented**.
Running those files will produce the JSON outputs for files in the `input/` folder.  

Assuming you are inside the `implementation/` directory:
```
$ python3 regex.py
$ python3 xpath.py
```

## Project structure
`input/` contains the 6 webpages from 3 sources, that are used to test the approaches.
`output/` contains JSON outputs generated by the methods for 6 webpages from 3 sources.
`implementation/` contains the source code of our implemented approaches.
`report.pdf` (note: in root folder) contains our report for the assignment.


2019, Jaka Stavanja, Matej Klemen & Andraž Povše
