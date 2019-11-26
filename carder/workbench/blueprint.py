from flask import Blueprint
from flask import render_template, request
import xlrd


workbench = Blueprint('workbench', __name__, template_folder='templates')


@workbench.route('/')
def index():
	""" index.func  get names of workbook & worksheet from bingo.html
				build list of all lines of excel table
				build list of card by collect lines to card
				check valid card
				mark valid card in card_list
				call render page"""
	workbook = xlrd.open_workbook(str(request.args.get('workbook')), on_demand=True)
	current_sheet = workbook.sheet_by_name(str(request.args.get('worksheet'))) 		
	
	raw_table = []
	card_list = []
	for line_number in range(1, current_sheet.nrows):
		line = current_sheet.row_values(line_number, 0, 14)
		raw_table.append(line)
		if line[1] and is_valid_line(line):
			card_list.append(line[0])

	print(card_list)	

	
	











	return render_template('workbench/index.html')


def is_valid_line(line:list):
	"""line is approximate correct if contains	energy_type,
												point,
												location 
												"""
	return (line[2] and line[4] and line[5])


