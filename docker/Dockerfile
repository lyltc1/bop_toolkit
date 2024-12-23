FROM continuumio/miniconda3:24.11.1-0

RUN apt-get update && apt-get install build-essential -y

WORKDIR /home
RUN git clone https://github.com/lyltc1/bop_toolkit
WORKDIR /home/bop_toolkit
RUN pip install numpy==1.26.0
RUN pip install -r requirements.txt -e .
RUN pip install git+https://github.com/MartinSmeyer/cocoapi.git@v1.0#subdirectory=PythonAPI
# RUN python3 --version


# build command: docker build -t bop_toolkit .
# run command: docker run -it bop_toolkit /bin/bash