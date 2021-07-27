import os 
import numpy as np
import glob

input_path = '/Users/yeelu/desktop/omer_gt_pc_npy/'

npy_list = glob.glob('/Users/yeelu/desktop/omer_gt_pc_npy/*.npy')

for npy in npy_list:

    input = os.path.join(input_path, npy)

    a = np.load(input, allow_pickle=True)
    np.asarray(a, dtype = np.float32)

    output = npy[:-4] + '.xyz.npy'

    np.save(output, a)






