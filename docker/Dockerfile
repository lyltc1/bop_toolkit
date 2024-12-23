FROM continuumio/miniconda3:24.11.1-0

RUN apt-get update && apt-get install build-essential -y

WORKDIR /home
RUN git clone https://github.com/lyltc1/bop_toolkit
RUN pip install -r /home/bop_toolkit/requirements.txt -e .

# RUN python3 --version


# build command: docker build -t bop_toolkit .
# run command: docker run -it bop_toolkit /bin/bash