print("Loading . . .")

from datetime import datetime
import os
import pandas as pd

def clear():
	if os.name == "nt":
		os.system("cls")
	elif os.name == "posix":
		os.system("clear")

clear()

today = datetime.now()
date = str(today.year) + '-' + str(today.month).zfill(2) + '-' + str(today.day).zfill(2)

ledger_df = pd.read_csv("ledger.csv", index_col=0).set_index("month")

print(ledger_df.loc[date[:7]])
