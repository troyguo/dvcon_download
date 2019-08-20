# dvcon_download
Download proccedings from DVCon

##Overview
This script is intented to download the DVCON papers from the offical website. For the url has some common format, downloading them by hand would be rather tedious. Here comes an idea to write a simple script to download them.


##How to use
```
git clone https://github.com/troyguo/dvcon_download.git

python3 dvcon_dowload/download.py
```
After running, folder named by location and year will be seen under the current folder, for example, USA_2018


##Limtation
Currently, for DVCON Europe, only the year afer 2016 can be downloaded, it's caused by the url format diffrence from the year 2015 and 2016.
