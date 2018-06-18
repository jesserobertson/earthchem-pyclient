""" file:   ternary.py (earthchem.plot)
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Ternary plots
"""

from matplotlib import pyplot as plt
import pandas as pd
import ternary


def ternaryplot(df, ax=None, components=None, **kwargs):
    """
    Plots scatter ternary diagrams, using a wrapper around the
    python-ternary library (gh.com/marcharper/python-ternary).

    Parameters
    ----------
    df: pandas DataFrame
        Dataframe from which to draw data.
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    components: list, None
        Elements or compositional components to plot.
    """

    try:
        if not len(df.columns)==3:
            assert len(components)==3
        components = components or df.columns.values
    except:
        raise AssertionError('Please either suggest three elements or a 3-element dataframe.')

    # Some default values
    scale = kwargs.get('scale') or 100.
    figsize = kwargs.get('size') or 8.
    gridsize = kwargs.get('gridsize') or 10.
    fontsize = kwargs.get('fontsize') or 12.

    sty = {}
    sty['marker'] = kwargs.get('marker') or 'D'
    sty['color'] = kwargs.get('color') or kwargs.get('c') or '0.5'
    sty['label'] = kwargs.get('label') or None
    sty['alpha'] = kwargs.get('alpha') or kwargs.get('a') or 1.

    ax = ax or plt.subplots(1, figsize=(figsize, figsize* 3**0.5 * 0.5))[1]
    d1 = ax.__dict__.copy()
    
     # Checking if there's already a ternary axis
    tax = getattr(ax, 'tax', None) or ternary.figure(ax=ax, scale=scale)[1]

    # Set attribute for future reference
    ax.tax = tax

    points = df.loc[:, components].div(df.loc[:, components].sum(axis=1), axis=0).values * scale
    if points.any():
        tax.scatter(points, **sty)

    if sty['label'] is not None:
        tax.legend(frameon=False,)

    if not len(tax._labels.keys()):
        tax.bottom_axis_label(components[0], fontsize=fontsize)
        tax.right_axis_label(components[1], fontsize=fontsize)
        tax.left_axis_label(components[2], fontsize=fontsize)

        tax.gridlines(multiple=gridsize, color='k', alpha=0.5)
        tax.ticks(axis='lbr', linewidth=1, multiple=gridsize)
        tax.boundary(linewidth=1.0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])

    return tax
