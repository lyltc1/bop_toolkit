FROM continuumio/miniconda3:24.11.1-0

RUN apt-get update && apt-get install build-essential -y

WORKDIR /home
RUN git clone https://github.com/lyltc1/bop_toolkit
WORKDIR /home/bop_toolkit
RUN pip install numpy==1.26.0 scipy==1.14.1 kiwisolver==1.4.7 matplotlib==3.10.0 imageio==2.5.0 pypng==0.20220715.0 Cython==3.0.11 PyOpenGL==3.1.0 triangle==20230923 glumpy==1.2.1 opencv-python==4.10.0.84 Pillow==11.0.0 vispy>=0.14.3 webdataset==0.2.100
RUN pip install git+https://github.com/MartinSmeyer/cocoapi.git@v1.0#subdirectory=PythonAPI


# build command: docker build -t bop_toolkit .  
#          （or) docker build --no-cache -t bop_toolkit .
# run command: docker run -it bop_toolkit /bin/bash