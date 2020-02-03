FROM python:3.8.1-slim-buster AS builder
WORKDIR /root
RUN apt-get update && \
  apt-get install -y --no-install-recommends git=1:2.* && \
  pip install awscli==1.17.9 boto3==1.11.9 pyyaml==5.2 && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  git clone --depth=1 -b spike/merge https://github.com/alumi/ecsub.git && \
  rm -rf /root/ecsub/.git

FROM python:3.8.1-slim-buster
LABEL maintainer="aokad <aokad@hgc.jp>"
COPY --from=builder /root/.cache /root/.cache
COPY --from=builder /root/ecsub /root/ecsub
WORKDIR /root/ecsub
RUN pip install awscli==1.17.9 boto3==1.11.9 pyyaml==5.2 && \
  python setup.py build install
WORKDIR /root/genomon_pipeline_cloud
COPY . /root/genomon_pipeline_cloud
RUN python setup.py build install
WORKDIR /root
RUN rm -rf /root/ecsub /root/genomon_pipeline_cloud /root/.cache
ENTRYPOINT ["genomon_pipeline_cloud", "--engine", "ecsub"]
