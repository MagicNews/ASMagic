#!/usr/bin/env bash

read -p "Do you want me to install Magic Anti Spam Bot? (Y/N): "

if [ "$REPLY" != "Y" ]; then
    echo "Exiting..."
else
    echo -e "\e[1;36mUpdating packages\e[0m"
    sudo apt-get update -y

    echo -e "\e[1;36mInstalling dependencies\e[0m"
    sudo apt-get install python2.7 python-pip -y
    
    
    echo -e "\e[1;36mInstalling python modules\e[0m"
    
    modules="requests redis"
    for module in $modules; do
        sudo pip install --upgrade $module
    done
        
    
    echo -e "\e[1;36mFetching latest Magic Anti Spam source code\e[0m"
    git clone https://github.com/MagicNews/ASMagic.git
    cd ASMagic
    sudo chmod 777 launch.sh
    echo -e "\e[1;32mMagicAntiSpam successfully installed! Change values in config file and run ./launch.sh\e[0m"
    echo " "
fi
