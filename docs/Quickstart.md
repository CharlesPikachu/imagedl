# 快速开始

#### API调用

示例代码如下:

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

config中的参数解释如下:

- savedir: 图片保存文件夹;
- auto_set_proxies: 本地IP因为请求过于频繁被目标服务器禁止访问后, 是否自带开启代理, 代理是用[freeproxy](https://github.com/CharlesPikachu/freeproxy)从网上抓取的;
- auto_set_headers: 请求过程中是否自动更好请求头;
- search_limits: 下载的图片数量;
- num_threadings: 使用的线程数量。

run函数支持的参数如下:

- target_src: 使用的图片源, 目前支持"bing", "baidu"和"google"。

#### 编译调用

pip安装之后, 环境变量中会自动生成image.exe文件, 只需要在终端直接输入imagedl即可调用, 使用方式如下:

```sh
Usage: imagedl [OPTIONS]

Options:
  --version                  Show the version and exit.
  -k, --keyword TEXT         想要搜索下载的图片关键字, 若不指定, 则进入imagedl终端版
  -s, --savedir TEXT         下载的图片的保存路径
  -t, --target TEXT          指定图片搜索下载的平台, 例如"baidu"
  -l, --limits INTEGER       下载的图片数量
  -n, --nthreadings INTEGER  使用的线程数量
  --help                     Show this message and exit.
```

例如:

```sh
imagedl -k 狗狗 -s dogs -t baidu -l 1000
```

效果如下:

<div align="center">
  <img src="https://github.com/CharlesPikachu/imagedl/raw/main/docs/screenshot.gif" width="600"/>
</div>
<br />