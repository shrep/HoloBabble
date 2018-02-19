'''
Created on 2018.2

a synthetic data set of key constraints, utilizing schemas from WikiSQL
it maps NL to IF-THEN statements

@author: Sherine
'''

import json
import sys
from random import randint

# deal with unicode encode error
reload(sys)  
sys.setdefaultencoding('utf8') 

tableNames = ["EMMA", "OLIVIA", "AVA", "ISABELLA", "SOPHIA", "MIA", "AMELIA", "CHARLOTTE", "HARPER", "ELLA", "LIAM", 
		"NOAH", "LOGAN", "LUCAS", "MASON", "OLIVER", "ETHAN", "ELIJAH", "AIDEN", "JAMES", "BENJAMIN", "SEBASTIAN", "JACKSON", 
		"ALEXANDER", "JACOB", "CARTER", "JAYDEN", "MICHAEL", "DANIEL", "LUKE", "WILLIAM", "MATTHEW", "WYATT", "JACK", 
		"ARIA", "EVELYN", "ABIGAIL", "EMILY", "AVERY", "SCARLETT", "MADISON", "SOFIA", "CHLOE", "LILY", "MILA", "LAYLA", 
		"RILEY", "ELLIE", "LUNA", "ZOEY", "ELIZABETH", "GRACE", "VICTORIA", "PENELOPE", "HANNAH", "AUBREY", "NORA", "CAMILA",
		"ADDISON", "STELLA", "BELLA", "NATALIE", "MAYA", "GRAYSON", "GABRIEL", "HENRY", "JULIAN", "LEVI", "OWEN", "LEO", 
		"RYAN", "JAXON", "LINCOLN", "ISAIAH", "NATHAN", "SAMUEL", "ADAM", "DAVID"]

# =================load in schemas===================
with open('train.tables.in.jsonl', 'r') as f:
	table_dict = json.load(f)

with open('test.tables.in.jsonl', 'r') as f:
	table_dict += json.load(f)

with open('dev.tables.in.jsonl', 'r') as f:
	table_dict += json.load(f)

schema = []
for t in table_dict:
	schema.append([tableNames[randint(0,len(tableNames)-1)], t['header']])
# ===================================================

inp = open("key_in.txt", "w")
outp = open("key_out.txt", "w")
schep = open("key_schema.txt", "w")


for i in range(0,1000):
	sche = schema[randint(0, len(schema)-1)]
	attriIndex = randint(0, len(sche[1])-1)
	attri = sche[1][attriIndex]
	tb1 = sche[0] + "_1."
	tb2 = sche[0] + "_2."
	out = ""

	inp.write(attri + " should be a superkey for " + sche[0] + ".\n")
	out += "If " + tb1 + attri + " = " + tb2 + attri + ", then "
	for a in sche[1]:
		if not a == attri and not a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + " AND "
		if not a == attri and a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + "\n"
		if a == sche[1][len(sche[1])-1] and a == attri:
			out += "\n"

	if out[len(out)-5 : len(out)-2] == "AND":
		out = out[0 : len(out)-6] + "\n"

	outp.write(out)


	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")




for i in range(0,1000):
	sche = schema[randint(0, len(schema)-1)]
	attriIndex = randint(0, len(sche[1])-1)
	attri = sche[1][attriIndex]
	tb1 = sche[0] + "_1."
	tb2 = sche[0] + "_2."
	out = ""

	inp.write(attri + " is a key.\n")
	out += "If " + tb1 + attri + " = " + tb2 + attri + ", then "
	for a in sche[1]:
		if not a == attri and not a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + " AND "
		if not a == attri and a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + "\n"
		if a == sche[1][len(sche[1])-1] and a == attri:
			out += "\n"

	if out[len(out)-5 : len(out)-2] == "AND":
		out = out[0 : len(out)-6] + "\n"

	outp.write(out)


	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")


for i in range(0,1000):
	sche = schema[randint(0, len(schema)-1)]
	attriIndex = randint(0, len(sche[1])-1)
	attri = sche[1][attriIndex]
	tb1 = sche[0] + "_1."
	tb2 = sche[0] + "_2."
	out = ""

	inp.write(attri + " determines every other attribute for " + sche[0] + ".\n")
	out += "If " + tb1 + attri + " = " + tb2 + attri + ", then "
	for a in sche[1]:
		if not a == attri and not a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + " AND "
		if not a == attri and a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + "\n"
		if a == sche[1][len(sche[1])-1] and a == attri:
			out += "\n"

	if out[len(out)-5 : len(out)-2] == "AND":
		out = out[0 : len(out)-6] + "\n"

	outp.write(out)

	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")


for i in range(0,1000):
	sche = schema[randint(0, len(schema)-1)]
	attriA = sche[1][randint(0, len(sche[1])-1)]
	attriB = sche[1][randint(0, len(sche[1])-1)]
	while attriA == attriB:
		attriB = sche[1][randint(0, len(sche[1])-1)]
	tb1 = sche[0] + "_1."
	tb2 = sche[0] + "_2."
	out = ""

	inp.write("A " + sche[0] + " is identified by its " + attriA + " and its " + attriB + ".\n")
	out += "If " + tb1 + attriA + " = " + tb2 + attriA + " AND " + tb1 + attriB + " = " + tb2 + attriB + ", then "
	for a in sche[1]:
		if not a == attriA and not a == attriB and not a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + " AND "
		if not a == attriA and not a == attriB and a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + "\n"
		if a == sche[1][len(sche[1])-1] and (a == attriA or a == attriB):
			out += "\n"

	if out[len(out)-5 : len(out)-2] == "AND":
		out = out[0 : len(out)-6] + "\n"

	outp.write(out)


	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")



for i in range(0,1000):
	sche = schema[randint(0, len(schema)-1)]
	attriA = sche[1][randint(0, len(sche[1])-1)]
	attriB = sche[1][randint(0, len(sche[1])-1)]
	while attriA == attriB:
		attriB = sche[1][randint(0, len(sche[1])-1)]
	tb1 = sche[0] + "_1."
	tb2 = sche[0] + "_2."
	out = ""

	inp.write(attriA + " and " + attriB + " is a composite key.\n")
	out += "If " + tb1 + attriA + " = " + tb2 + attriA + " AND " + tb1 + attriB + " = " + tb2 + attriB + ", then "
	for a in sche[1]:
		if not a == attriA and not a == attriB and not a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + " AND "
		if not a == attriA and not a == attriB and a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + "\n"
		if a == sche[1][len(sche[1])-1] and (a == attriA or a == attriB):
			out += "\n"

	if out[len(out)-5 : len(out)-2] == "AND":
		out = out[0 : len(out)-6] + "\n"

	outp.write(out)


	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")


for i in range(0,1000):
	sche = schema[randint(0, len(schema)-1)]
	attriIndex = randint(0, len(sche[1])-1)
	attri = sche[1][attriIndex]
	tb1 = sche[0] + "_1."
	tb2 = sche[0] + "_2."
	out = ""

	inp.write("No two " + sche[0] + " can share the same " + attri + ".\n")
	out += "If " + tb1 + attri + " = " + tb2 + attri + ", then "
	for a in sche[1]:
		if not a == attri and not a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + " AND "
		if not a == attri and a == sche[1][len(sche[1])-1]:
			out += tb1 + a + " = " + tb2 + a + "\n"
		if a == sche[1][len(sche[1])-1] and a == attri:
			out += "\n"

	if out[len(out)-5 : len(out)-2] == "AND":
		out = out[0 : len(out)-6] + "\n"

	outp.write(out)


	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")
