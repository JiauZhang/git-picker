from setuptools import setup, find_packages
from gitpicker import __version__

setup(
    name='git-picker',
    packages=find_packages(exclude=['examples']),
    version=__version__,
    license='MIT',
    description='git picker',
    author='JiauZhang',
    author_email='jiauzhang@163.com',
    url='https://github.com/JiauZhang/git-picker',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    keywords=[
        'GitHub',
    ],
    install_requires=[
        'httpx', 'lxml',
        'conippets==0.1.8',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)