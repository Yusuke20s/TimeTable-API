# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import os
import gspread
import datetime as dt
from datetime import datetime, timedelta, timezone
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

SPREADSHEET_KEY = os.getenv("SPREADSHEET_KEY")
json_file_name = #ふぁいるのなまえ
json_keyfile = f"{json_file_name}.json"
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
gc = gspread.authorize(credentials)

def sheet(sheet_name):
	try:
		workbook = gc.open_by_key(SPREADSHEET_KEY)
		worksheet = workbook.worksheet(sheet_name)
		return worksheet
	except:
		return

def day_of_the_week(year, month, day):
	try:
		date = dt.datetime(int(year), int(month), int(day))
		day = date.strftime("%A")
		return day
	except:
		return

def all_timetables(day_of_week, month, day):
	try:
		worksheet = sheet(day_of_week)
		cells_1 = worksheet.range("B2:B9")
		cells_2 = worksheet.range("C2:C9")
		cells_3 = worksheet.range("D2:D9")
		cells_4 = worksheet.range("E2:E9")
		cells_5 = worksheet.range("F2:F9")
		class_1 = []
		class_2 = []
		class_3 = []
		class_4 = []
		class_5 = []
		for i in range(8):
			class_1.append(str(cells_1[i].value))
		for i in range(8):
			class_2.append(str(cells_2[i].value))
		for i in range(8):
			class_3.append(str(cells_3[i].value))
		for i in range(8):
			class_4.append(str(cells_4[i].value))
		for i in range(8):
			class_5.append(str(cells_5[i].value))
		#時間割変更
		try:
			day_worksheet = sheet(f"{month}/{day}")
			day_cells_1 = day_worksheet.range("B2:B9")
			day_cells_2 = day_worksheet.range("C2:C9")
			day_cells_3 = day_worksheet.range("D2:D9")
			day_cells_4 = day_worksheet.range("E2:E9")
			day_cells_5 = day_worksheet.range("F2:F9")
			for i in range(8):
				value = str(day_cells_1[i].value)
				if value == "None" or value == "":
					pass
				elif value == class_1[i]:
					pass
				else:
					class_1[i] = "☆" + value
			for i in range(8):
				value = str(day_cells_2[i].value)
				if value == "None" or value == "":
					pass
				elif value == class_2[i]:
					pass
				else:
					class_2[i] = "☆" + value
			for i in range(8):
				value = str(day_cells_3[i].value)
				if value == "None" or value == "":
					pass
				elif value == class_3[i]:
					pass
				else:
					class_3[i] = "☆" + value
			for i in range(8):
				value = str(day_cells_4[i].value)
				if value == "None" or value == "":
					pass
				elif value == class_4[i]:
					pass
				else:
					class_4[i] = "☆" + value
			for i in range(8):
				value = str(day_cells_5[i].value)
				if value == "None" or value == "":
					pass
				elif value == class_5[i]:
					pass
				else:
					class_5[i] = "☆" + value
		except:
			pass
		json = {
				"1":class_1,
				"2":class_2,
				"3":class_3,
				"4":class_4,
				"5":class_5,
				}
		return json
	except:
		return

def timetable(day_of_week, month, day, class_number):
	try:
		worksheet = sheet(day_of_week)
		if class_number == 1:
			cells = worksheet.range("B2:B9")
		elif class_number == 2:
			cells = worksheet.range("C2:C9")
		elif class_number == 3:
			cells = worksheet.range("D2:D9")
		elif class_number == 4:
			cells = worksheet.range("E2:E9")
		elif class_number == 5:
			cells = worksheet.range("F2:F9")
		else:
			return
		class_list = []
		for i in range(8):
			class_list.append(str(cells[i].value))
		#時間割変更
		try:
			day_worksheet = sheet(f"{month}/{day}")
			if class_number == 1:
				day_cells = day_worksheet.range("B2:B9")
			elif class_number == 2:
				day_cells = day_worksheet.range("C2:C9")
			elif class_number == 3:
				day_cells = day_worksheet.range("D2:D9")
			elif class_number == 4:
				day_cells = day_worksheet.range("E2:E9")
			elif class_number == 5:
				day_cells = day_worksheet.range("F2:F9")
			else:
				return
			for i in range(8):
				value = str(day_cells[i].value)
				if value == "None" or value == "":
					pass
				elif value == class_list[i]:
					pass
				else:
					class_list[i] = "☆" + value
		except:
			pass
		json = {
				str(class_number):class_list
				}
		return json
	except:
		return

JST = timezone(timedelta(hours=+9), "JST")

@app.route("/")
def alive():
	return "Hello", 200

@app.route("/today", methods=["GET"])
def today():
	try:
		today = datetime.now(JST)
		year = today.strftime("%Y")
		month = today.strftime("%m")
		day = today.strftime("%d")
		day_of_week = day_of_the_week(year, month, day)
	except:
		return "Error", 500
	try:
		json = all_timetables(day_of_week, month, day)
		return jsonify(json)
	except:
		return "Error", 500

@app.route("/today/class/<int:class_number>", methods=["GET"])
def today_class(class_number):
	try:
		today = datetime.now(JST)
		year = today.strftime("%Y")
		month = today.strftime("%m")
		day = today.strftime("%d")
		day_of_week = day_of_the_week(year, month, day)
	except:
		return "Error", 500
	try:
		json = timetable(day_of_week, month, day, class_number)
		return jsonify(json)
	except:
		return "Error", 500

@app.route("/tomorrow", methods=["GET"])
def tomorrow():
	try:
		today = datetime.now(JST)
		tomorrow = today + timedelta(days=1)
		year = tomorrow.strftime("%Y")
		month = tomorrow.strftime("%m")
		day = tomorrow.strftime("%d")
		day_of_week = day_of_the_week(year, month, day)
	except:
		return "Error", 500
	try:
		json = all_timetables(day_of_week, month, day)
		return jsonify(json)
	except:
		return "Error", 500

@app.route("/tomorrow/class/<int:class_number>", methods=["GET"])
def tomorrow_class(class_number):
	try:
		today = datetime.now(JST)
		tomorrow = today + timedelta(days=1)
		year = tomorrow.strftime("%Y")
		month = tomorrow.strftime("%m")
		day = tomorrow.strftime("%d")
		day_of_week = day_of_the_week(year, month, day)
	except:
		return "Error", 500
	try:
		json = timetable(day_of_week, month, day, class_number)
		return jsonify(json)
	except:
		return "Error", 500

@app.route("/day/<int:year>/<int:month>/<int:day>", methods=["GET"])
def day(year, month, day):
	try:
		day_of_week = day_of_the_week(year, month, day)
	except:
		return "Error", 500
	try:
		json = all_timetables(day_of_week, month, day)
		return jsonify(json)
	except:
		return "Error", 500

@app.route("/weekday/<string:day_of_week>/class/<int:class_number>", methods=["GET"])
def weekday_class(day_of_week, class_number):
	try:
		if day_of_week == "monday":
			day_of_week = "Monday"
		elif day_of_week == "tuesday":
			day_of_week = "Tuesday"
		elif day_of_week == "wednesday":
			day_of_week = "Wednesday"
		elif day_of_week == "thursday":
			day_of_week = "Thursday"
		elif day_of_week == "friday":
			day_of_week = "Friday"
		json = timetable(day_of_week, 0, 0, class_number)
		return jsonify(json)
	except:
		return "Error", 500

@app.errorhandler(404)
def not_found(error):
    return "Not Found", 404

def start_up():
	app.run(host="0.0.0.0")