from app import app
from flask import render_template, request
import xlrd
import os


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/sheet', methods=['POST'])
def sheet():
	if request.method == 'POST':
		file = request.files['excel_file']
		if not file:
			return render_template('index.html')
		if file.filename.rsplit(".", 1)[1].lower() not in ['xlsx', 'xls']:
			return render_template('index.html')
		filename = file.filename
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		workbook = xlrd.open_workbook('./files/excel/{}'.format(filename), on_demand=True)
		worksheets = workbook.sheet_names()
		return render_template('sheet.html', filename=filename, context=worksheets)
	return render_template('index.html')