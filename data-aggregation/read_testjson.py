import json
import pandas as pd

data = open('test.json', 'r')
for value in data:
	json_value = json.load(value)
	print(json_value)