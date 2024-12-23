# Author: Tomas Hodan (hodantom@cmp.felk.cvut.cz)
# Center for Machine Perception, Czech Technical University in Prague

"""Configuration of the BOP Toolkit."""

import os

######## Docker ########
data_path = "/home/data/"
bop_folder = None
find_bop = False
for root, dirs, files in os.walk(data_path):
    for dir_name in dirs:
        if "bop" in dir_name.lower():
            bop_folder = os.path.join(root, dir_name)
            find_bop = True
            break
    if find_bop:
        break

os.environ["BOP_PATH"] = bop_folder
os.environ["EVAL_PATH"] = "/home/output/"
os.environ["OUTPUT_PATH"] = "/home/output/"
######## Basic ########

# Folder with the BOP datasets.
if "BOP_PATH" in os.environ:
    datasets_path = os.environ["BOP_PATH"]
else:
    datasets_path = r"/path/to/bop/datasets"

# Folder with pose results to be evaluated.
results_path = r"/home/input/"

# Folder for the calculated pose errors and performance scores.
if "EVAL_PATH" in os.environ:
    eval_path = os.environ["EVAL_PATH"]
else:
    eval_path = r"/path/to/eval/folder"

######## Extended ########

# Folder for outputs (e.g. visualizations).
if "OUTPUT_PATH" in os.environ:
    output_path = os.environ["OUTPUT_PATH"]
else:
    output_path = r"/path/to/output/folder"

# For offscreen C++ rendering: Path to the build folder of bop_renderer (github.com/thodan/bop_renderer).
bop_renderer_path = r"/path/to/bop_renderer/build"

# Executable of the MeshLab server.
meshlab_server_path = r"/path/to/meshlabserver.exe"

# Number of workers for the parallel evaluation of pose errors.
num_workers = 10

# use torch to calculate the errors
use_gpu = False
