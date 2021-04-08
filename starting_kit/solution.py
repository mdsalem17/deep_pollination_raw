import os
from os.path import isfile
import numpy as np
import pandas as pd


# ================ Small auxiliary functions =================

def read_solutions(data_dir):
    ''' Function to read the Labels from CSV files'''
    filenames_csv = data_dir +'/labels.csv'
   
    # print("\n\nContents of Directory: ", data_dir)
    # print(os.listdir(data_dir))
    
    
    if not isfile(filenames_csv):
        print('#--- ERROR ---# labels.csv NOT FOUND!')
        return 
    
    
    print('------------------------------------\nReading Solutions\n------------------------------------\n')
    file_names = pd.read_csv(filenames_csv)
    print('Number of solutions : %d' % file_names.shape[0])
    print("\nTrain solutions:", file_names[file_names.subset=='train'].subset.count())
    print("\nValidation solutions:", file_names[file_names.subset=='valid'].subset.count())
    print("\nTest solutions:", file_names[file_names.subset=='test'].subset.count())
    
    
    
    train_solution = file_names[file_names.subset=='train'].Labels.values
    valid_solution = file_names[file_names.subset=='valid'].Labels.values
    test_solution = file_names[file_names.subset=='test'].Labels.values
    
    solutions = []
    solution_names = []
    if train_solution.shape[0] > 0:
        solutions.append(train_solution)
        solution_names.append('train')

    if valid_solution.shape[0] > 0:
        solutions.append(valid_solution)
        solution_names.append('valid')
    
    if test_solution.shape[0] > 0:
        solutions.append(test_solution)
        solution_names.append('test')

    print("\n\nSolutions files are ready!")
    
    return (solution_names,solutions)


