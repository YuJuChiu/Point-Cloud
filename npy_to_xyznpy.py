import os 
import numpy as np
import glob

# input_path = '/Users/yeelu/desktop/omer_gt_pc_npy/'

# output_path = '/Users/yeelu/desktop/omer_gt_pc_xyznpy/'

# npy_list = glob.glob('/Users/yeelu/desktop/omer_gt_pc_npy/*.npy')

# for npy in npy_list:

#     input = os.path.join(input_path, npy)

#     a = np.load(input, allow_pickle=True)
#     np.asarray(a, dtype = np.float32)

#     output = npy[:-4] + '.xyz.npy'

#     np.save(output, a)

input = '/Users/yeelu/desktop/belnsor/429319c0c5bddfccd26c2593d1870bdb.xyz.npy'

# output_path = '/Users/yeelu/desktop/blensor/'

# npy_list = glob.glob('/Users/yeelu/desktop/omer_gt_pc_npy/*.npy')

# for npy in npy_list:

    # input = os.path.join(input_path, npy)

a = np.load(input, allow_pickle=True)
np.asarray(a, dtype = np.float32)

output = npy[:-8] + '.npy'

np.save(output, a)


