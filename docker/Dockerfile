FROM nvidia/cudagl:11.4.2-runtime-ubuntu20.04

ENV TZ=US/Pacific
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install wget git build-essential fontconfig -y

# Set the default shell to bash instead of sh
SHELL ["/bin/bash", "--login", "-c"]
# Install Miniconda
RUN cd / && wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /miniconda.sh && \
    /bin/bash /miniconda.sh -b -p /opt/conda &&\
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh &&\
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc &&\
    /bin/bash -c "source ~/.bashrc" && \
    /opt/conda/bin/conda update -n base -c defaults conda -y &&\
    /opt/conda/bin/conda create -n bop python=3.12
ENV PATH=$PATH:/opt/conda/envs/bop/bin
RUN conda init bash && \
    echo "conda activate bop" >> ~/.bashrc && \
    conda activate bop
# # Install bop_toolkit
WORKDIR /home
RUN git clone https://github.com/lyltc1/bop_toolkit
WORKDIR /home/bop_toolkit
RUN pip install numpy==1.26.0 scipy==1.14.1 kiwisolver==1.4.7 matplotlib==3.10.0 imageio==2.5.0 pypng==0.20220715.0 Cython==3.0.11 PyOpenGL==3.1.0 triangle==20230923 glumpy==1.2.1 opencv-python==4.10.0.84 Pillow==11.0.0 vispy>=0.14.3 webdataset==0.2.100
RUN pip install git+https://github.com/MartinSmeyer/cocoapi.git@v1.0#subdirectory=PythonAPI
RUN pip install -e .