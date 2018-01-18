raw_data = open("final_data_2.0.txt").read().split("\n")[:-1]
print "Length of Raw data: " , len(raw_data)

data = filter(lambda x: 'where' in x.lower() and len(x)>0, raw_data)
print "Length of data: " , len(data)



COND_OPS = ['=', '>', '<','<>','<=', '>=']
REL_OPS = ['AND']

def count_cond(q):
    c = 0
    for op in REL_OPS:
        c += q.count(op)
    return c + 1

def check_validity(q):
    if 'where' not in q:
        return False
    if 'OR' in q:
        return False
    for op in COND_OPS:
        if op in q:
            return True
    return False

clean_data = filter(lambda x: len(x.split('|')[1].strip().split()) != 0 and count_cond(x.split('|')[2].strip().split()) < 4 and check_validity(x.split('|')[2].strip().split()), data)
print "Length of Clean data: " , len(clean_data)

small_data = clean_data[:25000]
out_file = open("small_data.txt","w")
for d in small_data:
    out_file.write(d+"\n")