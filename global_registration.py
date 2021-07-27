import open3d as o3d
import numpy as np
import copy
from scipy.spatial.transform import Rotation as R

# def draw_registration_result(source, target, transformation):
#     source_temp = copy.deepcopy(source)
#     target_temp = copy.deepcopy(target)
#     source_temp.paint_uniform_color([1, 0.706, 0])
#     target_temp.paint_uniform_color([0, 0.651, 0.929])
#     source_temp.transform(transformation)
#     o3d.visualization.draw_geometries([source_temp, target_temp],
#                                       zoom=0.4559,
#                                       front=[0.6452, -0.3036, -0.7011],
#                                       lookat=[1.9892, 2.0208, 1.8945],
#                                       up=[-0.2779, -0.9482, 0.1556])

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])

def preprocess_point_cloud(pcd, voxel_size):
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh

def prepare_dataset(voxel_size):
    print(":: Load two point clouds and disturb initial pose.")
    source = o3d.io.read_point_cloud("/Users/yeelu/desktop/omer_gt_pc_ply/672e20cc6ffa29d41c6aa36e5af1449.ply")
    target = o3d.io.read_point_cloud("/Users/yeelu/desktop/omer_mesh/672e20cc6ffa29d41c6aa36e5af1449.ply")
    trans_init = np.identity(4)
    r = R.from_euler('y', -90, degrees=True)
    trans_init[:3, :3] = r.apply(trans_init[:3, :3])

    source.transform(trans_init)
    draw_registration_result(source, target, np.identity(4))

    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh

voxel_size = 0.05  # means 5cm for this dataset
source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(
    voxel_size)

def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
            distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    return result

result_ransac = execute_global_registration(source_down, target_down,
                                            source_fpfh, target_fpfh,
                                            voxel_size)
print(result_ransac)
draw_registration_result(source_down, target_down, result_ransac.transformation)

def refine_registration(source, target, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    print(":: Point-to-plane ICP registration is applied on original point")
    print("   clouds to refine the alignment. This time we use a strict")
    print("   distance threshold %.3f." % distance_threshold)
    o3d.geometry.PointCloud.estimate_normals(source, search_param = o3d.geometry.KDTreeSearchParamHybrid( radius = 0.1, max_nn = 30))
    o3d.geometry.PointCloud.estimate_normals(target, search_param = o3d.geometry.KDTreeSearchParamHybrid( radius = 0.1, max_nn = 30))
    result = o3d.pipelines.registration.registration_icp(
        source, target, distance_threshold, result_ransac.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    return result

result_icp = refine_registration(source, target, source_fpfh, target_fpfh,
                                 voxel_size)
print("1", result_icp.fitness, "2")
draw_registration_result(source, target, result_icp.transformation)



# # transform the partial pc with -90 degree along y axis 
# source = o3d.io.read_point_cloud("/Users/yeelu/desktop/omer_partial_pc_ply/2acc2a87aef7cc559ca96b2737246fca.ply")
# trans_init = np.identity(4)
# r = R.from_euler('y', -90, degrees=True)
# trans_init[:3, :3] = r.apply(trans_init[:3, :3])
# source.transform(trans_init)

# transform_partial_pc = source

# transform_pc = o3d.io.write_point_cloud("/Users/yeelu/desktop/omer_transform/2acc2a87aef7cc559ca96b2737246fca.ply", transform_partial_pc)

# # below has to be modified
# source = o3d.io.read_point_cloud("1e7c8833d231178fdcddd0cba5e9fbec_pc_4.ply")
# target = o3d.io.read_point_cloud("1e7c8833d231178fdcddd0cba5e9fbec_mesh_4.ply")
# source_temp = copy.deepcopy(source)
# target_temp = copy.deepcopy(target)
# source_temp.paint_uniform_color([1, 0.706, 0])
# target_temp.paint_uniform_color([0, 0.651, 0.929])
# source_temp.transform(transformation)
# o3d.visualization.draw_geometries([source_temp, target_temp])