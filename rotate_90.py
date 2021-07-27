import open3d as o3d
import numpy as np
import copy
from scipy.spatial.transform import Rotation as R
import os

input_path = '/Users/yeelu/desktop/omer_gt_pc_ply/'
output_path = '/Users/yeelu/desktop/omer_gt_transform/'

pc_list = os.listdir(input_path)


for pc in pc_list:

    input = input_path + pc
    source = o3d.io.read_point_cloud(input)

    trans_init = np.identity(4)
    
    # transform the partial pc with -90 degree along y axis 
    r = R.from_euler('y', -90, degrees=True)
    trans_init[:3, :3] = r.apply(trans_init[:3, :3])

    source.transform(trans_init)

    output = output_path + pc
    transform_pc = o3d.io.write_point_cloud(output, source)