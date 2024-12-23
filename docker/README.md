# BOP Toolkit Docker

This folder contains the Docker setup for the BOP Toolkit.


## Download the Docker Image
```sh

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
  bop_toolkit /bin/bash
```

Make sure to replace the paths with your actual paths.

### Inside the docker

```sh
export RESULT_FILENAMES=result_ycbv-test.csv
python scripts/eval_bop19_pose.py --result_filenames ${RESULT_FILENAMES} --use gpu
```