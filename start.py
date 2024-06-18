#!/usr/bin/python3
import os
from subprocess import run

print("Fetching for changes")
run('git pull', shell=True)

print("Starting up the bot")
run('/home/pawin/venv/bin/python main.py', shell=True)
