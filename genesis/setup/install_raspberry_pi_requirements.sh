echo "Installing Genesis dependencies..."
sudo apt-get install flac -y
sudo apt-get install git -y
sudo apt-get install portaudio19-dev -y
sudo apt-get install vlc -y
sudo apt-get install espeak -y
sudo python3 -m pip install --force-reinstall adafruit-blinka -y
sudo apt-get install python-alsaaudio
sudo apt-get install python3-alsaaudio
sudo apt-get install libttspico-utils
sudo apt-get source libttspico-utils
sudo apt-get install autoconf libtool help2man libpopt-dev debhelper
cd svox-1.0+git20130326/
dpkg-buildpackage -rfakeroot -us -uc
sudo dpkg-buildpackage -rfakeroot -us -uc
cd
sudo dpkg -i libttspico-data_*all.deb libttspico-utils*.deb libttspico0*.deb
sudo apt-get remove --purge autoconf libtool help2man libpopt-dev debhelper
sudo apt-get autoremove --purge
sudo wget -O - mic.raspiaudio.com | sudo bash
sudo wget -O - test.raspiaudio.com | sudo bash
sudo apt-get install python-pyaudio python3-pyaudio sox
sudo apt-get install libatlas-base-dev
wget http://downloads.sourceforge.net/swig/swig-3.0.10.tar.gz
sudo apt-get install libpcre3 libpcre3-dev
tar -xf swig-3.0.10.tar.gz
cd swig-3.0.10/
./configure --prefix=/usr --without-clisp --without-maximum-compile-warnings
make
sudo make install
install -v -m755 -d /usr/share/doc/swig-3.0.10 && cp -v -R Doc/* /usr/share/doc/swig-3.0.10
install -v -m755 -d /usr/share/doc/swig-3.0.10
sudo install -v -m755 -d /usr/share/doc/swig-3.0.10
echo "Installation complete!!"
echo "Rebooting..."
sudo reboot