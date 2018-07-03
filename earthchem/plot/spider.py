""" file:   spider.py (earthchem.plot)
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Spider plots
"""


import pyrolite.plot as pplot
from pyrolite.geochem import common_elements


def spiderplot(*args, **kwargs):
    """
    Plots spidergrams for trace elements data.
    By using separate lines and scatterplots, values between two null-valued
    items are still presented. Might be able to speed up the lines
    with a matplotlib.collections.LineCollection

    Parameters
    ----------
    df: pandas DataFrame
        Dataframe from which to draw data.
    components: list, None
        Elements or compositional components to plot.
    ax: Matplotlib AxesSubplot, None
        The subplot to draw on.
    plot: boolean, True
        Whether to plot lines and markers.
    fill:
        Whether to add a patch representing the full range.
    style:
        Styling keyword arguments to pass to matplotlib.
    """
    return pplot.spiderplot(*args, **kwargs)
