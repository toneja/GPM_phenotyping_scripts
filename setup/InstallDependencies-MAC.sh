#!/bin/sh

# verify pip is installed
which pip3
if [ $? != 0 ]
then
	echo "pip3 missing..."
	exit 1
fi

# install python packages
PKGS="matplotlib \
numpy \
openpyxl \
pandas \
pillow \
requests \
scikit-learn \
scipy \
statsmodels \
tabulate"
for P in $PKGS
do
	pip3 install "$P"
	if [ $? != 0 ]
	then
		echo "Unable to install $P..."
		exit 1
	fi
done

# install Fiji - ImageJ has too many quirks on MacOS
URL="https://downloads.imagej.net/fiji/stable/fiji-stable-macosx-jdk.zip"
curl -o fiji.zip "$URL"
unzip fiji.zip
rm fiji.zip
mv Fiji.app /Applications
xattr -dr com.apple.quarantine /Applications/Fiji.app

mkdir -p ../"ECHO Images" ../results ../ImageJ/GPM/images ../ImageJ/GPM/results
