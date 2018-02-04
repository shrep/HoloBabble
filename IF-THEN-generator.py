'''
Created on 2018.1.30

create a synthetic data set that maps NL to IF-THEN statements, utilizing schemas from WikiSQL

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


attriVals = ["Seattle", "Chicago", "Florida", "USA", "Boston", "New York", "Atlanta", "California", "Wisconsin", "engineer",
			"computer scientist", "instructor", "teacher", "professor", "researcher", "student", "Apple", "Amazon", "Microsoft", 
			"Facebook", "Houston", "Philadelphia", "Austin", "Phoenix", "Jacksonville", "Columbus", "Ohio", "Washington", "Dallas", 
			"Denver", "Texas", "Memphis", "Nashville", "Portland", "Maryland", "Baltimore", "Louisville", "Nevada", "Tennessee", 
			"Milwaukee", "Arizona", "Tucson", "Fresno", "Sacramento", "Mesa", "Omaha", "Virginia", "Missouri", "Nebraska", "Miami", 
			"London", "Paris", "Germany", "Tampa", "Arlington", "Honolulu", "Colorado", "Anaheim", "Riverside", "Lexington", "Pittsburgh", 
			"Alaska", "Anchorage", "Cincinnati", "Toledo", "Plano", "Greensboro", "Henderson", "Orlando", "Minnesota", "Buffalo", "Laredo", 
			"Irvine", "Durham",	"Norfolk", "Lubbock", "Glendale", "Reno", "Hialeah", "Garland", "Chesapeake", "Birmingham", "Spokane", 
			"Modesto", "Oxnard", "Tacoma", "Yonkers", "Amarillo", "Augusta", "Georgia", "Alabama", "Utah", "Kansas"]


attriAdjs = ["single", "married", "minor", "adult", "teenage", "professional", "amateur", "male", "female", "divorced",
			"audit", "blacklisted", "major", "public", "private", "adorable", "beautiful", "clean", "elegant", 
			"fancy", "handsome", "long", "magnificent", "old-fashioned", "plain", "red", "orange", "yellow", "green",
			"blue", "purple", "gray", "black", "white", "brown", "alive", "careful", "sour", "easy", "hard", "famous", 
			"helpful", "odd", "expensive", "rich", "shy", "poor", "gifted", "brave", "calm", "eager", "gentle",
			"happy", "kind", "lively", "nice", "proud", "relieved", "witty", "angry", "clumsy", "fierce", "grumpy", "itchy", 
			"jealous", "lazy", "mysterious", "nervous", "repulsive", "scary", "uptight", "worried", "broad", "crooked",
			"deep", "curved", "flat", "high", "low", "hollow", "narrow", "round", "shallow", 
			"skinny", "square", "straight", "wide", "big", "fat", "huge", "tiny", "deafening", "loud",
			"noisy", "quiet", "ancient", "brief", "early", "late", "fast", "slow", "modern", "old", "quick", "rapid", "young", 
			"bitter", "sweet", "fresh", "joicy", "icy", "loose", "melted", "tasteless", "strong", "salty", "broken", "chilly"]

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


opList = ["greater than", "greater than or equal to", "less than", "less than or equal to", "no less than", "equal to", 
		"the same as", "different from", "not equal to", "bigger than", "larger than", "bigger than or equal to", 
		"larger than or equal to", "fewer than", "fewer than or equal to", "less than but not equal to", 
		"greater than but not equal to"]

exprListNorm = ["must be", "should be", "is", "are"]
opSQLList = [">", ">=", "<", "<=", ">=", "=", "=", "!=", "!=", ">", ">", ">=", ">=", "<", "<=", "<", ">"]

exprListRev = ["cannot be", "should not be", "must not be", "is not", "are not"]
opSQLListRev = ["<=", "<", ">=", ">", "<", "!=", "!=", "=", "=", "<=", "<=", "<", "<", ">=", ">", ">=", "<="]


inp = open("in.txt", "w")
outp = open("out.txt", "w")
schep = open("schema.txt", "w")


for i in range(0,1000):
	sche = schema[randint(0, len(schema)-1)]
	attri = sche[1][randint(0, len(sche[1])-1)]
	exprNorm = exprListNorm[randint(0,len(exprListNorm)-1)]
	exprRev = exprListRev[randint(0,len(exprListRev)-1)]

	if (randint(0,1) == 0):
		inp.write("The " + attri + " of a " + sche[0] + " " + exprNorm + " negative.\n")
		outp.write("If TRUE then " + attri + " < 0.\n")
	else:
		inp.write("The " + attri + " of a " + sche[0] + " " + exprRev + " negative.\n")
		outp.write("If TRUE then " + attri + " >= 0.\n")

	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")


for i in range(0,500):
	sche = schema[randint(0, len(schema)-1)]
	attri = sche[1][randint(0, len(sche[1])-1)]
	exprNorm = exprListNorm[randint(0,len(exprListNorm)-1)]
	val = str(randint(100, 10000))

	inp.write("No " + sche[0] + " should have more than " + val + " " + attri + ".\n")
	outp.write("If TRUE then " + attri + " <= " + val + ".\n")

	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")



for i in range(0,500):
	sche = schema[randint(0, len(schema)-1)]
	attri = sche[1][randint(0, len(sche[1])-1)]
	exprNorm = exprListNorm[randint(0,len(exprListNorm)-1)]
	val = str(randint(100, 10000))

	inp.write("It's necessary that each " + sche[0] + " " + exprNorm + " at least " + val + " " + attri + ".\n")
	outp.write("If TRUE then " + attri + " >= " + val + ".\n")

	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")


for i in range(0,500):
	sche = schema[randint(0, len(schema)-1)]
	attriA = sche[1][randint(0, len(sche[1])-1)]
	attriB = sche[1][randint(0, len(sche[1])-1)]
	while attriA == attriB:
		attriB = sche[1][randint(0, len(sche[1])-1)]

	attriAval = attriVals[randint(0,len(attriVals)-1)]
	val = str(randint(100, 10000))

	inp.write("There cannot exist a " + attriA + " " + attriAval + " with " + attriB + " greater than " + val + ".\n")
	outp.write("If " + attriB + " > " + val + " then " + attriA + " != " + attriAval + ".\n")

	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")


for i in range(0,500):
	sche = schema[randint(0, len(schema)-1)]
	attriA = sche[1][randint(0, len(sche[1])-1)]
	attriB = sche[1][randint(0, len(sche[1])-1)]
	while attriA == attriB:
		attriB = sche[1][randint(0, len(sche[1])-1)]

	attriAval = attriVals[randint(0,len(attriVals)-1)]
	val = str(randint(100, 10000))

	inp.write(attriA + " " + attriAval + "'s " + attriB + " cannot be lower than " + val + ".\n")
	outp.write("If " + attriA + " = " + attriAval + " then " + attriB + " >= " + val + ".\n")

	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")


for i in range(0,500):
	sche = schema[randint(0, len(schema)-1)]
	attriA = sche[1][randint(0, len(sche[1])-1)]
	attriB = sche[1][randint(0, len(sche[1])-1)]
	while attriA == attriB:
		attriB = sche[1][randint(0, len(sche[1])-1)]

	inp.write("The " + attriA + " of a " + sche[0] + " cannot be before " + attriB + ".\n")
	outp.write("If TRUE then " + attriA + " >= " + attriB + ".\n")

	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")


for i in range(0,500):
	sche = schema[randint(0, len(schema)-1)]
	attriA = sche[1][randint(0, len(sche[1])-1)]
	attriB = sche[1][randint(0, len(sche[1])-1)]
	while attriA == attriB:
		attriB = sche[1][randint(0, len(sche[1])-1)]

	attriAval = attriAdjs[randint(0,len(attriAdjs)-1)]
	attriBval = attriAdjs[randint(0,len(attriAdjs)-1)]

	inp.write("One has to be " + attriAval + " " + attriA + " to have any " + attriBval + " " + attriB + ".\n")
	outp.write("If " + attriA + " = " + attriAval + " then " + attriB + " = " + attriBval + ".\n")

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

	attriAval = attriAdjs[randint(0,len(attriAdjs)-1)]
	attriBval = attriAdjs[randint(0,len(attriAdjs)-1)]
	val = str(randint(100, 10000))

	if (randint(0,1) == 0):
		inp.write("One must have " + attriA + " greater than " + val + ".\n")
		outp.write("If TRUE then " + attriA + " > " + val + ".\n")
	else:
		inp.write("One must have " + attriA + " greater than " + attriB + ".\n")
		outp.write("If TRUE then " + attriA + " > " + attriB + ".\n")

	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")


for i in range(0,500):
	sche = schema[randint(0, len(schema)-1)]
	attriA = sche[1][randint(0, len(sche[1])-1)]
	attriB = sche[1][randint(0, len(sche[1])-1)]
	while attriA == attriB:
		attriB = sche[1][randint(0, len(sche[1])-1)]

	attriAval = attriAdjs[randint(0,len(attriAdjs)-1)]
	attriBval = attriAdjs[randint(0,len(attriAdjs)-1)]

	inp.write("Only a " + attriAval + " " + attriA + " can be " + attriBval + " " + attriB + " of a " + sche[0] + ".\n")
	outp.write("If " + attriA + " = " + attriAval + " then " + attriB + " = " + attriBval + ".\n")

	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")


for i in range(0,500):
	sche = schema[randint(0, len(schema)-1)]
	attriA = sche[1][randint(0, len(sche[1])-1)]
	attriB = sche[1][randint(0, len(sche[1])-1)]
	while attriA == attriB:
		attriB = sche[1][randint(0, len(sche[1])-1)]

	attriAval = attriAdjs[randint(0,len(attriAdjs)-1)]
	attriBval = attriAdjs[randint(0,len(attriAdjs)-1)]

	inp.write(attriAval + " " + attriA + " cannot have " + attriBval + " " + attriB + ".\n")
	outp.write("If " + attriA + " = " + attriAval + " then " + attriB + " != " + attriBval + ".\n")

	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")


for i in range(0,500):
	sche = schema[randint(0, len(schema)-1)]
	attriA = sche[1][randint(0, len(sche[1])-1)]
	attriB = sche[1][randint(0, len(sche[1])-1)]
	while attriA == attriB:
		attriB = sche[1][randint(0, len(sche[1])-1)]

	attriAval = attriAdjs[randint(0,len(attriAdjs)-1)]
	attriBval = attriAdjs[randint(0,len(attriAdjs)-1)]

	inp.write("Every " + attriAval + " " + attriA + " must correspond to an " + attriBval + " " + attriB + ".\n")
	outp.write("If " + attriA + " = " + attriAval + " then " + attriB + " = " + attriBval + ".\n")

	schep.write(sche[0] + "(")
	for s in sche[1]:
		if not s == sche[1][len(sche[1])-1]:
			schep.write(s + ", ")
		else:
			schep.write(s + ")\n")
