#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# تحميل نسخة FFmpeg ثابتة وتجهيزها
mkdir -p ffmpeg
cd ffmpeg
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar xvf ffmpeg-release-amd64-static.tar.xz --strip-components=1
cd ..
export PATH=$PATH:$(pwd)/ffmpeg
