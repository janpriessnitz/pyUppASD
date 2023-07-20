import os
import time
from pyUppASD.restartfile import Restartfile


class AConfigFile:
    def __init__(self):
        self.fname = "abstract_config_file"

    def get_config_str(self):
        return ""

    def save_config(self, config_dir):
        config_str = self.get_config_str()
        with open(os.path.join(config_dir, self.fname), "w") as fp:
            fp.write(config_str)


class Posfile(AConfigFile):
    def __init__(self):
        self.fname = "posfile"
        # site number, atom type, x, y, z
        self.positions = [[1, 1, 0, 0, 0]]

    def __str__(self):
        return "posfile {}".format(self.fname)

    def get_config_str(self):
        ret = ""
        for pos in self.positions:
            ret += "{} {} {} {} {}\n".format(pos[0],
                                             pos[1], pos[2], pos[3], pos[4])
        return ret


class Exchangefile(AConfigFile):
    def __init__(self):
        self.fname = "jfile"
        # site #1, site #2, x, y, z, energy in mRy
        self.interactions = [[1, 1, 1, 0, 0, 0]]

    def __str__(self):
        return "exchange {}".format(self.fname)

    def get_config_str(self):
        ret = ""
        for inter in self.interactions:
            ret += "{} {} {} {} {} {}\n".format(
                inter[0], inter[1], inter[2], inter[3], inter[4], inter[5])
        return ret


class Momfile(AConfigFile):
    def __init__(self):
        self.fname = "momfile"
        # site num, atom type, moment in mu_b, x, y, z
        self.moms = [[1, 1, 1.00000, 0.0, 0.0, 1.0]]

    def __str__(self):
        return "momfile {}".format(self.fname)

    def get_config_str(self):
        ret = ""
        for mom in self.moms:
            ret += "{} {} {} {} {} {}\n".format(
                mom[0], mom[1], mom[2], mom[3], mom[4], mom[5])
        return ret


class Pdfile(AConfigFile):
    def __init__(self):
        self.fname = "pdfile"
        # site num, atom type, x, y, z, Jxx, Jyy, Jzz, Jxy, Jxz, Jyz
        self.interactions = []

    def __str__(self):
        if len(self.interactions) == 0:
            return ""
        else:
            return "pd {}".format(self.fname)

    def get_config_str(self):
        ret = ""
        for inter in self.interactions:
            interStrs = [str(x) for x in inter]
            ret += " ".join(interStrs) + "\n"
        return ret

    def save_config(self, config_dir):
        if len(self.interactions) > 0:
            super().save_config(config_dir)


class Dmfile(AConfigFile):
    def __init__(self):
        self.fname = "dmfile"
        # site num #1, atom type, x, y, z, DMx, DMy, DMz
        self.interactions = []

    def __str__(self):
        if len(self.interactions) == 0:
            return ""
        else:
            return "dm {}".format(self.fname)

    def get_config_str(self):
        ret = ""
        for inter in self.interactions:
            ret += "{} {} {} {} {} {} {} {}\n".format(
                inter[0], inter[1], inter[2], inter[3], inter[4], inter[5], inter[6], inter[7])
        return ret

    def save_config(self, config_dir):
        if len(self.interactions) > 0:
            super().save_config(config_dir)

class Symfile(AConfigFile):
    def __init__(self):
        self.fname = "sym.mat"
        # site num #1, atom type, x, y, z, DMx, DMy, DMz
        self.syms = []

    def __str__(self):
        return ""

    def get_config_str(self):
        ret = "{}\n".format(len(self.syms))
        for sym in self.syms:
            ret += "{} {} {}\n{} {} {}\n{} {} {}\n".format(
                sym[0,0], sym[0,1], sym[0,2], sym[1,0], sym[1,1], sym[1,2], sym[2,0], sym[2,1], sym[2,2])
        return ret

    def save_config(self, config_dir):
        if len(self.syms) > 0:
            super().save_config(config_dir)

class Anisotropyfile(AConfigFile):
    def __init__(self):
        self.fname = "kfile"
        # atom num, uniaxial(1)/cubic(2)/both(7), K1, K2, e_x, e_y, e_z, K_U/K_C (ratio of uniaxial/cubic; only if 2nd field == 7)
        self.terms = []

    def __str__(self):
        if len(self.terms) == 0:
            return ""
        else:
            return "anisotropy {}".format(self.fname)

    def get_config_str(self):
        ret = ""
        for term in self.terms:
            ret += "{} {} {} {} {} {} {} {}\n".format(
                term[0], term[1], term[2], term[3], term[4], term[5], term[6], term[7])
        return ret

    def save_config(self, config_dir):
        if len(self.terms) > 0:
            super().save_config(config_dir)


class AnnealSched:
    def __init__(self):
        self.sched = []

    def __str__(self):
        ret = "ip_mcanneal {}\n".format(len(self.sched))
        for step in self.sched:
            ret += "{} {}\n".format(step[0], step[1])
        return ret

    def set_sched(self, sched):
        self.sched = sched

    def add_step(self, reps, temp):
        self.sched.append([reps, temp])


class InpsdFile(AConfigFile):
    template = \
        '''simid     {exp_name}
ncell     {size_x}       {size_y}       {size_z}               System size
BC        {boundary_x}         {boundary_y}         {boundary_z}                 Boundary conditions (0=vacuum,P=periodic)
cell      {cell1_x}   {cell1_y}   {cell1_z}
          {cell2_x}   {cell2_y}   {cell2_z}
          {cell3_x}   {cell3_y}   {cell3_z}
Sym       {symmetry}                                     Symmetry of lattice (0 for no, 1 for cubic, 2 for 2d cubic, 3 for hexagonal, 4 for custom sym.mat file)

posfiletype {posfiletype}
maptype {maptype}
{posfile}
{exchangefile}
{momfile}
{pdfile}
{dmfile}
{anisotropyfile}

do_prnstruct {do_prnstruct}                                  Print lattice structure (0=no, 1=yes)

Mensemble {m_ens}                                     Number of samples in ensemble averaging
Initmag   {initmag}                                     (1=random, 2=cone, 3=spec., 4=file)
mseed {mseed}
tseed {tseed}
restartfile {restartfile}


ip_mode   {ip_mode}                                     Initial phase parameters
ip_hfield {ip_hx} {ip_hy} {ip_hz}
{ip_mcanneal}

{main_phase}

plotenergy {plotenergy}
do_avrg {do_avrg}
avrg_step {avrg_step}
do_tottraj {do_tottraj}
tottraj_step {tottraj_step}
do_cumu {do_cumu}
cumu_step {cumu_step}
cumu_buff {cumu_buff}
'''

    subtemplate_MC = \
        '''
mode      {mode}                                     S=SD, M=MC
temp      {temp}                                Measurement phase parameters
mcnstep     {steps}                             for MC/heatbath    --
hfield {hx} {hy} {hz}
'''

    subtemplate_SD = \
        '''
mode      {mode}                                     S=SD, M=MC
temp      {temp}                                Measurement phase parameters
Nstep {steps}                                   for SD
timestep {timestep}                             for SD
damping {damping}
hfield {hx} {hy} {hz}
'''

    def __init__(self):
        self.fname = "inpsd.dat"
        self.exp_name = "EXP_NAME"
        self.size_x = 21
        self.size_y = 21
        self.size_z = 1
        self.boundary_x = 'P'
        self.boundary_y = 'P'
        self.boundary_z = '0'
        self.cell1_x = 1
        self.cell1_y = 0
        self.cell1_z = 0
        self.cell2_x = -0.5
        self.cell2_y = 0.86603
        self.cell2_z = 0
        self.cell3_x = 0
        self.cell3_y = 0
        self.cell3_z = 1
        self.symmetry = 0
        self.symfile = Symfile()
        self.posfiletype='C'  # C=Cartesian, D=direct
        self.maptype = 1  # 1=Cartesian, 2=direct
        self.posfile = Posfile()
        self.exchangefile = Exchangefile()
        self.momfile = Momfile()
        self.pdfile = Pdfile()
        self.dmfile = Dmfile()
        self.anisotropyfile = Anisotropyfile()
        self.m_ens = 1
        self.do_prnstruct = 0
        self.initmag = 1
        self.restartfile = Restartfile()
        # microseconds modulo 1 billion
        self.tseed = int(time.time()*1e6) % 1000000000
        self.mseed = int(time.time()*1e6) % 1000000000
        self.ip_mode = 'M'
        self.ip_hx = 0
        self.ip_hy = 0
        self.ip_hz = 0
        self.ip_mcanneal = AnnealSched()
        self.mode = 'M'
        self.temp = 0.1
        self.timestep = 1e-15
        self.damping = 0.05
        self.steps = 0
        self.hx = 0
        self.hy = 0
        self.hz = 0
        self.plotenergy = 0
        self.do_avrg = 'N'
        self.avrg_step = 1000
        self.do_tottraj = 'N'
        self.tottraj_step = 1000
        self.do_cumu = 'N'
        self.cumu_step = 25
        self.cumu_buff = 10

    def get_config_str(self):
        if self.mode == 'S':
            main_phase = self.subtemplate_SD.format(**self.__dict__)
        else:
            main_phase = self.subtemplate_MC.format(**self.__dict__)
        return self.template.format(**self.__dict__, main_phase=main_phase)

    def save_all_configs(self, config_dir):
        self.save_config(config_dir)
        self.posfile.save_config(config_dir)
        self.exchangefile.save_config(config_dir)
        self.momfile.save_config(config_dir)
        self.dmfile.save_config(config_dir)
        self.pdfile.save_config(config_dir)
        self.anisotropyfile.save_config(config_dir)
        self.restartfile.save_config(config_dir)
        self.symfile.save_config(config_dir)

    def restartfile_fname(self):
        return "restart.{}.out".format(self.exp_name[:8] if len(self.exp_name) > 8 else self.exp_name)

    def coordfile_fname(self):
        return "coord.{}.out".format(self.exp_name[:8] if len(self.exp_name) > 8 else self.exp_name)

    def structfile_fname(self):
        return "struct.{}.out".format(self.exp_name[:8] if len(self.exp_name) > 8 else self.exp_name)

    def momentsfile_fname(self):
        return "moment.{}.out".format(self.exp_name[:8] if len(self.exp_name) > 8 else self.exp_name)

    def averagesfile_fname(self):
        return "averages.{}.out".format(self.exp_name[:8] if len(self.exp_name) > 8 else self.exp_name)

    def totenergyfile_fname(self):
        return "totenergy.{}.out".format(self.exp_name[:8] if len(self.exp_name) > 8 else self.exp_name)

    def cumulantsfile_fname(self):
        return "cumulants.{}.out".format(self.exp_name[:8] if len(self.exp_name) > 8 else self.exp_name)
