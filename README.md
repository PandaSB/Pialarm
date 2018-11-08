sudo apt-get install python-dev
sudo apt install python-pip
git clone https://github.com/nvl1109/orangepi_zero_gpio
sudo python setup.py install
sudo apt-get install python-serial
apt-get install autofs nfs-kernel-server nfs-common --install-recommends -f -y
sudo apt-get install python-smbus
sudo su -c 'echo "i2c-dev" >> /etc/modules'
sudo adduser pi i2c 
sudo apt install usb-modeswitch
cd /tmp && tar -xzvf /usr/share/usb_modeswitch/configPack.tar.gz 19d2\:0166
# update  /etc/usb_modeswitch.conf 


schematics

                    3.3V    1 * *  2 5V
    I2C_SDA     SDA/GPIO12  3 * *  4 5V      I2C_5V
    I2C_SDL     SDL/GPIO11  5 * *  6 GND     I2C_GND
    BUZZER 5V       GPIO6   7 * *  8 GPIO98
    BUZZER GNS      GND     9 * * 10 GPIO99
                RX2/GPIO1  11 * * 12 GPIO 7
                TX2/GPIO0  13 * * 14 GND
                    GPIO3  15 * * 16 GPIO19
                    3.3V   17 * * 18 GPIO18
                    GPIO15 19 * * 20 GND      LOOP_DETECTOR_IN
                    GPIO16 21 * * 22 GPIO2    LOOP_DETECTOR_GND
                    GPIO14 23 * * 24 GPIO13
    LED_GND         GND    25 * * 26 GPIO10   LED_OUTPUT



                                   MATRIX KEYBOARD
                                  L  L  L  L  C  C  C
                                  1  2  3  4  1  2  3
                            |  |  |  |  |  |  |  |  | 
                            I  |  |  |  |  |  |  |  | 
                            N  P  P  P  P  P  P  P  P
                            T  7  6  5  4  3  2  1  0
                            |  |  |  |  |  |  |  |  | 
                          +---------------------------+
I2C_5V     ---- VCC ----  |                           |
I2C_GND    ---- GND ----  |   PCF8574                 |
I2C_SDA    ---- SDA ----  |                           |
I2C_SCL    ---- SCL ----  |                           |
                          +---------------------------+

                             |\|
LED_OUTPOUT ----/\/\/\/\-----| |---- LED_GND
                             |/|
                | /
BUZZER_5V   ----|/  Active 
BUZZERT_GND ----|\  Buzzer 5V 
                | \

