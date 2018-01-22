import json

raw_data = open("final_data_2.0.txt").read().split("\n")[:-1]
print "Length of Raw data: " , len(raw_data)

data = filter(lambda x: 'where' in x.lower() and len(x)>0, raw_data)
print "Length of data: " , len(data)



COND_OPS = ['EQL', 'GT', 'LT','NEQL','LTEQL', 'GTEQL']
REL_OPS = ['AND']

def count_cond(q):
    c = 0
    for op in REL_OPS:
        c += q.count(op)
    return c + 1

def check_validity(q):
    if 'WHERE' not in q:
        return False
    if 'OR' in q:
        return False
    for op in COND_OPS:
        if op in q:
            return True
    return False

def check_num_pipes(q):
    if q.count('|') == 3:
        return True
    else:
        return False

mod_data   = map(lambda x: x.replace('where', 'WHERE').replace('(','').replace(')','').\
                    replace('<>','NEQL').replace('<=','LTEQL').replace('>=','GTEQL').\
                    replace('<','LT').replace('>','GT').replace('=','EQL').strip(), data)
clean_data = filter(lambda x: len(x.split('|')[1].strip().split()) != 0 and \
                    count_cond(x.split('|')[2].strip().split()) < 4 and \
                    check_validity(x.split('|')[2].strip().split()) and check_num_pipes(x), mod_data)
print "Length of Clean data: " , len(clean_data)

small_data = clean_data[:50000]
out_file = open("clean_data.txt","w")
for d in small_data:
    out_file.write(d+"\n")


json_data = []
for d in clean_data:
    sql = {}
    query_tok = d.split('|')[2].strip().split()
    query = ' '.join(query_tok)
    if len(d.split('|')[1].strip().split()) == 0 or \
        count_cond(d.split('|')[2].strip().split()) >= 4 or 'NEQLEQL' in query:
        continue
    cols = [' '.join(x.strip().split()) for x in d.split('|')[3].strip().split(',')]
    gt = []    
    try:
        start_ind = query_tok.index('WHERE') + 1
        curr_ind = start_ind + 1
        while (curr_ind < len(query_tok)):
            if query_tok[curr_ind] in COND_OPS:
                col = cols.index(' '.join(query_tok[start_ind:curr_ind]).strip())
                start_ind = curr_ind + 1
                op = COND_OPS.index(query_tok[curr_ind])
            if query_tok[curr_ind] in REL_OPS:
                val = ' '.join(query_tok[start_ind:curr_ind]).strip()
                start_ind = curr_ind + 1
                gt.append([col,op,val])            
            curr_ind += 1
        
        val = ' '.join(query_tok[start_ind:curr_ind]).strip()
        gt.append([col,op,val]) 
    except:
        continue
   
    if len(gt) >= 4:
        continue
   
    sql['query'] = query
    sql['query_tok'] = query_tok
    sql['schema'] = cols
    sql['NL']   = d.split('|')[1].strip()
    sql['NL_tok'] = d.split('|')[1].strip().split()
    sql['schema_tok'] = [x.strip().split() for x in cols]
    sql['sql'] = {'agg':None, 'sel':None}
    sql['sql']['conds'] = gt

    json_data.append(sql)

print len(json_data)

with open('constraint_data.json', 'w') as outfile:
    json.dump(json_data, outfile)  
