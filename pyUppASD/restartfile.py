import os
import numpy as np


class Restartfile:
    header = \
        '''################################################################################
# File type: R
# Simulation type: M
# Number of atoms:       0
# Number of ensembles:         0
################################################################################
#iter     ens   iatom           |Mom|             M_x             M_y             M_z
'''

    def __init__(self, fname=None):
        self.mag = None
        if fname != None:
            self.load_from_file(fname)

    def load_from_file(self, fname):
        self.mag = []
        with open(fname, 'r') as fp:
            last_ens = 1
            ens_mag = []
            for line in fp.readlines():
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                iter_str, ens_str, iatom_str, absmom_str, momx_str, momy_str, momz_str = stripped.split()
                ens = int(ens_str)
                if ens != last_ens:
                    # start new ensemble
                    self.mag.append(np.array(ens_mag))
                    ens_mag = []
                    last_ens = ens
                # hack: fortran prints extremely small numbers in a different format e. g.: 1.98532408-108 instead of 1.98532408E-108
                try:
                    absmom = float(absmom_str)
                except ValueError:
                    absmom = 0
                try:
                    momx = float(momx_str)
                except ValueError:
                    momx = 0
                try:
                    momy = float(momy_str)
                except ValueError:
                    momy = 0
                try:
                    momz = float(momz_str)
                except ValueError:
                    momz = 0

                ens_mag.append([absmom, momx, momy, momz])
            ens_mag = np.array(ens_mag)
        self.mag.append(ens_mag)

    def save_to_file(self, fname):
        iteration = -1
        with open(fname, 'w') as fp:
            fp.write(self.header)
            iens = 1
            for ens_mag in self.mag:
                iatom = 1
                for atom_mom in ens_mag:
                    fp.write("{} {} {} {} {} {} {}\n".format(
                        iteration, iens, iatom, atom_mom[0], atom_mom[1], atom_mom[2], atom_mom[3]))
                    iatom += 1
                iens += 1

    def avg_M(self):
        avgs_per_ens = self.avg_M_per_ens()
        avgs = [.0, .0, .0]
        for avgx, avgy, avgz in avgs_per_ens:
            avgs[0] += avgx
            avgs[1] += avgy
            avgs[2] += avgz
        avgs[0] /= len(avgs_per_ens)
        avgs[1] /= len(avgs_per_ens)
        avgs[2] /= len(avgs_per_ens)
        return avgs

    def avg_M_per_ens(self):
        avgs = []
        for ens_mag in self.mag:
            avgx, avgy, avgz = 0, 0, 0
            for absmom, momx, momy, momz in ens_mag:
                avgx += momx
                avgy += momy
                avgz += momz
            avgx /= len(ens_mag)
            avgy /= len(ens_mag)
            avgz /= len(ens_mag)
            avgs.append([avgx, avgy, avgz])
        return avgs

    RESTART_IN_NAME = "restart.in"

    def save_config(self, config_dir):
        if self.mag != None:
            self.save_to_file(os.path.join(config_dir, self.RESTART_IN_NAME))

    def __str__(self):
        return self.RESTART_IN_NAME

        # Legacy code


class Coordfile:
    def __init__(self, fname=None):
        self.coords = None
        if fname != None:
            self.load_from_file(fname)

    def load_from_file(self, fname):
        self.coords = []
        with open(fname, "r") as fp:
            for line in fp.readlines():
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                iatom_str, x_str, y_str, z_str, a_str, b_str = stripped.split()
                x = float(x_str)
                y = float(y_str)
                z = float(z_str)
                self.coords.append([x, y, z])
