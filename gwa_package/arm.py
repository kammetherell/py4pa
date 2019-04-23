import pandas as pd

def concat_fields(df, fields):
    """Creates the Concatenation fields for ARM

    Parameters
    ----------
    df: Pandas DataFrame
        DataFrame containing the source Data

    fields: List of Tuples
        List of Tuples containing the pairs of fields to be combined together. Each tuple should only length 2

    Returns
    -------
    df:
        Dataframe with new fields added
    """
    print(f'Creating {len(fields)} new fields')

    for field in fields:
        new_field = field[0] + '_' + field[1]
        df[new_field] = df[field[0]] + '_' + df[field[1]]
        print(f'{new_field} created')

    return df
