
# coding: utf-8

# In[39]:


import numpy as np
import glob
import os
from collections import OrderedDict


# In[40]:


def get_commands_out(dirname = './output_observation/'):
    fnames = []
    for fname in glob.glob(dirname+'*txt'):
        fnames.append(fname)
    
    commands = OrderedDict()
    for fname in fnames:
        command = os.path.basename(fname[2:]).split('_')
        #print(command)
        if command[0] == 'sarthi':
            command = command[1:4]
        else:
            command = command[:3]
        command[2] = command[2][0]
        #print(command)
        commands[fname] = command
        #commands   

    commands_out = OrderedDict()
    for fname, command in commands.items():
        with open(fname, 'r') as f:
            out_ = [l.strip() for l in f.readlines()]
        if len(out_) == 1:
            #print(out_)
            continue
        #print(fname, command)
        #print(*out_, sep = '\n')
        #print(fname, command)
        commands_out['_'.join(command)] = out_
            #print(commands_out.keys())
            #print()
        #commands_out 
    return commands_out


# In[41]:


def predict_probable_command(model_out = []):
    
    remove_out = {'_silence_', '_unknown_', 'sarthi'}
    j = 0
    l = len(model_out)
    final_commands = []
    while j < l - 1:
        out_l = []
        cmd_c = str(model_out[j][1:-1].split(',')[0][1:-1])
        val_c = float(model_out[j][1:-1].split(',')[1])
        out_l.append(val_c)
        j += 1
        if cmd_c in remove_out:
            continue
        
        cmd_n = str(model_out[j][1:-1].split(',')[0][1:-1])
        val_n = float(model_out[j][1:-1].split(',')[1])
        #print(cmd_c, val_c, cmd_n, val_n)
        
        while cmd_c == cmd_n and j < l - 1:
            out_l.append(val_n)
            j += 1
            cmd_n = str(model_out[j][1:-1].split(',')[0][1:-1])
            val_n = float(model_out[j][1:-1].split(',')[1])
            
        final_commands.append((cmd_c, np.max(out_l)))
        #print(cmd_c, np.max(out_l))
    #return final_l
    all_commands = [
    'create_track',
    'drop_track',
    'vrm_one',
    'vrm_two',
    'parallel_one',
    'parallel_two',
    'ebl_one',
    'ebl_two',
    'symbol_large',
    'symbol_small'
    ]
    
    first_commands = ['create', 'drop', 'vrm', 'parallel', 'ebl', 'symbol']
    second_commands = ['track', 'one', 'two', 'small', 'large']
    
    best_c, best_v = None, -1
    for i, f_c_1 in enumerate(final_commands):
        c1, v1 = f_c_1        
        if c1 in first_commands:
            for j, f_c_2 in enumerate(final_commands[i+1:]):
                c2, v2 = f_c_2
                can_c = c1+'_'+c2
                if can_c in all_commands:
                    can_v = v1 + v2
                    if can_v > best_v:
                        best_c = can_c
                        best_v = can_v
    #print(best_c, best_v)
    return str(best_c)                
        
    


# In[42]:


def get_accuracy(commands_out):
    acc_list = []
    for cmd, cmd_out in commands_out.items():
        cmd = cmd[:-2]
        pred_cmd = predict_probable_command(cmd_out)
        #print(cmd,'  ', pred_cmd)
        acc_ = cmd == pred_cmd
        #print(acc_)
        acc_list.append(acc_)
    return np.average(acc_list)


# In[43]:


commands_out = get_commands_out(dirname='./output_observation/')


# In[44]:


get_accuracy(commands_out)


# In[45]:


for folder in glob.glob('./all_observations/*'):
    commands_out = get_commands_out(folder+'/')
    acc_ = get_accuracy(commands_out)
    print('For folder: ', folder)
    print('accuracy is: ', acc_)


# In[46]:


os.getcwd()

