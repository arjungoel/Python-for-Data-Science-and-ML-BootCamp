import pandas as pd
import glob
import os

os.chdir("C:\Bitbucket\shared_scripts\AUDIT WORK")

extension = "csv"
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], sort=True)

combined_csv.to_csv("combined_csv.csv", index=False, encoding="utf-8-sig")
