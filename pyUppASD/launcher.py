import os
import shutil
import subprocess
from datetime import datetime
import copy
import pickle

from pyUppASD.restartfile import Restartfile
from pyUppASD.outputfile import AveragesFile, CoordFile, CumuFile, EnergyFile, MomentsFile, StructFile

SD_PATH = os.getenv("SD_PATH", "/home/jp/UppASD/bin/sd.gfortran")

class Result:
    def __init__(self, config, cmdres, exp_dir):
        self.config = copy.deepcopy(config)
        self.cmdres = cmdres
        self.exp_dir = exp_dir
        self.__restartfile = None
        self.__coordfile = None
        self.__structfile = None
        self.__averagesfile = None
        self.__momentsfile = None
        self.__energyfile = None
        self.__cumufile = None

    def error(self):
        return self.cmdres.returncode != 0 or len(self.cmdres.stderr) > 0 or 'ERROR' in str(self.cmdres.stdout)

    def restartfile(self):
        if not self.__restartfile:
            try:
                self.__restartfile = Restartfile(os.path.join(
                    self.exp_dir, self.config.restartfile_fname()))
            except FileNotFoundError:
                self.__restartfile = Restartfile()
        return self.__restartfile

    def coordfile(self):
        if not self.__coordfile:
            try:
                self.__coordfile = CoordFile(os.path.join(
                    self.exp_dir, self.config.coordfile_fname()))
            except (FileNotFoundError, OSError):
                self.__coordfile = CoordFile()
        return self.__coordfile

    def structfile(self):
        if not self.__structfile:
            try:
                self.__structfile = StructFile(os.path.join(
                    self.exp_dir, self.config.structfile_fname()))
            except (FileNotFoundError, OSError):
                self.__structfile = StructFile()
        return self.__structfile

    def averagesfile(self):
        if not self.__averagesfile:
            try:
                self.__averagesfile = AveragesFile(os.path.join(
                    self.exp_dir, self.config.averagesfile_fname()))
            except (FileNotFoundError, OSError):
                self.__averagesfile = AveragesFile()
        return self.__averagesfile

    def momentsfile(self):
        if not self.__momentsfile:
            try:
                self.__momentsfile = MomentsFile(os.path.join(
                    self.exp_dir, self.config.momentsfile_fname()))
            except (FileNotFoundError, OSError):
                self.__momentsfile = MomentsFile()
        return self.__momentsfile

    def energyfile(self):
        if not self.__energyfile:
            try:
                self.__energyfile = EnergyFile(os.path.join(
                    self.exp_dir, self.config.totenergyfile_fname()))
            except (FileNotFoundError, OSError):
                self.__energyfile = EnergyFile()
        return self.__energyfile

    def cumufile(self):
        if not self.__cumufile:
            try:
                self.__cumufile = CumuFile(os.path.join(
                    self.exp_dir, self.config.cumulantsfile_fname()))
            except (FileNotFoundError, OSError):
                self.__cumufile = CumuFile()
        return self.__cumufile

    def dump(self, fname):
        # call output files fns to load all data
        self.restartfile()
        self.coordfile()
        self.structfile()
        self.averagesfile()
        self.momentsfile()
        self.energyfile()
        self.cumufile()
        with open(fname, "wb") as fp:
            pickle.dump(self, fp)

class SDLauncher:
    def __init__(self):
        pass

    def run(self, config, config_dir):
        shutil.rmtree(config_dir, ignore_errors=True)
        os.makedirs(config_dir, exist_ok=True)
        config.save_all_configs(config_dir)
        print("launching UppASD [{}]".format(datetime.now()))
        fout = open(os.path.join(config_dir, "stdout"), "wb", buffering=0)
        ferr = open(os.path.join(config_dir, "stderr"), "wb", buffering=0)
        p = subprocess.run(SD_PATH, cwd=config_dir,
                           stdout=fout, stderr=ferr)
        fout.close()
        ferr.close()
        print("UppASD finished [{}]".format(datetime.now()))
        with open(os.path.join(config_dir, "stdout"), "r") as fout:
            stdout = fout.read()
        with open(os.path.join(config_dir, "stderr"), "r") as ferr:
            stderr = ferr.read()

        if p.returncode != 0 or len(stderr) > 0 or 'ERROR' in stdout:
            print(p)

        return Result(config, p, config_dir)
