from pyrolite.geochem import tochem, common_elements, common_oxides
from pyrolite.util.text import titlecase
from pyrolite.normalisation import ReferenceCompositions


def cleanup_dataframe(df, normalize_to=None):
    """
    Simple dataframe cleanup: reformats and reorders columns.
    Normalises to a reference composition as necessary
    (e.g. try 'Chondrite_PON' or 'PM_PON').

    Parameters
    ----------
    df: pandas DataFrame
        Dataframe to clean up.
    normalize_to: pandas DataFrame
        Dataframe to clean up.
    """
    df.columns = df.columns.map(lambda x: titlecase(x, abbrv=['ID', 'IGSN']))
    df.columns = tochem(df.columns)
    majors = [i for i in common_oxides(output='str')
              if i in df.columns.values]
    traces = [i for i in common_elements(output='str')
              if i in df.columns.values]
    # Everything else, then majors, then traces
    df = df.loc[:, [i for i in df.columns if i not in majors+traces] + \
                   majors + traces]
    if normalize_to is not None:
        df = ReferenceCompositions()[normalize_to].normalize(df)
    return df
