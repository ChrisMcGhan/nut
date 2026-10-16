FROM debian:trixie-slim@sha256:d7e12182ce18b85b93007c1dedf31f2d29e01ccf3182cc4017c709b6259bc132
RUN apt-get update && apt-get install -y --no-install-recommends build-essential autoconf automake libtool pkgconf git python3 zip file gcc-mingw-w64-x86-64 g++-mingw-w64-x86-64 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
