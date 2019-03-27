
### Host Setup

    sudo apt install libpcap-dev virtualbox

Download and Configure the Application portion of the server:

    sudo add-apt-repository ppa:gns3/ppa
    sudo apt-get update
    sudo apt-get install gns3-gui

### This will fix the problems associated with the newer versions of GNS3 and Python3
### This could also fix issues in regards to Disco Dingo.
### They may be unnecessary in the future

    sudo pip3 install gns3-gui gns3-server async-generator
    sudo mv /usr/share/gns3/gns3-server/bin/python3 /usr/share/gns3/gns3-server/bin/python3.bak
    sudo mv /usr/share/gns3/gns3-gui/bin/python3 /usr/share/gns3/gns3-gui/bin/python3.bak
    sudo ln -s /usr/bin/python3 /usr/share/gns3/gns3-gui/bin/
    sudo ln -s /usr/bin/python3 /usr/share/gns3/gns3-server/bin/

## This will allow the Debian VMware Guest to attach to GNS3

    git clone https://github.com/GNS3/ubridge.git
    make
    sudo make install

### Debian VM setup
modify networks to add a localhost network

build a new host:
- change only: memory, and PAE enablement.
- connect NIC #2 to the local host network

Export appliance to an OVA Format 1.0

## VMWare Setup
Import the new Debian7 OVA into VMWare workstation
Confirm that Eth1 is NAT and ETH0 is HostOnly (e.g. vmnet4)
Install the VMware tools, poweroff

Go and download the GNS3 VM from www.gns3.com
Download and Configure the GNS3 VM
Similarly:
Confirm that Eth1 is NAT and ETH0 is HostOnly (e.g. vmnet4)

#### 
Setup the GNS3 Application and use the associated project files / base images.

