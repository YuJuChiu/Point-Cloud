import os
import shutil
import numpy as np
import h5py
import open3d as o3d
import glob

# dir to stanford shapenet pc (format: .h5)
stanford_path = '/Users/yeelu/Desktop/AT3DCV/project/shapenet/train/gt/03001627/'

# dir to shapenet chair mesh
chair_mesh = '/Users/yeelu/Desktop/omer_mesh/'

# dir to store filtered shapenet mesh
filter_path = '/Users/yeelu/Desktop/omer_gt_pc_ply/'

stanford_list = os.listdir(stanford_path)
chair_list = os.listdir(chair_mesh)

dict_for = {}
for i, chair in enumerate(chair_list):
  
    dict_for[i] = chair[:-4]

for pc in stanford_list:

    if (pc[:-3] in dict_for.values()):
          pc_file = stanford_path + pc
          f = h5py.File(pc_file, 'r')
          data = f['data']
          np_data = np.array(data)

          file_name = "{0}npy".format(pc[:-2])

          np.save(os.path.join(filter_path, file_name), np_data)
print("DONE with save npy")

partial_file = glob.glob('/Users/yeelu/Desktop/omer_gt_pc_ply/*.npy')

for par_pc in partial_file:
    partial_pc_file = filter_path + par_pc
    pc_array = np.load(par_pc, allow_pickle=True)
    
    # read as point clound
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pc_array)

    # save to ply 
    output = par_pc[:-4] + '.ply'
    o3d.io.write_point_cloud(output, pcd)

print('done with ply conversion')

npy_pc_list = glob.glob('/Users/yeelu/Desktop/omer_gt_pc_ply/*.ply')
for pc in npy_pc_list:

    pcd = o3d.io.read_point_cloud(pc)
    
    # fit to unit cube
    pcd.scale(1 / np.max(pcd.get_max_bound() - pcd.get_min_bound()),
              center=[0,0,0])
    # save to output file 
    output = pc[:-4] + '.ply'
    o3d.io.write_point_cloud(output, pcd)
    
print('done with normalization')



