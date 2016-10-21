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
from numpy.random import permutation
from sklearn.neighbors import KNeighborsClassifier

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))


def make_ID_Dicts():
	all_files = [os.path.basename(name) for name in glob.glob('*/*') ]

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



######## bag o' words (extracing ngrams from files) ###############
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
					dictt[word.strip()] += 1

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
						# input()
					# print(word.strip(), len(word))
					# input()

	return 0

def make_row_from_file(file_name, bigrams, unigrams):

	# words = []

	row = []

	# onegram_dict = defaultdict(lambda:0)

	reader = open(file_name, 'r', errors = 'ignore')

	dictt = defaultdict(lambda:0)
	dictt_uni = defaultdict(lambda:0)

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
					dictt_uni[nextt] += 1


	for k in bigrams:
		row.append(dictt[k])
	for k in unigrams:
		row.append(dictt_uni[k])

	return row

####### load it all in ################
store = pd.HDFStore('variables.h5')
pd_total = store['RaceGender_Total']
pd_groups = pd_total.groupby(['Race_num', 'Sex'])

dict_of_dicts = defaultdict(lambda:defaultdict(lambda:0))
dict_of_dicts_race = defaultdict(lambda:defaultdict(lambda:0))
dict_of_dicts_gender = defaultdict(lambda:defaultdict(lambda:0))

dict_of_dicts_bg = defaultdict(lambda:defaultdict(lambda:0))
dict_of_dicts_race_bg = defaultdict(lambda:defaultdict(lambda:0))
dict_of_dicts_gender_bg = defaultdict(lambda:defaultdict(lambda:0))
####################################################################

rg_to_ID, ID_to_rg, race_to_ID, ID_to_race, gender_to_ID, ID_to_gender = make_ID_Dicts()

for k in glob.glob('*/*'):
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

for k in glob.glob('*/*'):
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

#########################################################

######## unigrams/bigrams to clean out ############
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
	("received", "eras"),
	('obstetrics', 'gynecology'), 
	('03/25/2016', 'dept'), 
	('\x00t\x00o\x00', '\x00v\x00i\x00e\x00w\x00'), 
	('\x00r\x00i\x00g\x00h\x00t\x00s\x00', '\x00t\x00o\x00'),
	('\x00s\x00h\x00e\x00', '\x00h\x00a\x00s\x00'),
	('ranaivari', 'fras'), ('surgery', 'page'),
	('clerkship', 'director'), ('professor', 'medicine'),
	('\x00m\x00e\x00d\x00i\x00c\x00a\x00l\x00','\x00c\x00e\x00n\x00t\x00e\x00r\x00'),
	('2015', 'dear'),
	('\x00s\x00h\x00e\x00', '\x00i\x00s\x00'),
	('\x00o\x00f\x00', '\x00t\x00h\x00e\x00'), 
	('#', '03/25/2016'),
	('\x00v\x00i\x00e\x00w\x00', '\x00t\x00h\x00i\x00s\x00'),
	('\x00d\x00o\x00', '\x00n\x00o\x00t\x00')
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
 ##########################################################


for kk in dict_of_dicts.keys():
	print(kk)
	dictt = dict_of_dicts[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove)]
	print(helpp.nlargest(30, 'count'))
	# input()

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
	# input()

for kk in dict_of_dicts_gender_bg.keys():
	print(kk)
	if kk == "FALSE":
		continue
	dictt = dict_of_dicts_gender_bg[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove_bg)]
	print(helpp.nlargest(50, 'count'))
	# input()


for kk in dict_of_dicts_race_bg.keys():
	print(kk)
	dictt = dict_of_dicts_race_bg[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove_bg)]
	print(helpp.nlargest(30, 'count'))
	# input()



# things i have: rg_to_ID, ID_to_rg, pd_total, pd_groups, dict_of_dicts

# testme = test_me[~test_me.word.isin(remove)]

# test_me = pd.DataFrame(list(dict_of_dicts[(8, 'Male')].items()))

### Make Data Set #################

bigrams = []

for kk in dict_of_dicts_bg.keys():
	print(kk)
	if kk == "FALSE":
		continue
	dictt = dict_of_dicts_bg[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove_bg)]
	print(helpp.nlargest(100, 'count'))
	# input()
	ok = helpp.nlargest(100, 'count')
	choices = list(ok.word)
	bigrams = union(choices, bigrams)
	# input()

prev_id = ''
unigrams = ['excellent', 'care', 'skills', 'great', 'outstanding', 'working', 'support', 'service', 'strong', 
'knowledge', 'recommend']
for kk in dict_of_dicts.keys():
	print(kk)
	if kk == "FALSE":
		continue
	dictt = dict_of_dicts[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove)]
	print(helpp.nlargest(100, 'count'))
	# input()
	ok = helpp.nlargest(100, 'count')
	choices = list(ok.word)
	unigrams = union(choices, unigrams)
	# input()



#### make dataframe ######
prev_id = ''
unigrams = []
table = [[("racengender"),"race", "gender"] + bigrams + unigrams]
id_row = defaultdict(lambda:[])

for k in glob.glob('*/*'):
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

		row = make_row_from_file(k, bigrams, unigrams)

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
x_cols = list(new_data.columns)[3:]
print(new_data.head())
input()
##################################################




####################### try out KNN, find best num of neighbors (stupid) #######

#### bigrams + unigrams #########
# y_cols = ['gender']
# x_cols = list(new_data.columns)[3:]
# random_indices = permutation(new_data.index)
# test_cutoff = math.floor(len(new_data)/3)
# test = new_data.loc[random_indices[1:test_cutoff]]
# train = new_data.loc[random_indices[test_cutoff:]]
# knn = KNeighborsClassifier(n_neighbors=3)
# knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
# predictions = knn.predict(test[x_cols])

# counter = 0
# for i in range(len(predictions)):
#     if predictions[i] == test['gender'].iloc[i]:
#         counter+=1

# print(counter / len(predictions))

# y_cols = ['gender']
# x_cols = list(new_data.columns)[3:]
# random_indices = permutation(new_data.index)
# test_cutoff = math.floor(len(new_data)/3)
# test = new_data.loc[random_indices[1:test_cutoff]]
# train = new_data.loc[random_indices[test_cutoff:]]
# knn = KNeighborsClassifier(n_neighbors=3)
# knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
# predictions = knn.predict(test[x_cols])

# counter = 0
# for i in range(len(predictions)):
#     if predictions[i] == test['gender'].iloc[i]:
#         counter+=1

# print(counter / len(predictions))


# y_cols = ['racengender']
# acc_racengender = []
# for j in range(1,51):
# 	counter = 0
# 	random_indices = permutation(new_data.index)
# 	test = new_data.loc[random_indices[1:test_cutoff]]
# 	train = new_data.loc[random_indices[test_cutoff:]]
# 	knn = KNeighborsClassifier(n_neighbors=j)

# 	knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
# 	predictions = knn.predict(test[x_cols])
# 	for i in range(len(predictions)):

# 		helpp = predictions[i]
# 		comp = (int(helpp[0]), helpp[1])
# 		if comp == test['racengender'].iloc[i]:
# 			counter+=1

# 		# print(tuple(predictions[i]), test['racengender'].iloc[i])
# 		# print(counter)
# 		# input()

# 	acc_racengender.append(counter / len(predictions))
# 	print(counter / len(predictions), j)


# y_cols = ['gender']
# acc_gend = []
# for j in range(1,51):
# 	counter = 0
# 	random_indices = permutation(new_data.index)
# 	test = new_data.loc[random_indices[1:test_cutoff]]
# 	train = new_data.loc[random_indices[test_cutoff:]]
# 	knn = KNeighborsClassifier(n_neighbors=j)

# 	knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
# 	predictions = knn.predict(test[x_cols])
# 	for i in range(len(predictions)):

# 		if predictions[i] == test['gender'].iloc[i]:
# 			counter+=1

# 	acc_gend.append(counter/len(predictions))
# 	print(counter / len(predictions), j)

# y_cols = ['race']
# acc_race = []
# for j in range(1,51):
# 	counter = 0
# 	random_indices = permutation(new_data.index)
# 	test = new_data.loc[random_indices[1:test_cutoff]]
# 	train = new_data.loc[random_indices[test_cutoff:]]
# 	knn = KNeighborsClassifier(n_neighbors=j)

# 	knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
# 	predictions = knn.predict(test[x_cols])
# 	for i in range(len(predictions)):

# 		if predictions[i] == test['race'].iloc[i]:
# 			counter+=1

# 	acc_race.append(counter/len(predictions))
# 	print(counter / len(predictions), j)

######### try just bigrams #############

# y_cols = ['racengender']
# x_cols = bigrams
# acc_racengender_bg = []
# for j in range(1,51):
# 	counter = 0
# 	random_indices = permutation(new_data.index)
# 	test = new_data.loc[random_indices[1:test_cutoff]]
# 	train = new_data.loc[random_indices[test_cutoff:]]
# 	knn = KNeighborsClassifier(n_neighbors=j)

# 	knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
# 	predictions = knn.predict(test[x_cols])
# 	for i in range(len(predictions)):

# 		helpp = predictions[i]
# 		comp = (int(helpp[0]), helpp[1])
# 		if comp == test['racengender'].iloc[i]:
# 			counter+=1

# 		# print(tuple(predictions[i]), test['racengender'].iloc[i])
# 		# print(counter)
# 		# input()

# 	acc_racengender_bg.append(counter / len(predictions))
# 	print(counter / len(predictions), j)


# y_cols = ['gender']
# acc_gend_bg = []
# for j in range(1,51):
# 	counter = 0
# 	random_indices = permutation(new_data.index)
# 	test = new_data.loc[random_indices[1:test_cutoff]]
# 	train = new_data.loc[random_indices[test_cutoff:]]
# 	knn = KNeighborsClassifier(n_neighbors=j)

# 	knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
# 	predictions = knn.predict(test[x_cols])
# 	for i in range(len(predictions)):

# 		if predictions[i] == test['gender'].iloc[i]:
# 			counter+=1

# 	acc_gend_bg.append(counter/len(predictions))
# 	print(counter / len(predictions), j)

# y_cols = ['race']
# acc_race_bg = []
# for j in range(1,51):
# 	counter = 0
# 	random_indices = permutation(new_data.index)
# 	test = new_data.loc[random_indices[1:test_cutoff]]
# 	train = new_data.loc[random_indices[test_cutoff:]]
# 	knn = KNeighborsClassifier(n_neighbors=j)

# 	knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
# 	predictions = knn.predict(test[x_cols])
# 	for i in range(len(predictions)):

# 		if predictions[i] == test['race'].iloc[i]:
# 			counter+=1

# 	acc_race_bg.append(counter/len(predictions))
# 	print(counter / len(predictions), j)


x_cols = list(new_data.columns)[3:]
y_cols = ['race']
test = new_data.loc[random_indices[1:test_cutoff]]
train = new_data.loc[random_indices[test_cutoff:]]
knn = KNeighborsClassifier(n_neighbors=26)
knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
predictions_r = knn.predict(test[x_cols])

x_cols = list(new_data.columns)[3:]
y_cols = ['gender']
# test = new_data.loc[random_indices[1:test_cutoff]]
# train = new_data.loc[random_indices[test_cutoff:]]
knn = KNeighborsClassifier(n_neighbors=44)
knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
predictions_g = knn.predict(test[x_cols])

x_cols = list(new_data.columns)[3:]
y_cols = ['racengender']
# test = new_data.loc[random_indices[1:test_cutoff]]
# train = new_data.loc[random_indices[test_cutoff:]]
knn = KNeighborsClassifier(n_neighbors=43)
knn.fit(train[x_cols], list(train[y_cols].values.ravel()))
predictions_rg = knn.predict(test[x_cols])

############################################################







######### try logistic regression


model = LogisticRegression(C = 1, max_iter = 8000000, tol = 1e-18)
mdl = model.fit(new_data[x_cols].iloc[:10000], new_data.gender_num.iloc[:10000].values)
# testt = new_data.iloc[:10000]
testt = new_data.iloc[10000:]
girls = []
boyz = []
predicts = model.predict_proba(testt[x_cols])
classif = model.predict(testt[x_cols])


girls = []
boyz = []
for k in range(len(predicts)):
    if testt.gender_num.iloc[k] == 1:
        girls.append(predicts[k][0])
    else:
        boyz.append(predicts[k][0])


c.distplot(girls, label = 'Female', kde = False, color = 'red')
c.distplot(boyz, label = 'Male', kde = False, color = 'blue')
plt.legend()
plt.title("Logistic Regression Score By Gender")
plt.show()

for_mat = new_data.iloc[:10000].copy()
for_mat["pred"] = classif
for_mat["diff"] = abs(for_mat.classif - for_mat.gender_num)
conf = confusion_matrix(for_mat.gender_num, classif)

####################################




####### random forest ##################

#### make white/nonwhite binary and gender binary

gend = []
racew = []

for k in range(new_data.shape[0]):
	if new_data.iloc[k].gender == "Female":
		gend.append(1)
	else:
		gend.append(0)

	if new_data.iloc[k].race == 8:
		racew.append(1)
	else:
		racew.append(0)

new_data['gender_num'] = gend
new_data['race_w'] = racew


########## do genders #########

from sklearn.ensemble import RandomForestClassifier
from numpy.random import permutation
from math import floor

rfc = RandomForestClassifier(n_estimators = 800, max_features =6)
random_indices = permutation(new_data.index)

test_cutoff = math.floor(len(new_data)/4)

test_set = new_data[x_cols].loc[random_indices[test_cutoff:]]
test_y = new_data.loc[random_indices[test_cutoff:]].gender_num
cv_set = new_data[x_cols].loc[random_indices[:test_cutoff]]
cv_y = new_data.loc[random_indices[:test_cutoff]].gender_num


trainer = rfc.fit(test_set, test_y)

predicts = rfc.predict_proba(test_set)
girls = []
boyz = []
for k in range(len(predicts)):
    if test_y.iloc[k] == 1:
        girls.append(predicts[k][0])
    else:
        boyz.append(predicts[k][0])


c.distplot(girls, label = 'Female', kde = False, color = 'red')
c.distplot(boyz, label = 'Male', kde = False, color = 'blue')
plt.legend()
plt.title("Random Forest, Training Set")
plt.xlabel("Male = 0, Female = 1")
plt.show()


predicts = rfc.predict_proba(cv_set)
girls = []
boyz = []
for k in range(len(predicts)):
    if cv_y.iloc[k] == 1:
        girls.append(predicts[k][0])
    else:
        boyz.append(predicts[k][0])

c.distplot(girls, label = 'Female', kde = False, color = 'red', bins = 50)
c.distplot(boyz, label = 'Male', kde = False, color = 'blue', bins = 50)
plt.legend()
plt.title("Random Forest, Cross Validation")
plt.xlabel("Male = 0, Female = 1")
plt.show()



######### race ########

rfc = RandomForestClassifier(n_estimators = 800, max_features = 6)
random_indices = permutation(new_data.index)
train_cutoff = math.floor(len(new_data)/4)
train_set = new_data[x_cols].loc[random_indices[train_cutoff:]]
train_y = new_data.loc[random_indices[train_cutoff:]].race_w
cv_set = new_data[x_cols].loc[random_indices[:train_cutoff]]
cv_y = new_data.loc[random_indices[:train_cutoff]].race_w


trainer = rfc.fit(train_set, train_y)

predicts = rfc.predict_proba(train_set)
white = []
nonwhite = []
for k in range(len(predicts)):
    if train_y.iloc[k] == 1:
        white.append(predicts[k][1])
    else:
        nonwhite.append(predicts[k][1])


c.distplot(white, label = 'White', kde = False, color = 'red')
c.distplot(nonwhite, label = 'Nonwhite', kde = False, color = 'blue')
plt.legend()
plt.title("Random Forest, Training Set")
plt.xlabel("Nonwhite = 0, White = 1")
plt.show()


###### gender #########

predicts = rfc.predict_proba(cv_set)
white = []
nonwhite = []
for k in range(len(predicts)):
    if cv_y.iloc[k] == 1:
        white.append(predicts[k][1])
    else:
        nonwhite.append(predicts[k][1])

c.distplot(white, label = 'White', kde = False, color = 'red')
c.distplot(nonwhite, label = 'Nonwhite', kde = False, color = 'blue')
plt.legend()
plt.title("Random Forest, Cross Validation")
plt.xlabel("Nonwhite = 0, White = 1")
plt.show()


#### look at most important features
ind = np.argpartition(trainer.feature_importances_, -50)[-50:]
checker = (x_cols[i] for i in ind)
checker = tuple(checker)


##### k - fold cv #########
from sklearn.cross_validation import cross_val_predict
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import KFold

rfc = RandomForestClassifier(n_estimators = 800, max_features = 6)

random_indices = permutation(new_data.index)
train_cutoff = math.floor(len(new_data)/4)
train_set = new_data[x_cols].loc[random_indices[test_cutoff:]]
train_y = new_data.loc[random_indices[test_cutoff:]].gender_num
cv_set = new_data[x_cols].loc[random_indices[:test_cutoff]]
cv_y = new_data.loc[random_indices[:test_cutoff]].gender_num


# both things below do the same thing -- just wanted to make sure scores was doing was what i wanted it to do
###
scores = cross_val_score(trainer, train_set, train_y, cv = 10)
###

########
male = []
female = []
kf = KFold(train_set.shape[0], 10)
for train, test in kf:
	rfc.fit(train_set.iloc[train], train_y.iloc[train])
	print(rfc.score(train_set.iloc[test], train_y.iloc[test]))
######## outputs:
# 0.644578313253
# 0.627510040161
# 0.682730923695
# 0.683417085427
# 0.67135678392
# 0.682412060302
# 0.67135678392
# 0.665326633166
# 0.659296482412
# 0.700502512563






