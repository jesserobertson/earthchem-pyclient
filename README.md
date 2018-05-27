# Earthchem & PyData

[![PyPI](https://img.shields.io/pypi/v/earthchem.svg)](https://pypi.python.org/pypi/earthchem/)
[![GitHub license](https://img.shields.io/github/license/jesserobertson/earthchem-pyclient.svg)](https://github.com/jesserobertson/earthchem-pyclient/blob/master/LICENSE.txt)

This project wraps the Earthchem web services to provide easy access to geochemical data from [IEDA](https://www.iedadata.org/) in ready-to-use format in your favourite PyData environment.

Maintainer: Jess Robertson (jesse.robertson _at_ csiro.au)

| **Service** | **master** | **develop** |
| ----------- |:----------:|:-----------:|
| Test status | [![Build Status](https://travis-ci.org/jesserobertson/earthchem-pyclient.svg?branch=master)](https://travis-ci.org/jesserobertson/earthchem-pyclient) | [![Build Status](https://travis-ci.org/jesserobertson/earthchem-pyclient.svg?branch=develop)](https://travis-ci.org/jesserobertson/earthchem-pyclient) |
| Test coverage | [![Codecov branch](https://img.shields.io/codecov/c/github/jesserobertson/earthchem-pyclient/master.svg)](https://codecov.io/gh/jesserobertson/earthchem-pyclient/branch/master) | [![Codecov branch](https://img.shields.io/codecov/c/github/jesserobertson/earthchem-pyclient/develop.svg)](https://codecov.io/gh/jesserobertson/earthchem-pyclient/branch/develop) |

### So why would I want to use this?

Say you wanted to know how many Archean-aged samples have been submitted to IEDA by your colleague named Dr S Barnes:

```python
>>> import earthchem
>>> q = earthchem.Query(
        author='barnes',
        geologicalage='archean'
    )
>>> q.count()
```
```
876
```

Nice, let's take a look at the compositions of these

```python
>>> df = q.dataframe()
>>> df.head()
```
```
Downloading pages: 100%|██████████| 18/18 [00:29<00:00,  1.66s/it]
```

![Table output](https://github.com/jesserobertson/earthchem-pyclient/raw/develop/docs/resources/table_output.png)


Great, so now I can make some little plots right?

```python
>>> df.plot('al2o3', 'sio2', 'scatter')
```

![Plot output](https://github.com/jesserobertson/earthchem-pyclient/raw/develop/docs/resources/plot_output.png)

### Great, I'm sold. How do I get it?

Provided you have python installed, this library is just a `pip install earthchem` away. 

If you don't have Python we recommend taking a look at the marvellous [Anaconda distribution](https://www.anaconda.com/) - just pick your relevant platform download [from here](https://www.anaconda.com/download/).