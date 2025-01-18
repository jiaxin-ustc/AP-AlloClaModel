import torch
from ast import parse
from mimetypes import init
import numpy as np
import os
import torch
import torch.nn as nn
import time
import torch.optim as optim
import random
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns

#初始化
def seed_torch(seed=42):
	random.seed(seed)
	os.environ['PYTHONHASHSEED'] = str(seed) # 为了禁止hash随机化，使得实验可复现
	np.random.seed(seed)
	torch.manual_seed(seed)
	torch.cuda.manual_seed(seed)
	torch.cuda.manual_seed_all(seed) # if you are using multi-GPU.
	torch.backends.cudnn.benchmark = False
	torch.backends.cudnn.deterministic = True
    #torch.use_deterministic_algorithms(True)  # 有检查操作，看下文区别

def init_weights(m):
    print(m)
    if type(m) == nn.Linear:
        nn.init.xavier_uniform_(m.weight) 

def get_feature(res_1_type,bond_type,res_2_type):
    '''
    res_1_type shape:(m)=(6217),取值为[0,22] TODO:need -1
    bond_type shape:(m)=(6217),取值为[0,4]
    '''
    #Res1
    index_res1=torch.tensor(res_1_type).unsqueeze(dim=-1)
    one_hot_res1 = torch.zeros(len(res_1_type), 23).scatter_(1, index_res1, 1)
    #Bond
    index_bond=torch.tensor(bond_type).unsqueeze(dim=-1)
    one_hot_bond = torch.zeros(len(bond_type), 5).scatter_(1, index_bond, 1)
    #Res2
    index_res2=torch.tensor(res_2_type).unsqueeze(dim=-1)
    one_hot_res2 = torch.zeros(len(res_2_type), 23).scatter_(1, index_res2, 1)

    X=torch.cat((one_hot_res1,one_hot_bond,one_hot_res2), 1)
    
    return X