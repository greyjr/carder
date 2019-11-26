from app import app
from flask import render_template, request
import xlrd

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/bingo')
def bingo():

	book =request.args.get('workbook')
	workbook =  xlrd.open_workbook(book, on_demand=True)
	sheet_names = workbook.sheet_names()

	return render_template('bingo.html', context=sheet_names, book=book)

