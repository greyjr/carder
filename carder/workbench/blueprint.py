from flask import Blueprint
from flask import render_template, request
import xlrd
import os


workbench = Blueprint('workbench', __name__, template_folder='templates')


@workbench.route('/')
def index():
	""" index.func  get names of workbook & worksheet from bingo.html
			+ build list of all lines of excel table
			+ build list of card with size
			+ check valid card
			+ mark valid card in card_list
			+ prepear context
			+ call render page"""

	filename = request.args.get('book')
	sheet = request.args.get('worksheet')
	workbook = xlrd.open_workbook('./files/excel/{}'.format(filename))
	#os.remove('./files/excel/{}'.format(filename))
	current_sheet = workbook.sheet_by_name(str(request.args.get('worksheet'))) 		

	raw_table, card_list = initial_page(current_sheet)		

	""" card_list: 	{sheet.row(int) :  [card_number(str), card_size(int), agregat_name(str), agregat_photo(str), card_is_valid]}
		raw_table:	[ energy_type, point, location, value_energy, photo, block, lock, area, folder of photo]	"""

	context = []
	for card_line, card_info in card_list.items():

		context_line = card_info[:]
		card_is_valid = card_info[4]
		context_line.extend(raw_table[card_line])
		context.append(context_line)
		for line in range(card_info[1] - 1):
			context_line = ['', '', '', '', card_is_valid]
			context_line.extend(raw_table[card_line + line + 1])
			context.append(context_line)

	return render_template('workbench/index.html', context=context)

# -----------------------------------------------------------------------------------------------------
def valid_cell(cell_value):
	return str(int(cell_value)) if type(cell_value) == float else cell_value


def initial_page(current_sheet):


	raw_table = [['header line']]
	card_list = {}
	current_photo_folder = ""

	for line_number in range(1,current_sheet.nrows):			# nrows = last row in excell sheet	
		line = current_sheet.row_values(line_number, 0, 14)		# take line
		line.extend(['']*(14 - len(line)))
		line_usefull = [valid_cell(line[i]) for i in [2,4,5,6,8,9,10,12,13]]
		raw_table.append(line_usefull)							# fill table from sheet
		
		if raw_table[line_number][8]:							# 
			current_photo_folder = raw_table[line_number][8]	# if photo's folder exist, update current photo's folder
		else:
			raw_table[line_number][8] = current_photo_folder	# if photo's folder cell is empty, take info from previous line

		if line[1]:												#                 ...and is_valid_line(line)
			card_list[line_number] = [valid_cell(line[0]), 1, line[1], valid_cell(line[7]), True]	
																# fill card list by card_number, card_size,
																# agregat_name, agregat_photo, card_is_valid=1	
	
	merged_cells = current_sheet.merged_cells					# all merged cells of sheet
	for cell in merged_cells:									
		if cell[2] == 1 and cell[0] in card_list:				# take merged cells only at agregat's column
			card_list[cell[0]][1] = (cell[1]-cell[0])			# and at once calculate size of card. and storage it
	
	for card_line, card_info in card_list.items():
		if not(card_info[0] and card_info[2] and card_info[3]):
			card_list[card_line][4] = False
			continue
		for line in range(card_info[1]):
			if not bool(all(raw_table[card_line + line][0:5]) and raw_table[card_line + line][6] and raw_table[card_line + line][8]):
				card_list[card_line][4] = False					# mark invalid cards

	return raw_table, card_list



def blockirator_total_count(card_list,raw_table):
	pass
	pass



@workbench.route('/go')
def carder():
	context = request.args.get('context')
	print('cards making...', len(context))
	return render_template('index.html')


def pocket():
	pass