<div align="center">
  <img src="./docs/logo.png" width="600"/>
</div>
<br />

[![docs](https://img.shields.io/badge/docs-latest-blue)](https://imagedl.readthedocs.io/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/imagedl)](https://pypi.org/project/imagedl/)
[![PyPI](https://img.shields.io/pypi/v/imagedl)](https://pypi.org/project/imagedl)
[![license](https://img.shields.io/github/license/CharlesPikachu/imagedl.svg)](https://github.com/CharlesPikachu/imagedl/blob/master/LICENSE)
[![PyPI - Downloads](https://pepy.tech/badge/imagedl)](https://pypi.org/project/imagedl/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/imagedl?style=flat-square)](https://pypi.org/project/imagedl/)
[![issue resolution](https://isitmaintained.com/badge/resolution/CharlesPikachu/imagedl.svg)](https://github.com/CharlesPikachu/imagedl/issues)
[![open issues](https://isitmaintained.com/badge/open/CharlesPikachu/imagedl.svg)](https://github.com/CharlesPikachu/imagedl/issues)

Documents: https://imagedl.readthedocs.io/


# Imagedl

```
Search and download images from specific websites.
You can star this repository to keep track of the project if it's helpful for you, thank you for your support.
```


# Support List

|  Source                               |   Support Search?  |  Support Download?   |  in Chinese          |
|  :----:                               |   :----:           |  :----:              |  :----:              |
|  [baidu](https://baidu.com/)          |   ✓                |  ✓                   |  百度图片            |


# Install

#### Pip install

```
run "pip install imagedl"
```

#### Source code install

```sh
(1) Offline
Step1: git clone https://github.com/CharlesPikachu/imagedl.git
Step2: cd imagedl -> run "python setup.py install"
(2) Online
run "pip install git+https://github.com/CharlesPikachu/imagedl.git@master"
```


# Quick Start

#### Run by leveraging the API

```python
from imagedl import imagedl

config = {
	'savedir': 'outputs',
	'auto_set_proxies': True,
	'auto_set_headers': True,
	'search_limits': 1000,
	'num_threadings': 5,
}
client = imagedl.imagedl(config=config)
client.run('baidu')
```

#### Run by leveraging compiled file

```
Usage: imagedl [OPTIONS]

Options:
  --version               Show the version and exit.
```


# Projects in Charles_pikachu

- [Games](https://github.com/CharlesPikachu/Games): Create interesting games by pure python.
- [DecryptLogin](https://github.com/CharlesPikachu/DecryptLogin): APIs for loginning some websites by using requests.
- [imagedl](https://github.com/CharlesPikachu/imagedl): A lightweight music downloader written by pure python.
- [Videodl](https://github.com/CharlesPikachu/videodl): A lightweight video downloader written by pure python.
- [Pytools](https://github.com/CharlesPikachu/pytools): Some useful tools written by pure python.
- [PikachuWeChat](https://github.com/CharlesPikachu/pikachuwechat): Play WeChat with itchat-uos.
- [Pydrawing](https://github.com/CharlesPikachu/pydrawing): Beautify your image or video.
- [ImageCompressor](https://github.com/CharlesPikachu/imagecompressor): Image compressors written by pure python.
- [FreeProxy](https://github.com/CharlesPikachu/freeproxy): Collecting free proxies from internet.
- [Paperdl](https://github.com/CharlesPikachu/paperdl): Search and download paper from specific websites.
- [Sciogovterminal](https://github.com/CharlesPikachu/sciogovterminal): Browse "The State Council Information Office of the People's Republic of China" in the terminal.
- [CodeFree](https://github.com/CharlesPikachu/codefree): Make no code a reality.
- [DeepLearningToys](https://github.com/CharlesPikachu/deeplearningtoys): Some deep learning toys implemented in pytorch.
- [DataAnalysis](https://github.com/CharlesPikachu/dataanalysis): Some data analysis projects in charles_pikachu.


# More

#### WeChat Official Accounts

*Charles_pikachu*  
![img](./docs/pikachu.jpg)