from twilio.rest import Client
import datetime
import logging
import os
import os.path
import requests
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite3")

def send_sms():

	account_sid = "ACc3eddd16ea435bf5ee04fff76ed8890c"
	auth_token = "f4c3b40bf3b1b8e071895b4e7b33078b"

	# DB Connection
	try:
		conn = sqlite3.connect(db_path)
		print("Connection to moorimi DB successful")
	except Error as e:
		print(e)
	else:
		cur = conn.cursor()

	leo = datetime.date.today()
	leo = leo.strftime('%Y-%m-%d')

	cur.execute("SELECT * FROM dairy_milk WHERE milking_date=?",(leo,))
	rows = cur.fetchall()

	if len(rows) < 1:
		client = Client(account_sid, auth_token)

		client.api.account.messages.create(
		    to="+254714152051",
		    from_="+18566198533",
		    body="No milk production data has been entered today!")
	else:
		print("We good")

	cur.close()
	try:
		conn.close()
		print("Connection to moorimi DB terminated")
	except:
		print("Connection to moorimi DB still open")
	




send_sms()

