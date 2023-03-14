FROM ubuntu
WORKDIR /usr/src/torchserve

FROM pytorch/torchserve:latest-gpu
USER root
RUN apt-get update --fix-missing && apt-get install -y \
&& apt-get install -y wget \
python3-pip \
default-jdk \ 
&& pip install wget \
&& python -m wget https://github.com/google/mtail/releases/download/v3.0.0-rc51/mtail_3.0.0-rc51_Linux_x86_64.tar.gz \
&& tar -xvzf mtail_3.0.0-rc51_Linux_x86_64.tar.gz \
&& chmod +x mtail \
&& rm mtail_3.0.0-rc51_Linux_x86_64.tar.gz

COPY model-server/config.properties ./
COPY model-server/metrics.yaml ./
COPY model-server/torchserve_custom.mtail ./
COPY scripts/torchserve_start.sh ./
COPY model-server/requirements_nn.txt ./
RUN pip install -r requirements_nn.txt

# Add NVIDIA container toolkit repository
 RUN distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
     && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add - \
     && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list \
     && apt-get update

 # Install NVIDIA container toolkit
 RUN apt-get install -y nvidia-container-toolkit

# Remove residual installation files
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*