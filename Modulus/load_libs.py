import ctypes
import sys
import os
from PySide2.QtCore import QObject, Signal


class Worker(QObject):
    finished = Signal()
    calc_param = None

    dir_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'Sources'))

    def values(self, calc_param):
        self.calc_param = calc_param
        print(self.calc_param)

    def run(self):
        """Long-running task."""
        print(self.calc_param['calType'])
        if(self.calc_param['calType'] == "Cahn Hilliard 2D"):
            self.lib_ch2d_qualitative()
        print("ended")
        self.finished.emit()

    def lib_hkl_2d(self, time):
        l_hdk_2d = ctypes.cdll.LoadLibrary(self.dir_path+'/hkl_2d.so')
        l_hdk_2d.hkl_2d(ctypes.c_float(time))

    def lib_ch2d_qualitative(self):
        print(self.calc_param['parameters']['fluctuation'])
        fluctuation = float(self.calc_param['parameters']['fluctuation'])
        lx = int(self.calc_param['parameters']['lx'])
        ly = int(self.calc_param['parameters']['ly'])
        c_avg = float(self.calc_param['parameters']['cAvg'])
        mobility = int(self.calc_param['parameters']['mobility'])
        delt = float(self.calc_param['parameters']['delT'])
        kappa = int(self.calc_param['parameters']['kappa'])
        delx = float(self.calc_param['parameters']['delX'])
        dely = float(self.calc_param['parameters']['delY'])
        time_interval = float(self.calc_param['timeInterval'])
        total_time = float(self.calc_param['totalTime'])
        resume = int(self.calc_param['resume'])
        resume_from = float(self.calc_param['resumeFrom'])
        print(self.calc_param)
        l_ch2d_qualitative = ctypes.cdll.LoadLibrary(
            self.dir_path+'/ch2d_qualitative.so')
        l_ch2d_qualitative.ch2d_qualitative(ctypes.c_float(fluctuation), ctypes.c_float(c_avg), ctypes.c_int(lx), ctypes.c_int(ly), ctypes.c_int(mobility), ctypes.c_float(
            delt), ctypes.c_int(kappa), ctypes.c_float(delx), ctypes.c_float(dely), ctypes.c_float(time_interval), ctypes.c_float(total_time), ctypes.c_int(resume), ctypes.c_float(resume_from))
