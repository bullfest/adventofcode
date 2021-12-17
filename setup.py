import requests
import argparse
import os
import shutil
import aocd

parser = argparse.ArgumentParser()
parser.add_argument("day", type=int)

args = parser.parse_args()

day = args.day
try:
    os.mkdir(f"{day}")
except:
    print("Day already created")
    exit(1)

shutil.copy("aoc-templ.py", f"{day}/sol.py")

with open(f"{day}/input", "w") as f:
    f.write(aocd.get_data(day=day))
