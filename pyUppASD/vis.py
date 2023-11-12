from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation

mRyToTesla = 235.0314  # 1 mRy ~ 235 Tesla for a spin with muB magnetic moment


def plot_mag_inner(coordfile, restartfile):
    def transform_xcoords(xs):
        L = int(np.sqrt(len(xs)))
        max_x = xs[L-1]
        return [x % max_x for x in xs]

    cmap = mpl.cm.get_cmap('bwr')
    coords = coordfile.coords()
    ens = 0

    xs = coords['x']
    ys = coords['y']

    L = int(np.sqrt(len(xs)))
    xs = transform_xcoords(xs)

    momxs, momys, momzs = restartfile.mag[ens].T[1:]
    csx = cmap((momxs+1)/2)
    csy = cmap((momys+1)/2)
    csz = cmap((momzs+1)/2)

    try:
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(
            10, 2.4), dpi=600, width_ratios=(1, 1, 1, 0.05))
    except Exception as e:
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(
            10, 2.4), dpi=600)


    # ax1.set_facecolor("lightgrey")
    # ax2.set_facecolor("lightgrey")
    # ax3.set_facecolor("lightgrey")

    ax1.set_xticks([])
    ax1.set_yticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax3.set_xticks([])
    ax3.set_yticks([])

    dotsize = 9*30*30/L/L

    ax1.scatter(xs, ys, color=csx, s=dotsize, marker='h')
    ax1.set_title("Mx")

    ax2.scatter(xs, ys, color=csy, s=dotsize, marker='h')
    ax2.set_title("My")

    ax3.scatter(xs, ys, color=csz, s=dotsize, marker='h')
    ax3.set_title("Mz")

    mpl.colorbar.ColorbarBase(
        ax4, cmap=cmap, orientation='vertical', norm=mpl.colors.Normalize(vmin=-1, vmax=1))
    return fig


def plot_mag(coordfile, restartfile, out_fname):
    fig = plot_mag_inner(coordfile, restartfile)
    plt.savefig(out_fname)
    plt.close()


def plot_mag_direct(coordfile, moments):
    cmap = mpl.colormaps.get_cmap('bwr')
    coords = coordfile.coords()
    ens = 0

    xs = coords['x']
    ys = coords['y']
    momxs, momys, momzs = moments['M_x'], moments['M_y'], moments['M_z']
    csx = cmap((momxs+1)/2)
    csy = cmap((momys+1)/2)
    csz = cmap((momzs+1)/2)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(
        1, 4, figsize=(18, 4), width_ratios=(1, 1, 1, 0.05))

    ax1.set_facecolor("lightgrey")
    ax2.set_facecolor("lightgrey")
    ax3.set_facecolor("lightgrey")

    ax1.set_xticks([])
    ax1.set_yticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax3.set_xticks([])
    ax3.set_yticks([])

    ax1.scatter(xs, ys, color=csx, s=5)
    ax1.set_title("Mx")

    ax2.scatter(xs, ys, color=csy, s=5)
    ax2.set_title("My")

    ax3.scatter(xs, ys, color=csz, s=5)
    ax3.set_title("Mz")

    mpl.colorbar.ColorbarBase(ax4, cmap=cmap, orientation='vertical')

    return fig


def anim_mag_direct(coordfile, moms, out_fname):
    print("begin anim_mag_direct [{}]".format(datetime.now()))
    cmap = mpl.cm.get_cmap('bwr')
    coords = coordfile.coords()

    xs, ys, zs = coords['x'], coords['y'], coords['z']

    momxs, momys, momzs = moms[0]['M_x'], moms[0]['M_y'], moms[0]['M_z']
    csx = cmap((momxs+1)/2)
    csy = cmap((momys+1)/2)
    csz = cmap((momzs+1)/2)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(
        1, 4, figsize=(18, 4), width_ratios=(1, 1, 1, 0.05))

    ax1.set_facecolor("lightgrey")
    ax2.set_facecolor("lightgrey")
    ax3.set_facecolor("lightgrey")

    sc1 = ax1.scatter(xs, ys, color=csx, s=5)
    ax1.set_title("Mx")

    sc2 = ax2.scatter(xs, ys, color=csy, s=5)
    ax2.set_title("My")

    sc3 = ax3.scatter(xs, ys, s=5)
    ax3.set_title("Mz")

    mpl.colorbar.ColorbarBase(ax4, cmap=cmap, orientation='vertical')

    def animate_init():
        return (sc1, sc2, sc3)

    def animate(j):
        momxs, momys, momzs = moms[j]['M_x'], moms[j]['M_y'], moms[j]['M_z']
        csx = cmap((momxs+1)/2)
        csy = cmap((momys+1)/2)
        csz = cmap((momzs+1)/2)

        sc1.set(color=csx)
        sc2.set(color=csy)
        sc3.set(color=csz)
        return (sc1, sc2, sc3)

    anim = animation.FuncAnimation(fig, animate, init_func=animate_init,
                                   frames=moms.shape[0], interval=200, blit=True)

    FFwriter = animation.FFMpegWriter()
    anim.save(out_fname, writer=FFwriter)
    print("end anim_mag_direct [{}]".format(datetime.now()))


def anim_mag_direct_imshow(coordfile, moms, out_fname):
    print("begin anim_mag_direct_imshow [{}]".format(datetime.now()))

    cmap = mpl.cm.get_cmap('bwr')
    coords = coordfile.coords()

    # xs, ys, zs = coords['x'], coords['y'], coords['z']

    momxs, momys, momzs = moms[0]['M_x'], moms[0]['M_y'], moms[0]['M_z']
    # csx = cmap((momxs+1)/2)
    # csy = cmap((momys+1)/2)
    # csz = cmap((momzs+1)/2)

    L = int(np.sqrt(momxs.shape[0]))

    momxs = momxs.reshape((L, L))
    momys = momys.reshape((L, L))
    momzs = momzs.reshape((L, L))

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(
        1, 4, figsize=(18, 4), width_ratios=(1, 1, 1, 0.05))

    ax1.set_facecolor("lightgrey")
    ax2.set_facecolor("lightgrey")
    ax3.set_facecolor("lightgrey")

    imx = ax1.imshow(momxs, cmap='bwr')
    ax1.set_title("Mx")

    imy = ax2.imshow(momys, cmap='bwr')
    ax2.set_title("My")

    imz = ax3.imshow(momzs, cmap='bwr')
    ax3.set_title("Mz")

    mpl.colorbar.ColorbarBase(ax4, cmap=cmap, orientation='vertical')

    def animate_init():
        return imx, imy, imz

    def animate(j):
        momxs, momys, momzs = moms[j]['M_x'], moms[j]['M_y'], moms[j]['M_z']

        momxs = momxs.reshape((L, L))
        momys = momys.reshape((L, L))
        momzs = momzs.reshape((L, L))

        imx.set_array(momxs)
        imy.set_array(momys)
        imz.set_array(momzs)
        return imx, imy, imz

    anim = animation.FuncAnimation(fig, animate, init_func=animate_init,
                                   frames=moms.shape[0], interval=200)

    FFwriter = animation.FFMpegWriter()
    anim.save(out_fname, writer=FFwriter)
    print("end anim_mag_direct_imshow [{}]".format(datetime.now()))


def anim_mag(coordfile, restartfiles, out_fname):
    cmap = mpl.cm.get_cmap('bwr')

    xs = []
    ys = []
    csx = []
    csy = []
    csz = []

    nAtoms = len(coordfile.coords())
    ens = 0

    for i in range(nAtoms):
        x, y, z = coordfile.coords()[i]
        momx, momy, momz = restartfiles[0].mag[ens][i][1:]

        colorx = cmap((momx+1)/2)
        colory = cmap((momy+1)/2)
        colorz = cmap((momz+1)/2)
        xs.append(x)
        ys.append(y)
        csx.append(colorx)
        csy.append(colory)
        csz.append(colorz)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 3))

    # plt.figure(1, figsize=(10,10))
    sc1 = ax1.scatter(xs, ys, color=csx, s=5)
    ax1.set_title("X")
    # plt.colorbar()

    # plt.figure(2, figsize=(10,10))
    sc2 = ax2.scatter(xs, ys, color=csy, s=5)
    ax2.set_title("Y")
    # plt.colorbar()

    # plt.figure(3, figsize=(10,10))
    sc3 = ax3.scatter(xs, ys, s=5)
    ax3.set_title("Z")
    sc3.set(color=csz)
    plt.colorbar(plt.cm.ScalarMappable(
        cmap=cmap, norm=mpl.colors.Normalize(vmin=-1, vmax=1)))

    # animation function.  This is called sequentially

    def animate(j):
        restartfile = restartfiles[j]
        for i in range(nAtoms):
            momx, momy, momz = restartfile.mag[ens][i][1:]

            colorx = cmap((momx+1)/2)
            colory = cmap((momy+1)/2)
            colorz = cmap((momz+1)/2)
            csx[i] = colorx
            csy[i] = colory
            csz[i] = colorz
        sc1.set(color=csx)
        sc2.set(color=csy)
        sc3.set(color=csz)

    anim = animation.FuncAnimation(fig, animate,
                                   frames=int(len(restartfiles)), interval=200)

    FFwriter = animation.FFMpegWriter()
    anim.save(out_fname, writer=FFwriter)

    # HTML(anim.to_jshtml())
    # HTML(anim.to_html5_video())

# plt.show()


def anim_mag_overview(coordfile, restartfiles, configs, out_fname):
    cmap = mpl.cm.get_cmap('bwr')

    xs = []
    ys = []
    csx = []
    csy = []
    csz = []

    nAtoms = len(coordfile.coords())
    ens = 0

    for i in range(nAtoms):
        x, y, z = coordfile.coords()[i]
        momx, momy, momz = restartfiles[0].mag[ens][i][1:]

        colorx = cmap((momx+1)/2)
        colory = cmap((momy+1)/2)
        colorz = cmap((momz+1)/2)
        xs.append(x)
        ys.append(y)
        csx.append(colorx)
        csy.append(colory)
        csz.append(colorz)

    fig, ((ax1, ax2, ax3), (ax21, ax22, ax23)
          ) = plt.subplots(2, 3, figsize=(15, 7))

    # plt.figure(1, figsize=(10,10))
    sc1 = ax1.scatter(xs, ys, color=csx, s=10)
    ax1.set_title("X")
    # plt.colorbar()

    # plt.figure(2, figsize=(10,10))
    sc2 = ax2.scatter(xs, ys, color=csy, s=10)
    ax2.set_title("Y")
    # plt.colorbar()

    # plt.figure(3, figsize=(10,10))
    sc3 = ax3.scatter(xs, ys, s=10)
    ax3.set_title("Z")
    sc3.set(color=csz)
    plt.colorbar(plt.cm.ScalarMappable(
        cmap=cmap, norm=mpl.colors.Normalize(vmin=-1, vmax=1)))

    mx = []
    my = []
    line21 = ax21.plot([], [])
    ax21.set_xlim(0, len(restartfiles))
    ax21.set_ylim(-1.1, 1.1)
    ax21.set_xlabel("t")
    ax21.set_ylabel("M")

    hx = []
    hy = []
    line22 = ax22.plot(hx, hy)
    ax22.set_xlim(0, len(restartfiles))
    ax22.set_ylim(-10, 10)
    ax22.set_xlabel("t")
    ax22.set_ylabel("H")

    # MH curve
    line23 = ax23.plot([], [])
    # ax23.set_xlim(-2, 2)
    ax23.set_ylim(-1.1, 1.1)
    ax23.set_xlabel("H")
    ax23.set_ylabel("M")
    mhs = {}

    plt.tight_layout()

    # animation function.  This is called sequentially
    def animate(j):
        restartfile = restartfiles[j]
        config = configs[j]
        for i in range(nAtoms):
            momx, momy, momz = restartfile.mag[ens][i][1:]

            colorx = cmap((momx+1)/2)
            colory = cmap((momy+1)/2)
            colorz = cmap((momz+1)/2)
            csx[i] = colorx
            csy[i] = colory
            csz[i] = colorz
        sc1.set(color=csx)
        sc2.set(color=csy)
        sc3.set(color=csz)

        mx.append(j)
        my.append(restartfile.avg_M()[0])
        line21[0].set_data(mx, my)
        # ax21.set_ylim(np.array(my).min()-1, np.array(my).max()+1)

        hx.append(j)
        hy.append(config.hx)
        line22[0].set_data(hx, np.array(hy)/mRyToTesla)
        ax22.set_ylim((np.array(hy).min()-1)/mRyToTesla,
                      (np.array(hy).max()+1)/mRyToTesla)

        mhs[hy[-1]] = my[-1]
        mhx = []
        mhy = []
        for k, v in mhs.items():
            mhx.append(k)
            mhy.append(v)

        line23[0].set_data(np.array(mhx)/mRyToTesla, mhy)
        ax23.set_xlim(np.array(mhx).min()/mRyToTesla,
                      np.array(mhx).max()/mRyToTesla)
        # ax23.set_ylim(np.array(mhy).min(), np.array(mhy).max())

    anim = animation.FuncAnimation(fig, animate,
                                   frames=int(len(restartfiles)), interval=200)

    return anim
    # FFwriter = animation.FFMpegWriter()
    # anim.save(out_fname, writer = FFwriter)

    # HTML(anim.to_jshtml())
    # HTML(anim.to_html5_video())

# plt.show()


def plot_hyst(res):
    hs = [x.hz for x in res['configs']]
    ms = [x.avg_M()[2] for x in res['restartfiles']]
    fig = plt.figure()
    plt.scatter(hs, ms)
    plt.savefig("hysteresis.png")


def fourier(lat, qx, qy):
    def mom(x, y):
        return lat[(x % l) + (y % l)*l]
    l = int(np.sqrt(lat.shape[0]))
    fmx = 0
    fmy = 0
    fmz = 0
    for x in range(l):
        for y in range(l):
            _, mx, my, mz = mom(x, y)
            fmx += mx*np.exp(2j*np.pi*(qx*x + qy*y))
            fmy += my*np.exp(2j*np.pi*(qx*x + qy*y))
            fmz += mz*np.exp(2j*np.pi*(qx*x + qy*y))

    return fmx/l/l, fmy/l/l, fmz/l/l


def plot_fourier(restartfile, out_fname):
    cmap = mpl.cm.get_cmap('bwr')
    ens = 0

    # xs = []
    # ys = []
    # fxs = []
    # fys = []
    # fzs = []

    # for qx in np.linspace(-1, 1, 11):
    #   for qy in np.linspace(-1, 1, 11):
    #     xs.append(qx)
    #     ys.append(qy)
    #     fx, fy, fz = fourier(restartfile.mag[ens], qx, qy)
    #     fxs.append(fx)
    #     fys.append(fy)
    #     fzs.append(fz)

    # fxs = np.array(fxs)
    # fys = np.array(fys)
    # fzs = np.array(fzs)

    # fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(10, 2.4), dpi=600, width_ratios=(1, 1, 1, 0.05))

    # print(fourier(restartfile.mag[ens], 0, 0))

    # print(fzs)

    # csx = cmap((fxs+1)/2)
    # csy = cmap((fys+1)/2)
    # csz = cmap((fzs+1)/2)

    # # ax1.set_facecolor("lightgrey")
    # # ax2.set_facecolor("lightgrey")
    # # ax3.set_facecolor("lightgrey")

    # ax1.set_xticks([])
    # ax1.set_yticks([])
    # ax2.set_xticks([])
    # ax2.set_yticks([])
    # ax3.set_xticks([])
    # ax3.set_yticks([])

    # dotsize = 10

    # ax1.scatter(xs, ys, color=csx, s=dotsize)
    # ax1.set_title("Mx")

    # ax2.scatter(xs, ys, color=csy, s=dotsize)
    # ax2.set_title("My")

    # ax3.scatter(xs, ys, color=csz, s=dotsize)
    # ax3.set_title("Mz")

    mxs, mys, mzs = restartfile.mag[ens].T

    fxs = []
    fys = []
    fzs = []

    for qx in np.linspace(-1, 1, 51):
        fxs.append([])
        fys.append([])
        fzs.append([])
        for qy in np.linspace(-1, 1, 51):
            fx, fy, fz = fourier(restartfile.mag[ens], qx, qy)
            fxs[-1].append(np.float(fx))
            fys[-1].append(np.float(fy))
            fzs[-1].append(np.float(fz))

    fxs = np.array(fxs)
    fys = np.array(fys)
    fzs = np.array(fzs)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(
        10, 2.4), dpi=600, width_ratios=(1, 1, 1, 0.05))

    print(fourier(restartfile.mag[ens], 0, 0))

    print(fzs)

    csx = cmap((fxs+1)/2)
    csy = cmap((fys+1)/2)
    csz = cmap((fzs+1)/2)

    # ax1.set_facecolor("lightgrey")
    # ax2.set_facecolor("lightgrey")
    # ax3.set_facecolor("lightgrey")

    ax1.set_xticks([])
    ax1.set_yticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax3.set_xticks([])
    ax3.set_yticks([])

    dotsize = 10

    im1 = ax1.imshow(fxs)
    ax1.set_title("Mx")
    fig.colorbar(im1, cax=ax4, orientation='vertical')

    ax2.imshow(fys)
    ax2.set_title("My")

    ax3.imshow(fzs)
    ax3.set_title("Mz")

    # mpl.colorbar.ColorbarBase(ax4, cmap=cmap, orientation = 'vertical',norm=mpl.colors.Normalize(vmin=-1, vmax=1))

    plt.savefig(out_fname)
    plt.close()
