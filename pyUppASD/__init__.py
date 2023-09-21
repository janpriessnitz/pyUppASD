import numpy as np
import pickle

mRyToTesla = 235.0314  # 1 mRy ~ 235 Tesla for a spin with 1*muB magnetic moment
mRyToKelvin = 157.88766343200544  # 1 mRy ~ 158 K
eVtoRy = 0.0734985857  # 1 eV ~ 0.0734985857 Ry

def fourier(ms, qxs, qys):
    qw, qh = qxs.shape
    qxs = np.reshape(qxs, (qw, qh, 1, 1))
    qys = np.reshape(qys, (qw, qh, 1, 1))
    h, w = ms.shape
    xs = np.arange(w)
    ys = np.arange(h)
    xgrid, ygrid = np.meshgrid(xs, ys)
    xgrid = np.reshape(xgrid, (1, 1, w, h))
    ygrid = np.reshape(ygrid, (1, 1, w, h))
    exps = (xgrid - 0.5*ygrid)*qxs + (0.86603*ygrid)*qys
    # exps = xgrid*Nx + ygrid*Ny
    # print((ms*np.exp(1j*exps)).shape)
    fs = np.sum(ms*np.exp(1j*exps), axis=(2, 3)) * \
        np.sum(ms*np.exp(-1j*exps), axis=(2, 3))/w/w/h/h

    return fs


def structure_factor(ms, qs):
    mxs, mys, mzs = ms.T
    xgrid, ygrid = np.meshgrid(qs, qs)
    return np.abs(fourier(mxs, xgrid, ygrid) + fourier(mys, xgrid, ygrid) + fourier(mzs, xgrid, ygrid))


def load_exp(fname):
    with open(fname, "rb") as fp:
        return pickle.load(fp)


def evalE(lat, J, dm, hz):
    def mom(x, y):
        return lat[(x % l) + (y % l)*l]
    l = int(np.sqrt(lat.shape[0]))
    Ej = 0
    Edm = 0
    Ehz = 0
    for x in range(l):
        for y in range(l):
            _, mx, my, mz = mom(x, y)
            Ehz += hz*mz

            _, mx1, my1, mz1 = mom(x+1, y)
            _, mx2, my2, mz2 = mom(x-1, y)
            _, mx3, my3, mz3 = mom(x, y+1)
            _, mx4, my4, mz4 = mom(x, y-1)
            _, mx5, my5, mz5 = mom(x+1, y+1)
            _, mx6, my6, mz6 = mom(x-1, y-1)
            Ej += J*mx*(mx1+mx2+mx3+mx4+mx5+mx6)
            Ej += J*my*(my1+my2+my3+my4+my5+my6)
            Ej += J*mz*(mz1+mz2+mz3+mz4+mz5+mz6)

            Edm += dm*(mx*my1-my*mx1)
            Edm -= dm*(mx*my2-my*mx2)
            Edm += dm*(mx*my3-my*mx3)
            Edm -= dm*(mx*my4-my*mx4)
            Edm += dm*(mx*my6-my*mx6)
            Edm -= dm*(mx*my5-my*mx5)
    return Ej/l/l, Edm/l/l, Ehz/l/l
