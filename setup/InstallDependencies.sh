#!/bin/bash

# Check if Python3 is already installed
if command -v python3 &>/dev/null; then
  echo "Python is already installed."
else
  # Check which package manager is used by the system
  if command -v apt-get &>/dev/null; then
    package_manager="apt-get"
  elif command -v dnf &>/dev/null; then
    package_manager="dnf"
  elif command -v yum &>/dev/null; then
    package_manager="yum"
  elif command -v pacman &>/dev/null; then
    package_manager="pacman"
  else
    echo "Unable to determine the package manager for this system."
    exit 1
  fi

  # Install Python using the package manager
  case $package_manager in
    apt-get)
      sudo apt-get update
      sudo apt-get install -y python3
      ;;
    dnf)
      sudo dnf install -y python3
      ;;
    yum)
      sudo yum install -y python3
      ;;
    pacman)
      sudo pacman -S python3
      ;;
    *)
      echo "Unable to determine the package manager for this system."
      exit 1
      ;;
  esac

  # Check if Python3 was installed successfully
  if command -v python3 &>/dev/null; then
    echo "Python3 was installed successfully."
  else
    echo "Failed to install Python3."
    exit 1
  fi
fi

# Install the required Python3 modules
modules="openpyxl pandas sklearn tabulate tqdm"
sudo pip3 install $modules

# Install ImageJ
cd $(dirname $0)/../
wget https://wsr.imagej.net/distros/linux/ij153-linux64-java8.zip
if [ $? != 0 ]; then
	echo "Failed to download ImageJ archive."
	exit 1
fi
unzip ij153-linux64-java8.zip
if [ $? != 0 ]; then
	echo "Failed to unpack ImageJ archive."
	exit 1
fi
rm ij153-linux64-java8.zip
echo "Installed ImageJ application."
echo
echo "Setup Complete!"
