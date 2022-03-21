'''
Function:
    setup the imagedl
Author:
    Charles
微信公众号:
    Charles的皮卡丘
GitHub:
    https://github.com/CharlesPikachu
'''
import imagedl
from setuptools import setup, find_packages


'''readme'''
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


'''setup'''
setup(
    name=imagedl.__title__,
    version=imagedl.__version__,
    description=imagedl.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    author=imagedl.__author__,
    url=imagedl.__url__,
    author_email=imagedl.__email__,
    license=imagedl.__license__,
    include_package_data=True,
    entry_points={'console_scripts': ['imagedl = imagedl.imagedl:imagedlcmd']},
    install_requires=list(open('requirements.txt', 'r').readlines()),
    zip_safe=True,
    packages=find_packages()
)