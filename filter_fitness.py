import open3d as o3d
import numpy as np
import copy
from scipy.spatial.transform import Rotation as R
import os 

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])

def preprocess_point_cloud(pcd, voxel_size):

    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2

    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5

    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh

def prepare_dataset(voxel_size, PC, MESH):

    source = o3d.io.read_point_cloud(PC)
    target = o3d.io.read_point_cloud(MESH)
    trans_init = np.identity(4)
    r = R.from_euler('y', -90, degrees=True)
    trans_init[:3, :3] = r.apply(trans_init[:3, :3])

    source.transform(trans_init)


    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh



def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5

    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
            distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    return result




def refine_registration(source, target, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5

    o3d.geometry.PointCloud.estimate_normals(source, search_param = o3d.geometry.KDTreeSearchParamHybrid( radius = 0.1, max_nn = 30))
    o3d.geometry.PointCloud.estimate_normals(target, search_param = o3d.geometry.KDTreeSearchParamHybrid( radius = 0.1, max_nn = 30))
    result = o3d.pipelines.registration.registration_icp(
        source, target, distance_threshold, result_ransac.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    return result




input_path_pc = '/Users/yeelu/desktop/omer_transform/'
input_path_mesh = '/Users/yeelu/desktop/omer_mesh/'
output_path = '/Users/yeelu/desktop/omer_fitness_pc/'

pc_file = os.listdir(input_path_pc)
mesh_file = os.listdir(input_path_mesh)


for pc in pc_file:
    
    input_pc = input_path_pc + pc
    PC = o3d.io.read_point_cloud(input_pc)
    pc_unvariant = o3d.io.read_point_cloud(input_pc)

    input_mesh = input_path_mesh + pc
    MESH = o3d.io.read_point_cloud(input_mesh)

    # set initial parameters
    voxel_size = 0.05  # means 5cm for this dataset


    trans_init = np.identity(4)
    r = R.from_euler('y', -90, degrees=True)
    trans_init[:3, :3] = r.apply(trans_init[:3, :3])

    PC.transform(trans_init)

    source_down, source_fpfh = preprocess_point_cloud(PC, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(MESH, voxel_size)
    

    source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(voxel_size, PC, MESH)

    # global registration
    result_ransac = execute_global_registration(source_down, target_down,
                                                source_fpfh, target_fpfh,
                                                voxel_size)
    # local refinement
    result_icp = refine_registration(PC, MESH, source_fpfh, target_fpfh,
                                    voxel_size)

    print(result_icp.fitness)
 
    if (result_icp.fitness > 0.8):
        output = output_path + pc
        o3d.io.write_point_cloud(output, pc_unvariant)
