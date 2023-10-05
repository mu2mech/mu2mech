import glob
import os
import subprocess
import ffmpeg
from PIL import Image
import pyvista as pv
import numpy as np
from matplotlib.colors import ListedColormap
import yaml


# For input.dat file
def write_input(data, file_path):
    input_arr = []
    if(data['calType'] == "Cahn Hilliard 2D alloy" or data['calType'] == "Cahn Hilliard 3D alloy"):
        for key in data['coff']:
            input_arr.append(f'{key} {data["coff"][key]}')

    for key in data['parameters']:
        input_arr.append(f'{key} {data["parameters"][key]}')

    input_arr.append(f'timeInterval {data["timeInterval"]}')
    input_arr.append(f'totalTime {data["totalTime"]}')
    input_arr.append(f'resume {data["resume"]}')
    input_arr.append(f'resumeFrom {data["resumeFrom"]:.2f}')

    # Writes input.dat file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    input_file = open(file_path, "w")
    for row in input_arr:
        input_file.write(row+"\n")
    input_file.close()


def generate_HPC_input(data):
    # Writes configuration file
    with open(data['file_path'], 'w') as file:
        documents = yaml.dump(data["scheduler_details"], file, sort_keys=False)


# Converts keys from  variable "data"  to line edit name strings
def data_to_lineedit_string(self, data):
    eval_arr = []
    for key in data['parameters']:
        s = list(key)
        s[0] = s[0].upper()
        n = "".join(s)
        line_edit_name = "lineEdit"+n
        eval_arr.append("self."+line_edit_name +
                        ".setText(str(variables.data['parameters']['"+key+"']))")
    return eval_arr


# Saves values from line edit to variable "data"
def lineedit_string_to_data(self, data):
    eval_arr = []
    for key in data['parameters']:
        s = list(key)
        s[0] = s[0].upper()
        n = "".join(s)
        line_edit_name = "lineEdit"+n
        data['parameters'][key] = eval("self."+line_edit_name+".text()")

    return data


# Delete files from directory
def delete_files(path):
    for f in glob.glob(path):
        os.remove(f)


# Returns list of files
def get_time_list(path, extension):
    tmp = glob.glob(path+'/*'+extension)
    return sorted(list(map(lambda x: float(x.replace(
        path+"/output_", "").replace(extension, "")), tmp)), key=float)


# Takes image path, file path and time interval as an argument  and converts list of images to video
def convert_to_video(images_path, file_path, time_interval):
    frame_rate = 1000/float(time_interval)

    img_time_list = get_time_list(images_path, '.png')

    # exec_ute FFmpeg sub-process, with stdin pipe as input, and jpeg_pipe input format
    process = ffmpeg.input('pipe:', r=frame_rate).output(
        file_path, vcodec='libx264').overwrite_output().run_async(pipe_stdin=True)

    # Iterate files, read the content of each file and write it to stdin
    for time in img_time_list:
        with open(f'{images_path}/output_{time:.2f}.png', 'rb') as f:
            # Read the Image file content
            img_data = f.read()

            # Write Image data to stdin pipe of FFmpeg process
            process.stdin.write(img_data)
    # Close stdin pipe - FFmpeg fininsh encoding the output file.
    process.stdin.close()
    process.wait()


# Remove transparency and resize image
def trim_image(image_path):
    im = Image.open(image_path)
    im.getbbox()
    im = im.crop(im.getbbox())
    width, height = im.size
    left, top, right, bottom = 1, 1, width-1, height-1
    im1 = im.crop((left, top, right, bottom))
    # newsize = (size_x, size_y)
    # im1 = im1.resize(newsize)
    im1.save(image_path)


def color_gradient(mesh, variables):
    # Define the colors we want to use

    colors = {
        "red": np.array([1.0, 0.0, 0.0, 1.0]),
        "green": np.array([0.0, 128/256, 0.0, 1.0]),
        "blue": np.array([0.0, 0.0, 1.0, 1.0]),
        "yellow": np.array([1.0, 1.0, 0.0, 1.0])
    }

    my_colormap = None
    type = variables.plot_colors["m_plot"]["selected"]["color_type"]
    value = variables.plot_colors["m_plot"]["selected"]["color_value"]
    if(type == "discrete"):
        color_arr = value.split("-")
        color1 = color_arr[0]
        color2 = color_arr[1]

        mapping = np.linspace(mesh['values'].min(), mesh['values'].max(), 256)
        newcolors = np.empty((256, 4))
        newcolors[mapping > 0.5] = colors[color1]
        newcolors[mapping <= 0.5] = colors[color2]

        # Make the colormap from the listed colors
        my_colormap = ListedColormap(newcolors)
    elif(type == "continuous"):
        my_colormap = value

    return my_colormap


# Converts .dat to .vtk and export its screenshot
def convert_save_2d_vtk(time, image_path, actor_mesh, variables):
    plotter = pv.Plotter(off_screen=True)
    file_name = f'Output/Data/output_{time:.2f}.dat'
    plot_data = np.genfromtxt(
        file_name, delimiter=" ", usemask=True)
    plot_data_3d = np.repeat(
        plot_data[:, :, np.newaxis], 2, axis=2)
    mesh = pv.wrap(plot_data_3d)
    if(actor_mesh):
        plotter.remove_actor(actor_mesh)

    my_colormap = color_gradient(mesh, variables)
    actor_mesh = plotter.add_mesh(
        mesh, cmap=my_colormap, clim=[0.0, 1.0], show_scalar_bar=False)
    plotter.enable_parallel_projection()
    plotter.camera_position = 'xy'
    plotter.camera.zoom(1.2)
    plotter.screenshot(image_path, transparent_background=True)
    trim_image(image_path)
    plotter.close()
    plotter.deep_clean()
    return actor_mesh


# Runs bash command
def bash_command(command, args):
    return subprocess.run([command, args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)