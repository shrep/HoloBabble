import json
import spacy
nlp = spacy.load('en')


raw_data = map(lambda x: x, open("final_data_2.0.txt").read().split("\n")[:-1])
#raw_data = map(lambda x: x, open("data/test_toy.txt").read().split("\n")[:-1])
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
                    replace('"','').replace('<','LT').replace('>','GT').replace('=','EQL').strip(), data)
clean_data = filter(lambda x: len(x.split('|')[1].strip().split()) != 0 and \
                    count_cond(x.split('|')[2].strip().split()) < 4 and \
                    check_validity(x.split('|')[2].strip().split()) and check_num_pipes(x), mod_data)
print "Length of Clean data: " , len(clean_data)

small_data = clean_data[:50000]
out_file = open("clean_data.txt","w")
for d in small_data:
    out_file.write(d+"\n")

toy = True
json_data = []
json_data_toy = []
for d in clean_data:
    sql = {}
    sql['NL']   = d.split('|')[1].strip().lower()
    sql['NL_tok'] = [str(y) for y in nlp(unicode(d.split('|')[1].lower(),'utf-8')) if str(y).strip()!='']
    query_tok = [str(x) for x in nlp(unicode(d.split('|')[2], 'utf-8')) if str(x).strip()!='']
    #print query_tok
    query = d.split('|')[2].strip()
    if "how" in sql['NL'] or "what" in sql['NL']:
        continue
    if len(d.split('|')[1].strip().split()) == 0 or \
        count_cond(d.split('|')[2].strip().split()) >= 4 or 'NEQLEQL' in query:
        continue
    cols = [' '.join(x.strip().split()).lower() for x in d.split('|')[3].strip().split(',')]
    gt = []   
    toy_gt = []
    
    val_ind = []
    try:
        flag = 0
        start_ind = query_tok.index('WHERE') + 1
        curr_ind = start_ind + 1
        while (curr_ind < len(query_tok)):
            if query_tok[curr_ind] in COND_OPS:
                col = cols.index(' '.join(query_tok[start_ind:curr_ind]).lower().strip())
                start_ind = curr_ind + 1
                op = COND_OPS.index(query_tok[curr_ind])
            if query_tok[curr_ind] in REL_OPS:
                val = ' '.join(query_tok[start_ind:curr_ind]).strip().lower()
                val_ind.append((start_ind,curr_ind))
                if val not in sql['NL']:
                    flag = 1
                start_ind = curr_ind + 1
                gt.append([col,op,val])   
                if val == d.split('|')[1].strip().lower().split()[0]:
                    toy_gt.append([col,op,val])   
            curr_ind += 1
        
        val = ' '.join(query_tok[start_ind:curr_ind]).strip().lower()
        val_ind.append((start_ind,curr_ind))
        if val not in sql['NL']:
            flag = 1
        if val == d.split('|')[1].strip().lower().split()[0]:
            toy_gt.append([col,op,val])   
        gt.append([col,op,val]) 
    except:
        #print "error"
        continue
   
    if len(gt) >= 3 or flag == 1:
        continue
   
    try:
        flag = 0
        if toy == True:
            val1 = sql['NL_tok'][:2]
            val2 = sql['NL_tok'][-2:]
            for k,ind in enumerate(val_ind):
                if ind[1] - ind[0] >= 2:
                    query_tok[ind[0]] = eval('val'+str(k+1))[0]
                    query_tok[ind[0]+1] = eval('val'+str(k+1))[1]
                    for j in range(ind[0]+2, ind[1]):
                        del query_tok[j]
                
                else:
                    #print "initial:", query_tok
                    if query_tok[ind[0]] in COND_OPS:
                        flag = 1
                        break
                    query_tok[ind[0]] = eval('val'+str(k+1))[0]
                    tmp = query_tok[-1]
                    for j in range(len(query_tok)-1, ind[1], -1):
                        query_tok[j] = query_tok[j-1]
                    query_tok.append(tmp)
                    query_tok[ind[1]] = eval('val'+str(k+1))[1]
                    #print "final:", query_tok

            val1 = ' '.join(sql['NL_tok'][:2]).strip().lower()
            val2 = ' '.join(sql['NL_tok'][-2:]).strip().lower()
            query = ' '.join(query_tok)
            gt[0][2] =  val1
            gt[1][2] =  val2
    except:
        continue

    if flag == 1:
        continue

    

    sql['query'] = query
    sql['query_tok'] = query_tok
    sql['schema'] = cols
    #sql['NL']   = d.split('|')[1].strip().lower()
    #sql['NL_tok'] = [str(y) for y in nlp(unicode(d.split('|')[1].lower(),'utf-8')) if str(y).strip()!=''] 
    sql['schema_tok'] = [[str(y) for y in nlp(unicode(x.lower(),'utf-8')) if str(y).strip()!=''] for x in cols]
    sql['sql'] = {'agg':None, 'sel':None}
    sql['sql']['conds'] = gt

    json_data.append(sql)
    """if len(toy_gt) == 1:
        sql['query'] = 'select * WHERE '+ cols[toy_gt[0][0]] + " " + COND_OPS[toy_gt[0][1]] + " " + toy_gt[0][2]
        sql['query_tok'] =[str(x) for x in nlp(unicode(sql['query'], 'utf-8')) if str(x).strip()!='']
        sql['sql']['conds'] = toy_gt
        json_data_toy.append(sql)"""

    if (len(json_data) + 1) % 1000 == 0:
       print (len(json_data) + 1),"items done"
       print sql['NL'], query

print len(json_data)
#json_data = json_data[:50]
with open('constraint_data_toyv2.json', 'w') as outfile:
    json.dump(json_data, outfile)  

with open('constraint_toy_v2.json', 'w') as outfile:
    json.dump(json_data_toy, outfile) 
