FROM ubuntu:16.04
MAINTAINER Yuichi Shiraishi <friend1ws@gmail.com> 

ARG MINIMAP2_VERSION=2.17
ARG MINIMAP2_RELEASE=minimap2-${MINIMAP2_VERSION}_x64-linux

RUN apt-get update && apt-get install -y \
    git \
    wget \
    bzip2 \
    make \
    gcc \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    python \
    python-pip

RUN wget https://github.com/samtools/htslib/releases/download/1.7/htslib-1.7.tar.bz2 && \
    tar jxvf htslib-1.7.tar.bz2 && \
    cd htslib-1.7 && \
    make && \
    make install

RUN wget https://github.com/lh3/minimap2/releases/download/v${MINIMAP2_VERSION}/${MINIMAP2_RELEASE}.tar.bz2 && \
    tar xf ${MINIMAP2_RELEASE}.tar.bz2 && \
    cp ${MINIMAP2_RELEASE}/minimap2 /usr/local/bin && \
    rm -rf ${MINIMAP2_RELEASE}

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install annot_utils==0.2.0
RUN pip install pysam==0.13

RUN git clone -b feature/blat-replacement-with-minimap2 https://github.com/chrovis/fusionfusion.git && \
    cd fusionfusion && \
    python setup.py install

RUN pip install chimera_utils==0.4.1

RUN apt-get update && apt-get install -y \
    libkrb5-3 \
    libpng12-0

RUN wget https://github.com/friend1ws/fusion_utils/archive/v0.2.0.tar.gz && \
    tar xzvf v0.2.0.tar.gz && \
    cd fusion_utils-0.2.0 && \
    python setup.py install
