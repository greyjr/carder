import xlrd


def is_valid_line(line:list):
	return (line[2] and line[4] and line[5])


def valid_cell(cell_value):
	return str(int(cell_value)) if type(cell_value) == float else cell_value


workbook = xlrd.open_workbook('Общая БМП.xlsx', on_demand=True)
current_sheet = workbook.sheet_by_name('тест') 		

raw_table = []
card_list = {}
for line_number in range(1, current_sheet.nrows):
	line = current_sheet.row_values(line_number, 0, 14)
	raw_table.append(line)
	if line[1] and is_valid_line(line):
		card_list[line_number] = [valid_cell(line[0]),1]
		
merged_cells = current_sheet.merged_cells
for cell in merged_cells:
	if cell[2] == 1:
		card_list[cell[0]][1] = (cell[1]-cell[0])







print(card_list)	
