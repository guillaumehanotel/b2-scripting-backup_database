#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# ====================================================
# TITLE           : Cron chooser
# DESCRIPTION     : Ask the user for a frequency and transform it into crontab.
# AUTHORS		  : Guillaume HANOTEL
# DATE            : 23/03/2018
# ====================================================

import sys
from functions import clear_screen


def ask_question(possible_choices) -> str:
	try:
		choice = int(input("\n > "))
	except ValueError:
		sys.stderr.write("Error : Undefined choice\n")
		sys.exit(1)
	if choice not in possible_choices:
		sys.stderr.write("Error : Undefined choice\n")
		sys.exit(1)
	return choice


def ask_per_minutes() -> str:
	possible_choices = [1, 2, 3, 5, 10, 15, 20, 30]
	print("Enter the number that corresponds to the interval of minutes in which you want to start the backup : ")

	for choice in possible_choices:
		print("\tOn every {} minutes".format(choice))

	minute_choice = ask_question(possible_choices)

	return "*/{} * * * *".format(minute_choice)


def ask_hourly() -> str:
	possible_choices = [1, 2, 3, 4, 6, 8, 12]
	print("Enter the number that corresponds to the interval of hours in which you want to start the backup : ")

	for choice in possible_choices:
		print("\tOn every {} hours".format(choice))

	hour_choice = ask_question(possible_choices)

	return "0 */{} * * *".format(hour_choice)


def ask_hour() -> str:
	print("Enter the hour [0-23] : ")
	possible_choices = list(range(0, 24))
	hour_choice = ask_question(possible_choices)
	return hour_choice


def ask_minutes() -> str:
	print("Enter the minute [0-59] : ")
	possible_choices = list(range(0, 60))
	minute_choice = ask_question(possible_choices)
	return minute_choice


def ask_day_of_week() -> str :
	print("Enter the day of the week : ")
	possible_choices = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

	i = 0
	for choice in possible_choices:
		print("\t[{}] => On every {} ".format(i, choice))
		i = i + 1

	try:
		day_choice = int(input("\n > "))
	except ValueError:
		sys.stderr.write("Error : Undefined choice\n")
		sys.exit(1)

	if day_choice < 0 or day_choice > len(possible_choices)-1:
		sys.stderr.write("Error : Undefined choice !\n")
		sys.exit(1)

	return day_choice


def ask_day_of_month() -> str:
	print("Enter the day of month [1-30] : ")
	possible_choices = list(range(1, 31))
	day_choice = ask_question(possible_choices)
	return day_choice


def ask_daily():
	hour = ask_hour()
	minute = ask_minutes()
	return "{} {} * * *".format(minute, hour)


def ask_weekly():
	day = ask_day_of_week()
	hour = ask_hour()
	minute = ask_minutes()
	return "{} {} * * {}".format(minute, hour, day)


def ask_monthly():
	day = ask_day_of_month()
	hour = ask_hour()
	minute = ask_minutes()
	return "{} {} {} * *".format(minute, hour, day)


def generate_cron(user_choice) -> str:

	# Per minutes
	if user_choice == 1:
		return ask_per_minutes()

	# Hourly
	elif user_choice == 2:
		return ask_hourly()

	# Daily
	elif user_choice == 3:
		return ask_daily()

	# Weekly
	elif user_choice == 4:
		return ask_weekly()

	# Monthy
	elif user_choice == 5:
		return ask_monthly()


def ask_frequency():

	clear_screen()
	print("How frequently/often do you want to schedule the backup?\n")

	print("\t[1] => Per minutes")
	print("\t[2] => Hourly")
	print("\t[3] => Daily")
	print("\t[4] => Weekly")
	print("\t[5] => Monthy")

	try:
		user_choice = int(input("Enter your choice: \n > "))
	except ValueError:
		sys.stderr.write("Error : Undefined choice\n")
		sys.exit(1)

	cron = generate_cron(user_choice)
	return cron


cron = ask_frequency()
print(cron)
