from Modulus import utils

import yaml
import os
import shutil
import stat


# Saves project
def save(file_path, data, mu2mech_dir):

    # Creates directory
    os.mkdir(file_path)

    # Writes configuration file
    file_name = file_path.split('/')[-1]+'.pf'
    print(file_name)
    with open(file_path+'/'+file_name, 'w') as file:
        documents = yaml.dump(data, file, sort_keys=False)

    root_src_dir = os.getcwd()+'/Output'  # Path/Location of the Output directory
    root_dst_dir = file_path+'/Output'   # Path to the destination folder

    utils.write_input(data, f"{file_path}/input.dat")

    if (data['calType'] == "Cahn Hilliard 1D"):
        source = "Sources/ch1d.o"
    elif (data['calType'] == "Cahn Hilliard 2D"):
        source = "Sources/ch2d_qualitative.o"
    elif (data['calType'] == "Cahn Hilliard 2D alloy"):
        source = "Sources/ch2d_alloy.o"
    elif (data['calType'] == "Cahn Hilliard 3D alloy"):
        source = "Sources/ch3d_alloy.o"

    os.makedirs(f"{file_path}/Sources", exist_ok=True)
    source_path = f"{mu2mech_dir}/{source}"
    destination_path = f"{file_path}/{source}"
    shutil.copyfile(source_path, f"{file_path}/{source}")
    copy_files_dirs(root_src_dir, root_dst_dir)


# Load project
def load(file_path):

    # Load config file
    with open(file_path) as file:
        data = yaml.full_load(file)

    tmp = file_path.rsplit('/', 1)
    root_src_dir = tmp[0]+"/Output"
    file_name = tmp[1]
    root_dst_dir = os.getcwd()+'/Output'

    # Delete previous files
    utils.delete_files(root_dst_dir+'/Data/*.dat')

    # Copy saved output data
    copy_files_dirs(root_src_dir, root_dst_dir)

    # Delete unnecessary config file
    utils.delete_files(os.getcwd()+'/Output/'+file_name)
    return data


# Copies files and directories from 'root_src_dir' to 'root_dst_dir'
def copy_files_dirs(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)
