# Imagedl Installation

#### Environment Requirements

- Operating system: Linux, macOS, or Windows.
- Python version: Python 3.10+ with requirements in [pyimagedl requirements.txt](https://github.com/CharlesPikachu/imagedl/blob/main/requirements.txt).

#### Installation Instructions

You have three installation methods to choose from,

```sh
# from pip
pip install pyimagedl
# from github repo method-1
pip install git+https://github.com/CharlesPikachu/imagedl.git@main
# from github repo method-2
git clone https://github.com/CharlesPikachu/imagedl.git
cd imagedl
python setup.py install
```

Please note that some image sources need to be crawled using [DrissionPage](https://www.drissionpage.cn/), such as `EverypixelImageClient` and `GoogleImageClient`. 
If DrissionPage cannot find a suitable browser in the current environment, it will automatically download the latest compatible beta version of Google Chrome for the current system. 
So if you notice that the program is downloading a browser, there is no need to be overly concerned.