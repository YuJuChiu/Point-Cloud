import h5py
import numpy as np
import open3d as o3d
import glob
import os

h5_files = glob.glob('*.h5')


BASE_PATH = "/Users/yeelu/Desktop/np_pc"

for fname in h5_files:
	print(fname)
	f = h5py.File(fname, 'r')
	data = f['data']
	np_data = np.array(data)

	file_name = "{0}npy".format(fname[:-2])

	np.save(os.path.join(BASE_PATH, file_name), np_data)


print("DONE")

