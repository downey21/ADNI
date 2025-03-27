#!/bin/bash

curl -fLO https://github.com/rordenlab/dcm2niix/releases/download/v1.0.20241211/dcm2niix_lnx.zip
unzip dcm2niix_lnx.zip
chmod +x dcm2niix

mv dcm2niix /usr/local/bin/

rm dcm2niix_lnx.zip

echo "dcm2niix installation complete! Version check:"
dcm2niix -v
