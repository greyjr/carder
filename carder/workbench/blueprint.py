from flask import Blueprint
from flask import render_template, request
import xlrd


workbench = Blueprint('workbench', __name__, template_folder='templates')


@workbench.route('/')
def index():
	""" index.func  get names of workbook & worksheet from bingo.html
				+ build list of all lines of excel table
				+ build list of card with size
				check valid card
				mark valid card in card_list
				prepear context
				call render page"""
	workbook = xlrd.open_workbook(str(request.args.get('workbook')), on_demand=True)
	current_sheet = workbook.sheet_by_name(str(request.args.get('worksheet'))) 		
	
	
	energy_types = ['электричество', 'масло', 'вода', 'газ', 'пар', 'кислород', 'воздух', 'кислота']


	raw_table = [['header line']]
	card_list = {}
	current_photo_folder = ""

	for line_number in range(1,current_sheet.nrows):			# nrows = last row in excell sheet	
		line = current_sheet.row_values(line_number, 0, 14)		# take line
		raw_table.append(line)									# fill table from sheet
		
		if raw_table[line_number][13]:							# 
			current_photo_folder = raw_table[line_number][13]	# if photo's folder exist, update current photo's folder
		else:
			raw_table[line_number][13] = current_photo_folder	# if photo's folder cell is empty, take info from previous line

		if line[1]:												#                 ...and is_valid_line(line)
			card_list[line_number] = [valid_cell(line[0]),1,1]	# fill card list by card_number, "1", "1"
	
		



	merged_cells = current_sheet.merged_cells					# all merged cells of sheet
	
	for cell in merged_cells:									# 
		if cell[2] == 1 and cell[0] in card_list:				# take merged cells only at agregat's column
			card_list[cell[0]][1] = (cell[1]-cell[0])			# and at once calculate size of card. and storage it

	
	for card_line, card_info in card_list.items():				#
		for i in range(card_info[1]):							# card size is counter
			if raw_table[card_line+i][2] not in energy_types:	# 										FIX IT !!!     NEED MAPPING !!!
				card_list[card_line][2] = 0

	print(card_list)	

	context = []
	for line in range(1, len(raw_table)):
		context_line = [raw_table[line][0],raw_table[line][1],raw_table[line][4],raw_table[line][13]]
		context.append(context_line)

	return render_template('workbench/index.html', context=context)


def is_valid_line(line:list):
	"""line is approximate correct if contains	energy_type,
												point,
												location 
												"""
	return (line[2] and line[4] and line[5])

def valid_cell(cell_value):
	return str(int(cell_value)) if type(cell_value) == float else cell_value

