import json
import os
import sys

def resource_path(relative_path):# function to get the path for files when using PyInstaller
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def user_data_path(relative_path):
    return os.path.join(os.path.expanduser("~"), relative_path)



def load_data(file_path):# function to load data from file to use, used for high scores
    try:
        # the file already exists
        with open(file_path) as load_file:
            data = json.load(load_file)
    except:
        data = {}
        # create the file and store initial values
        with open(file_path, "w") as store_file:
            json.dump(data, store_file)
    return data

def store_data(file_path, data):# function to store data to file, used for high scores
    with open(file_path, "w") as store_file:
        json.dump(data, store_file)