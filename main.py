import flet

# global scope variables
references = {}
types = ["Beverages", "B&L", "Entertainment", "Household", "Others", "Restaurant", "Services", "Food", "Stationery", "Transport", "Utility"]
variables = {"buttonHeight": 40, "marginLeft": 20, "marginRight": 20, "marginTop": 30, "marginBottom": 30, "widgetSpacing": 10}

# helper functions to create some widgets in settings page
def section_header(title: str):
	return flet.Container(
		content=flet.Text(
			title.upper(),
			size=13,
			weight=flet.FontWeight.W_500,
			color="#6D6D72"
		),
		padding=flet.Padding.only(left=20, top=24, bottom=6)
	)

def divider():
	return flet.Divider(height=1, color="#E5E5EA", trailing_indent=0)

def card(*rows):
	children = []
	for i, row in enumerate(rows):
		children.append(row)
		if i < len(rows) - 1:
			children.append(divider())
	return flet.Container(
		content=flet.Column(children, spacing=0),
		border_radius=12,
		clip_behavior=flet.ClipBehavior.HARD_EDGE,
		margin=flet.Margin.symmetric(horizontal=0)
	)

def setting_row(icon: flet.IconData, icon_bg, label, key="", subtitle="", trailing=None, on_click=None):
	def _click(e):
		if on_click:
			on_click(e)

	icon_container = flet.Container(
		content=flet.Icon(icon, color="white", size=18),
		width=32,
		height=32,
		border_radius=8,
		bgcolor=icon_bg,
		alignment=flet.Alignment.CENTER,
	)

	text_ref = flet.Ref[flet.Text]()
	text_col = flet.Column(
		[
			flet.Text(label, size=16, color="#1C1C1E", weight=flet.FontWeight.W_400),
			*(
				[flet.Text(subtitle, size=13, color="#8E8E93", ref=text_ref)]
				if subtitle
				else []
			),
		],
		spacing=1,
		tight=True,
	)
	references[key] = text_ref

	row_content = flet.Row(
		[
			icon_container,
			flet.Container(content=text_col, expand=True, padding=flet.Padding.only(left=14)),
			trailing
			if trailing
			else flet.Icon(flet.Icons.CHEVRON_RIGHT, color="#C7C7CC", size=20),
		],
		vertical_alignment=flet.CrossAxisAlignment.CENTER,
	)

	return flet.Container(
		content=row_content,
		padding=flet.Padding.symmetric(horizontal=16, vertical=12),
		bgcolor="white",
		ink=True,
		on_click=_click,
	)

def add_record(amount, ftype, detail):
	try:
		with open(variables["applicationLogsPath"], 'r') as file:
			next_index_to_write = len(file.read().splitlines())
	except FileNotFoundError:
		next_index_to_write = 0

	today = flet.DatePicker().current_date.strftime("%Y%m%dT%H%M")
	line_to_write = f"{next_index_to_write},{today},{amount},{ftype},{detail}\n"

	try:
		with open(variables["applicationLogsPath"], 'a') as file:
			file.write(line_to_write)
	except FileNotFoundError:
		with open(variables["applicationLogsPath"], 'w') as file:
			file.write(line_to_write)

def on_click_record_yes(event: flet.Event):
	add_record(
		references["textfieldAmount"].current.value,
		types.index(references["dropdownType"].current.value),
		references["textfieldDetail"].current.value
	)

	references["textfieldAmount"].current.value = ""
	references["dropdownType"].current.value = None
	references["textfieldDetail"].current.value = ""
	event.page.pop_dialog()
	event.page.update()

def on_click_record(event: flet.Event):
	if not references["textfieldAmount"].current.value.isnumeric():
		references["errorAmount"].current.value = "ERROR: enter an integer"
	else:
		references["errorAmount"].current.value = ""
	if references["dropdownType"].current.value:
		references["errorType"].current.value = ""
	else:
		references["errorType"].current.value = "ERROR: please select a category"
	if references["textfieldDetail"].current.value:
		references["errorDetail"].current.value = ""
	else:
		references["errorDetail"].current.value = "ERROR: please enter the detail of your expenditure"

	str0 = ''.join([
		references["errorAmount"].current.value,
		references["errorType"].current.value,
		references["errorDetail"].current.value
	])
	if "ERROR" in str0:
		event.page.update()
		return

	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Confirmation"),
		content=flet.Text("Are you sure?"),
		actions=[
			flet.TextButton("Yes", on_click=on_click_record_yes),
			flet.TextButton("No", on_click=event.page.pop_dialog)
		],
		actions_alignment=flet.MainAxisAlignment.END
	))
	event.page.update()

def set_logs_path(event: flet.Event):
	variables["applicationLogsPath"] = references["logsFilePathField"].current.value
	references["applicationLogsPath"].current.value = references["logsFilePathField"].current.value
	event.page.pop_dialog()
	event.page.update()

def set_config_path(event: flet.Event):
	variables["applicationConfigPath"] = references["configFilePathField"].current.value
	references["applicationConfigPath"].current.value = references["configFilePathField"].current.value
	event.page.pop_dialog()
	event.page.update()

def set_button_height(event: flet.Event):
	variables["buttonHeight"] = int(references["buttonHeightField"].current.value)
	references["buttonHeight"].current.value = f"{references['buttonHeightField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def dialog_change_button_height(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set button height"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["buttonHeight"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Confirm", on_click=set_button_height)]
	))
	references["buttonHeightField"] = textfield_ref

def set_margin_left(event: flet.Event):
	variables["marginLeft"] = int(references["marginLeftField"].current.value)
	references["marginLeft"].current.value = f"{references['marginLeftField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def dialog_change_margin_left(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set left margin size"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["marginLeft"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Confirm", on_click=set_margin_left)]
	))
	references["marginLeftField"] = textfield_ref

def set_margin_right(event: flet.Event):
	variables["marginRight"] = int(references["marginRightField"].current.value)
	references["marginRight"].current.value = f"{references['marginRightField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def dialog_change_margin_right(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set right margin size"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["marginRight"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Confirm", on_click=set_margin_right)]
	))
	references["marginRightField"] = textfield_ref

def set_margin_top(event: flet.Event):
	variables["marginTop"] = int(references["marginTopField"].current.value)
	references["marginTop"].current.value = f"{references['marginTopField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def dialog_change_margin_top(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set top margin size"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["marginTop"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Confirm", on_click=set_margin_top)]
	))
	references["marginTopField"] = textfield_ref

def set_margin_bottom(event: flet.Event):
	variables["marginBottom"] = int(references["marginBottomField"].current.value)
	references["marginBottom"].current.value = f"{references['marginBottomField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def dialog_change_margin_bottom(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set bottom margin size"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["marginBottom"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Confirm", on_click=set_margin_bottom)]
	))
	references["marginBottomField"] = textfield_ref

def set_widget_spacing(event: flet.Event):
	variables["widgetSpacing"] = int(references["widgetSpacingField"].current.value)
	references["widgetSpacing"].current.value = f"{references['widgetSpacingField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def dialog_change_widget_spacing(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set space between widgets"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["widgetSpacing"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Confirm", on_click=set_widget_spacing)]
	))
	references["widgetSpacingField"] = textfield_ref

def dialog_change_logs_path(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set path"),
		content=flet.TextField(
			label="Path",
			border=flet.InputBorder.UNDERLINE,
			value=variables["applicationLogsPath"],
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_logs_path)]
	))
	references["logsFilePathField"] = textfield_ref

def dialog_change_config_path(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set path"),
		content=flet.TextField(
			label="Path",
			border=flet.InputBorder.UNDERLINE,
			value=variables["applicationConfigPath"],
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_config_path)]
	))
	references["configFilePathField"] = textfield_ref

def read_logs() -> list[list[str]]:
	try:
		with open(variables["applicationLogsPath"], 'r') as file:
			logs = file.read().strip('\n').split('\n')
	except FileNotFoundError:
		logs = ["0,19000101T0000,0,0,None"]

	return [*map(lambda x: x.split(','), logs)]

def edit_mode_off(event: flet.Event):
	event.control.parent.content = flet.Text(event.control.value, color="#000000")
	event.page.update()

def edit_mode_on(event: flet.Event):
	event.control.content = flet.TextField(
		value=event.control.content.value,
		border=flet.InputBorder.UNDERLINE,
		color="#000000",
		width=event.control.content.width,
		on_submit=edit_mode_off
	)
	event.page.update()

def build_logs_table(thead: list[str], tbody: list[list[str]]) -> flet.DataTable:
	head_row, body_rows = [], []
	for cell in thead:
		cell_control = flet.Text(cell, weight=flet.FontWeight.W_900)
		cell_control.color = flet.Colors.BLACK
		cell_control = flet.DataColumn(label=cell_control)
		head_row.append(cell_control)
	for row in tbody:
		table_row = []
		i = 0
		for cell in row:
			if i == 3:
				cell = types[int(cell)]
			cell_control = flet.Text(cell)
			cell_control.color = flet.Colors.BLACK
			cell_control = flet.DataCell(cell_control, on_double_tap=edit_mode_on, on_long_press=edit_mode_on)
			table_row.append(cell_control)
			i += 1
		body_rows.append(flet.DataRow(cells=table_row))

	table = flet.DataTable(
		column_spacing=10,
		columns=head_row,
		rows=body_rows
	)

	return table

def save_logs(event: flet.Event, save_path = str()):
	i = j = 0
	row, rows = [], []
	while True:
		if type(event.page.get_control(i)) == flet.DataCell:
			if j % 5 == 3:
				row.append(f"{types.index(event.page.get_control(i).content.value)}")
			elif j % 5 == 4:
				row.append(event.page.get_control(i).content.value)
				rows.append(','.join(row) + '\n')
				row = []
			else:
				row.append(event.page.get_control(i).content.value)
			j += 1
		elif type(event.page.get_control(i)) == flet.DataTable:
			break
		i += 1

	if save_path:
		with open(f"{save_path}/logs.csv", 'w') as file:
			file.write(''.join(rows))
	else:
		with open(variables["applicationLogsPath"], 'w') as file:
			file.write(''.join(rows))

def save_config(event: flet.Event, save_path = str()):
	lines_to_write = [f"{key},{value}\n" for key, value in variables.items()]

	if save_path:
		with open(f"{save_path}/config.csv", 'w') as file:
			file.write(''.join(lines_to_write))
	else:
		with open(variables["applicationConfigPath"], 'w') as file:
			file.write(''.join(lines_to_write))

def time_format_transform(yyyymm: str):
	months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	if len(yyyymm) == 6:
		new_format = yyyymm[:4] + ", " + months_list[int(yyyymm[4:])-1]
	else:
		new_format = yyyymm[:4] + str(months_list.index(yyyymm[6:])+1).zfill(2)
	return new_format

def aggregate_logs() -> dict:
	default_pairs = {fi: 0 for fi in types}
	logs = read_logs()
	result = {"190001": default_pairs}

	for row in logs:
		month_key = row[1][:6]
		result.setdefault(month_key, default_pairs.copy())
		result[month_key][types[int(row[3])]] += int(row[2])

	return result

def build_summary_table(month_data: dict) -> flet.DataTable:
	table_columns = []
	table_rows = []
	total = 0
	for dp in ["CATEGORY", "AMOUNT"]:
		dpo = flet.Text(dp)
		dpo.weight = flet.FontWeight.W_900
		dpo.color = flet.Colors.BLACK
		dpo = flet.DataColumn(label=dpo)
		table_columns.append(dpo)
	for key, value in month_data.items():
		total += int(value)
		c1 = flet.Text(key)
		c2 = flet.Text(value)
		c1.color = c2.color = flet.Colors.BLACK
		c1, c2 = flet.DataCell(c1), flet.DataCell(c2)
		table_rows.append(flet.DataRow(cells=[c1, c2]))
	c1, c2 = flet.Text("Total"), flet.Text(str(total))
	c1.color = c2.color = flet.Colors.BLACK
	c1, c2 = flet.DataCell(c1), flet.DataCell(c2)
	table_rows.append(flet.DataRow(cells=[c1, c2]))

	table = flet.DataTable(
		column_spacing=10,
		columns=table_columns,
		rows=table_rows
	)

	return table

def change_summary_table(event: flet.Event):
	month = time_format_transform(event.control.value)
	event.page.controls[0].controls[2] = build_summary_table(aggregate_logs()[month])
	event.page.update()

async def export_logs(event: flet.Event):
	logs_file_path = await flet.FilePicker().get_directory_path() or ""
	save_logs(event, logs_file_path)

async def export_config(event: flet.Event):
	config_file_path = await flet.FilePicker().get_directory_path() or ""
	save_config(event, config_file_path)

# main page building functions
def build_record_page() -> flet.ListView:
	ref_amount, ref_error_amount = flet.Ref[flet.TextField](), flet.Ref[flet.Text]()
	text_amount = flet.Text(
		color=flet.Colors.BLACK,
		value="How much have you spent?"
	)
	textfield_amount = flet.TextField(
		border=flet.InputBorder.UNDERLINE,
		color=flet.Colors.BLACK,
		label="Amount",
		ref=ref_amount
	)
	text_amount_error = flet.Text(
		color=flet.Colors.RED,
		ref=ref_error_amount,
		value=""
	)
	references["textfieldAmount"], references["errorAmount"] = ref_amount, ref_error_amount

	ref_type, ref_error_type = flet.Ref[flet.Dropdown](), flet.Ref[flet.Text]()
	text_type = flet.Text(
		color=flet.Colors.BLACK,
		value="Which category you spent on?"
	)
	dropdown_type = flet.Dropdown(
		color="#000000",
		label="Type",
		menu_height=300,
		options=[*map(lambda x: flet.dropdown.Option(x), types)],
		ref=ref_type
	)
	text_type_error = flet.Text(
		color=flet.Colors.RED,
		ref=ref_error_type,
		value=""
	)
	references["dropdownType"], references["errorType"] = ref_type, ref_error_type

	ref_detail, ref_error_detail = flet.Ref[flet.TextField](), flet.Ref[flet.Text]()
	text_detail = flet.Text(
		color=flet.Colors.BLACK,
		value="Where have you spent?"
	)
	textfield_detail = flet.TextField(
		border=flet.InputBorder.UNDERLINE,
		color=flet.Colors.BLACK,
		label="Detail",
		ref=ref_detail
	)
	text_detail_error = flet.Text(
		color=flet.Colors.RED,
		ref=ref_error_detail,
		value=""
	)
	references["textfieldDetail"], references["errorDetail"] = ref_detail, ref_error_detail

	button_record = flet.Button(
		bgcolor="#36618E",
		color="#FFFFFF",
		content="Record",
		height=variables["buttonHeight"],
		on_click=on_click_record,
		style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=8))
	)

	page_record = [
		text_amount,
		textfield_amount,
		text_amount_error,
		text_type,
		dropdown_type,
		text_type_error,
		text_detail,
		textfield_detail,
		text_detail_error,
		flet.Container(height=30),
		button_record
	]

	return flet.ListView(
		page_record,
		spacing=variables["widgetSpacing"],
		expand_loose=True,
		margin=flet.Margin.only(
			left=variables["marginLeft"],
			right=variables["marginRight"],
			top=variables["marginTop"],
			bottom=variables["marginBottom"]
		)
	)

def build_query_page(month = "190001"):
	label_months = flet.Text(
		color=flet.Colors.BLACK,
		value="Select a month"
	)
	dropdown_months = flet.Dropdown(
		color=flet.Colors.BLACK,
		label="Month",
		on_select=change_summary_table,
		options=[*map(lambda a: flet.dropdown.Option(time_format_transform(a)), aggregate_logs().keys())]
	)
	dropdown_months.options[0].disabled = True
	dropdown_months.value = month

	table_summary = build_summary_table(aggregate_logs()[dropdown_months.value])

	page_query = [
		label_months,
		dropdown_months,
		table_summary
	]

	return flet.ListView(
		page_query,
		spacing=variables["widgetSpacing"],
		expand_loose=True,
		margin=flet.Margin.only(
			left=variables["marginLeft"],
			right=variables["marginRight"],
			top=variables["marginTop"],
			bottom=variables["marginBottom"]
		)
	)

def build_logs_page():
	button_save_logs = flet.Button(
		bgcolor="#36618E",
		color="#FFFFFF",
		content="Save",
		expand=True,
		height=variables["buttonHeight"],
		icon=flet.Icons.SAVE,
		on_click=save_logs,
		style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=8))
	)
	button_export_logs = flet.Button(
		bgcolor="#36618E",
		color="#FFFFFF",
		content="Export",
		expand=True,
		height=variables["buttonHeight"],
		icon=flet.Icons.FILE_UPLOAD,
		on_click=export_logs,
		style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=8))
	)
	table_logs = flet.Row(
		controls=[build_logs_table(["SL", "TIME", "AMOUNT", "TYPE", "DETAIL"], read_logs())],
		scroll=flet.ScrollMode.AUTO
	)

	page_logs = [
		flet.Row(controls=[button_save_logs, button_export_logs], intrinsic_height=True),
		flet.ListView([table_logs], expand=True)
	]

	return flet.Column(
		controls=page_logs,
		spacing=variables["widgetSpacing"],
		expand=True,
		margin=flet.Margin.only(
			left=variables["marginLeft"],
			right=variables["marginRight"],
			top=variables["marginTop"],
			bottom=variables["marginBottom"]
		)
	)

def build_settings_page():
	button_save_config = flet.Button(
		bgcolor="#36618E",
		color="#FFFFFF",
		content="Save",
		expand=True,
		height=variables["buttonHeight"],
		icon=flet.Icons.SAVE,
		on_click=save_config,
		style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=8))
	)
	button_export_config = flet.Button(
		bgcolor="#36618E",
		color="#FFFFFF",
		content="Export",
		expand=True,
		height=variables["buttonHeight"],
		icon=flet.Icons.FILE_UPLOAD,
		on_click=export_config,
		style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=8))
	)

	interface_section = flet.Column([
		section_header("Interface"),
		card(
			setting_row(
				flet.Icons.STRAIGHTEN, "#34C759", "Button height",
				key="buttonHeight",
				subtitle=f"{variables['buttonHeight']} px",
				on_click=dialog_change_button_height
			),
			setting_row(
				flet.Icons.STRAIGHTEN, "#007AFF", "Margin - left",
				key="marginLeft",
				on_click=dialog_change_margin_left,
				subtitle=f"{variables['marginLeft']} px"
			),
			setting_row(
				flet.Icons.STRAIGHTEN, "#FF9500", "Margin - right",
				key="marginRight",
				on_click=dialog_change_margin_right,
				subtitle=f"{variables['marginRight']} px"
			),
			setting_row(
				flet.Icons.STRAIGHTEN, "#FF3B30", "Margin - top",
				key="marginTop",
				on_click=dialog_change_margin_top,
				subtitle=f"{variables['marginTop']} px"
			),
			setting_row(
				flet.Icons.STRAIGHTEN, "#636366", "Margin - bottom",
				key="marginBottom",
				on_click=dialog_change_margin_bottom,
				subtitle=f"{variables['marginBottom']} px"
			),
			setting_row(
				flet.Icons.STRAIGHTEN, "#5856D6", "Widget spacing",
				key="widgetSpacing",
				subtitle=f"{variables['widgetSpacing']} px",
				on_click=dialog_change_widget_spacing
			)
		)
	])

	system_section = flet.Column([
		section_header("Settings"),
		card(
			setting_row(
				flet.Icons.LANGUAGE, "#FF2D55", "Logs file path",
				key="applicationLogsPath",
				subtitle=variables["applicationLogsPath"],
				on_click=dialog_change_logs_path
			),
			setting_row(
				flet.Icons.LANGUAGE, "#30B0C7", "Config file path",
				key="applicationConfigPath",
				subtitle=variables["applicationConfigPath"],
				on_click=dialog_change_config_path
			)
		)
	])

	page_settings = [
		flet.Row(controls=[button_save_config, button_export_config], intrinsic_height=True),
		flet.ListView([interface_section, system_section], expand=True)
	]

	return flet.Column(
		controls=page_settings,
		spacing=variables["widgetSpacing"],
		expand=True,
		margin=flet.Margin.only(
			left=variables["marginLeft"],
			right=variables["marginRight"],
			top=variables["marginTop"],
			bottom=variables["marginBottom"]
		)
	)

# function to facilitate page navigation
def change_page(event: flet.Event):
	idn = event.page.navigation_bar.selected_index
	if idn == 0:
		event.page.clean()
		event.page.add(build_record_page())
	elif idn == 1:
		event.page.clean()
		event.page.add(build_query_page())
	elif idn == 2:
		event.page.clean()
		event.page.add(build_logs_page())
	else:
		event.page.clean()
		event.page.add(build_settings_page())

	event.page.update()

async def main(page: flet.Page):
	storage_paths = flet.StoragePaths()

	# code block to get the allocated Documents directory for the application
	try:
		value = await storage_paths.get_application_documents_directory()
	except flet.FletUnsupportedPlatformException as e:
		value = f"Not supported: {e}"
	except Exception as e:
		value = f"Error: {e}"
	else:
		if isinstance(value, list):
			value = ", ".join(value)
		elif value is None:
			value = "Unavailable"
	variables["applicationLogsPath"] = f"{value}/logs.csv"
	variables["applicationConfigPath"] = f"{value}/config.csv"

	# code block to load the saved application configuration variables
	try:
		with open(variables['applicationConfigPath'], 'r') as file:
			lines = file.read().strip().split('\n')
		for variable in lines:
			varname, val = variable.split(',')
			if val.isnumeric():
				variables[varname] = int(val)
			else:
				variables[varname] = val
	except FileNotFoundError:
		pass

	# basic setup of the window
	page.title = "Expense Tracker"
	page.bgcolor = "#F8F9FF"

	page.add(build_record_page())

	page.navigation_bar = flet.NavigationBar(
		destinations=[
			flet.NavigationBarDestination(icon=flet.Icons.EDIT, label="Record"),
			flet.NavigationBarDestination(icon=flet.Icons.SEARCH, label="Query"),
			flet.NavigationBarDestination(icon=flet.Icons.DESCRIPTION, label="Logs"),
			flet.NavigationBarDestination(icon=flet.Icons.SETTINGS, label="Settings")
		],
		on_change=change_page
	)
	page.update()

flet.run(main)
