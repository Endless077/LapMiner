
![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)


# LapMiner

LapMiner is an mlti-tool capable of generating a dataset from fastestlap.com, analysing, updating and exporting the data in various intelligible formats.


## Acknowledgements

Using a Linux Base system and python version 3.8.10:

 - [Python](https://www.python.org/)
 - [Requests](https://docs.python-requests.org/en/latest/index.html)
 - [BeutifulSoup4](https://beautiful-soup-4.readthedocs.io/en/latest/)

 See the requirements.txt file for the complete list of dependencies.


## Installation

Install LapMiner: just clone this repository and install python (prefer 3.8.10 or higher version).

Then create a virtual environment (needs pip and venv installed):

```bash
  python3 -m venv venv
```

Activate the venv:

```bash
  source ../path/venv/bin/activate
```

(use "deactivate" command to exit)

At last, install all requirements:

```bash
  pip install -r ../path/requirements.txt
```


## Usage/Examples

The main usage is:

```bash
  python3 ../path/main/scrap.py
```

this command start the scraping from fastestlasp.com.

Other commands:

```bash
  python3 ../path/main/scav.py file.csv | vehicle_name source_uri
```

```bash
  python3 ../path/main/report.py
```

the first one starts the scav tool.

the second one starts the report tool.


## Documentation

No documentation allowed, contact me for any issue (just read comments).


## Authors

This is the thesis project of:

[@Endless077](https://github.com/Endless077) - Antonio Garofalo


## License
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

This project is free to use:
[GPL v3](https://choosealicense.com/licenses/gpl-3.0/)

Thanks to support.


## FAQ

#### Free to use?

Yes.

#### Does the programme use proxies?

No, but in utils.py you can implement your own function or fill lists.

#### What is it intended for?

Used in Lap Time Prediction research, it can be extended with new tools.

#### Other questions?

Contact me for any issue.
