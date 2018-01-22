'''
Created on Dec, 2017

Parse data set from WikiSQL and create a final data set containing NL, SQL, and schema

@author: Sherine
'''

import json
import sys
from random import randint

# deal with unicode encode error
reload(sys)  
sys.setdefaultencoding('utf8') 


random = ["EMMA", "OLIVIA", "AVA", "ISABELLA", "SOPHIA", "MIA", "AMELIA", "CHARLOTTE", "HARPER", "ELLA", "LIAM", 
			"NOAH", "LOGAN", "LUCAS", "MASON", "OLIVER", "ETHAN", "ELIJAH", "AIDEN", "JAMES", "BENJAMIN", "SEBASTIAN", "JACKSON", 
			"ALEXANDER", "JACOB", "CARTER", "JAYDEN", "MICHAEL", "DANIEL", "LUKE", "WILLIAM", "MATTHEW", "WYATT", "JACK", 
			"ARIA", "EVELYN", "ABIGAIL", "EMILY", "AVERY", "SCARLETT", "MADISON", "SOFIA", "CHLOE", "LILY", "MILA", "LAYLA", 
			"RILEY", "ELLIE", "LUNA", "ZOEY", "ELIZABETH", "GRACE", "VICTORIA", "PENELOPE", "HANNAH", "AUBREY", "NORA", "CAMILA",
			"ADDISON", "STELLA", "BELLA", "NATALIE", "MAYA", "GRAYSON", "GABRIEL", "HENRY", "JULIAN", "LEVI", "OWEN", "LEO", 
			"RYAN", "JAXON", "LINCOLN", "ISAIAH", "NATHAN", "SAMUEL", "ADAM", "DAVID"]
time = ['am', 'pm']

# ==========================QUESTION===========================
with open('train.in.jsonl', 'r') as f:
    q_dict = json.load(f)

with open('train.tables.in.jsonl', 'r') as f:
    table_dict = json.load(f)

# 0 = question, 1 = table ID
questions = []
for q in q_dict:
	questions.append([q['question'], q['table_id']])


count = 0
omit = []
keyword = []
original = []
for q in questions:
	original.append(q[0])
	if 'name the' in q[0].lower() or 'highest' in q[0].lower() or 'lowest' in q[0].lower():
		keyword.append('')
		omit.append('omit')
	else:
		if 'what' in q[0].lower()[0:5]:
			k = random[randint(0,len(random)-1)]
			keyword.append(k)
			q[0] = q[0].lower().replace('what', k)
			omit.append('what')
		elif 'which' in q[0].lower()[0:5]:
			k = random[randint(0,len(random)-1)]
			keyword.append(k)
			q[0] = q[0].lower().replace('which', k)
			omit.append('which')
		elif 'where' in q[0].lower()[0:5]:
			k = random[randint(0,len(random)-1)]
			keyword.append(k)
			q[0] = q[0].lower().replace('where', 'in '+k)
			omit.append('where')
		elif 'when' in q[0].lower()[0:5]:
			k = str(randint(0, 12)) + time[randint(0,1)]
			keyword.append(k)
			q[0] = q[0].lower().replace('when', 'at '+k)
			omit.append('when')
		elif 'who' in q[0].lower()[0:5]:
			k = random[randint(0,len(random)-1)]
			keyword.append(k)
			q[0] = q[0].lower().replace('who', k)
			omit.append('who')
		elif 'what' in q[0].lower():
			k = random[randint(0,len(random)-1)]
			keyword.append(k)
			q[0] = q[0].lower().replace('what', k)
			omit.append('what')
		elif 'which' in q[0].lower():
			k = random[randint(0,len(random)-1)]
			keyword.append(k)
			q[0] = q[0].lower().replace('which', k)
			omit.append('which')
		elif 'where' in q[0].lower():
			k = random[randint(0,len(random)-1)]
			keyword.append(k)
			q[0] = q[0].lower().replace('where', 'in '+k)
			omit.append('where')
		elif 'when' in q[0].lower():
			k = str(randint(0, 12)) + time[randint(0,1)]
			keyword.append(k)
			q[0] = q[0].lower().replace('when', 'at '+k)
			omit.append('when')
		elif 'who' in q[0].lower():
			k = random[randint(0,len(random)-1)]
			keyword.append(k)
			q[0] = q[0].lower().replace('who', k)
			omit.append('who')
		else:
			keyword.append('')
			omit.append('omit')

		if '?' in q[0]:
			q[0] = q[0].replace('?', '')

		if 'tell me' in q[0].lower():
			q[0] = q[0].lower().replace('tell me', '')

		if ' did ' in q[0].lower():
			din = q[0].lower().index('did')
			q[0] = q[0][din:] + ' ' + q[0][0:din-1]
			q[0] = q[0].strip('did ').strip()

	count += 1

# ==========================SCHEMA===========================
# 0 = table ID, 1 = attributes
tables = []
for t in table_dict:
	tables.append([t['id'], t['header']])

schema = []
schema_temp = []
for q in questions:
	for t in tables:
		if q[1] == t[0]:
			temp = ''
			for s in t[1]:
				temp += s
				if not s == t[1][len(t[1])-1]:
					temp += ', '
			schema.append(temp)
			schema_temp.append(t)
			break

# ==========================SQL===========================
sql = []
sql_temp = []
for q in q_dict:
	temp = str(q['sql']).strip('[').strip(']')
	temp = temp.replace('\'', '\"')
	temp = temp.replace('{u"', '{"')
	temp = temp.replace(' u"', ' "')
	temp = temp.replace('""', '"')
	temp = temp.replace('L\\xe9opold', 'L\\u00e9opold')
	temp = temp.replace('"s ', '\'s ')

	ain = temp.index('"agg"')
	sin = temp.index('"sel"')
	cin = temp.index('"conds"')

	agg = int(temp[ain+6:sin-2].strip())
	sel = int(temp[sin+6:cin-2].strip())
	cond = temp[cin+8:len(temp)-2].strip()
	
	# 0 = aggregation operator, 1 = select, 2 = where
	sql_temp.append([agg, sel, cond])


cond_ops = ['=', '>', '<', 'OP']
count = 0

for s in sql_temp:
	temp = 'select * '
	#temp += str(schema_temp[count][0])
	
	# parse conditions
	s[2] = s[2][1:len(s[2])]
	tp = s[2].split('],')
	conds = []
	for t in tp:
		tp2 = t.strip().strip('[').strip(']').split(',')
		for t2 in tp2:
			t2 = t2.strip()
		if len(tp2) == 4:
			tp2 = [tp2[0], tp2[1], str(tp2[2])+str(tp2[3])]
		conds.append(tp2)

	if len(conds[0]) == 3:
		temp += ' where '

		where = ''
		for c in conds:
			# column
			where += str(schema_temp[count][1][int(c[0])])
			where += ' '
			# operator
			where += cond_ops[int(c[1])]
			where += ' '
			# comparison value
			where += str(c[2])
			if not c == conds[len(conds)-1]:
				where += ' AND '

		# change to violation
		ques = ''
		if not keyword[count] == '':
			if omit[count] == 'what' or omit[count] == 'which':
				ques = questions[count][0]
				print ques
				qin = ques.lower().index(keyword[count].lower())
				ques = ques[qin+len(keyword[count]):qin+len(keyword[count])+6]
				
				if ' is ' in ques or ' was ' in ques or ' were ' in ques or ' are ' in ques:
					where = '(' + where + ') AND '
					where += str(schema_temp[count][1][s[1]]) + ' <> ' + keyword[count]
				else:
					where = where.replace('AND', 'OR')
					where = where.replace(' = ', ' <>')
					where = where.replace(' > ', ' <=')
					where = where.replace(' < ', ' >=')
					where = '(' + where + ') AND '
					where += str(schema_temp[count][1][s[1]]) + ' = ' + keyword[count]
			elif omit[count] == 'where' or omit[count] == 'when' or omit[count] == 'who':
				where = '(' + where + ') AND '
				where += str(schema_temp[count][1][s[1]]) + ' <> ' + keyword[count]
			else:
				where = where.replace('AND', 'OR')
				where = where.replace(' = ', ' <>')
				where = where.replace(' > ', ' <=')
				where = where.replace(' < ', ' >=')
				where = '(' + where + ') AND '
				where += str(schema_temp[count][1][s[1]]) + ' = ' + keyword[count]

		temp += where

	sql.append(temp)
	count += 1

# ==========================FINAL===========================
final = []
for i in range(0,len(questions)):
	if not omit[i] == 'omit':
		final.append([original[i], questions[i][0], sql[i], schema[i]])


# ==========================OUTPUT===========================
outp = open('train.out.jsonl', 'w')
for f in final:
	for f2 in f:
		outp.write(str(f2))
		if not f2 == f[len(f)-1]:
			outp.write(' | ')
	outp.write('\n')
