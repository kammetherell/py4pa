import pandas as pd

def csv_to_utf8(file):
    df = pd.read_csv(
        file,
        encoding = 'latin'
    )

    fName = file[:-4] + '-reformatted.csv'

    df.to_csv(
        fName,
        index=False
    )

    print(f'{fName} created')

    return fName
