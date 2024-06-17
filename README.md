![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)

# LapMiner

LapMiner is a versatile tool designed to generate, analyze, update, and export datasets from fastestlap.com into various intelligible formats.

## Features

- **Data Scraping**: Extract lap time data from fastestlap.com.
- **Data Analysis**: Analyze the collected data to derive meaningful insights.
- **Data Export**: Export data in various formats for easy consumption.
- **Extensibility**: Easily extendable with new tools and functionalities.

## Acknowledgements

Built on a Linux-based system and Python version 3.8.10:

- [Python](https://www.python.org/)
- [Requests](https://docs.python-requests.org/en/latest/index.html)
- [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/en/latest/)

See the `requirements.txt` file for the complete list of dependencies.

## Installation

To install LapMiner, clone this repository and ensure Python (version 3.8.10 or higher) is installed.

Then, create a virtual environment (requires `pip` and `venv`):

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
  source ../path/venv/bin/activate
```

(use the deactivate command to exit the virtual environment)

Finally, install all requirements:

```bash
  pip install -r ../path/requirements.txt
```


## Usage/Examples

The primary usage is:

```bash
  python3 ../path/main/scrap.py
```

this command initiates scraping from fastestlap.com.

Additional commands:

```bash
  python3 ../path/main/scav.py file.csv | vehicle_name source_uri
```

```bash
  python3 ../path/main/report.py
```

- The first command starts the scavenging tool.
- The second command starts the reporting tool.

## Documentation

No formal documentation is available. For any issues, please contact me directly.
Refer to the comments in the code for guidance.


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

#### Does the program use proxies?

No, but you can implement your own function or fill lists in utils.py.
(I'm not sure that it is leagal)

#### What is it intended for?

You can contribute by submitting issues, bug reports, or suggesting features on the GitHub repository. Feel free to fork the repository and submit pull requests.

#### Other questions?

Contact me for any issue.
