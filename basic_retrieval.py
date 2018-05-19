import json, os, sys
from pprint import pprint
from Document.get_document import read_json, make_document


if __name__ == '__main__':
	bookkeeping_path = os.path.join(os.getcwd(), 'WEBPAGES_RAW', "bookkeeping.json")
	lookup = read_json(bookkeeping_path)
	with open('index.json') as index_file:
		inverted_index = json.load(index_file)
	while True:
		query = raw_input("Input term you want to find. Otherwise, press !q to quit ")
		if query == "!q":
			break
		if query in inverted_index:
			for p in inverted_index[query][:10]:
				print(lookup[p['doc_id']])
		else:
			print("Query {} not found".format(query))
	print("Thanks for searching")
