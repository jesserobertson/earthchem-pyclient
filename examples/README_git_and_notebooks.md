Managing notebooks in git is a right PITA.

To preserve our sanity we're using [nbdime](http://nbdime.readthedocs.io/en/stable). It has nice git integration but you will need to install it on your system to commit jupyter notebooks back to the repository. 

Install nbdime and nbstripout with:

```bash
$ pip install nbstripout nbdime
```

and it should then just work nicely with this repo (since we've already configured nbdime to be the default diff client for jupyter notebooks in `earthchem/.gitattributes`). 

### Diffing with nbdime

If you want to enable this behavior everywhere then you can do

```bash
$ nbdime config-git --enable --global
```

If you want to launch the browser-based diff viewer you can run the following:

```bash
$ nbdiff-web $REF_1 $REF_2
$ git mergetool --tool nbdime -- *.ipynb
```

where `$REF_N` are files or git hashes.

Alternatively you can install the notebook extension to give you a button to get git diffs in the notebook interface with

```bash
$ jupyter serverextension enable --py nbdime [--sys-prefix/--user/--system]
$ jupyter nbextension install --py nbdime [--sys-prefix/--user/--system]
$ jupyter nbextension enable --py nbdime [--sys-prefix/--user/--system]
```

Note that this doesn't seem to work in jupyter lab yet so you have to be 
running `jupyter notebook` rather than `jupyter lab` to get these goodies.

### Stripping output with nbstripout

We'd like to not include megabytes and megabytes of output that we can regenerate ourselves in the git repo. It's easy to stop this happening if you use nbstripout, which basically does what it says on the tin.

You can set up the git filters using the following:

```bash
$ git config filter.nbstripout.clean '$(which nbstripout)'
$ git config filter.nbstripout.smudge cat
$ git config filter.nbstripout.required true
```
