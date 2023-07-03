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
                self.__restartfile = None
        return self.__restartfile

    def coordfile(self):
        if not self.__coordfile:
            try:
                self.__coordfile = CoordFile(os.path.join(
                    self.exp_dir, self.config.coordfile_fname()))
            except FileNotFoundError:
                self.__coordfile = None
        return self.__coordfile

    def structfile(self):
        if not self.__structfile:
            try:
                self.__structfile = StructFile(os.path.join(
                    self.exp_dir, self.config.structfile_fname()))
            except FileNotFoundError:
                self.__structfile = None
        return self.__structfile

    def averagesfile(self):
        if not self.__averagesfile:
            try:
                self.__averagesfile = AveragesFile(os.path.join(
                    self.exp_dir, self.config.averagesfile_fname()))
            except FileNotFoundError:
                self.__averagesfile = None
        return self.__averagesfile

    def momentsfile(self):
        if not self.__momentsfile:
            try:
                self.__momentsfile = MomentsFile(os.path.join(
                    self.exp_dir, self.config.momentsfile_fname()))
            except FileNotFoundError:
                self.__momentsfile = None
        return self.__momentsfile

    def energyfile(self):
        if not self.__energyfile:
            try:
                self.__energyfile = EnergyFile(os.path.join(
                    self.exp_dir, self.config.totenergyfile_fname()))
            except FileNotFoundError:
                self.__energyfile = None
        return self.__energyfile

    def cumufile(self):
        if not self.__cumufile:
            try:
                self.__cumufile = CumuFile(os.path.join(
                    self.exp_dir, self.config.cumulantsfile_fname()))
            except FileNotFoundError:
                self.__cumufile = None
        return self.__cumufile

    def dump(self, fname):
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
        p = subprocess.run(SD_PATH, cwd=config_dir,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("UppASD finished [{}]".format(datetime.now()))
        if p.returncode != 0 or len(p.stderr) > 0 or 'ERROR' in str(p.stdout):
            print(p)

        return Result(config, p, config_dir)
