import os
import shutil
import glob

# # dir to stanford shapenet
# stanford_path = '/Users/yeelu/Desktop/AT3DCV/project/shapenet/train/partial/03001627/'

# # dir to shapenet chair mesh
# chair_mesh = '/Users/yeelu/Desktop/03_meshes/'

# # dir to store filtered shapenet mesh
# filter_path = '/Users/yeelu/Desktop/omer_mesh/'

# stanford_list = os.listdir(stanford_path)
# chair_list = os.listdir(chair_mesh)

# dict_for = {}
# for i, pc in enumerate(stanford_list):
#     dict_for[i] = pc[:-3]
#     # print(pc[:-3])

# for chair in chair_list:
#     # print(chair[:-4])
#     if (chair[:-4] in dict_for.values()):
#         original = chair_mesh + chair 
#         # print(original)
#         trans = filter_path + chair
#         # print(trans)
#         shutil.copyfile(original, trans)

# filter the mesh with cleaned pc

# dir to omer_fitness_pc
omer_path = '/Users/yeelu/Desktop/omer_fitness_pc/'

# dir to shapenet chair mesh
chair_mesh = '/Users/yeelu/Desktop/omer_mesh/'

# dir to store filtered shapenet mesh
filter_path = '/Users/yeelu/Desktop/omer_fitness_mesh/'

omer_list = os.listdir(omer_path)
chair_list = os.listdir(chair_mesh)

dict_for = {}
for i, pc in enumerate(omer_list):
    dict_for[i] = pc[:-4]
    # print(pc[:-3])

for chair in chair_list:
    # print(chair[:-4])
    if (chair[:-4] in dict_for.values()):
        original = chair_mesh + chair 
        # print(original)
        trans = filter_path + chair
        # print(trans)
        shutil.copyfile(original, trans)