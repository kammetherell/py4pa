import pandas as pd
import pkg_resources
from subprocess import call
from datetime import datetime

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

def upgradeAllPackages():
    packages = [dist.project_name for dist in pkg_resources.working_set]

    packages_to_ignore = [
        'pycurl',
        'pywin32'
    ]

    for p in packages_to_ignore:
        if (p in packages):
            packages.remove(p)
            print(f'Skipping {p}')

    call("pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade " + ' '.join(packages), shell=True)

def installPackage(package):
    try:
        call(f"pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org {package}", shell=True)
        print(f'{package} successfully installed')
    except Exception as e:
        print("Error - {}".format(e))

def getDateTimeStamp(time=True):
    now = datetime.now()
    stamp = str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2)
    if time:
        stamp = stamp + "_" + str(now.hour).zfill(2) + str(now.minute).zfill(2)
    return stamp