import numpy as np


class OutputFile:
    header = ""
    def __init__(self, fname=None, dtype=None):
        self.fname = fname
        self.dtype = dtype
        self.data = None
        if fname != None:
            self.load_from_file(fname, dtype)

    def load_from_file(self, fname, dtype):
        self.data = np.genfromtxt(fname, dtype=dtype)

    def save_to_file(self, fname):
        if not self.data is None:
            np.savetxt(fname, self.data, header=self.header)


# i, x, y, z, site number, atom type number
class CoordFile(OutputFile):
    header = "i, x, y, z, site number, atom type number"
    def __init__(self, fname=None):
        super().__init__(fname, dtype=[
            ('i', 'i4'), ('x', 'f8'), ('y', 'f8'), ('z', 'f8'), ('site_num', 'i4'), ('atom_type', 'i4')])

    def n_atoms(self):
        return self.data.shape[0]

    # coordinates only (no atom types)
    def coords(self):
        return self.particles()[['x', 'y', 'z']]

    # return complete sorted data
    def particles(self):
        # sort in case i is not in increasing order
        return self.data[self.data['i'].argsort()]


#  iatom jatom  itype  jtype        r_{ij}^x        r_{ij}^y        r_{ij}^z          J_{ij}        |r_{ij}|
class StructFile(OutputFile):
    header = "iatom jatom  itype  jtype        r_{ij}^x        r_{ij}^y        r_{ij}^z          J_{ij}        |r_{ij}|"
    def __init__(self, fname=None):
        super().__init__(fname, dtype=[('iatom', 'i4'), ('jatom', 'i4'), ('itype', 'i4'), (
            'jtype', 'i4'), ('r_x', 'f8'), ('r_y', 'f8'), ('r_z', 'f8'), ('J', 'f8'), ('r_abs', 'f8')])


# Iter           <M>_x           <M>_y           <M>_z             <M>        M_{stdv}
class AveragesFile(OutputFile):
    header = "Iter           <M>_x           <M>_y           <M>_z             <M>        M_{stdv}"
    def __init__(self, fname=None):
        super().__init__(fname, dtype=[('iter', 'i4'), ('M_x', 'f8'),
                                       ('M_y', 'f8'), ('M_z', 'f8'), ('M', 'f8'), ('M_stdv', 'f8')])


# Iter                 Tot                 Exc                 Ani                  DM                  PD               BiqDM                  BQ                 Dip              Zeeman                 LSF                Chir                Ring                  SA
class EnergyFile(OutputFile):
    header = "Iter                 Tot                 Exc                 Ani                  DM                  PD               BiqDM                  BQ                 Dip              Zeeman                 LSF                Chir                Ring                  SA"
    def __init__(self, fname=None):
        super().__init__(fname, dtype=[('iter', 'i4'), ('tot', 'f8'), ('exc', 'f8'), ('ani', 'f8'), ('dm', 'f8'), ('pd', 'f8'), (
            'biqdm', 'f8'), ('bq', 'f8'), ('dip', 'f8'), ('zeeman', 'f8'), ('lsf', 'f8'), ('chir', 'f8'), ('ring', 'f8'), ('sa', 'f8')])


# Iter             <M>           <M^2>           <M^4>      U_{Binder}            \chi        C_v(tot)             <E>       <E_{exc}>       <E_{lsf}>
class CumuFile(OutputFile):
    header = "Iter             <M>           <M^2>           <M^4>      U_{Binder}            \chi        C_v(tot)             <E>       <E_{exc}>       <E_{lsf}>"
    def __init__(self, fname=None):
        super().__init__(fname, dtype=[('iter', 'i4'), ('M', 'f8'), ('M2', 'f8'), ('M4', 'f8'), (
            'U_Binder', 'f8'), ('chi', 'f8'), ('C_v', 'f8'), ('E', 'f8'), ('E_exc', 'f8'), ('E_lsf', 'f8')])


# iter   ens   iatom           |Mom|             M_x             M_y             M_z
class MomentsFile(OutputFile):
    header = "iter   ens   iatom           |Mom|             M_x             M_y             M_z"
    def __init__(self, fname=None):
        super().__init__(fname, dtype=[('iter', 'i4'), ('ens', 'i4'), (
            'iatom', 'i4'), ('M_abs', 'f8'), ('M_x', 'f8'), ('M_y', 'f8'), ('M_z', 'f8')])

    # return numpy array in shape (ens, iter, iatom)
    def moments(self):
        iters_ens = []
        iters = np.split(self.data, np.unique(
            self.data['iter'], return_index=True)[1][1:])
        for iter in iters:
            iters_ens.append(np.split(iter, np.unique(
                iter['ens'], return_index=True)[1][1:]))
        iters_ens = np.array(iters_ens)
        ens_iters = np.transpose(iters_ens, axes=(1, 0, 2))
        return ens_iters
