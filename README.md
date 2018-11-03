sudo apt-get install python-dev
sudo apt install python-pip
git clone https://github.com/duxingkei33/orangepi_PC_gpio_pyH3.git
sudo python setup.py install
sudo apt-get install python-serial
apt-get install autofs nfs-kernel-server nfs-common --install-recommends -f -y
sudo apt-get install python-smbus
sudo su -c 'echo "i2c-dev" >> /etc/modules'
sudo adduser pi i2c 
sudo apt install usb-modeswitch
cd /tmp && tar -xzvf /usr/share/usb_modeswitch/configPack.tar.gz 19d2\:0166
# update  /etc/usb_modeswitch.conf 
