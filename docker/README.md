# BOP Toolkit Docker

This folder contains the Docker setup for the BOP Toolkit.


## Download the Docker Image

```sh
docker pull lyltc1/bop_toolkit:latest
```

## (or) Build the Docker Image by Yourself
To build the Docker image, you can use one of the following commands:

```sh
docker build -t lyltc1/bop_toolkit:latest .
```

or

```sh
docker build --no-cache -t lyltc1/bop_toolkit:latest .
```

## Run the Docker Container

To run the Docker container, use the following command:

```sh
# make sure BOP/${DATASET} exists in ${FOLDER_CONTAINS_BOP}, i.e. BOP/ycbv
export FOLDER_CONTAINS_BOP=/mnt/2T/Data
# make sure xxx.csv exists in CSV_FOLDER
export CSV_FOLDER=~/git/dupe/Pose_Estimation_Model/log/pose_estimation_model_base_id0/ycbv_eval_iter600000/
# This is where the output file generated in
export OUTPUT_DIR=~/git/dupe/Pose_Estimation_Model/log/pose_estimation_model_base_id0/ycbv_eval_iter600000/output/
docker run -it \
  --runtime=nvidia \
  --gpus all \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  --shm-size 12G \
  -v ${FOLDER_CONTAINS_BOP}:/home/data:ro \
  -v ${OUTPUT_DIR}:/home/output:rw \
  -v ${CSV_FOLDER}:/home/input:rw \
  lyltc1/bop_toolkit:latest /bin/bash
```

Make sure to replace the paths with your actual paths.

### bop19 eval

```sh 
# (Inside the docker)
git pull  # get the updated code
export RESULT_FILENAMES=result_ycbv-test.csv
python scripts/eval_bop19_pose.py --result_filenames ${RESULT_FILENAMES} --use_gpu
```

### visualize result
``` sh
# (Inside the docker)
git pull  # get the updated code
export RESULT_FILENAMES=result_ycbv-test.csv
python scripts/vis_est_poses.py --result_filenames ${RESULT_FILENAMES} --vis_per_obj_id False --vis_origin_color True
```

### visualize ground truth
``` sh
# (Inside the docker)
git pull  # get the updated code
# --vis_rect whether to visualize the 2D bounding box
# --vis_rgb_background if False, black background will be used
python scripts/vis_gt_poses.py --dataset ycbv --scene_ids 58 --im_ids 86 --vis_rgb_background False --vis_rect False 
```

### vis symmetry
``` sh
# (Inside the docker)
git pull  # get the updated code
python scripts/vis_object_symmetries.py --dataset ycbv
```