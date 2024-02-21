from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QSlider, QLabel, QVBoxLayout, QWidget, QFrame, QAction, QSplashScreen
from PySide2.QtCore import Qt, QProcess, QCoreApplication, QObject, QThread, Signal, SIGNAL
from PySide2.QtGui import QCursor, QIcon, QPixmap, QTextCursor, QColor

from Forms.main import Ui_MainWindow
from Forms.dialog_generate_input_hpc import Ui_DialogGenerateHPCInput
from Forms.dialog_param_ch1d import Ui_DialogParamCH1D
from Forms.dialog_param_ch2d import Ui_DialogParamCH2D
from Forms.dialog_param_ch2d_alloy import Ui_DialogParamCH2DAlloy
from Forms.dialog_param_ch3d_alloy import Ui_DialogParamCH3DAlloy
from Forms.dialog_new_calc import Ui_DialogNewCalc
from Forms.dialog_convert_to_video import Ui_DialogConvertToVideo
from Forms.dialog_2d_post_processing import Ui_DialogPostProcessing2D
from Forms.dialog_particles import Ui_DialogParticles
from Forms.dialog_3d_post_processing import Ui_DialogPostProcessing3D
from Forms.dialog_oof2_calculation import Ui_DialogOOF2Calculation
from Forms.dialog_plot_colors import Ui_DialogPlotColors
from Forms.dialog_view_calc_param import Ui_DialogViewCalcParam

from Modulus import variables
from Modulus import load_save_project, utils, load_libs
from Modulus import oof2_script

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pyvista as pv
from pyvistaqt import QtInteractor
import math
import numpy as np
import threading
import os
import shutil


class Ui_PhaseField (Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mu2mech")
        self.setupUi(self)
        self.setFixedSize(860, 680)
      

        self.pushButtonPlot.setEnabled(False)
        self.pushButtonEdit.clicked.connect(self.edit_prameters)
        self.pushButtonPostProcessing.clicked.connect(self.post_processing)
        self.actionNew.triggered.connect(self.new_calc)
        self.actionSave.triggered.connect(self.save_project)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionLoad.triggered.connect(self.load_project)
        self.actionExportAnimation.triggered.connect(self.export_animation)
        self.actionQuit.triggered.connect(QCoreApplication.instance().quit)
        self.pushButtonStartStopResume.clicked.connect(self.perform_calc)
        self.pushButtonStartStopResume.setEnabled(False)
        self.pushButtonEdit.setEnabled(False)
        self.pushButtonPostProcessing.setEnabled(False)
        self.pushButtonPlot.clicked.connect(self.plot_data)
        self.horizontalSlider.valueChanged.connect(self.slider_moved)
        self.actionSavePlot.setStatusTip('Save Plot')
        self.actionSavePlot.triggered.connect(self.save_plot)
        self.actionSaveAllPlots.triggered.connect(self.save_all_plots)
        self.checkBoxAxis.stateChanged.connect(self.checkbox_axis_changed)
        self.checkBoxColorbar.stateChanged.connect(
            self.checkbox_colorbar_changed)

        self.pushButtonLeft.clicked.connect(self.plot_left)
        self.pushButtonRight.clicked.connect(self.plot_right)
        self.pushButtonLeft.setIcon(QIcon('Images/Icons/left_arrow.png'))
        self.pushButtonRight.setIcon(QIcon('Images/Icons/right_arrow.png'))

        self.actionPlotColors.triggered.connect(self.select_plot_colors)

        # Delete old files
        utils.delete_files("./Output/PostData/*.dat")
        utils.delete_files("./Output/Data/*.dat")
        utils.delete_files("./Output/Img/*.png")
        utils.delete_files("./PostProcessing/Plots/*.png")

        # add the pyvista interactor object
        self.vlayout = QVBoxLayout()
        self.plotter = QtInteractor(self.framePlot)
        self.vlayout.addWidget(self.plotter)
        self.framePlot.setLayout(self.vlayout)
        self.actor_mesh = None
        self.actor_plane_mesh = None

        self.calc_process = None
        self.calc_thread_status = False
        self.job_submitted_hpc = False
        self.is_color_bar = True
        self.is_axis = True
        self.save_process = None

        self.slider_current_pos = 0

        # Close the splash screen
        splash.close()

    def select_plot_colors(self):
        PlotColors(self).exec_()

    def calc_running(self):
        self.lineEditTimeInterval.setEnabled(False)
        self.lineEditTotalTime.setEnabled(False)
        self.pushButtonEdit.setEnabled(False)
        self.pushButtonStartStopResume.setText("Pause")
        self.pushButtonPlot.setEnabled(False)
        self.labelStatus.setText("Performing calculation ...")
        self.labelStatus.setStyleSheet('color: black')
        self.labelStatus.repaint()

    def start_calc(self):
        print("starting calculation")
        self.display_char_values()
        # For running jobs in normal servers
        if(self.calc_process == None):
            self.calc_thread_status = True
            self.calc_process = QProcess()
            # print(self.source_binary)
            self.calc_process.start(self.source_binary, [])
            self.set_progress_status()
            self.calc_process.finished.connect(self.calc_completed)
        self.calc_running()


    def display_char_values(self):
        energy = variables.temp_selected_coff["a"]
        length = variables.temp_selected_coff["char_length"]
        time  =  variables.temp_selected_coff["char_time"]

        self.labelEnergyValue.setText(f"{energy:.2f}")
        self.labelLengthValue.setText(f"{length:.2f}")
        self.labelTimeValue.setText(f"{time:.2E}")

    def get_job_submitted_info(self, dl):
        self.job_id = dl.job_id
        self.calc_running()
        self.calc_thread_status = True
        self.set_progress_status()

    def calc_completed(self):
        self.calc_process = None

        self.calState = 2
        self.calc_thread_status = False
        self.lineEditTotalTime.setEnabled(True)
        self.pushButtonPlot.setEnabled(True)
        self.pushButtonStartStopResume.setText("Resume")
        self.labelStatus.setText("Calculation completed")
        self.labelStatus.setStyleSheet('color: green')
        self.pushButtonPostProcessing.setEnabled(True)

    def checkbox_axis_changed(self):
        self.is_axis = self.checkBoxAxis.isChecked()

    def checkbox_colorbar_changed(self):
        self.is_color_bar = self.checkBoxColorbar.isChecked()

    def new_calc_values(self):
        self.calState = 0
        self.slider_time_diff = 0
        self.source_binary = ""
        self.img_path = ""
        self.resume_plot_from = 0
        self.time_arr = []

        self.pushButtonEdit.setEnabled(True)
        self.labelCurrentStatus.setText("0")
        self.lineEditTimeInterval.setEnabled(True)
        self.pushButtonStartStopResume.setText("Start")
        self.plotLabel.clear()

    def new_calc(self):
        NewCalc(self).exec_()
        self.labelCalType.setText(variables.data['calType'])

        # Removing old files
        utils.delete_files("./Output/Data/*.dat")
        utils.delete_files("./Output/Img/*.png")

        self.new_calc_values()
        self.load_default_values()
        self.pushButtonPlot.setEnabled(False)

    def save_project(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save')

        self.labelStatus.setText("Saving project..")
        self.labelStatus.setStyleSheet('color: black')
        self.labelStatus.repaint()

        variables.data['totalTime'] = int(self.lineEditTotalTime.text())
        variables.data['timeInterval' ] = int(self.lineEditTimeInterval.text())
        load_save_project.save(file_path, variables.data)
        self.labelStatus.setText("Project saved")
        self.labelStatus.setStyleSheet('color: green')

    def load_project(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Load')

        self.labelStatus.setText("Loading Project..")
        self.labelStatus.setStyleSheet('color: black')
        variables.data = load_save_project.load(file_path)
        self.labelStatus.setText("Project loaded")
        self.labelStatus.setStyleSheet('color: green')

        # Set label and text field after project load
        self.labelCalType.setText(variables.data['calType'])
        self.lineEditTimeInterval.setText(
            str(variables.data['timeInterval']))
        self.lineEditTotalTime.setText(str(variables.data['totalTime']))
        self.pushButtonEdit.setEnabled(False)
        self.lineEditTimeInterval.setEnabled(False)
        self.pushButtonPostProcessing.setEnabled(True)
        self.pushButtonStartStopResume.setEnabled(True)
        self.pushButtonStartStopResume.setText("Resume")
        self.pushButtonStartStopResume.setEnabled(True)

        self.get_completed_calc_list()
        self.slider_init()
        self.calState = 2
        if(len(self.time_arr) > 0):
            percent_completed = int(
                self.time_arr[-1]/variables.data['totalTime']*100)
            self.labelProgress.setText(f'{percent_completed}%')
        self.labelCurrentStatus.setText(str(self.time_arr[-1]))

        if (variables.data['calType'] == "Cahn Hilliard 1D"):
            self.source_binary = "Sources/ch1d.o"
        elif (variables.data['calType'] == "Cahn Hilliard 2D"):
            self.source_binary = "Sources/ch2d_qualitative.o"
        elif (variables.data['calType'] == "Cahn Hilliard 2D alloy"):
            self.source_binary = "Sources/ch2d_alloy.o"
        elif (variables.data['calType'] == "Cahn Hilliard 3D alloy"):
            self.source_binary = "Sources/ch3d_alloy.o"
        print(self.source_binary)

    def export_animation(self):
        ExportAnimation(self).exec_()

    def load_default_values(self):
        variables.selected_temperature = None
        variables.selected_alloy = None
        
        if (variables.data['calType'] == "Cahn Hilliard 1D"):
            variables.data['parameters'] = {
                'lx': 256,
                'delT': 0.5,
                'kappa': 1,
                'delX': 0.5,
                'dTilda': 1.0
            }
            self.source_binary = "Sources/ch1d.o"

        elif (variables.data['calType'] == "Cahn Hilliard 2D"):
            variables.data['parameters'] = {
                'fluctuation': 0.0001,
                'cAvg': 0.4,
                'lx': 256,
                'ly': 256,
                'delT': 1,
                'delX': 0.4,
                'delY': 0.4
            }
            self.source_binary = "Sources/ch2d_qualitative.o"

        elif (variables.data['calType'] == "Cahn Hilliard 2D alloy"):
            variables.data['parameters'] = {
                'fluctuation': 0.0001,
                'cAvg': 0.4,
                'lx': 256,
                'ly': 256,
                'delT': 1,
                'delX': 0.4,
                'delY': 0.4
            }
            variables.data['coff'] = {
                'aa': 0,
                'bb': 0,
                'cc': 0,
                'dd': 0,
                'ee': 0
            }
            self.source_binary = "Sources/ch2d_alloy.o"

        elif (variables.data['calType'] == "Cahn Hilliard 3D alloy"):
            variables.data['parameters'] = {
                'fluctuation': 0.0001,
                'cAvg': 0.5,
                'lx': 32,
                'ly': 32,
                'lz': 32,
                'delT': 1,
                'delX': 0.4,
                'delY': 0.4,
                'delZ': 0.4
            }
            variables.data['coff'] = {
                'aa': 0,
                'bb': 0,
                'cc': 0,
                'dd': 0,
                'ee': 0,
            }
            self.source_binary = "Sources/ch3d_alloy.o"

        self.lineEditTimeInterval.setText(
            str(variables.data['timeInterval']))
        self.lineEditTotalTime.setText(str(variables.data['totalTime']))

    def edit_prameters(self):
        self.pushButtonStartStopResume.setEnabled(True)
        if (variables.data['calType'] == "Cahn Hilliard 1D"):
            ParamCH1D(self).exec_()
        elif (variables.data['calType'] == "Cahn Hilliard 2D"):
            ParamCH2D(self).exec_()
        elif (variables.data['calType'] == "Cahn Hilliard 2D alloy"):
            ParamCH2DAlloy(self).exec_()
        elif (variables.data['calType'] == "Cahn Hilliard 3D alloy"):
            ParamCH3DAlloy(self).exec_()

        self.pushButtonStartStopResume.setEnabled(True)

    def post_processing(self):
        if (variables.data['calType'] == "Cahn Hilliard 2D" or variables.data['calType'] == "Cahn Hilliard 2D alloy"):
            PostProcessing2D(self).show()
        elif(variables.data['calType'] == "Cahn Hilliard 3D alloy"):
            self.labelStatus.setText("Not implemented yet")
            self.labelStatus.setStyleSheet('color: black')

    def perform_calc(self):

        # for calState values
        # 0 - Calculation has not started
        # 1 - Calculation is running
        # 2 - Calculation is paused
        if(self.calState == 0 or self.calState == 2):
            self.calState = 1
            variables.data["timeInterval"] = int(
                self.lineEditTimeInterval.text())
            variables.data["totalTime"] = float(
                self.lineEditTotalTime.text())

            # write input.dat
            utils.write_input(variables.data, "Sources/input.dat")

            self.start_calc()

        elif(self.calState == 1):
            self.pushButtonPostProcessing.setEnabled(True)
            self.pushButtonPlot.setEnabled(True)
            self.calc_completed()
            variables.data['resume'] = 1
            variables.data['resumeFrom'] = self.time_arr[-1]

    # Gets the list of time for which calculations was completed
    def get_completed_calc_list(self):
        self.time_arr = utils.get_time_list('Output/Data', '.dat')

    # Plot data
    def plot_data(self):
        self.labelStatus.setText("Plotting results ...")
        self.labelStatus.setStyleSheet('color: black')
        self.pushButtonPlot.setEnabled(False)
        self.labelStatus.repaint()
        self.resume_plot_from = self.time_arr[-1]
        self.slider_init()
        self.labelStatus.setText("Plots generated")
        self.labelStatus.setStyleSheet('color: green')
        self.labelStatus.repaint()
        self.pushButtonPlot.setEnabled(True)

    # Sets currently calculated/plotted status
    def set_progress_status(self):
        if(self.calc_thread_status):
            threading.Timer(0.1, self.set_progress_status).start()
        self.get_completed_calc_list()
        if(len(self.time_arr) > 0):
            percent_completed = int(
                self.time_arr[-1]/variables.data['totalTime']*100)
            self.labelProgress.setText(f'{percent_completed}%')
            self.labelCurrentStatus.setText(str(self.time_arr[-1]))

    def slider_init(self):
        self.horizontalSlider.setSliderPosition(0)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)

        self.slider_time_diff = self.time_arr[1]-self.time_arr[0]
        slider_min = int(self.time_arr[0]/self.slider_time_diff)
        slider_max = int(self.time_arr[-1]/self.slider_time_diff)
        self.horizontalSlider.setMinimum(slider_min)
        self.horizontalSlider.setMaximum(slider_max)
        self.slider_moved()

    # Gets called when slider is moved
    def slider_moved(self):
        self.slider_current_pos = self.horizontalSlider.value()
        time = self.horizontalSlider.value()*self.slider_time_diff
        width = self.plotLabel.width()
        height = self.plotLabel.height()

        if (variables.data['calType'] == "Cahn Hilliard 3D alloy"):
            if(self.actor_mesh):
                self.plotter.remove_actor(self.actor_mesh)
            file_name = f'Output/Data/output_{time:.2f}.dat'
            plot_data_3d = np.genfromtxt(
                file_name, delimiter="\n", usemask=True)

            lx, ly, lz = int(variables.data['parameters']['lx']), int(variables.data[
                'parameters']['ly']), int(variables.data['parameters']['lz'])
            plot_data_3d = plot_data_3d.reshape(lx, ly, lz)
            mesh = pv.wrap(plot_data_3d)
            my_colormap = utils.color_gradient(mesh, variables)
            plot_type = variables.plot_colors["m_plot"]["selected"]["plot_type"]
            if plot_type == "volume":
                self.actor_mesh = self.plotter.add_volume(
                    mesh, cmap=my_colormap, clim=[0.0, 1.0], show_scalar_bar=self.is_color_bar, scalars="values", opacity="sigmoid")
            elif plot_type == "surface":
                self.actor_mesh = self.plotter.add_mesh(
                    mesh, cmap=my_colormap, clim=[0.0, 1.0], show_scalar_bar=self.is_color_bar, scalars="values")

            self.plotter.camera_position = 'iso'
            self.plotter.show_bounds(
                show_xaxis=self.is_axis, show_yaxis=self.is_axis, show_zaxis=self.is_axis)

        else:
            file_name = f'Output/Data/output_{time:.2f}.dat'
            plot_data = np.genfromtxt(
                file_name, delimiter=" ", usemask=True)
            plot_data_3d = np.repeat(plot_data[:, :, np.newaxis], 2, axis=2)
            mesh = pv.wrap(plot_data_3d)
            if(self.actor_mesh):
                self.plotter.remove_actor(self.actor_mesh)

            my_colormap = utils.color_gradient(mesh, variables)
            self.actor_mesh = self.plotter.add_mesh(
                mesh, cmap=my_colormap, clim=[0.0, 1.0], show_scalar_bar=self.is_color_bar, pickable=True)

            self.plotter.enable_point_picking()
            self.plotter.enable_parallel_projection()
            self.plotter.camera_position = 'xy'
            # self.plotter.camera.zoom(1.2)
            self.plotter.show_bounds(
                show_xaxis=self.is_axis, show_yaxis=self.is_axis, show_zaxis=False)

        self.plotter.track_click_position(
            callback=self.mouseclick_callback, side='left', viewport=False)
        self.plotter.show()
        variables.current_time = time
        self.timeDisplayLabel.setText(str(time))

    # Get mouse positions
    def mouseclick_callback(self, y):
        variables.mouse_position["x"] = int(y[0])
        variables.mouse_position["y"] = int(y[1])
        variables.mouse_position["z"] = int(y[2])
        self.update_pos_label()

    def update_pos_label(self):
        if(variables.data['calType'] == "Cahn Hilliard 3D alloy"):
            pos = f"x:{variables.mouse_position['x']}, y:{variables.mouse_position['y']}, z:{variables.mouse_position['z']}"
        elif (variables.data['calType'] == "Cahn Hilliard 2D" or variables.data['calType'] == "Cahn Hilliard 2D alloy"):
            pos = f"x:{variables.mouse_position['x']}, y:{variables.mouse_position['y']}"
        self.labelMousePosition.setText(pos)

    def plot_left(self):
        if(self.slider_current_pos >= 0):
            self.slider_current_pos -= 1
            self.horizontalSlider.setSliderPosition(self.slider_current_pos)

    def plot_right(self):
        slider_max = int(self.time_arr[-1]/self.slider_time_diff)
        if(self.slider_current_pos <= slider_max):
            self.slider_current_pos += 1
            self.horizontalSlider.setSliderPosition(self.slider_current_pos)

    def closeEvent(self, event):
        self.plotter.close()

    def save_plot(self):
        image_path, _ = QFileDialog.getSaveFileName(
            self, 'Save PLot', '.png', '*.png')
        actor_mesh = None
        actor_mesh = utils.convert_save_2d_vtk(
            variables.current_time, image_path, actor_mesh,variables)
        self.labelStatus.setText("Plot saved")
        self.labelStatus.setStyleSheet('color: green')

    def save_all_plots(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save')
        os.mkdir(file_path)

        try:
            # Create and start the worker thread
            self.thread = SaveThread(file_path, self.time_arr)
            self.thread.finished.connect(self.save_completed)
            self.thread.start()

            self.labelStatus.setText("Exporting plots ...")
            self.labelStatus.setStyleSheet('color: black')
            self.labelStatus.repaint()
        except:
            self.labelStatus.setText("Saving plots failed!")
            self.labelStatus.setStyleSheet('color: red')
            self.labelStatus.repaint()


    def saving_files(self, file_path):
        actor_mesh = None
        for time in self.time_arr:
            image_path = f'{file_path}/output_{time:.2f}.png'
            actor_mesh = utils.convert_save_2d_vtk(
                time, image_path, actor_mesh, variables)

    def save_completed(self):
        self.labelStatus.setText("All plots exported")
        self.labelStatus.setStyleSheet('color: green')


class SaveThread(QThread):
    def __init__(self, file_path, time_arr, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.time_arr = time_arr

    def run(self):
        actor_mesh = None
        for time in self.time_arr:
            image_path = f'{self.file_path}/output_{time:.2f}.png'
            actor_mesh = utils.convert_save_2d_vtk(
                time, image_path, actor_mesh, variables)


# For submitting jobs in HPC
class CreateInput(Ui_DialogGenerateHPCInput, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(370, 230)
        self.job_submitted = False
        self.pushButtonGenerateInput.clicked.connect(self.generate_input)
        self.pushButtonOutDir.clicked.connect(self.select_path)

    def select_path(self):
        self.file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save PLot', '.hpc', '*.hpc')
        self.lineEditOutDir.setText(self.file_path)

    def generate_input(self):
        data = {
            "file_path": self.file_path,
            "scheduler_details": {
                "scheduler_type": self.comboBoxScheduler.currentText(),
                "cores":  int(self.lineEditCores.text()),
                "time_hours": self.lineEditTimeHour.text(),
                "time_mins": self.lineEditTimeMinute.text(),
                "time_seconds": self.lineEditTimeSecond.text()
            }
        }
        utils.generate_HPC_input(data)
        self.labelMsg.setText("File generated")
        self.labelMsg.setStyleSheet('color: green')

# For changing the plot colors
class PlotColors(Ui_DialogPlotColors, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(320, 460)
        self.radioButtonContinuous.toggled.connect(
            self.radio_button_continuous)
        self.radioButtonDiscrete.toggled.connect(
            self.radio_button_discrete)
        self.buttonBox.accepted.connect(self.selected_colors)
        self.load_data()

    def load_data(self):

        # Load data for composition vs Axis
        for color in variables.plot_colors["c_a_plot"]["options"]["colors"]:
            # print(color)
            self.comboBoxColor.addItem(color)

        self.lineEditLThickness.setText(
            str(variables.plot_colors["c_a_plot"]["selected"]["thickness"]))

        # Load data for microstructure plot
        for option in variables.plot_colors["m_plot"]["options"]:
            for color in variables.plot_colors["m_plot"]["options"][option]:
                eval(f'self.comboBox{option.capitalize()}.addItem("{color}")')

        type = variables.plot_colors["m_plot"]["selected"]["color_type"]
        eval(f'self.radioButton{type.capitalize()}.setChecked(True)')
        value = variables.plot_colors["m_plot"]["selected"]["color_value"]
        eval(f'self.comboBox{type.capitalize()}.setCurrentText("{value}")')
        if(type == "discrete"):
            self.radio_button_discrete()
        elif(type == "continuous"):
            self.radio_button_continuous()

        self.comboBoxPlotType.setCurrentText(
            variables.plot_colors["m_plot"]["selected"]["plot_type"])

    def selected_colors(self):

        # Set data for composition vs Axis
        variables.plot_colors["c_a_plot"]["selected"]["thickness"] = float(
            self.lineEditLThickness.text())
        variables.plot_colors["c_a_plot"]["selected"]["color"] = self.comboBoxColor.currentText(
        )

        # Save data for 2D microstructure in "variables"
        for key in variables.plot_colors["m_plot"]["options"]:
            if eval(f'self.radioButton{key.capitalize()}.isChecked()'):
                variables.plot_colors["m_plot"]["selected"]["color_type"] = key
                variables.plot_colors["m_plot"]["selected"]["color_value"] = eval(
                    f'self.comboBox{key.capitalize()}.currentText()')
                break

        variables.plot_colors["m_plot"]["selected"]["plot_type"] = self.comboBoxPlotType.currentText(
        )

    def radio_button_continuous(self):
        self.comboBoxDiscrete.setEnabled(False)
        self.comboBoxContinuous.setEnabled(True)

    def radio_button_discrete(self):
        self.comboBoxContinuous.setEnabled(False)
        self.comboBoxDiscrete.setEnabled(True)


# For starting new calculation
class NewCalc(Ui_DialogNewCalc, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(320, 150)
        self.buttonBoxNew.accepted.connect(self.new_calc_values)

    def new_calc_values(self):
        variables.data['calType'] = self.comboBoxCalType.currentText()
        self.close()


# For editing parameters of Cahn Hillard 1D
class ParamCH1D(Ui_DialogParamCH1D, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(250, 300)

        eval_arr = utils.data_to_lineedit_string(self, variables.data)
        for e in eval_arr:
            eval(e)

        self.buttonBoxPramCH1D.accepted.connect(self.save_pram_ch1d)

    def save_pram_ch1d(self):
        variables.data = utils.lineedit_string_to_data(self, variables.data)


# For editing parameters of Cahn Hilliard 2D qualitiative
class ParamCH2D(Ui_DialogParamCH2D, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(250, 450)
        # hides close button
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint)

        eval_arr = utils.data_to_lineedit_string(self, variables.data)
        for e in eval_arr:
            eval(e)

        self.buttonBoxPramCH2D.clicked.connect(self.save_pram_ch2d)

    def save_pram_ch2d(self):
        variables.data = utils.lineedit_string_to_data(self, variables.data)
        self.close()


# For editing parameters of Cahn Hilliard 2D for alloy
class ParamCH2DAlloy(Ui_DialogParamCH2DAlloy, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(410, 370)
        self.buttonBoxPramCH2DAlloy.clicked.connect(self.save_pram_ch2d)
        self.pushButtonViewPhaseDiagram.clicked.connect(
            self.view_phase_diagram)
        self.pushButtonViewParameters.clicked.connect(self.view_gibbs_param)
        self.comboBoxAlloy.currentTextChanged.connect(
            self.load_temperature_data)
        # hides close button
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint)

        # copy values from variables to linedit
        eval_arr = utils.data_to_lineedit_string(self, variables.data)
        for e in eval_arr:
            eval(e)     
        
        files_list = os.listdir("TC_Data/Coff/")
        variables.alloys = []
        
        # Replace the '.csv' extension with an empty string
        for file in files_list:
            alloy = file.replace('.csv', '')
            variables.alloys.append(alloy)
        
        for alloy in variables.alloys:
            self.comboBoxAlloy.addItem(alloy)

        # copy selected alloy and temperature from variable to combobox   
        if(variables.selected_alloy):
            self.comboBoxAlloy.setCurrentText(variables.selected_alloy)
            
        if(variables.selected_temperature):
            self.comboBoxTemperature.setCurrentText(variables.selected_temperature)

        temperature = self.comboBoxTemperature.currentText()
        variables.temp_selected_coff = self.coff_data[temperature]


    def view_phase_diagram(self):
        self.dialogPhaseDiagarm = QDialog(self)
        self.labelPhaseDiagram = QLabel(self.dialogPhaseDiagarm)
        self.dialogPhaseDiagarm.setFixedSize(800, 800)
        self.dialogPhaseDiagarm.setWindowTitle(QCoreApplication.translate(
            "DialogPhaseDiagram", f'{self.comboBoxAlloy.currentText()} Phase Diagram', None))
        self.img_path = f'TC_Data/Phase_Diagram/{self.comboBoxAlloy.currentText()}.png'
        pixmap = QPixmap(self.img_path)
        width = 800
        height = 800
        self.labelPhaseDiagram.setPixmap(pixmap.scaled(
            width, height, Qt.KeepAspectRatio))

        self.dialogPhaseDiagarm.show()

    def view_gibbs_param(self):
        temperature = self.comboBoxTemperature.currentText()
        variables.temp_selected_coff = self.coff_data[temperature]
        ViewCalcParam(self).show()
        
    def load_temperature_data(self):
        try:
            file_path = f'TC_Data/Coff/{self.comboBoxAlloy.currentText()}.csv'
        except:
            print("File does not exist")
        loaded_data = np.genfromtxt(file_path, delimiter=',')
        self.comboBoxTemperature.clear()
        self.coff_data = {}
        
        try:
            for d in loaded_data:
                self.coff_data[str(d[0])] = {}
                self.coff_data[str(d[0])]['temperature'] = d[0]
                self.coff_data[str(d[0])]['aa'] = d[1]
                self.coff_data[str(d[0])]['bb'] = d[2]
                self.coff_data[str(d[0])]['cc'] = d[3]
                self.coff_data[str(d[0])]['dd'] = d[4]
                self.coff_data[str(d[0])]['ee'] = d[5]
                self.coff_data[str(d[0])]['a'] = d[6]
                self.coff_data[str(d[0])]['diffusivity'] = d[7]
                self.coff_data[str(d[0])]['gb_energy'] = d[8]
                self.coff_data[str(d[0])]['kappa'] = d[9]
                self.coff_data[str(d[0])]['char_length'] = d[10]
                self.coff_data[str(d[0])]['char_time'] = d[11]
                self.coff_data[str(d[0])]['elem'] = self.comboBoxAlloy.currentText()
                self.comboBoxTemperature.addItem(str(d[0]))
        except:
            print(f"Data not in correct format for {self.comboBoxAlloy.currentText()}")
            
    def save_pram_ch2d(self):
        variables.selected_alloy = self.comboBoxAlloy.currentText()
        variables.selected_temperature = self.comboBoxTemperature.currentText()
        variables.data = utils.lineedit_string_to_data(self, variables.data)
        variables.data['coff']['aa'] = str(self.coff_data[self.comboBoxTemperature.currentText(
        )]['aa'])
        variables.data['coff']['bb'] = str(self.coff_data[self.comboBoxTemperature.currentText(
        )]['bb'])
        variables.data['coff']['cc'] = str(self.coff_data[self.comboBoxTemperature.currentText(
        )]['cc'])
        variables.data['coff']['dd'] = str(self.coff_data[self.comboBoxTemperature.currentText(
        )]['dd'])
        variables.data['coff']['ee'] = str(self.coff_data[self.comboBoxTemperature.currentText(
        )]['ee'])
        self.close()


class ViewCalcParam(Ui_DialogViewCalcParam, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(710, 440)
        self.coff = {}
        self.coff['a'] = variables.temp_selected_coff['aa']
        self.coff['b'] = variables.temp_selected_coff['bb']
        self.coff['c'] = variables.temp_selected_coff['cc']
        self.coff['d'] = variables.temp_selected_coff['dd']
        self.coff['e'] = variables.temp_selected_coff['ee']
        self.coff['A'] = variables.temp_selected_coff['a']
        self.coff['diffusivity'] = variables.temp_selected_coff['diffusivity']
        self.coff['gb_energy'] = variables.temp_selected_coff['gb_energy']
        self.coff['kappa'] = variables.temp_selected_coff['kappa']
        self.coff['char_length'] = variables.temp_selected_coff['char_length']
        self.coff['char_time'] = variables.temp_selected_coff['char_time']
        
        x_arr = np.arange(0, 1, 0.01)

        # Inflection points
        point_1 = (-6 * self.coff['b'] + math.sqrt(36 * self.coff['b'] * self.coff['b'] - 96 * self.coff['a'] * self.coff['c'])) / (24 * self.coff['a'])
        point_2 = (-6 * self.coff['b'] - math.sqrt(36 * self.coff['b'] * self.coff['b'] - 96 * self.coff['a'] * self.coff['c'])) / (24 * self.coff['a'])
        # Check and swap if necessary
        if point_1 > point_2:
            point_1, point_2 = point_2, point_1
        self.labelInflextionPointValue.setText(f'{point_1:.2f}, {point_2:.2f}')

        # binodal points
        self.binodal_points = self.obtain_binodal_points()
        self.labelBinodalPointValue.setText(f'{self.binodal_points[0]:.2f}, {self.binodal_points[1]:.2f}')

        # Barrier height
        barrier_height = self.barrier_height_non_dim() * self.coff["A"]
        self.labelBarrierHeightValue.setText(f'{barrier_height:.2f}')

        # Diffusivity
        self.labelDiffusivityValue.setText(f'{self.coff["diffusivity"]:.2E}')

        # GB energy
        self.labelGBEnergyValue.setText(f'{self.coff["gb_energy"]:.2f}')

        vfunc = np.vectorize(self.fun) 
        y_arr = vfunc(x_arr) * self.coff['A']
        elem = variables.temp_selected_coff["elem"].split('-')[-1]

        # PLot G vs X
        fig = plt.figure(figsize=(4, 5), dpi=300)
        ax = fig.add_subplot()
        plt.plot(x_arr, y_arr)
        img = f'Images/gx.png'
        plt.xlim([0, 1])
        plt.xlabel(f"Mole fraction of {elem}", fontsize=12)
        plt.ylabel("Gibbs energy (KJ/mole)", fontsize=12)
        plt.savefig(img, bbox_inches="tight", dpi=300)
        plt.close()
        pixmap = QPixmap(img)
        self.labelGXPlot.setPixmap(pixmap)
        self.labelGXPlot.setScaledContents(True)
        self.resize(pixmap.width(), pixmap.height())
    

    # Equation for G vs X plot
    def fun(self,x):
        return self.coff['a']*x**4+self.coff['b']*x**3+self.coff['c']*x**2+self.coff['d']*x+self.coff['e']
        
    def obtain_binodal_points(self):
        # Specify the range [0, 1] and step size
        start = 0
        end = 1
        step_size = 0.001

        binodal_x_values = []

        # Iterate over the range and identify local minima
        for x in np.arange(start, end, step_size):
            # Check if x is not at the boundary
            if start < x < end:
                # Check if the derivative changes sign around x
                if self.fun(x - step_size) > self.fun(x) < self.fun(x + step_size):
                    binodal_x_values.append(x)

        return sorted(binodal_x_values)
    
    def barrier_height_non_dim(self):        
        # Generate x values for the plot
        x_values = np.linspace(0, 1, 1000)
        y_values = self.fun(x_values)

        # Find critical points numerically by checking where the derivative changes sign
        f_prime = np.gradient(y_values, x_values)
        derivative_sign_changes = np.where(np.diff(np.sign(f_prime)))[0]
        critical_points_numerical = x_values[derivative_sign_changes]

        # Evaluate the function at critical points and find the maximum and minimum values
        function_values_numerical = self.fun(critical_points_numerical)
        max_value_numerical = max(function_values_numerical)
        min_value_numerical = min(function_values_numerical)

        # Calculate the difference between the highest and lowest points
        diff = max_value_numerical - min_value_numerical

        return diff


class ParamCH3DAlloy(Ui_DialogParamCH3DAlloy, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(430, 420)

        eval_arr = utils.data_to_lineedit_string(self, variables.data)
        for e in eval_arr:
            eval(e)

        self.buttonBoxPramCH3DAlloy.clicked.connect(self.save_pram_ch3d)
        self.pushButtonViewPhaseDiagram.clicked.connect(
            self.view_phase_diagram)
        self.pushButtonViewParameters.clicked.connect(self.view_gibbs_param)
        self.comboBoxAlloy.currentTextChanged.connect(
            self.load_temperature_data)
        # hides close button
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint)

        files_list = os.listdir("TC_Data/Coff/")
        variables.alloys = []
        
        # Replace the '.csv' extension with an empty string
        for file in files_list:
            alloy = file.replace('.csv', '')
            variables.alloys.append(alloy)
        
        for alloy in variables.alloys:
            self.comboBoxAlloy.addItem(alloy)

        temperature = self.comboBoxTemperature.currentText()
        variables.temp_selected_coff = self.coff_data[temperature]
            
            
    def view_gibbs_param(self):
        temperature = self.comboBoxTemperature.currentText()
        variables.temp_selected_coff = self.coff_data[temperature]
        ViewCalcParam(self).show()


    def view_phase_diagram(self):
        self.dialogPhaseDiagarm = QDialog(self)
        self.labelPhaseDiagram = QLabel(self.dialogPhaseDiagarm)
        self.dialogPhaseDiagarm.setFixedSize(800, 800)
        self.dialogPhaseDiagarm.setWindowTitle(QCoreApplication.translate(
            "DialogPhaseDiagram", f'{self.comboBoxAlloy.currentText()} Phase Diagram', None))
        self.img_path = f'TC_Data/Phase_Diagram/{self.comboBoxAlloy.currentText()}.png'
        pixmap = QPixmap(self.img_path)
        width = 800
        height = 800
        self.labelPhaseDiagram.setPixmap(pixmap.scaled(
            width, height, Qt.KeepAspectRatio))

        self.dialogPhaseDiagarm.show()


    def load_temperature_data(self):
        try:
            file_path = f'TC_Data/Coff/{self.comboBoxAlloy.currentText()}.csv'
        except:
            print("File does not exist")
        loaded_data = np.genfromtxt(file_path, delimiter=',')
        self.comboBoxTemperature.clear()
        self.coff_data = {}
        try:
            for d in loaded_data:
                self.coff_data[str(d[0])] = {}
                self.coff_data[str(d[0])]['temperature'] = d[0]
                self.coff_data[str(d[0])]['aa'] = d[1]
                self.coff_data[str(d[0])]['bb'] = d[2]
                self.coff_data[str(d[0])]['cc'] = d[3]
                self.coff_data[str(d[0])]['dd'] = d[4]
                self.coff_data[str(d[0])]['ee'] = d[5]
                self.coff_data[str(d[0])]['a'] = d[6]
                self.coff_data[str(d[0])]['diffusivity'] = d[7]
                self.coff_data[str(d[0])]['gb_energy'] = d[8]
                self.coff_data[str(d[0])]['kappa'] = d[9]
                self.coff_data[str(d[0])]['char_length'] = d[10]
                self.coff_data[str(d[0])]['char_time'] = d[11]
                self.coff_data[str(d[0])]['elem'] = self.comboBoxAlloy.currentText()
                self.comboBoxTemperature.addItem(str(d[0]))
        except:
            print(f"Data not in correct format for {self.comboBoxAlloy.currentText()}")
            
    def save_pram_ch3d(self):
        variables.data = utils.lineedit_string_to_data(self, variables.data)
        variables.data['coff']['aa'] = str(self.coff_data[self.comboBoxTemperature.currentText(
        )]['aa'])
        variables.data['coff']['bb'] = str(self.coff_data[self.comboBoxTemperature.currentText(
        )]['bb'])
        variables.data['coff']['cc'] = str(self.coff_data[self.comboBoxTemperature.currentText(
        )]['cc'])
        variables.data['coff']['dd'] = str(self.coff_data[self.comboBoxTemperature.currentText(
        )]['dd'])
        variables.data['coff']['ee'] = str(self.coff_data[self.comboBoxTemperature.currentText(
        )]['ee'])
        # print(variables.data)
        self.close()


class PostProcessing2D(Ui_DialogPostProcessing2D, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        utils.delete_files("PostProcessing/Plots/*.png")

        # Set icons
        self.pushButtonBrowseSavePlot.setIcon(QIcon('Images/Icons/folder.png'))
        self.pushButtonBrowseSaveAllPlots.setIcon(
            QIcon('Images/Icons/folder.png'))
        self.pushButtonBrowseExportAnimation.setIcon(
            QIcon('Images/Icons/folder.png'))
        self.pushButtonGetMousePosition.setIcon(
            QIcon('Images/Icons/mouse.png'))

        self.horizontalSliderTime.valueChanged.connect(self.slider_moved)
        self.pushButtonGetMousePosition.clicked.connect(self.get_mouse_pos)
        self.pushButtonPlot.clicked.connect(self.plot_graph)
        self.pushButtonBrowseSavePlot.clicked.connect(self.select_plot_path)
        self.pushButtonSavePlot.clicked.connect(self.save_plot)
        self.pushButtonBrowseSaveAllPlots.clicked.connect(
            self.select_all_plot_path)
        self.pushButtonSaveAllPlots.clicked.connect(self.save_all_plots)
        self.pushButtonBrowseExportAnimation.clicked.connect(
            self.select_animation_path)
        self.pushButtonExportAnimation.clicked.connect(self.export_animation)
        self.comboBoxVideoFormat.currentIndexChanged.connect(
            self.reset_file_path)
        self.pushButtonParticlesInfo.clicked.connect(self.particles_info)
        self.pushButtonPredictProperty.clicked.connect(self.predict_property)

        self.pushButtonLeft.clicked.connect(self.plot_left)
        self.pushButtonRight.clicked.connect(self.plot_right)
        self.pushButtonLeft.setIcon(QIcon('Images/Icons/left_arrow.png'))
        self.pushButtonRight.setIcon(QIcon('Images/Icons/right_arrow.png'))

        # Width of plotting area in main window in pixels
        self.width_x = 442
        self.width_y = 431

        # Offset of plotting area from the start plot
        self.offset_x = 77
        self.offset_y = 98

        self.time_arr = utils.get_time_list('Output/Data', '.dat')
        self.slider_init()

        self.slider_current_pos = 0

    # Slide the slider left by one step
    def plot_left(self):
        if(self.slider_current_pos >= 0):
            self.slider_current_pos -= 1
            self.horizontalSliderTime.setSliderPosition(
                self.slider_current_pos)

    # Slide the slider right by one step
    def plot_right(self):
        slider_max = int(self.time_arr[-1]/self.slider_time_diff)
        if(self.slider_current_pos <= slider_max):
            self.slider_current_pos += 1
            self.horizontalSliderTime.setSliderPosition(
                self.slider_current_pos)

    # Get mouse positions
    def get_mouse_pos(self):
        self.lineEditX.setText(str(variables.mouse_position['x']))
        self.lineEditY.setText(str(variables.mouse_position['y']))

    def predict_property(self):
        OOF2Calculation(self).show()

    def particles_info(self):
        Particles2D(self).show()

    def reset_file_path(self):
        self.lineEditFilePathExportAnimation.setText("")

    # intialize slider
    def slider_init(self):
        self.horizontalSliderTime.setSliderPosition(0)
        self.horizontalSliderTime.setTickInterval(1)
        self.horizontalSliderTime.setSingleStep(1)
        self.horizontalSliderTime.setTickPosition(QSlider.TicksBelow)

        self.slider_time_diff = self.time_arr[1]-self.time_arr[0]
        slider_min = int(self.time_arr[0]/self.slider_time_diff)
        slider_max = int(self.time_arr[-1]/self.slider_time_diff)
        self.horizontalSliderTime.setMinimum(slider_min)
        self.horizontalSliderTime.setMaximum(slider_max)
        self.slider_moved()

    # Gets called when slider is moved
    def slider_moved(self):
        time = self.horizontalSliderTime.value()*self.slider_time_diff
        width = self.labelPlot.width()
        height = self.labelPlot.height()
        self.img_path = f'PostProcessing/Plots/output_{time:.2f}.png'
        pixmap = QPixmap(self.img_path)
        self.labelPlot.setPixmap(pixmap.scaled(
            width, height, Qt.KeepAspectRatio))
        self.show()
        self.labelTime.setText(str(time))
        self.lineEditTime.setText(str(time))

    def plot_graph(self):
        self.grid_x = int(self.lineEditX.text())
        self.grid_y = int(self.lineEditY.text())
        self.labelStatus.setText("Plotting ...")
        self.labelStatus.setStyleSheet('color: black')
        self.labelStatus.repaint()
        for time in self.time_arr:

            # Reads data from a file
            file_name = f'Output/Data/output_{time:.2f}.dat'
            plot_data = np.genfromtxt(
                file_name, delimiter=" ", usemask=True)

            plot_data_post = None
            if(self.comboBoxAxis.currentText() == "x"):
                plot_data_post = plot_data[self.grid_y, :]
            else:
                plot_data_post = plot_data[:, self.grid_x]

            grid = np.arange(0, len(plot_data_post), 1)

            fig = plt.figure(figsize=(5, 5), dpi=300)
            ax = fig.add_subplot()
            plt.xlabel("x")
            plt.ylabel("Composition")

            plot_type = self.comboBoxPlotType.currentText()
            color = variables.plot_colors["c_a_plot"]["selected"]["color"]
            thickness = float(
                variables.plot_colors["c_a_plot"]["selected"]["thickness"])
            if(plot_type == "line"):
                plt.plot(grid, plot_data_post, linewidth=thickness, c=color)
            elif(plot_type == "dotted"):
                plt.scatter(grid, plot_data_post, linewidth=thickness, c=color)

            plt.xlim(0, len(plot_data_post))
            plt.ylim(0, 1.1)
            img = f'PostProcessing/Plots/output_{time:.2f}.png'
            plt.savefig(img, bbox_inches="tight")
            plt.close()

        self.slider_init()
        self.labelStatus.setText("Plots generated")
        self.labelStatus.setStyleSheet('color: green')
        self.labelStatus.repaint()

    def select_plot_path(self):
        self.file_path, _ = QFileDialog.getSaveFileName(
            self, 'Export Plot', '.png', '*.png')
        self.lineEditFilePathSavePlot.setText(self.file_path)

    def save_plot(self):
        time = float(self.lineEditTime.text())
        image_path = f'PostProcessing/Plots/output_{time:.2f}.png'
        try:
            pixmap = QPixmap(image_path)
            pixmap.save(self.file_path)
            self.labelStatus.setText("Plot saved")
            self.labelStatus.setStyleSheet('color: green')
        except:
            self.labelStatus.setText("Error: Plot could not be exported")
            self.labelStatus.setStyleSheet('color: red')

    def select_all_plot_path(self):
        self.file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save')
        self.lineEditFilePathSaveAllPlots.setText(self.file_path)

    def save_all_plots(self):
        try:
            os.mkdir(self.file_path)
            for time in self.time_arr:
                image_path = f'PostProcessing/Plots/output_{time:.2f}.png'
                pixmap = QPixmap(image_path)
                pixmap.save(f'{self.file_path}/output_{time:.2f}.png')
            self.labelStatus.setText("All plots saved")
            self.labelStatus.setStyleSheet('color: green')
        except:
            self.labelStatus.setText("Error: Plots could not be exported")
            self.labelStatus.setStyleSheet('color: red')

    def select_animation_path(self):
        video_format = self.comboBoxVideoFormat.currentText()
        self.file_path, _ = QFileDialog.getSaveFileName(
            self, 'Export PLot Animation', f'.{video_format}', f'*.{video_format}')
        self.lineEditFilePathExportAnimation.setText(self.file_path)

    def export_animation(self):
        images_path = 'PostProcessing/Plots'
        self.file_path = self.lineEditFilePathExportAnimation.text()
        if(len(os.listdir(images_path)) != 0 and self.file_path):
            self.labelStatus.setText("Converting...")
            self.labelStatus.setStyleSheet('color: black')
            self.labelStatus.repaint()
            time_interval = self.lineEditTimeInterval.text()
            utils.convert_to_video(images_path, self.file_path, time_interval)
            self.labelStatus.setText("Animation exported")
            self.labelStatus.setStyleSheet('color: green')
        else:
            self.labelStatus.setText("Error: Animation could not be exported")
            self.labelStatus.setStyleSheet('color: red')


class OOF2Calculation(Ui_DialogOOF2Calculation, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(600, 580)
        self.pushButtonGetMousePosition.clicked.connect(self.get_mouse_pos)
        self.pushButtonBrowseOutDir.clicked.connect(self.save_path)
        self.pushButtonPredict.clicked.connect(self.predict)
        self.pushButtonGetMousePosition.setIcon(
            QIcon('Images/Icons/mouse.png'))
        self.actor_mesh = None
        self.calc_process = None
        
        self.load_default()
        
    
    # Load default values
    def load_default(self):
        self.lineEditPhase1C11.setText(variables.oof2_param['elastic_constants']['phase_1']['C11'])
        self.lineEditPhase1C12.setText(variables.oof2_param['elastic_constants']['phase_1']['C12'])
        self.lineEditPhase1C44.setText(variables.oof2_param['elastic_constants']['phase_1']['C44'])
        self.lineEditPhase2C11.setText(variables.oof2_param['elastic_constants']['phase_2']['C11'])
        self.lineEditPhase2C12.setText(variables.oof2_param['elastic_constants']['phase_2']['C12'])
        self.lineEditPhase2C44.setText(variables.oof2_param['elastic_constants']['phase_2']['C44'])
        self.lineEditXElements.setText(variables.oof2_param['mesh']['x_elements'])
        self.lineEditYElements.setText(variables.oof2_param['mesh']['y_elements'])
        self.comboBoxElementType.setCurrentText(variables.oof2_param['mesh']['element_type'])
        self.lineEditBC1Value.setText(variables.oof2_param['boundary_conditions']['bc1']['value'])
        self.lineEditBC2Value.setText(variables.oof2_param['boundary_conditions']['bc2']['value'])
        
        
    # Co-ordinates for phase selection
    def get_mouse_pos(self):
        self.lineEditX.setText(str(variables.mouse_position['x']))
        self.lineEditY.setText(str(variables.mouse_position['y']))
        self.labelStatus.setText("Continious phase selected")
        self.labelStatus.setStyleSheet('color: green')
        
    # Copy parameters from GUI to "variables"
    def oof2_parameters(self):
        os.mkdir(self.output_path)
        self.convert_to_image()
        self.script_path = f"{os.getcwd()}/OOF2/temp_scripts/script"
        variables.oof2_param['image_path'] = self.image_path
        variables.oof2_param['image_name'] = self.image_path.split('/')[-1]
        variables.oof2_param['output_path'] = self.output_path
        variables.oof2_param['coordinate']['x'] = self.lineEditX.text()
        variables.oof2_param['coordinate']['y'] = self.lineEditY.text()
        variables.oof2_param['elastic_constants']['phase_1']['C11'] = self.lineEditPhase1C11.text()
        variables.oof2_param['elastic_constants']['phase_1']['C12'] = self.lineEditPhase1C12.text()
        variables.oof2_param['elastic_constants']['phase_1']['C44'] = self.lineEditPhase1C44.text()
        variables.oof2_param['elastic_constants']['phase_2']['C11'] = self.lineEditPhase2C11.text()
        variables.oof2_param['elastic_constants']['phase_2']['C12'] = self.lineEditPhase2C12.text()
        variables.oof2_param['elastic_constants']['phase_2']['C44'] = self.lineEditPhase2C44.text()
        variables.oof2_param['mesh']['x_elements'] = self.lineEditXElements.text()
        variables.oof2_param['mesh']['y_elements'] = self.lineEditYElements.text()
        variables.oof2_param['mesh']['element_type'] = self.comboBoxElementType.currentText()
        variables.oof2_param['boundary_conditions']['bc1']['value'] = self.lineEditBC1Value.text()
        variables.oof2_param['boundary_conditions']['bc2']['value'] = self.lineEditBC2Value.text()
        
        print(variables.oof2_param)
        
      

    def save_path(self):
        self.output_path, _ = QFileDialog.getSaveFileName(
            self, 'Save')
        self.lineEditOutDir.setText(self.output_path)


    def predict(self):
        self.oof2_parameters()

        # Run OOF2
        self.run_oof2()

        # Set running status
        self.labelStatus.setText("Performing Calculations...")
        self.labelStatus.setStyleSheet('color: black')

    def run_script(self, completed_fn_str):
        calc_command = f"oof2 --image {self.image_path} --script {os.getcwd()}/OOF2/temp_scripts/script"
        if(self.calc_process == None):
            self.calc_process = QProcess()
            self.calc_process.start(calc_command)
            self.calc_process.finished.connect(eval(completed_fn_str))


    # Read values from output of OOF2
    def read_strain(self, file_path):
        with open(file_path) as file:
            lines = file.readlines()

        return float(lines[-1].split(',')[-1])

    def step1_completed(self):
        print("step1 completed")
        self.calc_process = None
        self.step1_postprocessing()
        oof2_script.step2(variables.oof2_param)

        # Run step 2
        self.run_script("self.step2_completed")

    def step1_postprocessing(self):
        strain_x = self.read_strain(
            f"{variables.oof2_param['output_path']}/bcn1_elastic_strain_xx")
        strain_y = self.read_strain(
            f"{variables.oof2_param['output_path']}/bcn1_elastic_strain_yy")
        variables.oof2_param['p_ratio'] = -strain_y/strain_x
        print(strain_x,-strain_y)

    def run_oof2(self):
        oof2_script.step1(variables.oof2_param)
        self.run_script("self.step1_completed")

    def step2_completed(self):
        self.calc_process == None
        self.labelStatus.setText("Completed")
        self.labelStatus.setStyleSheet('color: green')
        self.oof2_output()

    # For reading the output generated from OOF2
    def read_oof2_output(self, file_path):
        file1 = open(file_path, "r+")
        data = file1.readlines()
        val = data[-1].split(" ")[-1]
        return float(val)

    # Dislays OOF2 calculation results
    def oof2_output(self):
        output_path = variables.oof2_param['output_path']
        strain_xx = self.read_oof2_output(
            f"{output_path}/bcn2_elastic_strain_xx")

        stress_xx = self.read_oof2_output(f"{output_path}/bcn2_stress_xx ")
        strain_yy = self.read_oof2_output(
            f"{output_path}/bcn2_elastic_strain_yy")
        stress_yy = self.read_oof2_output(f"{output_path}/bcn2_stress_yy ")
        out_str = f'Young\'s modulus : {stress_xx/strain_xx:.2f} GPa\nPoission\'s Ratio :  {-strain_yy/strain_xx:.2f}'
        self.labelOutput.setText(out_str)

    # Converts mesh to image
    def convert_to_image(self):
        self.plotter = pv.Plotter(off_screen=True)
        file_name = f'Output/Data/output_{variables.current_time:.2f}.dat'
        if(self.actor_mesh):
            self.plotter.remove_actor(self.actor_mesh)
        elif (variables.data['calType'] == "Cahn Hilliard 2D" or variables.data['calType'] == "Cahn Hilliard 2D alloy"):
            plot_data = np.genfromtxt(
                file_name, delimiter=" ", usemask=True)
            plot_data_3d = np.repeat(
                plot_data[:, :, np.newaxis], 2, axis=2)
            mesh = pv.wrap(plot_data_3d)
            my_colormap = utils.color_gradient(mesh, variables)
            self.actor_mesh = self.plotter.add_mesh(
                mesh, cmap=my_colormap, clim=[0.0, 1.0], show_scalar_bar=False)
            self.plotter.enable_parallel_projection()
            self.plotter.camera_position = 'xy'
            self.plotter.camera.zoom(1.2)

        self.image_path = f"{self.output_path}/output_{variables.current_time:.2f}.png"
        self.plotter.screenshot(self.image_path, transparent_background=True)
        utils.trim_image(self.image_path)

    def closeEvent(self, event):
        print(variables.oof2_param)


class Particles2D(Ui_DialogParticles, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        input_arr = []
        input_arr.append(f"lx {variables.data['parameters']['lx']}")
        input_arr.append(f"ly {variables.data['parameters']['ly']}")
        input_arr.append(f"time {variables.current_time}")
        input_file = open("Sources/input.dat", "w")
        self.source_binary = "./Sources/hkl_2d.o"
        for row in input_arr:
            input_file.write(row+"\n")
        input_file.close()

        self.start_calc()

    def start_calc(self):
        try:
            self.p = QProcess()
            self.p.finished.connect(self.calc_completed)
            self.p.start(self.source_binary, [])
        except NameError:
            self.p = None

    def handle_stdout(self):
        d = self.p.readAllStandardOutput()

    def calc_completed(self):
        file_name = f'Output/PostData/volume_{variables.current_time:.2f}.dat'
        p_vol_data = np.genfromtxt(file_name, delimiter=" ", usemask=True)
        file_name = f'Output/PostData/avg_rad_{variables.current_time:.2f}.dat'
        p_avg_rad_data = np.genfromtxt(file_name, delimiter=" ", usemask=True)

        self.setWindowTitle(
            f'Time {variables.current_time:.2f}')
        self.labelParticlesTop.setText("No.\tVolume\tSize")
        s = ''
        # print(p_vol_data)
        for data in p_vol_data:
            s += f'{data[0]:.0f}\t{data[2]:.2f}\t{data[3]:.2f}\n'
        self.labelParticles.setText(s)

        s = f'Total Particles: {p_avg_rad_data[3]:.0f}\nAverage size: {p_avg_rad_data[1]:.2f}'
        self.labelAvgParticles.setText(s)


class Particles3D(Ui_DialogParticles, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        input_arr = []
        input_arr.append(f"lx {variables.data['parameters']['lx']}")
        input_arr.append(f"ly {variables.data['parameters']['ly']}")
        input_arr.append(f"lz {variables.data['parameters']['lz']}")
        input_arr.append(f"time {variables.current_time}")
        input_file = open("Sources/input.dat", "w")
        self.source_binary = "./Sources/hkl_3d.o"
        for row in input_arr:
            input_file.write(row+"\n")
        input_file.close()

        self.start_calc()

    def start_calc(self):
        try:
            self.p = QProcess()
            self.p.finished.connect(self.calc_completed)
            self.p.start(self.source_binary, [])
        except NameError:
            self.p = None

    def handle_stdout(self):
        d = self.p.readAllStandardOutput()

    def calc_completed(self):
        file_name = f'Output/PostData/volume_{variables.current_time:.2f}.dat'
        p_vol_data = np.genfromtxt(file_name, delimiter=" ", usemask=True)
        file_name = f'Output/PostData/avg_rad_{variables.current_time:.2f}.dat'
        p_avg_rad_data = np.genfromtxt(file_name, delimiter=" ", usemask=True)
        self.setWindowTitle(
            f'3D Particles at time {variables.current_time:.2f}')
        self.labelParticlesTop.setText("No.\tVolume\tSize")
        s = ''
        # print(p_vol_data.shape)
        if(p_vol_data.shape == (4,)):
            # print("test")
            p_vol_data = p_vol_data.reshape((1, 4))
        # print(p_vol_data.shape)
        for data in p_vol_data:
            # print(data)
            s += f'{data[0]:.0f}\t{data[2]:.2f}\t{data[3]:.2f}\n'
        self.labelParticles.setText(s)

        s = f'Total Particles: {p_avg_rad_data[2]:.0f}\nAverage size: {p_avg_rad_data[1]:.2f}'
        self.labelAvgParticles.setText(s)


class PostProcessing3D(Ui_DialogPostProcessing3D, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # add the pyvista interactor object
        self.vlayout = QVBoxLayout()
        self.plotter = QtInteractor(self.framePlot)
        self.vlayout.addWidget(self.plotter)
        self.framePlot.setLayout(self.vlayout)

        self.x_max = int(variables.data['parameters']['lx'])-1
        self.y_max = int(variables.data['parameters']['ly'])-1
        self.z_max = int(variables.data['parameters']['lz'])-1
        self.max_val = 0
        self.time_arr = utils.get_time_list('Output/Data', '.dat')

        self.comboBoxAxis.currentTextChanged.connect(self.axis_selected)
        self.horizontalSliderAxis.valueChanged.connect(self.axis_slider_moved)
        self.horizontalSliderTime.valueChanged.connect(self.plot_slider_moved)
        self.pushButtonPlot.clicked.connect(self.generate_plot)
        self.checkBoxAxis.stateChanged.connect(self.checkbox_axis_changed)
        self.checkBoxColorbar.stateChanged.connect(
            self.checkbox_colorbar_changed)
        self.pushButtonParticlesInfo.clicked.connect(self.particles_info)
        self.pushButtonBrowseSaveIntersection.clicked.connect(
            self.select_intersection_path)
        self.pushButtonSaveIntersection.clicked.connect(self.save_intersection)

        self.axis_selected()

        self.actor_mesh = None
        self.is_color_bar = True
        self.is_axis = True

        self.time_intersection()

    def time_intersection(self):
        for time in self.time_arr:
            self.comboBoxTimeIntersection.addItem(str(time))

    def select_intersection_path(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save')
        self.lineEditFilePathSaveIntersection.setText(file_path)

    def save_intersection(self):
        try:
            self.labelStatus.setText("Saving plots ...")
            self.labelStatus.setStyleSheet('color: black')
            self.labelStatus.repaint()
            folder_path = self.lineEditFilePathSaveIntersection.text()
            os.mkdir(folder_path)
            time = float(self.comboBoxTimeIntersection.currentText())
            file_name = f'Output/Data/output_{time:.2f}.dat'
            plot_data_3d = np.genfromtxt(
                file_name, delimiter="\n", usemask=True)
            lx, ly, lz = int(variables.data['parameters']['lx']), int(variables.data[
                'parameters']['ly']), int(variables.data['parameters']['lz'])
            plot_data_3d = plot_data_3d.reshape(lx, ly, lz)
            axis = self.comboBoxAxisINtersection.currentText()

            if(axis == "x"):
                size = lx
            elif(axis == "y"):
                size = ly
            elif(axis == "z"):
                size = lz

            plotter = pv.Plotter(off_screen=True)
            for ind in range(size):
                if(axis == "x"):
                    plot_data_intersection = plot_data_3d[ind, :, :]
                elif(axis == "y"):
                    plot_data_intersection = plot_data_3d[:, ind, :]
                elif(axis == "z"):
                    plot_data_intersection = plot_data_3d[:, :, ind]

                plot_data_2d = np.repeat(
                    plot_data_intersection[:, :, np.newaxis], 2, axis=2)
                mesh = pv.wrap(plot_data_2d)
                if(self.actor_mesh):
                    plotter.remove_actor(self.actor_mesh)
                self.actor_mesh = plotter.add_mesh(mesh, cmap="OrRd", clim=[
                    0.0, 1.0], show_scalar_bar=False)
                image_path = f'{folder_path}/output_{ind}.png'
                plotter.enable_parallel_projection()
                plotter.camera_position = 'xy'
                plotter.camera.zoom(1.2)
                plotter.screenshot(
                    image_path, transparent_background=True)
                utils.trim_image(image_path)

            self.labelStatus.setText("Plot saved")
            self.labelStatus.setStyleSheet('color: green')
        except:
            self.labelStatus.setText("Error: Plot could not be exported")
            self.labelStatus.setStyleSheet('color: red')

    def particles_info(self):
        Particles3D(self).exec_()

    def checkbox_axis_changed(self):
        self.is_axis = self.checkBoxAxis.isChecked()

    def checkbox_colorbar_changed(self):
        self.is_color_bar = self.checkBoxColorbar.isChecked()

    def generate_plot(self):
        self.pushButtonPlot.setEnabled(False)
        self.labelStatus.setText("Plotting...")
        self.labelStatus.repaint()
        self.plot_data_all = {}

        for time in self.time_arr:
            file_name = f'Output/Data/output_{time:.2f}.dat'
            plot_data = np.genfromtxt(
                file_name, delimiter="\n", usemask=True)
            plot_data = plot_data[9:]
            self.plot_data_all[time] = np.empty(
                [self.x_max+1, self.y_max+1, self.z_max+1], dtype=float)
            for z in range(0, self.z_max+1):
                for y in range(0, self.y_max+1):
                    for x in range(0, self.x_max+1):
                        self.plot_data_all[time][x, y, z] = plot_data[x*(self.y_max+1)
                                                                      * (self.z_max+1)+y*(self.z_max+1)+z]

        self.pushButtonPlot.setEnabled(True)
        self.labelStatus.setText("Done")
        self.plot_slider_init()

    def plot_slider_init(self):
        self.horizontalSliderTime.setSliderPosition(0)
        self.horizontalSliderTime.setTickInterval(1)
        self.horizontalSliderTime.setSingleStep(1)
        self.horizontalSliderTime.setTickPosition(QSlider.TicksBelow)

        self.slider_time_diff = self.time_arr[1]-self.time_arr[0]
        slider_min = int(self.time_arr[0]/self.slider_time_diff)
        slider_max = int(self.time_arr[-1]/self.slider_time_diff)
        self.horizontalSliderTime.setMinimum(slider_min)
        self.horizontalSliderTime.setMaximum(slider_max)
        self.plot_slider_moved()

    def plot_slider_moved(self):

        time = self.horizontalSliderTime.value()*self.slider_time_diff
        c_text = self.comboBoxAxis.currentText()
        p_data = 0
        if(c_text == "x"):
            plot_data = self.plot_data_all[time][self.current_val, :, :]
        elif(c_text == "y"):
            plot_data = self.plot_data_all[time][:, self.current_val, :]
        elif(c_text == "z"):
            plot_data = self.plot_data_all[time][:, :, self.current_val]

        plot_data_3d = np.repeat(plot_data[:, :, np.newaxis], 2, axis=2)
        mesh = pv.wrap(plot_data_3d)
        if(self.actor_mesh):
            self.plotter.remove_actor(self.actor_mesh)
        self.actor_mesh = self.plotter.add_mesh(
            mesh, cmap="OrRd", clim=[0.0, 1.0], show_scalar_bar=self.is_color_bar)
        self.plotter.show_bounds(
            show_xaxis=self.is_axis, show_yaxis=self.is_axis, show_zaxis=False)
        self.plotter.enable_parallel_projection()
        self.plotter.camera_position = 'xy'
        self.plotter.camera.zoom(1.2)
        self.plotter.show()
        self.labelTime.setText(str(time))

    def axis_selected(self):
        c_text = self.comboBoxAxis.currentText()

        if(c_text == "x"):
            self.max_val = self.x_max
        elif(c_text == "y"):
            self.max_val = self.y_max
        elif(c_text == "z"):
            self.max_val = self.z_max

        self.labelMaxVal.setText(str(self.max_val))
        self.axis_slider_init()

    # intialize slider

    def axis_slider_init(self):
        self.horizontalSliderAxis.setSliderPosition(0)
        self.horizontalSliderAxis.setTickInterval(1)
        self.horizontalSliderAxis.setSingleStep(1)
        self.horizontalSliderAxis.setMinimum(0)
        self.horizontalSliderAxis.setMaximum(self.max_val)

        self.axis_slider_moved()

    def axis_slider_moved(self):
        self.current_val = self.horizontalSliderAxis.value()
        self.labelCurrentVal.setText(str(self.current_val))

    def closeEvent(self, event):
        self.plotter.close()


class ExportAnimation(Ui_DialogConvertToVideo, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(460, 140)
        self.lineEditTimeInterval.setText("200")
        self.pushButtonBrowse.clicked.connect(self.select_file_path)
        self.pushButtonExport.clicked.connect(self.convert_to_video)
        self.comboBoxVideoFormat.currentIndexChanged.connect(
            self.reset_file_path)
        self.pushButtonBrowse.setIcon(QIcon('Images/Icons/folder.png'))

        self.time_arr = utils.get_time_list('Output/Data', '.dat')

        self.actor_mesh = None
        self.actor_plane_mesh = None

    def reset_file_path(self):
        self.lineEditFilePath.setText("")

    def select_file_path(self):
        video_format = self.comboBoxVideoFormat.currentText()
        self.file_path, _ = QFileDialog.getSaveFileName(
            self, 'Export Animation', f'.{video_format}', f'*.{video_format}')
        self.lineEditFilePath.setText(self.file_path)

    def convert_to_video(self):
        self.labelConvertingStatus.setText("Processing...")
        self.labelConvertingStatus.setStyleSheet('color: black')
        self.labelConvertingStatus.repaint()

        if (variables.data['calType'] == "Cahn Hilliard 3D alloy"):
            self.time_arr = utils.get_time_list('Output/Data', '.dat')
            for time in self.time_arr:
                self.plotter = pv.Plotter(off_screen=True)
                file_name = f'Output/Data/output_{time:.2f}.dat'
                if(self.actor_mesh):
                    self.plotter.remove_actor(self.actor_mesh)

                plot_data_3d = np.genfromtxt(
                    file_name, delimiter="\n", usemask=True)
                lx, ly, lz = int(variables.data['parameters']['lx']), int(variables.data[
                    'parameters']['ly']), int(variables.data['parameters']['lz'])
                plot_data_3d = plot_data_3d.reshape(lx, ly, lz)
                mesh = pv.wrap(plot_data_3d)
                self.actor_mesh = self.plotter.add_mesh(
                    mesh, cmap="OrRd", clim=[0.0, 1.0], show_scalar_bar=False)
                self.plotter.screenshot(
                    f'Output/Img/output_{time:.2f}.png', transparent_background=True)
        elif (variables.data['calType'] == "Cahn Hilliard 2D" or variables.data['calType'] == "Cahn Hilliard 2D alloy"):
            self.time_arr = utils.get_time_list('Output/Data', '.dat')
            actor_mesh = None
            for time in self.time_arr:
                image_path = f'Output/Img/output_{time:.2f}.png'
                actor_mesh = utils.convert_save_2d_vtk(
                    time, image_path, actor_mesh, variables)

        time_interval = self.lineEditTimeInterval.text()
        utils.convert_to_video('Output/Img', self.file_path, time_interval)
        self.labelConvertingStatus.setText("Saved")
        self.labelConvertingStatus.setStyleSheet('color: green')


app = QApplication([])

# Create a splash screen and set the background image
splash = QSplashScreen()
pixmap = QPixmap("Images/100.png")
splash.setPixmap(pixmap)

# Set a message that will be displayed below the background image
splash.showMessage("Loading...", alignment=Qt.AlignBottom |
                   Qt.AlignCenter, color=QColor("white"))

# Show the splash screen
splash.show()

window = Ui_PhaseField()
icon = QIcon("Images/app_icon.png")
window.setWindowIcon(icon)
window.show()
app.exec_()
