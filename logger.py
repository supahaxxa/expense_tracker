print("\nLoading . . .")

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

ledger_fields = ["month", "beverages", "b&l", "entertainment", "fares", "household", "others", "restaurant", "services", "snacks", "stationery", "utility"]
log_fields = ["date", "field", "content", "cost"]
today = datetime.now()

if not os.path.exists("logs.csv"):
	pd.DataFrame(columns=log_fields).to_csv("logs.csv")
if not os.path.exists("ledger.csv"):
	pd.DataFrame(columns=ledger_fields).to_csv("ledger.csv")

log_df = pd.read_csv("logs.csv", index_col=0)
ledger_df = pd.read_csv("ledger.csv", index_col=0).set_index("month")

message = ""
to_be_continued = False
while True:
	clear()
	if message:
		print(message)
		message = ""

	for serial, value in enumerate(ledger_fields[1:], start=1):
		print('[' + str(serial).zfill(2) + '] ' + value)

	prompt = input("\n>> ")
	if prompt == '':
		clear()
		break
	if prompt not in map(str, range(1, 12)):
		message = colorama.Fore.RED + "ValueError: Invalid value entered." + colorama.Fore.RESET + "\nPlease enter a number within the range 1 to 11."
		continue
	prompt = int(prompt)
	clear()
	print(ledger_fields[prompt] + '\n')

	while True:
		if message:
			clear()
			print(ledger_fields[prompt] + '\n')
			print(message)
			message = ""

		amount = input("[?] Enter the amount you have spent:\n\t>> ")
		if amount == '':
			clear()
			to_be_continued = True
			break
		if not amount.isdigit():
			message = colorama.Fore.RED + "ValueError: Invalid value entered." + colorama.Fore.RESET + "\nPlease enter a number."
			continue
		amount = int(amount)
		clear()
		print(ledger_fields[prompt], '\n', amount, '\n', sep='')
		break
	if to_be_continued:
		to_be_continued = False
		continue

	note = input("[?] Remarks:\n\t>> ")
	if note == '':
		clear()
		continue
	clear()
	print(ledger_fields[prompt], '\n', amount, '\n', note, '\n', sep='')

	date = str(today.year) + '-' + str(today.month).zfill(2) + '-' + str(today.day).zfill(2)
	try:
		ledger_df.loc[date[:7]][ledger_fields[prompt]] += amount
		ledger_df.loc[date[:7]]["total"] += amount
	except KeyError:
		ledger_df.loc[date[:7]] = [0 for i in range(len(ledger_fields))]
		ledger_df.loc[date[:7]][ledger_fields[prompt]] += amount
		ledger_df.loc[date[:7]]["total"] += amount
	log_df.loc[len(log_df)] = [date, ledger_fields[prompt], note, amount]

ledger_df.reset_index().to_csv("ledger.csv")
log_df.to_csv("logs.csv")
