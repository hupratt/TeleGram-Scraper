import pickle
invite_sent_list = []
with open("invite_sent_list.pkl", "rb") as file:
	invite_sent_list = pickle.load(file)

print(len(invite_sent_list))
for person in invite_sent_list:
	print(person.user_id)