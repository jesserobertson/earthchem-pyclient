Managing notebooks in git is a right PITA.

To preserve our sanity we're using [nbdime](http://nbdime.readthedocs.io/en/stable). It has nice git integration but you will need to install it on your system to commit jupyter notebooks back to the repository. 

Install nbdime with `pip install nbdime`, and it should then just work nicely with this repo (since we've already configured nbdime to be the default diff client for jupyter notebooks in `earthchem/.gitattributes`). If you want to enable this behavior everywhere then you can do

```bash
$ nbdime config-git --enable --global
```

If you want to launch the browser-based diff viewer you can run the following:

```bash
$ nbdiff-web $REF_1 $REF_2
$ git mergetool --tool nbdime -- *.ipynb
```

where `$REF_N` are files or git hashes.