FROM arm64v8/ubuntu:latest

LABEL version="0.1.0"
LABEL David Sean "https://github.com/davidsean/pyleton"

WORKDIR /pyleton

RUN apt update && \
    apt install -y python3-pip
# install package locally (for development)
COPY . .
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "./docker/dev/entry.sh" ]