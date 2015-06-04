# Load-VIRL-Configs
Makes a VIRL XML file from configuration files.

This script works on Python 2.7.

usage: lvc.py [-h] virl_file configs_path new_virl_file

Process configurations and integrate them into a VIRL file.

positional arguments:
  virl_file      The VIRL topology file we're looking for.
  configs_path   Path to the configuration files you want to add to the VIRL
                 file. The VIRL topology nodes must have the same names as the
                 configuration files' filenames. Ex. /home/configs/
  new_virl_file  The VIRL topology file we're creating with the configurations
                 in it.

optional arguments:
  -h, --help     show this help message and exit
