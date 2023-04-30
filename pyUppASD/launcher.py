import os
import shutil
import subprocess
from datetime import datetime
import copy

from pyUppASD.restartfile import Restartfile
from pyUppASD.outputfile import AveragesFile, CoordFile, CumuFile, EnergyFile, MomentsFile, StructFile

SD_PATH = os.getenv("SD_PATH", "/home/jp/UppASD/bin/sd.gfortran")


class Result:
    def __init__(self, config, cmdres, restartfile, coordfile, structfile, averagesfile, momentsfile, energyfile, cumufile):
        self.config = copy.deepcopy(config)
        self.cmdres = cmdres
        self.restartfile = restartfile
        self.coordfile = coordfile
        self.structfile = structfile
        self.averagesfile = averagesfile
        self.momentsfile = momentsfile
        self.energyfile = energyfile
        self.cumufile = cumufile


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
            return Result(config, p, None, None, None, None, None, None, None)
        restartfile = Restartfile(os.path.join(
            config_dir, config.restartfile_fname()))
        if config.do_prnstruct == 1 or config.do_prnstruct == 2:
            coordfile = CoordFile(os.path.join(
                config_dir, config.coordfile_fname()))
        else:
            coordfile = None
        if config.do_prnstruct == 1:
            structfile = StructFile(os.path.join(
                config_dir, config.structfile_fname()))
        else:
            structfile = None
        if config.do_avrg == 'Y':
            averagesfile = AveragesFile(os.path.join(
                config_dir, config.averagesfile_fname()))
        else:
            averagesfile = None
        if config.do_tottraj == 'Y':
            momentsfile = MomentsFile(os.path.join(
                config_dir, config.momentsfile_fname()))
        else:
            momentsfile = None
        if config.plotenergy == 1:
            energyfile = EnergyFile(os.path.join(
                config_dir, config.totenergyfile_fname()))
        else:
            energyfile = None
        if config.do_cumu == 'Y':
            cumufile = CumuFile(os.path.join(
                config_dir, config.cumulantsfile_fname()))
        else:
            cumufile = None

        return Result(config, p, restartfile,
                      coordfile, structfile, averagesfile, momentsfile, energyfile, cumufile)
