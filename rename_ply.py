import numpy as np
import open3d as o3d
import os
import glob

# input_path = '/Users/yeelu/desktop/blensor/*.npy'

# output_path = '/Users/yeelu/desktop/blensor/'


# partial_file = glob.glob('/Users/yeelu/Desktop/blensor/*.npy')
# # partial_pc_list = os.listdir(filter_path)
# for par_pc in partial_file:
#     partial_pc_file = input_path + par_pc
#     # print(partial_pc_file)
#     # read as numpy array
#     pc_array = np.load(par_pc, allow_pickle=True)
    
#     # read as point clound
#     pcd = o3d.geometry.PointCloud()
#     pcd.points = o3d.utility.Vector3dVector(pc_array)

#     # save to ply 
#     output = par_pc[:-4] + '.ply'
#     o3d.io.write_point_cloud(output, pcd)

file = "/Users/yeelu/downloads/bunny_extra_noisy.xyz.npy"

# partial_pc_file = input_path + par_pc
# print(partial_pc_file)
# read as numpy array
pc_array = np.load(file, allow_pickle=True)
    
# read as point clound
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(pc_array)

# save to ply 
output = file[:-4] + '.ply'
o3d.io.write_point_cloud(output, pcd)