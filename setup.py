#!/usr/bin/env python3
import requests
import argparse
import os
import shutil
import aocd
from datetime import date

parser = argparse.ArgumentParser()
parser.add_argument("--day", type=int)
parser.add_argument("--year", type=int, default=date.today().year)

args = parser.parse_args()
day = args.day
year = args.year

try:
    os.makedirs(f"{year}/{day}")
except:
    print("Day already created")
    exit(1)

shutil.copy("aoc-templ.py", f"{year}/{day}/sol.py")

