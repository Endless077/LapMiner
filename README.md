![Wallpaper](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)

# 🏎️ LapMiner

LapMiner is a versatile tool designed to generate, analyze, update, and export datasets from fastestlap.com into various intelligible formats.


## 🌟 Features

- **Data Scraping**: Extract lap time data from fastestlap.com.
- **Data Analysis**: Analyze the collected data to derive meaningful insights.
- **Data Export**: Export data in various formats for easy consumption.
- **Extensibility**: Easily extendable with new tools and functionalities.


## ✔️ Acknowledgements

Built on a Linux-based system and Python version 3.8.10:

- [Python](https://www.python.org/)
- [Requests](https://docs.python-requests.org/en/latest/index.html)
- [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/en/latest/)

See the `requirements.txt` file for the complete list of dependencies.


## 🛠️ Installation

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


## 🚀 Usage/Examples

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


## 📝 Documentation

No formal documentation is available. For any issues, please contact me directly.
Refer to the comments in the code for guidance.


## 🖐 Authors

This is the thesis project of:

[@Endless077](https://github.com/Endless077) - Antonio Garofalo

<div align="center">
<p><em>A crawler for automatic mining of vehicle data</em></p>
</div>  


## 💾 License

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

©️ GNU General Public License (GPL), more details [here](https://www.gnu.org/licenses/gpl-3.0.en.html).


## ❓ FAQ

#### 🆓 Free to use?

Yes, LapMiner is completely free to use under the GPL v3 license. You can download, modify, and share it as you see fit, provided you adhere to the license terms.

#### 🛡️ Does the program use proxies?

No, LapMiner does not include built-in proxy support. However, if you need to use proxies for your scraping activities, you can easily implement your own proxy handling in `utils.py`. Just be aware of the legal and ethical implications of using proxies.

#### 🎯 What is it intended for?

LapMiner is primarily intended for enthusiasts and developers who want to analyze lap time data from fastestlap.com. It’s a versatile tool that can be used for data analysis, research, or even to contribute to open-source projects by submitting issues, bug reports, or suggesting new features on the GitHub repository. Contributions are welcome, and you can fork the repository and submit pull requests.

#### 🔧 Can I extend LapMiner with additional features?

Yes, LapMiner is designed to be extensible. You can easily add new tools, functionalities, or integrate it with other systems. The codebase is modular, so adding new features should be straightforward. Feel free to contribute back any useful features to the community!

#### 💻 What platforms are supported?

LapMiner is developed and tested on Linux-based systems, but it should work on any platform that supports Python 3.8.10 or higher, including Windows and macOS. If you encounter any platform-specific issues, please report them on GitHub.

#### ⚠️ Are there any limitations I should be aware of?

While LapMiner is a powerful tool, it’s important to use it responsibly. Scraping websites, especially at scale, can put a load on their servers and may violate their terms of service. Always ensure you have permission to scrape data, and be mindful of rate limits and legal considerations.

#### 🔍 How can I troubleshoot issues with LapMiner?

If you encounter any issues, first check the error messages and logs for clues. Make sure all dependencies are installed correctly and that you're using the correct Python version. If the problem persists, you can open an issue on the GitHub repository or contact the author directly for support.

#### 🤔 Other questions?

If you have any additional questions or need further assistance, feel free to contact me directly through GitHub. I'm happy to help with any issues, feature requests, or general inquiries about LapMiner.
