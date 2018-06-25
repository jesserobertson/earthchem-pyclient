""" file:   spider.py (earthchem.plot)
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Spider plots
"""

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import warnings
from ..geochem import common_elements


def spiderplot(df, ax=None, components:list=None, plot=True, fill=False, **kwargs):
    """
    Plots spidergrams for trace elements data.
    By using separate lines and scatterplots, values between two null-valued
    items are still presented. Might be able to speed up the lines
    with a matplotlib.collections.LineCollection

    Parameters
    ----------
    df: pandas DataFrame
        Dataframe from which to draw data.
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    components: list, None
        Elements or compositional components to plot.
    plot: boolean, True
        Whether to plot lines and markers.
    fill:
        Whether to add a patch representing the full range.
    style:
        Styling keyword arguments to pass to matplotlib.
    """

    try:
        assert plot or fill
    except:
        raise AssertionError('Please select to either plot values or fill between ranges.')
    sty = {}
    # Some default values
    sty['marker'] = kwargs.get('marker') or 'D'
    sty['color'] = kwargs.get('color') or kwargs.get('c') or None
    sty['alpha'] = kwargs.get('alpha') or kwargs.get('a') or 1.
    if sty['color'] is None:
        del sty['color']

    components = components or [el for el in common_elements(output='str')
                                if el in df.columns]
    assert len(components) != 0
    c_indexes = np.arange(len(components))

    ax = ax or plt.subplots(1, figsize=(len(components)*0.25, 4))[1]

    if plot:
        ls = ax.plot(c_indexes,
                     df[components].T.values.astype(np.float),
                     **sty)

        sty['s'] = kwargs.get('markersize') or kwargs.get('s') or 5.
        if sty.get('color') is None:
            sty['color'] = ls[0].get_color()
        sc = ax.scatter(np.tile(c_indexes, (df[components].index.size,1)).T,
                        df[components].T.values.astype(np.float), **sty)

    for s_item in ['marker', 's']:
        if s_item in sty:
            del sty[s_item]

    if fill:
        mins, maxs = df[components].min(axis=0), df[components].max(axis=0)
        ax.fill_between(c_indexes, mins, maxs, **sty)

    ax.set_xticks(c_indexes)
    ax.set_xticklabels(components, rotation=60)
    ax.set_yscale('log')
    ax.set_xlabel('Element')

    unused_keys = [i for i in kwargs if i not in list(sty.keys()) + \
                  ['alpha', 'a', 'c', 'color', 'marker']]
    if len(unused_keys):
        warnings.warn('Styling not yet implemented for:{}'.format(unused_keys))
