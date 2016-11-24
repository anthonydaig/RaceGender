import re
import sys
import random
from collections import defaultdict
import math
import glob
import os
import pandas as pd
import seaborn as c
import matplotlib.pyplot as plt
from operator import add

def make_ID_Dicts():
	all_files = [os.path.basename(name) for name in glob.glob('*6/*') ]

	IDs = []

	for file in all_files:
		num = ''
		for ele in file:
			if ele == '_':
				break
			num+= ele
		if int(num) in IDs:
			pass
		else:
			IDs.append(int(num))


	rg_to_ID = defaultdict(lambda:[])
	ID_to_rg = defaultdict(lambda:0)

	race_to_ID = defaultdict(lambda:[])
	ID_to_race = defaultdict(lambda:0)

	gender_to_ID = defaultdict(lambda:[])
	ID_to_gender = defaultdict(lambda:0)

	for i in IDs:
		if i in pd_total.index:
			help_me = (pd_total.loc[i].Race_num, pd_total.loc[i].Sex)
			ID_to_rg[i] = help_me
			rg_to_ID[help_me] = rg_to_ID[help_me]+[i]

			ID_to_race[i] = pd_total.loc[i].Race_num
			race_to_ID[pd_total.loc[i].Race_num] += [i]

			ID_to_gender[i] = pd_total.loc[i].Sex
			gender_to_ID[pd_total.loc[i].Sex] += [i]

		else:
			continue

	return rg_to_ID, ID_to_rg, race_to_ID, ID_to_race, gender_to_ID, ID_to_gender

remove = ['and',
 'the',
 'his',
 'her',
 'with',
 'for',
 'this',
 'was',
 'applicant',
 'that',
 'Medicine',
 'has',
 'LoR',
 'not',
 'Medical',
 'Program',
 'have',
 'medical',
 'The',
 'patients',
 'Center',
 'application',
 'him',
 'will',
 'waived',
 'information',
 'our',
 'year',
 'program',
 'outside',
 'very',
 'Confidential',
 'view',
 'distribute',
 'persons',
 'disclose',
 'residency',
 'process',
 'Page',
 'rights',
 'clinical',
 'University',
 'student',
 '2015',
 'residency/fellowship',
 'letter',
 '1/3',
 'KMcCausland',
 'students',
 '03/25/2016',
 'Director',
 'you',
 'Haven',
 'New',
 'Yale',
 'YaleNew',
 'your',
 'during',
 'research',
 'Surgery',
 'from',
 'Professor',
 'team',
 'Department',
 'rotation',
 'medicine',
 'Internal',
 'had',
 'she',
 'His',
 'who',
 'all',
 'level',
 'also',
 'ERAS',
 'to',
 'contact',
 'are',
 'time',
 'and',
 'School',
 'would',
 'years',
 'of',
 'recommendation',
 'to',
 'and',
 'the',
 'which',
 'of',
 'and',
 'AAMC',
 'were',
 'Dear',
 'resident',
 'about',
 'Chair',
 'been',
 'see',
 'school',
 'right',
 'Hospital',
 'Emergency',
 'She',
 'other',
 'Middle',
 'other',
 'questions',
 'a',
 'Pass',
 'their',
 'Sincerely']


def make_bag_from_file(file_name, dictt):

	# words = []

	# onegram_dict = defaultdict(lambda:0)

	reader = open(file_name, 'r', errors = 'ignore')

	for k in reader:
		if len(k) == 1:
			continue

		else:
			words = k.translate({ord(c): None for c in '.,?!#@:()\'\"-'})
			words = words.split()
			for word in words:
				if(len(word) > 3):
					# print(word.strip(), len(word))
					# input()
					dictt[word.strip().lower()] += 1

	return dictt



def make_bag_from_file_bg(file_name, dictt):

	# words = []

	# onegram_dict = defaultdict(lambda:0)

	reader = open(file_name, 'r', errors = 'ignore')

	starter = '#'

	for k in reader:
		if len(k) == 1:
			continue

		else:
			words = k.translate({ord(c): None for c in '.,?!#@:()\'\"-'})
			words = words.split()
			words = words
			for word in words:
				if(len(word) > 3):
					nextt = word.strip()
					nextt = nextt.lower()
					tupler = (starter, nextt)
					starter = nextt
					# print(word.strip(), len(word))
					# input()
					dictt[tupler] += 1

	return dictt

def find_file(file_name, tuple_check):

	# words = []

	# onegram_dict = defaultdict(lambda:0)

	reader = open(file_name, 'r', errors = 'ignore')

	starter = '#'

	for k in reader:
		if len(k) == 1:
			continue

		else:
			words = k.translate({ord(c): None for c in '.,?!#@:()\'\"-'})
			words = words.split()
			words = words
			for word in words:
				if(len(word) > 3):
					nextt = word.strip()
					nextt = nextt.lower()
					tupler = (starter, nextt)
					starter = nextt
					if tupler == tuple_check:
						print(file_name)
						input()
					# print(word.strip(), len(word))
					# input()

	return 0




# dict_keys([(7, 'Female'), (7, 'Male'), (8, 'Male'), (7, 'FALSE'), (3, 'Male'), 
# 	(1, 'Male'), (4, 'Female'), (0, 'Male'), (1, 'Female'), (4, 'Male'), (2, 'Male'),
# 	 (0, 'Female'), (-1, 'Female'), (3, 'Female'), (2, 'Female'), (-1, 'Male'), 
# 	 (8, 'Female')])
# for dictt in dict_of_dicts.keys():
# 	lst_of_df.append(pd.DataFrame(list(dict_of_dicts[dictt].items())))

# for kk in lst_of_df:
# 	kk.columns = ['word', 'count']

# def main():

store = pd.HDFStore('variables.h5')
pd_total = store['RaceGender_Total']
pd_groups = pd_total.groupby(['Race_num', 'Sex'])

dict_of_dicts = defaultdict(lambda:defaultdict(lambda:0))
dict_of_dicts_race = defaultdict(lambda:defaultdict(lambda:0))
dict_of_dicts_gender = defaultdict(lambda:defaultdict(lambda:0))

dict_of_dicts_bg = defaultdict(lambda:defaultdict(lambda:0))
dict_of_dicts_race_bg = defaultdict(lambda:defaultdict(lambda:0))
dict_of_dicts_gender_bg = defaultdict(lambda:defaultdict(lambda:0))


rg_to_ID, ID_to_rg, race_to_ID, ID_to_race, gender_to_ID, ID_to_gender = make_ID_Dicts()

for k in glob.glob('*6/*'):
	id_num = os.path.basename(k)

	num = ''
	for ele in id_num:
		if ele == '_':
			break

		else:
			num += ele

	number = float(num)

	if ID_to_rg[number]:

		dict_to_use = dict_of_dicts_race[ID_to_race[number]]

		make_bag_from_file( k ,dict_to_use )

		dict_to_use = dict_of_dicts_gender[ID_to_gender[number]]

		make_bag_from_file( k, dict_to_use )

		dict_to_use = dict_of_dicts[(ID_to_race[number], ID_to_gender[number])]

		make_bag_from_file( k, dict_to_use)

for k in glob.glob('*6/*'):
	id_num = os.path.basename(k)

	num = ''
	for ele in id_num:
		if ele == '_':
			break

		else:
			num += ele

	number = float(num)

	if ID_to_rg[number]:

		dict_to_use = dict_of_dicts_race_bg[ID_to_race[number]]

		make_bag_from_file_bg( k ,dict_to_use )

		dict_to_use = dict_of_dicts_gender_bg[ID_to_gender[number]]

		make_bag_from_file_bg( k, dict_to_use )

		dict_to_use = dict_of_dicts_bg[(ID_to_race[number], ID_to_gender[number])]

		make_bag_from_file_bg( k, dict_to_use)




for k in glob.glob('*6/*'):
	id_num = os.path.basename(k)
	num = ''
	for ele in id_num:
		if ele == '_':
			break

		else:
			num+= ele

		number = float(num)

		if ID_to_rg[number]:
			find_file(k, ("middle", "below"))




remove_bg = [
	("medical", "center"),
	("information", "persons"),
	("persons", "outside"),
	("applicant", "information"),
	("distribute", "applicant"),
	("residency/fellowship", "application"),
	("disclose", "distribute"),
	("view", "this"),
	("confidential", "disclose"),
	("yalenew", "haven"),
	("rights", "view"),
	("waived", "rights"),
	("applicant", "waived"),
	("this", "letter"),
	("haven", "medical"),
	("this", "letter"),
	("center", "program"),
	("internal", "medicine"),
	("this", "confidential"),
	("kmccausland", "applicant"),
	("program", "director"),
	("page", "kmccausland"),
	("residency", "program"),
	("medical", "student"),
	("waived", "right"),
	("dear", "program"),
	("letter", "recommendation"),
	("work", "with"),
	("medical", "school"),
	("application", "process"),
	("school", "medicine"),
	("emergency", "medicine"),
	("medicine", "page"),
	("september", "2015"),
	("september", "2016"),
	("program", "internal"),
	("worked", "with"),
	("right", "this"),
	("medicine", "clerkship"),
	("kmccausland", "confidential"),
	("year", "medical"),
	("outside", "residency/fellowship"),
	("portal", "uploaded"),
	("eras", "2015"),
	("that", "will"),
	("department", "medicine"),
	("dept", "chair"),
	("orthopaedic", "surgery"),
	("write", "this"),
	("your", "program"),
	("august", "2015"),
	("your", "residency"),
	("received", "eras")
]



check_bg = [
	("with", "patients"),
	("working", "with"),
	("work", "ethic"),
	("patient", "care"),
	("high", "pass"),
	("very", "well"),
	("knowledge", "base"),
	("above", "peers"),
	("below", "peers"),
	("peers", "middle"),
	("peers", "level"),
	("well", "with"),
	("level", "peers"),
	("peers", "lower"),
	("middle", "below"),
	("level", "peers"),
	("above", "peers"),
	("peers", "level"),
	("peers", "lower"),
	("below", "peers"),
	("assistant", "professor"),
	("03/25/2016", "dept"),
	("ranaivari", "fras")
]


for kk in dict_of_dicts.keys():
	print(kk)
	dictt = dict_of_dicts[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove)]
	print(helpp.nlargest(30, 'count'))
	input()

for kk in dict_of_dicts_gender.keys():
	print(kk)
	dictt = dict_of_dicts_gender[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove)]
	print(helpp.nlargest(30, 'count'))
	# input()


for kk in dict_of_dicts_race.keys():
	print(kk)
	dictt = dict_of_dicts_race[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove)]
	print(helpp.nlargest(30, 'count'))
	# input()




for kk in dict_of_dicts_bg.keys():
	print(kk)
	dictt = dict_of_dicts_bg[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove_bg)]
	print(helpp.nlargest(50, 'count'))
	input()

for kk in dict_of_dicts_gender_bg.keys():
	print(kk)
	if kk == "FALSE":
		continue
	dictt = dict_of_dicts_gender_bg[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove_bg)]
	print(helpp.nlargest(50, 'count'))
	input()


for kk in dict_of_dicts_race_bg.keys():
	print(kk)
	dictt = dict_of_dicts_race_bg[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove_bg)]
	print(helpp.nlargest(30, 'count'))
	input()



# things i have: rg_to_ID, ID_to_rg, pd_total, pd_groups, dict_of_dicts

# testme = test_me[~test_me.word.isin(remove)]

# test_me = pd.DataFrame(list(dict_of_dicts[(8, 'Male')].items()))



bigrams = []

for kk in dict_of_dicts_gender_bg.keys():
	print(kk)
	if kk == "FALSE":
		continue
	dictt = dict_of_dicts_gender_bg[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove_bg)]
	print(helpp.nlargest(50, 'count'))
	ok = helpp.nlargest(80, 'count')
	choices = list(ok.word)
	bigrams = union(choices, bigrams)
	# input()



def make_row_from_file_bg(file_name, bigrams):

	# words = []

	row = []

	# onegram_dict = defaultdict(lambda:0)

	reader = open(file_name, 'r', errors = 'ignore')

	dictt = defaultdict(lambda:0)

	starter = '#'

	for k in reader:
		if len(k) == 1:
			continue

		else:
			words = k.translate({ord(c): None for c in '.,?!#@:()\'\"-'})
			words = words.split()
			words = words
			for word in words:
				if(len(word) > 3):
					nextt = word.strip()
					nextt = nextt.lower()
					tupler = (starter, nextt)
					starter = nextt
					# print(word.strip(), len(word))
					# input()
					dictt[tupler] += 1

	for k in bigrams:
		row.append(dictt[k])

	return row




table = [[("racengender"),"race", "gender"] + bigrams]
prev_id = ''
id_row = defaultdict(lambda:[])

for k in glob.glob('*6/*'):
	id_num = os.path.basename(k)

	num = ''
	for ele in id_num:
		if ele == '_':
			break

		else:
			num += ele

	number = float(num)

	if ID_to_rg[number]:

		race = ID_to_race[number]
		gender = ID_to_gender[number]

		row = make_row_from_file_bg(k, bigrams)

		id_row[(number, race, gender)].append(row)


for key in id_row.keys():
	lst = id_row[key]
	helper = [0]*len((lst[0]))

	for k in lst:
		helper = map(add, helper, k)


	helper = [(key[1], key[2]), key[1], key[2]] + list(helper)
	table.append(helper)

headers = table.pop(0)

new_data = pd.DataFrame(table, columns = headers)



y_cols = ['gender']
x_cols = list(new_data.columns)[3:]
random_indices = permutation(new_data.index)
test_cutoff = math.floor(len(new_data)/3)
test = new_data.loc[random_indices[1:test_cutoff]]
train = new_data.loc[random_indices[test_cutoff:]]
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
predictions = knn.predict(test[x_cols])

counter = 0
for i in range(len(predictions)):
    if predictions[i] == test['gender'].iloc[i]:
        counter+=1

print(counter / len(predictions))


y_cols = ['racengender']

for j in range(1,51):
	counter = 0
	random_indices = permutation(new_data.index)
	test = new_data.loc[random_indices[1:test_cutoff]]
	train = new_data.loc[random_indices[test_cutoff:]]
	knn = KNeighborsClassifier(n_neighbors=j)

	knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
	predictions = knn.predict(test[x_cols])
	for i in range(len(predictions)):

		helpp = predictions[i]
		comp = (int(helpp[0]), helpp[1])
		if comp == test['racengender'].iloc[i]:
			counter+=1

		# print(tuple(predictions[i]), test['racengender'].iloc[i])
		# print(counter)
		# input()

	print(counter / len(predictions), j)


y_cols = ['gender']

for j in range(1,51):
	counter = 0
	random_indices = permutation(new_data.index)
	test = new_data.loc[random_indices[1:test_cutoff]]
	train = new_data.loc[random_indices[test_cutoff:]]
	knn = KNeighborsClassifier(n_neighbors=j)

	knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
	predictions = knn.predict(test[x_cols])
	for i in range(len(predictions)):

		if predictions[i] == test['gender'].iloc[i]:
			counter+=1

	print(counter / len(predictions), j)












