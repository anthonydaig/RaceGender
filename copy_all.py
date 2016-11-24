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
from sklearn.ensemble import RandomForestClassifier
from numpy.random import permutation
from math import floor
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import auc
from sklearn.model_selection import KFold
from sklearn.model_selection import permutation_test_score
from sklearn.model_selection import StratifiedKFold

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

		dict_of_dicts_race[ID_to_race[number]] = make_bag_from_file( k ,dict_to_use )

		dict_to_use = dict_of_dicts_gender[ID_to_gender[number]]

		dict_of_dicts_gender[ID_to_gender[number]] = make_bag_from_file( k, dict_to_use )

		dict_to_use = dict_of_dicts[(ID_to_race[number], ID_to_gender[number])]

		dict_of_dicts[(ID_to_race[number], ID_to_gender[number])] = make_bag_from_file( k, dict_to_use)

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

		dict_of_dicts_race_bg[ID_to_race[number]]=make_bag_from_file_bg( k ,dict_to_use )

		dict_to_use = dict_of_dicts_gender_bg[ID_to_gender[number]]

		dict_of_dicts_gender_bg[ID_to_gender[number]]=make_bag_from_file_bg( k, dict_to_use )

		dict_to_use = dict_of_dicts_bg[(ID_to_race[number], ID_to_gender[number])]

		dict_of_dicts_bg[(ID_to_race[number], ID_to_gender[number])]=make_bag_from_file_bg( k, dict_to_use)

#########################################################

######## unigrams/bigrams to clean out ############
remove_bg = [
 ('\x00a\x00p\x00p\x00l\x00i\x00c\x00a\x00n\x00t\x00',
  '\x00i\x00n\x00f\x00o\x00r\x00m\x00a\x00t\x00i\x00o\x00n\x00'),
  ('\x00r\x00e\x00s\x00i\x00d\x00e\x00n\x00c\x00y\x00/\x00f\x00e\x00l\x00l\x00o\x00w\x00s\x00h\x00i\x00p\x00',
  '\x00a\x00p\x00p\x00l\x00i\x00c\x00a\x00t\x00i\x00o\x00n\x00'),
('\x00t\x00h\x00i\x00s\x00', '\x00l\x00e\x00t\x00t\x00e\x00r\x00'),
('\x00p\x00r\x00o\x00g\x00r\x00a\x00m\x00', '\x00d\x00i\x00r\x00e\x00c\x00t\x00o\x00r\x00\x00'),
   ('\x00a\x00p\x00p\x00l\x00i\x00c\x00a\x00n\x00t\x00',
  '\x00w\x00a\x00i\x00v\x00e\x00d\x00'),
    ('\x00i\x00n\x00', '\x00t\x00h\x00e\x00'),
    ('\x00n\x00o\x00t\x00', '\x00d\x00i\x00s\x00c\x00l\x00o\x00s\x00e\x00'),
     ('\x00d\x00i\x00s\x00c\x00l\x00o\x00s\x00e\x00', '\x00o\x00r\x00'),
      ('\x00p\x00e\x00r\x00s\x00o\x00n\x00s\x00',
  '\x00o\x00u\x00t\x00s\x00i\x00d\x00e\x00'),
       ('\x00t\x00h\x00e\x00',
  '\x00r\x00e\x00s\x00i\x00d\x00e\x00n\x00c\x00y\x00/\x00f\x00e\x00l\x00l\x00o\x00w\x00s\x00h\x00i\x00p\x00'),
        ('\x00y\x00a\x00l\x00e\x00\x00n\x00e\x00w\x00',
  '\x00h\x00a\x00v\x00e\x00n\x00'),
         ('\x00d\x00i\x00s\x00t\x00r\x00i\x00b\x00u\x00t\x00e\x00',
  '\x00a\x00p\x00p\x00l\x00i\x00c\x00a\x00n\x00t\x00'),
          ('\x00o\x00r\x00', '\x00d\x00i\x00s\x00t\x00r\x00i\x00b\x00u\x00t\x00e\x00'),
           ('\x00o\x00u\x00t\x00s\x00i\x00d\x00e\x00', '\x00t\x00h\x00e\x00'),
 ('\x00i\x00n\x00f\x00o\x00r\x00m\x00a\x00t\x00i\x00o\x00n\x00',
  '\x00t\x00o\x00'),
 ('\x00w\x00a\x00i\x00v\x00e\x00d\x00', '\x00r\x00i\x00g\x00h\x00t\x00s\x00'),
 ('\x00a\x00p\x00p\x00l\x00i\x00c\x00a\x00t\x00i\x00o\x00n\x00',
 	('\x00p\x00r\x00o\x00g\x00r\x00a\x00m\x00', '\x00d\x00i\x00r\x00e\x00c\x00t\x00o\x00r\x00\x00'),
 ('\x00p\x00a\x00g\x00e\x00', '\x00k\x00\x00m\x00c\x00c\x00a\x00u\x00s\x00l\x00a\x00n\x00d\x00'),
 ('\x00t\x00o\x00', '\x00t\x00h\x00e\x00'),
 ('\x00w\x00i\x00l\x00l\x00', '\x00b\x00e\x00'),
 ('\x00h\x00e\x00', '\x00w\x00a\x00s\x00'),
 ('\x00h\x00e\x00', '\x00i\x00s\x00'),
 ('\x00d\x00u\x00r\x00i\x00n\x00g\x00', '\x00h\x00e\x00r\x00'),('\x00o\x00f\x00', '\x00h\x00e\x00r\x00'),
  '\x00p\x00r\x00o\x00c\x00e\x00s\x00s\x00\x00'),
 ('\x00t\x00h\x00e\x00', '\x00a\x00p\x00p\x00l\x00i\x00c\x00a\x00n\x00t\x00'),
  ('\x00t\x00h\x00i\x00s\x00', '\x00l\x00o\x00r\x00'),
   ('\x00c\x00e\x00n\x00t\x00e\x00r\x00',
  '\x00p\x00r\x00o\x00g\x00r\x00a\x00m\x00\x00'),
   ('\x00h\x00a\x00v\x00e\x00n\x00', '\x00m\x00e\x00d\x00i\x00c\x00a\x00l\x00'),
    ('\x00c\x00e\x00n\x00t\x00e\x00r\x00',
  '\x00p\x00r\x00o\x00g\x00r\x00a\x00m\x00\x00'),	("medical", "center"),
	("information", "persons"),
	('health', 'maringillisfiuedu'),
	 ('\x00o\x00f\x00',
  '\x00d\x00e\x00r\x00m\x00a\x00t\x00o\x00l\x00o\x00g\x00y\x00'),
	 ('\x00k\x00\x00m\x00c\x00c\x00a\x00u\x00s\x00l\x00a\x00n\x00d\x00',
  '\x00t\x00h\x00e\x00'),
	 ('13141981', '03/25/2016'),
	 ('institution', 'mm/yy'),
	 ('student', 'waived'),
	 ('page', 'medicine/pediatrics'),
	 ('sinal', '12805457'),
	 ('internal', 'medicine/pediatrics'),
	 ('\x00p\x00r\x00o\x00g\x00r\x00a\x00m\x00\x00',
  '\x00p\x00a\x00t\x00h\x00o\x00l\x00o\x00g\x00y\x00\x00a\x00n\x00a\x00t\x00o\x00m\x00i\x00c\x00'),
	 ('\x00a\x00n\x00d\x00', '\x00c\x00l\x00i\x00n\x00i\x00c\x00a\x00l\x00'),
	 ('chow', '13141981'),
	 ('13305910', '03/25/2016'),
	  ('beano', 'hamza'),
	   ('that', 'katharine'),
	   ('university', 'hospital'),
	    ('\x00a\x00t\x00', '\x00t\x00h\x00e\x00'),
	    ('general', 'medicine'),
	    ('\x00u\x00n\x00i\x00v\x00e\x00r\x00s\x00i\x00t\x00y\x00', '\x00o\x00f\x00'),
	    ('arun', 'gosain'),
	    ('center', 'waterbury'),
 ('katharine', 'lawrence'),
 ('rights', 'privacy'),
 ('mohammad', 'javad'),
 ('alex', '13305910'),
 ('\x00h\x00e\x00', '\x00h\x00a\x00s\x00'),
  ('internal', 'medicinepediatrics'),
  ('wilmington', 'delaware'),
  ('\x00o\x00f\x00', '\x00p\x00a\x00t\x00h\x00o\x00l\x00o\x00g\x00y\x00'),
  ('education', 'lcme'),
 ('robert', 'lurie'),
 ('this', 'yalenew'),
 ('program', 'surgerygeneral'),
 ('irna', 'pnrial'),
 ('young', 'lady;'),
 ('13093147', '03/25/2016'),
 ('\x00p\x00r\x00o\x00g\x00r\x00a\x00m\x00\x00',
  '\x00d\x00e\x00r\x00m\x00a\x00t\x00o\x00l\x00o\x00g\x00y\x00'),
 ('#', 'patel'),
 ('rigni', 'irna'),
  ('chris', 'buresh'),
   ('3053480570', 'medicinefiuedu'),
   ('miami', '33199'),
   ('\x00d\x00e\x00p\x00a\x00r\x00t\x00m\x00e\x00n\x00t\x00', '\x00o\x00f\x00'),
   ('medicinepediatrics', 'residency'),
   ('paraim', 'kmccausland'),
   ('support', 'katharine'),
   ('herbert', 'wertheim'),
   ('hall', 'alex'),
   ('12805457', '10/20/2015'),
   ('pnrial', 'ininariari'),
   ('\x00p\x00a\x00t\x00h\x00o\x00l\x00o\x00g\x00y\x00\x00a\x00n\x00a\x00t\x00o\x00m\x00i\x00c\x00',
  '\x00a\x00n\x00d\x00'),
   ('waterbury', 'program'),
 ('howard', 'grossman'),
 ('\x00o\x00f\x00', '\x00m\x00e\x00d\x00i\x00c\x00i\x00n\x00e\x00'),
 ('\x00s\x00h\x00e\x00', '\x00w\x00a\x00s\x00'),
 ('program', 'anesthesiology'),
 ('florida', 'international'),
  ('his/her', 'right'),
   ('hamza', '13316364'),
   ('medicine', 'kmccausland'),
   ('pmsource', 'portal'),('medicine/pediatrics', 'kmccausland'),
	 ('applicant', 'name'),
 ('assistant', 'professor'),
 ('33199', '3053484554'),
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
	('johns', 'hopkins'),
	("work", "with"),
	("medical", "school"),
	("application", "process"),
	("school", "medicine"),
	("emergency", "medicine"),
	("medicine", "page"),
	("september", "2015"),
	("september", "2016"),
	("program", "internal"),
	('young', 'woman'),
	('page', 'aasnes'),
	('gynecology', 'page'),
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
	('\x00a\x00p\x00p\x00l\x00i\x00c\x00a\x00t\x00i\x00o\x00n\x00', '\x00p\x00r\x00o\x00c\x00e\x00s\x00s\x00\x00') ,
	('\x00t\x00h\x00e\x00', '\x00r\x00e\x00s\x00i\x00d\x00e\x00n\x00c\x00y\x00/\x00f\x00e\x00l\x00l\x00o\x00w\x00s\x00h\x00i\x00p\x00') ,
	('\x00l\x00o\x00r\x00', '\x00c\x00o\x00n\x00f\x00i\x00d\x00e\x00n\x00t\x00i\x00a\x00l\x00') ,
	('ional', 'university') ,
('\x00n\x00o\x00t\x00', '\x00d\x00i\x00s\x00c\x00l\x00o\x00s\x00e\x00') ,
	('\x00s\x00h\x00e\x00', '\x00i\x00s\x00'),
	('\x00o\x00f\x00', '\x00t\x00h\x00e\x00'), 
	('#', '03/25/2016'),
	('\x00v\x00i\x00e\x00w\x00', '\x00t\x00h\x00i\x00s\x00'),
	('\x00d\x00o\x00', '\x00n\x00o\x00t\x00'),
	('\x00c\x00o\x00n\x00f\x00i\x00d\x00e\x00n\x00t\x00i\x00a\x00l\x00',
  '\x00d\x00o\x00'),
('\x00t\x00o\x00', '\x00p\x00e\x00r\x00s\x00o\x00n\x00s\x00'),
('support', 'application'),
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
 'She',
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
 'she',
 'a',
 'Pass',
 'their',
 '\x00t\x00h\x00e\x00',
 '\x00o\x00f\x00',
 '\x00a\x00n\x00d\x00',
  '\x00i\x00n\x00',
  '\x00t\x00o\x00',
  '2014',
  'pediatrics',
 'professor',
 'Ability',
 'yalenew',
 'department',
 'otolaryngology'
 'obstetrics',
 'Obstetrics',
 'gynecology',
 'John'
 'Gynecology',
'she',
 'Sincerely']
 ##########################


bg_use = [
	('honor', 'medical') ,
	('experiences', 'also') ,
	('honors', 'high') ,
	('this', 'students') ,
	('support', 'application') ,
	('passion', 'organization') ,
	('this', 'capacity') ,
	('chapter', 'alpha') ,("with", "patients"),
('alpha', 'honor') ,
('care', 'highly') ,
('that', 'assistant') ,
('written', 'paper') ,
('medical', 'duties') ,
('hard', 'work') ,
('students', 'underserved') ,
('pleasure', 'that') ,
('mentored', 'role') ,
('cannot', 'assess') ,
('candidacy', 'including') ,
('impressed', 'with') ,
('during', 'internal') ,
('primary', 'care') ,
('performed', 'research') ,
('conscientiousness', 'technical') ,
('patients', 'their') ,
('communicate', 'caring') ,
('nature', 'contact') ,
('caring', 'nature') ,
('assessment', 'compared') ,
('compassion', 'hard') ,
('recommended', 'last') ,
('pleasure', 'work') ,
('above', 'peers') ,
('lower', 'unlikely') ,
('applicant', 'outstanding') ,
('applicants', 'work') ,
('applicants', 'strongest') ,
('applicant', 'rotated') ,
('medical', 'knowledge') ,
('patients', 'families') ,
('lower', 'ability') ,
('level', 'judgement') ,
('your', 'internal') ,
('students', 'rotating') ,
('with', 'others') ,
('community', 'involvement') ,
('this', 'candidate') ,
('with', 'great') ,
('interpersonal', 'skills') ,
('recommended', 'each') ,
('questionable', 'unethical') ,
('above', 'beyond') ,
('team', 'player') ,
('highest', 'recommendation') ,
('positive', 'attitude') ,
('with', 'highest') ,
('care', 'patients') ,
('this', 'student') ,
('knowledge', 'base') ,
('leadership', 'compassion') ,
('with', 'team') ,
('very', 'well') ,
('very', 'happy') ,
('advanced', 'medicine') ,
('lower', 'work') ,
('extended', 'direct') ,
('balance', 'community') ,
('excellent', 'command') ,
('directly', 'with') ,
('academic', 'skills') ,
('recognition', 'limits') ,
('qualifications', 'compare') ,
('know', 'indirectly') ,
('altruism', 'recognition') ,
('enough', 'good') ,
('cohesive', 'treatment') ,
('rapport', 'with') ,
('applicants', 'weakest') ,
('have', 'doubt') ,
('excellent', 'good') ,
('ethical', 'issues') ,
('research', 'projects') ,
('excellent', 'performance') ,
('hard', 'working') ,
('performance', 'during') ,
('than', 'peers') ,
('very', 'good') ,
('strongest', 'point') ,
('applicant', 'performed') ,
('been', 'very') ,
('technical', 'ability') ,
('great', 'pleasure') ,
('relevant', 'noncognitive') ,
('ethics', 'public') ,
('work', 'ethic') ,
('while', 'maintaining') ,
('without', 'reservation') ,
('very', 'active') ,
('patient', 'care') ,
('exposure', 'unable') ,
('presentations', 'were') ,
('fund', 'knowledge') ,
('leadership', 'skills') ,
('social', 'determinants') ,
('closely', 'with') ,
('paper', 'with') ,
('above', 'average') ,
('most', 'appropriate')
]




ug_use = [
 'highly',
 'ethics',
  'learning',
 'happy',
  'professionalism',
 'directly',
 'personal',
  'performing',
   'demonstrated',
    'strong',
     'best',
      'support',
       'great',
        'working',
         'knowledge',
 'active',
 'appropriate',
 'first',
 'care',
 'inpatient',
  'excellent',
   'impressed',
    'experiences',
     'good',
      'writing',
  'performance',
   'highest',
    'ethic',
     'impressive',
      'communicate',
       'player',
        'ability',
 'strongest',
 'outstanding'
]
print('Finished Making Dicts')
 ########################################
bigrams = bg_use

for kk in dict_of_dicts_gender_bg.keys():
	# print(kk)
	if kk == "FALSE":
		continue
	dictt = dict_of_dicts_gender_bg[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove_bg)]
	# print(helpp.nlargest(100, 'count'))
	# input()
	ok = helpp.nlargest(250, 'count')
	choices = list(ok.word)
	bigrams = union(choices, bigrams)
	# input()


########################################
unigrams = ug_use

for kk in dict_of_dicts.keys():
	# print(kk)
	if kk == "FALSE":
		continue
	dictt = dict_of_dicts[kk]
	dff = pd.DataFrame(list(dictt.items()))
	dff.columns = ['word', 'count']
	helpp = dff[~dff.word.isin(remove)]
	# print(helpp.nlargest(150, 'count'))
	# input()
	ok = helpp.nlargest(150, 'count')
	choices = list(ok.word)
	unigrams = union(choices, unigrams)
	# input()


###########################
#data_frame_fam
prev_id = ''
# unigrams = ug_use
# bigrams = bg_use
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


new_data_norm = (new_data[x_cols] - new_data[x_cols].mean()) / (new_data[x_cols].max() - new_data[x_cols].min())
new_data_norm['race_w'] = new_data['race_w']
new_data_norm['gender_num'] = new_data['gender_num']
# x_cols.remove('Ability')
print('Finished Making DataSet')
def predict_gender(df, x_cols):

	rfc = RandomForestClassifier(n_estimators = 800, max_features =7, oob_score = True)
	random_indices = permutation(df.index)

	test_cutoff = math.floor(df.shape[0]/4)

	test_set = df[x_cols].loc[random_indices[test_cutoff:]]
	test_y = df.loc[random_indices[test_cutoff:]].gender_num
	cv_set = df[x_cols].loc[random_indices[:test_cutoff]]
	cv_y = df.loc[random_indices[:test_cutoff]].gender_num
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
	print(rfc.oob_score_)
	return rfc


def predict_race(df, x_cols):

	rfc = RandomForestClassifier(n_estimators = 1500, max_features =7, oob_score = True, class_weight = 'balanced')
	random_indices = permutation(df.index)

	test_cutoff = math.floor(df.shape[0]/4)

	test_set = df[x_cols].loc[random_indices[test_cutoff:]]
	test_y = df.loc[random_indices[test_cutoff:]].race_w
	cv_set = df[x_cols].loc[random_indices[:test_cutoff]]
	cv_y = df.loc[random_indices[:test_cutoff]].race_w
	trainer = rfc.fit(test_set, test_y)

	predicts = rfc.predict_proba(test_set)
	girls = []
	boyz = []
	for k in range(len(predicts)):
	    if test_y.iloc[k] == 1:
	        girls.append(predicts[k][0])
	    else:
	        boyz.append(predicts[k][0])


	c.distplot(girls, label = 'White', kde = False, color = 'red')
	c.distplot(boyz, label = 'Nonwhite', kde = False, color = 'blue')
	plt.legend()
	plt.title("Random Forest, Training Set")
	plt.xlabel("Nonwhite = 0, White = 1")
	plt.show()


	predicts = rfc.predict_proba(cv_set)
	girls = []
	boyz = []
	for k in range(len(predicts)):
	    if cv_y.iloc[k] == 1:
	        girls.append(predicts[k][0])
	    else:
	        boyz.append(predicts[k][0])

	c.distplot(girls, label = 'White', kde = False, color = 'red', bins = 50)
	c.distplot(boyz, label = 'Nonwhite', kde = False, color = 'blue', bins = 50)
	plt.legend()
	plt.title("Random Forest, Cross Validation")
	plt.xlabel("Nonwhite = 0, White = 1")
	plt.show()
	print(rfc.oob_score_)
	return rfc
# x_cols.remove('General')
# x_cols.remove('Grucral')


print('Starting the Permutation Testing')

by_race = new_data.groupby('race')
black = by_race.get_group(3)
white = by_race.get_group(8)
for i in x_cols:
	print(i)

input()



data_array = white[x_cols].values
data_array_y = white.gender_num.values


rfc = RandomForestClassifier(n_estimators = 1500, max_features =7, oob_score = True, class_weight = 'balanced')
cv = StratifiedKFold(10)

score, permutation_scores, pvalue = permutation_test_score(
    rfc, data_array, data_array_y, scoring="roc_auc", cv=cv, n_permutations=150)

print(score)
print(permutation_scores)
print(pvalue)

# plt.hist(permutation_scores, bins =20, label='Permutation scores')
# ylim = plt.ylim()
# # BUG: vlines(..., linestyle='--') fails on older versions of matplotlib
# #plt.vlines(score, ylim[0], ylim[1], linestyle='--',
# #          color='g', linewidth=3, label='Classification Score'
# #          ' (pvalue %s)' % pvalue)
# #plt.vlines(1.0 / n_classes, ylim[0], ylim[1], linestyle='--',
# #          color='k', linewidth=3, label='Luck')
# plt.plot(2 * [score], ylim, '--g', linewidth=3,
#          label='Classification Score'
#          ' (pvalue %s)' % pvalue)
# # plt.plot(2 * [1. / 2], ylim, '--k', linewidth=3, label='Luck')

# plt.ylim(ylim)
# plt.legend()
# plt.xlabel('ROC_AUC')
# plt.title('Null Hypothesis Distribution, Gender Classification in the entire dataset')

# plt.show()


###### gender_all ###########
# 0.739406213876
# [ 0.50437504,  0.49224605,  0.49191995,  0.49566848,  0.49492412,  0.48702513,
#   0.49115403,  0.48533501,  0.49805792 , 0.48684543,  0.48980403,  0.49669477,
#   0.50122436,  0.49920821,  0.49322527,  0.5002172 ,  0.49936136,  0.48923928,
#   0.49348848,  0.49869563,  0.51201327,  0.50579795,  0.49724359,  0.49589884,
#   0.48731175,  0.5009984 ,  0.49846776,  0.50167   ,  0.49915925,  0.50415856,
#   0.49316189,  0.50881753,  0.50181381,  0.49507037,  0.50038005,  0.49465273,
#   0.50134407,  0.49440519,  0.49550935,  0.49462646,  0.50050174 , 0.50646697,
#   0.50168243,  0.49439942,  0.50632046,  0.50319404,  0.50524299,  0.49283034,
#   0.49599869,  0.49063093,  0.4993611 ,  0.50554208,  0.48781361,  0.49785781,
#   0.49752882,  0.49106908,  0.49655983,  0.49139112,  0.49752044,  0.48778922,
#   0.49640709,  0.49273588,  0.49686474,  0.51478742,  0.50403216,  0.5000754,
#   0.5020368 ,  0.50877752,  0.49432229,  0.48611627,  0.50192598,  0.50568073,
#   0.49518297,  0.49219663,  0.49482647,  0.49373603,  0.50346483,  0.50072786,
#   0.49997537,  0.51703013,  0.49633941,  0.49028236,  0.50854157,  0.50856681,
#   0.49408143,  0.49276744,  0.5102487 ,  0.49721311,  0.50527343,  0.50794338,
#   0.48823618,  0.50652733,  0.50613052,  0.49784451,  0.51360225,  0.49611091,
#   0.49571173,  0.48563578,  0.50127042,  0.49431938,  0.51037535,  0.50846868,
#   0.50369432,  0.49868827,  0.50235916,  0.49546812,  0.50103608,  0.50374759,
#   0.4961585 ,  0.50107658,  0.491594  ,  0.50845275,  0.49276216,  0.49606649,
#   0.50678535,  0.50542218,  0.5004665 ,  0.49198584,  0.50127204,  0.5100256,
#   0.48891449,  0.49829505,  0.497816  ,  0.50881741,  0.49927171,  0.50316143,
#   0.50211645,  0.50748643,  0.49623243,  0.5046071 ,  0.49675133,  0.5053474,
#   0.50337425,  0.49786658,  0.50936399,  0.49856615,  0.51331728,  0.49676327,
#   0.50117522,  0.50030525,  0.50191843,  0.49962853,  0.50171019,  0.49087868,
#   0.4940388 ,  0.50005597,  0.49437952,  0.49258372,  0.49170534,  0.50298808]
# 0.00662251655629
