# dvcon_download 
Download proceedings from DVCon USA/ DVCon Euorpe

## Overview 
This script is intended to download the DVCON papers from the official website. For the url has some common format, downloading them by hand would be rather tedious. Here comes an idea to write a simple script to download them.


## How to use 
```python
git clone https://github.com/troyguo/dvcon_download.git

python3 dvcon_dowload/download.py
```
After running, folder named by location and year will be seen under the current folder, for example, USA_2018


## Limitation 
Currently, for DVCON Europe, only the year after 2016 can be downloaded, it's caused by the url format difference from the year 2015 and 2016.





## TODO:

1. Add dvcon India/China downloading
2. compatible with DVCon Europe 2015 format.

