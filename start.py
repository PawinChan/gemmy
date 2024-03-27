#!/usr/bin/python3
import os
from subprocess import run

print("Fetching for changes")
run('git pull', shell=True)

print("Starting up the bot")
run('python3 main.py', shell=True)
