sudo apt-get install autoconf automake autotools-dev curl python3 python3-pip libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev ninja-build git cmake libglib2.0-dev libslirp-dev -y
git clone https://github.com/riscv/riscv-gnu-toolchain && cd riscv-gnu-toolchain
./configure --prefix=/opt/riscv32 --with-arch=rv32im --with-abi=ilp32 --disable-linux
# add /opt/riscv32/bin to PATH
sudo make  # takes a lot of time, about ~1 hour.
