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

Run this example in a live Jupyter notebook: [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/jesserobertson/earthchem-pyclient/master?filepath=examples%2Frest_queries.ipynb)

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
>>> df = q.dataframe(max_rows=500)
>>> df.head()
```
```
Downloading pages: 100%|██████████| 10/10 [00:04<00:00,  2.24it/s]
```

![Table output](https://github.com/jesserobertson/earthchem-pyclient/raw/develop/docs/resources/table_output.png)

Hmm looks like Dr Barnes is a bit of a komatiite expert

```python
>>> fig = df.mgo.hist()
>>> fig.set_xlabel('MgO (wt %)')
>>> fig.set_ylabel('Sample count')
```

![Plot output](https://github.com/jesserobertson/earthchem-pyclient/raw/develop/docs/resources/mgo.png)

Maybe we'd like to see this as a ternary plot instead...

```python
>>> earthchem.plot.ternaryplot(df, components=['mgo', 'al2o3', 'cao'])
```

![Plot output](https://github.com/jesserobertson/earthchem-pyclient/raw/develop/docs/resources/ternary.png)

### Great, I'm sold. How do I get it?

Provided you have python installed, this library is just a `pip install earthchem` away. 

If you don't have Python we recommend taking a look at the marvellous [Anaconda distribution](https://www.anaconda.com/) - just pick your relevant platform download [from here](https://www.anaconda.com/download/).
