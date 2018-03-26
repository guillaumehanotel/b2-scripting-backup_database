#!/bin/bash

# This script allows the Database Management Program to set up a crontab in order to launch the database backup script.

# This script takes a string as an argument
# This string is generated from another script asking the user to chose and set the frequency in order to launch the database backup script.


crontab_frequency=$1
crontab_command='crontab command'


# * * * * * + command 