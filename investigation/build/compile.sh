#!/bin/sh
set -eu
mkdir -p /work/src /out
cp -a /source/. /work/src/
cd /work/src
./autogen.sh > /out/bootstrap.log 2>&1
./configure --host=x86_64-w64-mingw32 --build=aarch64-linux-gnu --prefix=/ --with-all=no --without-ssl --without-doc --with-confdir=/etc > /out/configure.log 2>&1
make -j4 > /out/build.log 2>&1
make DESTDIR=/out/stage install > /out/install.log 2>&1
dpkg-query -W > /out/toolchain-packages.txt
find /out/stage -type f -name '*.exe' -exec file {} \; > /out/binaries.txt
