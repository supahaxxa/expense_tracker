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

ledger_fields = ["month", "beverages", "b&l", "entertainment", "fares", "household", "others", "restaurant", "services", "snacks", "stationery", "utility"]
log_fields = ["date", "field", "content", "cost"]
today = datetime.now()

if not os.path.exists("logs.csv"):
	pd.DataFrame(columns=log_fields).to_csv("logs.csv")
if not os.path.exists("ledger.csv"):
	pd.DataFrame(columns=ledger_fields).to_csv("ledger.csv")

log_df = pd.read_csv("logs.csv", index_col=0)
ledger_df = pd.read_csv("ledger.csv", index_col=0).set_index("month")

while True:
	clear()

	for serial, value in enumerate(ledger_fields[1:], start=1):
		print('[' + str(serial).zfill(2) + ']' + value)

	prompt = input()
	if prompt == '':
		clear()
		break
	prompt = int(prompt)
	clear()
	print(ledger_fields[prompt] + '\n')

	amount = input("[?] Enter the amount you have spent:\n\t>> ")
	if amount == '':
		clear()
		continue
	amount = int(amount)
	clear()
	print(ledger_fields[prompt], '\n', amount, '\n', sep='')

	note = input("[?] Remarks:\n\t>> ")
	if note == '':
		clear()
		continue
	clear()
	print(ledger_fields[prompt], '\n', amount, '\n', note, '\n', sep='')

	print("Storing input . . .")

	date = str(today.year) + '-' + str(today.month).zfill(2) + '-' + str(today.day).zfill(2)
	try:
		ledger_df.loc[date[:7]][ledger_fields[prompt]] += amount
		ledger_df.loc[date[:7]]["total"] += amount
	except KeyError:
		ledger_df.loc[date[:7]] = [0 for i in range(len(ledger_fields))]
		ledger_df.loc[date[:7]][ledger_fields[prompt]] += amount
		ledger_df.loc[date[:7]]["total"] += amount
	log_df.loc[len(log_df)] = [date, ledger_fields[prompt], note, amount]

	#sleep(2)
	print("Naahhh, I'm kidding. It didn't take this long. :D")
	#sleep(1)

ledger_df.reset_index().to_csv("ledger.csv")
log_df.to_csv("logs.csv")
