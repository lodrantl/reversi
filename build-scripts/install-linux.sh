sudo lsb_release -a
sudo add-apt-repository -y ppa:mc3man/trusty-media
sudo apt-get update
sudo apt-get install -y  build-essential  git ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
pip install --upgrade pip virtualenv setuptools
pip install Cython
pip install pygments docutils pyinstaller
pip install git+https://github.com/kivy/kivy.git@master