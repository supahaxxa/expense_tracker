import flet

references = {}
types = ["Beverages", "B&L", "Entertainment", "Household", "Others", "Restaurant", "Services", "Snacks", "Stationery",
	"Transport", "Utility"]
variables = {
	"recordButtonHeight": 40,
	"recordMarginTop": 40,
	"recordMarginLeft": 20,
	"recordMarginBottom": 30,
	"recordMarginRight": 20,
	"settingsMarginTop": 30,
	"settingsMarginLeft": 20,
	"settingsMarginBottom": 30,
	"settingsMarginRight": 20,
	"spacingOverButtonGroup": 30,
	"widgetSpacing": 10
}

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
	"""Wrap rows in a rounded white card with dividers."""
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
		with open(f"{variables['applicationDocumentsDirectory']}/logs.csv", 'r') as file:
			next_index_to_write = len(file.read().splitlines())
	except FileNotFoundError:
		next_index_to_write = 0

	today = flet.DatePicker().current_date.strftime("%Y%m%dT%H%M")
	line_to_write = f"{next_index_to_write},{today},{amount},{ftype},{detail}\n"

	try:
		with open(f"{variables['applicationDocumentsDirectory']}/logs.csv", 'a') as file:
			file.write(line_to_write)
	except FileNotFoundError:
		with open(f"{variables['applicationDocumentsDirectory']}/logs.csv", 'w') as file:
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

async def on_click_quit(event: flet.Event):
	await event.page.window.destroy()

def update_config(event: flet.Event):
	lines_to_write = [f"{key},{value}\n" for key, value in variables.items()]

	with open(f"{variables['applicationDocumentsDirectory']}/config.csv", 'w') as file:
		file.write(''.join(lines_to_write))

def set_io_path(event: flet.Event):
	variables["applicationDocumentsDirectory"] = references["fileIOPathField"].current.value
	references["fileIOPath"].current.value = references["fileIOPathField"].current.value
	event.page.pop_dialog()
	event.page.update()

def set_record_margin_top(event: flet.Event):
	variables["recordMarginTop"] = int(references["recordMarginTopField"].current.value)
	references["recordMarginTop"].current.value = f"{references['recordMarginTopField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def set_record_margin_left(event: flet.Event):
	variables["recordMarginLeft"] = int(references["recordMarginLeftField"].current.value)
	references["recordMarginLeft"].current.value = f"{references['recordMarginLeftField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def set_record_margin_bottom(event: flet.Event):
	variables["recordMarginBottom"] = int(references["recordMarginBottomField"].current.value)
	references["recordMarginBottom"].current.value = f"{references['recordMarginBottomField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def set_record_margin_right(event: flet.Event):
	variables["recordMarginRight"] = int(references["recordMarginRightField"].current.value)
	references["recordMarginRight"].current.value = f"{references['recordMarginRightField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def set_record_button_height(event: flet.Event):
	variables["recordButtonHeight"] = int(references["recordButtonHeightField"].current.value)
	references["recordButtonHeight"].current.value = f"{references['recordButtonHeightField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def set_widget_spacing(event: flet.Event):
	variables["widgetSpacing"] = int(references["widgetSpacingField"].current.value)
	references["widgetSpacing"].current.value = f"{references['widgetSpacingField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def set_spacing_over_button_group(event: flet.Event):
	variables["spacingOverButtonGroup"] = int(references["spacingOverButtonGroupField"].current.value)
	references["spacingOverButtonGroup"].current.value = f"{references['spacingOverButtonGroupField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def set_settings_margin_top(event: flet.Event):
	variables["settingsMarginTop"] = int(references["settingsMarginTopField"].current.value)
	references["settingsMarginTop"].current.value = f"{references['settingsMarginTopField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def set_settings_margin_left(event: flet.Event):
	variables["settingsMarginLeft"] = int(references["settingsMarginLeftField"].current.value)
	references["settingsMarginLeft"].current.value = f"{references['settingsMarginLeftField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def set_settings_margin_bottom(event: flet.Event):
	variables["settingsMarginBottom"] = int(references["settingsMarginBottomField"].current.value)
	references["settingsMarginBottom"].current.value = f"{references['settingsMarginBottomField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def set_settings_margin_right(event: flet.Event):
	variables["settingsMarginRight"] = int(references["settingsMarginRightField"].current.value)
	references["settingsMarginRight"].current.value = f"{references['settingsMarginRightField'].current.value} px"
	event.page.pop_dialog()
	event.page.update()

def dialog_change_settings_margin_right(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set margin"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["settingsMarginRight"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_settings_margin_right)]
	))
	references["settingsMarginRightField"] = textfield_ref

def dialog_change_settings_margin_bottom(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set margin"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["settingsMarginBottom"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_settings_margin_bottom)]
	))
	references["settingsMarginBottomField"] = textfield_ref

def dialog_change_settings_margin_left(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set margin"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["settingsMarginLeft"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_settings_margin_left)]
	))
	references["settingsMarginLeftField"] = textfield_ref

def dialog_change_settings_margin_top(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set margin"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["settingsMarginTop"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_settings_margin_top)]
	))
	references["settingsMarginTopField"] = textfield_ref

def dialog_change_spacing_over_button_group(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set spacing"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["spacingOverButtonGroup"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_spacing_over_button_group)]
	))
	references["spacingOverButtonGroup"] = textfield_ref

def dialog_change_widget_spacing(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set spacing"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["widgetSpacing"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_widget_spacing)]
	))
	references["widgetSpacingField"] = textfield_ref

def dialog_change_record_button_height(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set height"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["recordButtonHeight"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_record_button_height)]
	))
	references["recordButtonHeightField"] = textfield_ref

def dialog_change_record_margin_right(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set margin"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["recordMarginRight"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_record_margin_right)]
	))
	references["recordMarginRightField"] = textfield_ref

def dialog_change_record_margin_bottom(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set margin"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["recordMarginBottom"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_record_margin_bottom)]
	))
	references["recordMarginBottomField"] = textfield_ref

def dialog_change_record_margin_left(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set margin"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["recordMarginLeft"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_record_margin_left)]
	))
	references["recordMarginLeftField"] = textfield_ref

def dialog_change_record_margin_top(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set margin"),
		content=flet.TextField(
			label="Value",
			border=flet.InputBorder.UNDERLINE,
			value=str(variables["recordMarginTop"]),
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_record_margin_top)]
	))
	references["recordMarginTopField"] = textfield_ref

def dialog_change_io_path(event: flet.Event):
	textfield_ref = flet.Ref[flet.TextField]()
	event.page.show_dialog(flet.AlertDialog(
		modal=True,
		title=flet.Text("Set path"),
		content=flet.TextField(
			label="Path",
			border=flet.InputBorder.UNDERLINE,
			value=f"{variables['applicationDocumentsDirectory']}",
			ref=textfield_ref
		),
		actions=[flet.TextButton("Set", on_click=set_io_path)]
	))
	references["fileIOPathField"] = textfield_ref

def read_logs() -> list[list[str]]:
	with open(f"{variables['applicationDocumentsDirectory']}/logs.csv", 'r') as file:
		logs = file.read().strip('\n').split('\n')

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
		cell_control = flet.Text(cell)
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

def save_logs(event: flet.Event):
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

	with open(f"{variables['applicationDocumentsDirectory']}/logs.csv", 'w') as file:
		file.write(''.join(rows))

async def main(page: flet.Page):
	# ── Initializing system ────────────────────────────────
	storage_paths = flet.StoragePaths()

	for label, method in [
		("applicationCacheDirectory", storage_paths.get_application_cache_directory),
		("applicationDocumentsDirectory", storage_paths.get_application_documents_directory),
		("applicationSupportDirectory", storage_paths.get_application_support_directory),
		("downloadsDirectory", storage_paths.get_downloads_directory),
		("externalCacheDirectories", storage_paths.get_external_cache_directories),
		("externalStorageDirectories", storage_paths.get_external_storage_directories),
		("libraryDirectory", storage_paths.get_library_directory),
		("externalStorageDirectory", storage_paths.get_external_storage_directory),
		("temporaryDirectory", storage_paths.get_temporary_directory),
		("consoleLogFilename", storage_paths.get_console_log_filename),
	]:
		try:
			value = await method()
		except flet.FletUnsupportedPlatformException as e:
			value = f"Not supported: {e}"
		except Exception as e:
			value = f"Error: {e}"
		else:
			if isinstance(value, list):
				value = ", ".join(value)
			elif value is None:
				value = "Unavailable"
		variables[label] = value

	try:
		with open(f"{variables['applicationDocumentsDirectory']}/config.csv", 'r') as file:
			lines = file.read().strip().split('\n')
		for variable in lines:
			varname, val = variable.split(',')
			if val.isnumeric():
				variables[varname] = int(val)
			else:
				variables[varname] = val
	except FileNotFoundError:
		pass

	page.title = "Expense Tracker"
	page.bgcolor = "#F8F9FF"
	page.window.width, page.window.height = 460, 950

	# ── Record section ─────────────────────────────────────
	ref_amount, ref_error_amount = flet.Ref[flet.TextField](), flet.Ref[flet.Text]()
	text_amount = flet.Text("How much have you spent?", color=flet.Colors.BLACK)
	textfield_amount = flet.TextField(label="Amount", border=flet.InputBorder.UNDERLINE, color=flet.Colors.BLACK,
		ref=ref_amount)
	text_amount_error = flet.Text("", color=flet.Colors.RED, ref=ref_error_amount)
	references["textfieldAmount"], references["errorAmount"] = ref_amount, ref_error_amount

	ref_type, ref_error_type = flet.Ref[flet.Dropdown](), flet.Ref[flet.Text]()
	text_type = flet.Text("Which category you spent on?", color=flet.Colors.BLACK)
	dropdown_type = flet.Dropdown(label="Type", color="#000000", menu_height=300,
		options=[*map(lambda x: flet.dropdown.Option(x), types)], ref=ref_type)
	text_type_error = flet.Text("", color=flet.Colors.RED, ref=ref_error_type)
	references["dropdownType"], references["errorType"] = ref_type, ref_error_type

	ref_detail, ref_error_detail = flet.Ref[flet.TextField](), flet.Ref[flet.Text]()
	text_detail = flet.Text("Where have you spent?", color=flet.Colors.BLACK)
	textfield_detail = flet.TextField(label="Detail", border=flet.InputBorder.UNDERLINE, color=flet.Colors.BLACK,
		ref=ref_detail)
	text_detail_error = flet.Text("", color=flet.Colors.RED, ref=ref_error_detail)
	references["textfieldDetail"], references["errorDetail"] = ref_detail, ref_error_detail

	button_record = flet.Button("Record", bgcolor="#36618E", color="#FFFFFF", height=variables["recordButtonHeight"],
		on_click=on_click_record)
	button_quit = flet.Button("Quit", bgcolor="#EA4335", color="#FFFFFF", height=variables["recordButtonHeight"],
		on_click=on_click_quit)

	# ── Logs section ───────────────────────────────────────
	button_save_logs = flet.Button("Save Logs", icon=flet.Icons.SAVE, bgcolor="#36618E", color="#FFFFFF", height=40,
		on_click=save_logs)
	table_logs = flet.Row(
		scroll=flet.ScrollMode.AUTO,
		controls=[build_logs_table(["SL", "TIME", "AMOUNT", "TYPE", "DETAIL"], read_logs())]
	)

	# ── Settings section ───────────────────────────────────
	record_section = flet.Column(
		[
			section_header("Record"),
			card(
				setting_row(
					flet.Icons.LANGUAGE, "#34C759", "File I/O Path",
					key="fileIOPath",
					subtitle=f"{variables['applicationDocumentsDirectory']}",
					on_click=dialog_change_io_path
				),
				setting_row(
					flet.Icons.STRAIGHTEN, "#007AFF", "Margin Top",
					key="recordMarginTop",
					subtitle=f"{variables['recordMarginTop']} px",
					on_click=dialog_change_record_margin_top
				),
				setting_row(
					flet.Icons.STRAIGHTEN, "#FF9500", "Margin Left",
					key="recordMarginLeft",
					subtitle=f"{variables['recordMarginLeft']} px",
					on_click=dialog_change_record_margin_left
				),
				setting_row(
					flet.Icons.STRAIGHTEN, "#FF3B30", "Margin Bottom",
					key="recordMarginBottom",
					subtitle=f"{variables['recordMarginBottom']} px",
					on_click=dialog_change_record_margin_bottom
				),
				setting_row(
					flet.Icons.STRAIGHTEN, "#636366", "Margin Right",
					key="recordMarginRight",
					subtitle=f"{variables['recordMarginRight']} px",
					on_click=dialog_change_record_margin_right
				),
				setting_row(
					flet.Icons.STRAIGHTEN, "#5856D6", "Button Height",
					key="recordButtonHeight",
					subtitle=f"{variables['recordButtonHeight']} px",
					on_click=dialog_change_record_button_height
				),
				setting_row(
					flet.Icons.STRAIGHTEN, "#FF2D55", "Widget Spacing",
					key="widgetSpacing",
					subtitle=f"{variables['widgetSpacing']} px",
					on_click=dialog_change_widget_spacing
				),
				setting_row(
					flet.Icons.STRAIGHTEN, "#FF3B30", "Spacing over Button Group",
					key="spacingOverButtonGroup",
					subtitle=f"{variables['spacingOverButtonGroup']} px",
					on_click=dialog_change_spacing_over_button_group
				)
			),
		],
		spacing=0,
	)

	settings_section = flet.Column(
		[
			section_header("Settings"),
			card(
				setting_row(
					flet.Icons.STRAIGHTEN, "#30B0C7", "Margin Top",
					key="settingsMarginTop",
					subtitle=f"{variables['settingsMarginTop']} px",
					on_click=dialog_change_settings_margin_top
				),
				setting_row(
					flet.Icons.STRAIGHTEN, "#34C759", "Margin Left",
					key="settingsMarginLeft",
					subtitle=f"{variables['settingsMarginLeft']} px",
					on_click=dialog_change_settings_margin_left
				),
				setting_row(
					flet.Icons.STRAIGHTEN, "#007AFF", "Margin Bottom",
					key="settingsMarginBottom",
					subtitle=f"{variables['settingsMarginBottom']} px",
					on_click=dialog_change_settings_margin_bottom
				),
				setting_row(
					flet.Icons.STRAIGHTEN, "#FF9500", "Margin Right",
					key="settingsMarginRight",
					subtitle=f"{variables['settingsMarginRight']} px",
					on_click=dialog_change_settings_margin_right
				)
			)
		]
	)

	button_save_settings = flet.Button("Save Settings", icon=flet.Icons.SAVE, bgcolor="#36618E", color="#FFFFFF",
		height=40, on_click=update_config)

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
		button_record,
		button_quit
	]
	page_logs = [
		button_save_logs,
		table_logs
	]
	page_settings = [
		record_section,
		settings_section,
		button_save_settings
	]

	page.add(flet.ListView(
		page_record,
		spacing=variables["widgetSpacing"],
		expand=True,
		margin=flet.Margin.only(
			left=variables["recordMarginLeft"],
			right=variables["recordMarginRight"],
			top=variables["recordMarginTop"],
			bottom=variables["recordMarginBottom"]
		)
	))

	def change_page(event: flet.Event):
		idn = event.page.navigation_bar.selected_index
		if idn == 0:
			event.page.clean()
			event.page.add(flet.ListView(
				page_record,
				spacing=variables["widgetSpacing"],
				expand=True,
				margin=flet.Margin.only(
					left=variables["recordMarginLeft"],
					right=variables["recordMarginRight"],
					top=variables["recordMarginTop"],
					bottom=variables["recordMarginBottom"]
				)
			))
		elif idn == 1:
			event.page.clean()
			event.page.add(flet.ListView(
				page_logs,
				spacing=variables["widgetSpacing"],
				expand=True,
				margin=flet.Margin.only(
					left=20,
					right=20,
					top=30,
					bottom=30
				)
			))
		else:
			event.page.clean()
			event.page.add(flet.ListView(
				page_settings,
				spacing=variables["widgetSpacing"],
				expand=True,
				margin=flet.Margin.only(
					left=variables["settingsMarginLeft"],
					right=variables["settingsMarginRight"],
					top=variables["settingsMarginTop"],
					bottom=variables["settingsMarginBottom"]
				)
			))

		event.page.update()

	page.navigation_bar = flet.NavigationBar(
		destinations=[
			flet.NavigationBarDestination(icon=flet.Icons.EDIT_OUTLINED, label="Record"),
			flet.NavigationBarDestination(icon=flet.Icons.SD_STORAGE_OUTLINED, label="Logs"),
			flet.NavigationBarDestination(icon=flet.Icons.SETTINGS, label="Settings")
		],
		on_change=change_page
	)

	page.update()

flet.run(main)
