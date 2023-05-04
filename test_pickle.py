
import csv
invite_sent_list_saved=[]
with open('invite_sent_list.csv', newline='\n') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		invite_sent_list_saved.append(row[0])

invite_sent_list_saved
'5374020267' not in invite_sent_list_saved