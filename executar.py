#!/usr/bin/env python

import os

def main():
    actual_directory = os.getcwd()
    os.system("source"+ actual_directory + "env/bin/activate")
    os.system("pip install --upgrade pip")
    os.system("pip install -r requirements.txt")
    os.system("flask run")

if __name__ == "__main__":
    main()
