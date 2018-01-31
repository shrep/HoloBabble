import json
import torch
from sqlnet.utils import *
from sqlnet.model.seq2sql import Seq2SQL
from sqlnet.model.sqlnet import SQLNet
import numpy as np
import datetime

import argparse
COND_OPS = ['EQL', 'GT', 'LT','NEQL','LTEQL', 'GTEQL']

def gen_cond_str(conds, header):
    if len(conds) == 0:
        return 'None'
    cond_str = []
    for cond in conds:
        cond_str.append(header[cond[0]] + ' ' +
                COND_OPS[cond[1]] + ' ' + unicode(cond[2]).lower())
    return 'WHERE ' + ' AND '.join(cond_str)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--toy', action='store_true', 
            help='If set, use small data; used for fast debugging.')
    parser.add_argument('--ca', action='store_true',
            help='Use conditional attention.')
    parser.add_argument('--dataset', type=int, default=0,
            help='0: original dataset, 1: re-split dataset')
    parser.add_argument('--rl', action='store_true',
            help='Use RL for Seq2SQL.')
    parser.add_argument('--baseline', action='store_true', 
            help='If set, then test Seq2SQL model; default is SQLNet model.')
    parser.add_argument('--train_emb', action='store_true',
            help='Use trained word embedding for SQLNet.')
    parser.add_argument('--constraint', action='store_true',
            help='Test NL to SQL constraint translation.')
    args = parser.parse_args()

    N_word=300
    B_word=42
    if args.toy:
        USE_SMALL=True
        GPU=True
        BATCH_SIZE=15
    else:
        USE_SMALL=False
        GPU=True
        BATCH_SIZE=64

    if args.constraint:
        TEST_ENTRY=(False, False, True)  # (AGG, SEL, COND) 
        #data = json.load(open('constraint_test.json'))
        data = json.load(open('constraint_toy_test.json'))
    else:
        TEST_ENTRY=(True, True, True)  # (AGG, SEL, COND)
        sql_data, table_data, val_sql_data, val_table_data, \
            test_sql_data, test_table_data, \
            TRAIN_DB, DEV_DB, TEST_DB = load_dataset(
                    args.dataset, use_small=USE_SMALL)

    word_emb = load_word_emb('glove/glove.%dB.%dd.txt'%(B_word,N_word), \
        load_used=True, use_small=USE_SMALL) # load_used can speed up loading

    if args.baseline:
        model = Seq2SQL(word_emb, N_word=N_word, gpu=GPU, trainable_emb = True)
    else:
        model = SQLNet(word_emb, N_word=N_word, use_ca=args.ca, gpu=GPU,
                trainable_emb = True)

    if args.train_emb:
        agg_m, sel_m, cond_m, agg_e, sel_e, cond_e = best_model_name(args)
        print "Loading from %s"%agg_m
        model.agg_pred.load_state_dict(torch.load(agg_m))
        print "Loading from %s"%sel_m
        model.sel_pred.load_state_dict(torch.load(sel_m))
        print "Loading from %s"%cond_m
        model.cond_pred.load_state_dict(torch.load(cond_m))
        print "Loading from %s"%agg_e
        model.agg_embed_layer.load_state_dict(torch.load(agg_e))
        print "Loading from %s"%sel_e
        model.sel_embed_layer.load_state_dict(torch.load(sel_e))
        print "Loading from %s"%cond_e
        model.cond_embed_layer.load_state_dict(torch.load(cond_e))

    elif args.constraint:
        agg_m, sel_m, cond_m = best_model_name(args)
        cond_m = 'saved_model/epoch23.cond_modeltoy'
        print "Loading from %s"%cond_m
        perm=np.random.permutation(len(data))
        model.cond_pred.load_state_dict(torch.load(cond_m))
        q_seq, col_seq, col_num, ans_seq, query_seq, gt_cond_seq, \
        raw_data  = to_batch_seq_constraint(data,perm, 0, len(data),ret_vis_data=True)
        raw_q_seq = [x[0] for x in raw_data]
        raw_col_seq = [x[1] for x in raw_data]
        raw_query_sq = [x[2] for x in raw_data]
        query_gt= to_batch_query_constraint(data, perm, 0, len(data))
        gt_sel_seq = [x[1] for x in ans_seq]
        score = model.forward(q_seq, col_seq, col_num,
                TEST_ENTRY, gt_sel = gt_sel_seq)
        pred_queries = model.gen_query(score, q_seq, col_seq,
                raw_q_seq, raw_col_seq, TEST_ENTRY)
        print 'NL:', raw_q_seq
        print 'query:', raw_query_sq
        print 'Cols:', raw_col_seq

        for i in range(len(raw_q_seq)):
                print "Prediction: SELECT * " + gen_cond_str(pred_queries[i]['conds'], raw_data[i][1])  
        
        
    else:
        agg_m, sel_m, cond_m = best_model_name(args)
        print "Loading from %s"%agg_m
        model.agg_pred.load_state_dict(torch.load(agg_m))
        print "Loading from %s"%sel_m
        model.sel_pred.load_state_dict(torch.load(sel_m))
        print "Loading from %s"%cond_m
        model.cond_pred.load_state_dict(torch.load(cond_m))

    print "Dev acc_qm: %s;\n  breakdown on (agg, sel, where): %s"%epoch_acc(
            model, BATCH_SIZE, val_sql_data, val_table_data, TEST_ENTRY)
    print "Dev execution acc: %s"%epoch_exec_acc(
            model, BATCH_SIZE, val_sql_data, val_table_data, DEV_DB)
    print "Test acc_qm: %s;\n  breakdown on (agg, sel, where): %s"%epoch_acc(
            model, BATCH_SIZE, test_sql_data, test_table_data, TEST_ENTRY)
    print "Test execution acc: %s"%epoch_exec_acc(
            model, BATCH_SIZE, test_sql_data, test_table_data, TEST_DB)
