ARG PYTORCH="1.13.1"
ARG CUDA="11.6"
ARG CUDNN="8"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-runtime
RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/lyltc1/bop_toolkit