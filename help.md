After some struggle, I finally make ta-lib work! Here are my installation procedure:
$ conda create -n finance python=3
$ conda activate finance
$ brew install ta-lib
$ conda install -c conda-forge ta-lib # do not use: pip install ta-lib
Then:
$ python
Python 3.9.5 (default, May 18 2021, 12:31:01)
[Clang 10.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
' >>> import talib '
' >>> talib.**ta_version** '
b'0.4.0 (Sep 29 2020 17:41:45)'
It work! (that is, no more complain about Symbol not found: \_TA_ACOS, and talib works!)

Below are more details on my MacBook Pro with M1 CPU:
$ where brew
/opt/homebrew/bin/brew
(finance) $ conda list | grep ta-lib
libta-lib 0.4.0 haf1e3a3_0 conda-forge
ta-lib 0.4.19 py39h026c905_2 conda-forge
(finance) $ pip list | grep ta-lib
(finance) $
