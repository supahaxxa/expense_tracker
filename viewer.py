print("Loading . . .")

from datetime import datetime
import colorama
import os
try:
	import pandas as pd
except ModuleNotFoundError:
	print(colorama.Fore.RED + "\'pandas\' module not found.\nPlease install it using the command \'pip install pandas\'" + colorama.Fore.WHITE)
	quit()

def clear():
	os_dict = {"nt": "cls", "posix": "clear"}
	os.system(os_dict[os.name])

clear()

today = datetime.now()
date = str(today.year) + '-' + str(today.month).zfill(2)

try:
	ledger_df = pd.read_csv("ledger.csv", index_col=0).set_index("month")
except FileNotFoundError:
	print(colorama.Fore.RED + "FileNotFoundError: Record you are looking for doesn't exist." + colorama.Fore.RESET + "\nTry recording data using logger.py before.")
	quit()
except KeyError:
	print(colorama.Fore.RED + "KeyError: Record you are looking for doesn't exist." + colorama.Fore.RESET + "\nTry recording data using logger.py before.")
	quit()

print(ledger_df.loc[date])
