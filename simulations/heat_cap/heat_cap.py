#!/usr/bin/env python3

import sys, os

from pyUppASD import config
from pyUppASD import launcher
from pyUppASD import vis
import pyUppASD

import numpy as np

def apply_config_alphaUH3(config):
  J1 = 8.559*pyUppASD.eVtoRy
  # J1 = 9.3*pyUppASD.eVtoRy
  # J2 = 7.8*pyUppASD.eVtoRy
  # J3 = -0.5*pyUppASD.eVtoRy
  U_mom = 1.0

  config.symmetry = 1
  config.exchangefile.interactions = [
    [1, 1, 0.5, 0.5, 0.5, J1],
    # [1, 1, 1, 0, 0, J2],
    # [1, 1, 1, 1, 0, J3],
  ]

  config.posfile.positions = [
    [1, 1, 0, 0, 0],
    [2, 1, 0.5, 0.5, 0.5],
  ]

  config.momfile.moms = [
    [1, 1, U_mom, 0, 0, 1],
    [2, 1, U_mom, 0, 0, 1],
  ]

  config.cell1_x = 1
  config.cell1_y = 0
  config.cell1_z = 0

  config.cell2_x = 0
  config.cell2_y = 1
  config.cell2_z = 0

  config.cell3_x = 0
  config.cell3_y = 0
  config.cell3_z = 1

  config.boundary_x = 'P'
  config.boundary_y = 'P'
  config.boundary_z = 'P'

  return config

def apply_config_MnO(config):
  J1 = -5.90*pyUppASD.eVtoRy/2
  J2 = -4.14*pyUppASD.eVtoRy/2
  Mn_mom = 4.5  # TODO

  config.symmetry = 1
  config.exchangefile.interactions = [
    [1, 1, 0.5, 0.5, 0, J1],
    [1, 1, 1, 0, 0, J2],
  ]

  config.posfile.positions = [
    [1, 1, 0, 0, 0],
    [2, 1, 0, 0.5, 0.5],
    [3, 1, 0.5, 0, 0.5],
    [4, 1, 0.5, 0.5, 0],
  ]

  config.momfile.moms = [
    [1, 1, Mn_mom, 0, 0, 1],
    [2, 1, Mn_mom, 0, 0, 1],
    [3, 1, Mn_mom, 0, 0, 1],
    [4, 1, Mn_mom, 0, 0, 1],
  ]

  config.cell1_x = 1
  config.cell1_y = 0
  config.cell1_z = 0

  config.cell2_x = 0
  config.cell2_y = 1
  config.cell2_z = 0

  config.cell3_x = 0
  config.cell3_y = 0
  config.cell3_z = 1

  config.boundary_x = 'P'
  config.boundary_y = 'P'
  config.boundary_z = 'P'

  return config

def apply_config_NiO(config):
  J1 = 1.5*pyUppASD.eVtoRy/2
  J2 = -20*pyUppASD.eVtoRy/2
  Co_mom = 2.7

  config.symmetry = 1
  config.exchangefile.interactions = [
    [1, 1, 0.5, 0.5, 0, J1],
    [1, 1, 1, 0, 0, J2],
  ]

  config.posfile.positions = [
    [1, 1, 0, 0, 0],
    [2, 1, 0, 0.5, 0.5],
    [3, 1, 0.5, 0, 0.5],
    [4, 1, 0.5, 0.5, 0],
  ]

  config.momfile.moms = [
    [1, 1, Co_mom, 0, 0, 1],
    [2, 1, Co_mom, 0, 0, 1],
    [3, 1, Co_mom, 0, 0, 1],
    [4, 1, Co_mom, 0, 0, 1],
  ]

  config.cell1_x = 1
  config.cell1_y = 0
  config.cell1_z = 0

  config.cell2_x = 0
  config.cell2_y = 1
  config.cell2_z = 0

  config.cell3_x = 0
  config.cell3_y = 0
  config.cell3_z = 1

  config.boundary_x = 'P'
  config.boundary_y = 'P'
  config.boundary_z = 'P'

  return config

def apply_config_CoO(config):
  J1 = 1.5*pyUppASD.eVtoRy
  J2 = -12.2*pyUppASD.eVtoRy
  Co_mom = 2.7

  config.symmetry = 1
  config.exchangefile.interactions = [
    [1, 1, 0.5, 0.5, 0, J1],
    [1, 1, 1, 0, 0, J2],
  ]

  config.posfile.positions = [
    [1, 1, 0, 0, 0],
    [2, 1, 0, 0.5, 0.5],
    [3, 1, 0.5, 0, 0.5],
    [4, 1, 0.5, 0.5, 0],
  ]

  config.momfile.moms = [
    [1, 1, Co_mom, 0, 0, 1],
    [2, 1, Co_mom, 0, 0, 1],
    [3, 1, Co_mom, 0, 0, 1],
    [4, 1, Co_mom, 0, 0, 1],
  ]

  config.cell1_x = 1
  config.cell1_y = 0
  config.cell1_z = 0

  config.cell2_x = 0
  config.cell2_y = 1
  config.cell2_z = 0

  config.cell3_x = 0
  config.cell3_y = 0
  config.cell3_z = 1

  config.boundary_x = 'P'
  config.boundary_y = 'P'
  config.boundary_z = 'P'

  return config

def get_config(config_fn, n_steps):
  init_temp = 0.01
  c = config.InpsdFile()
  c = config_fn(c)

  c.size_x = 10
  c.size_y = 10
  c.size_z = 10

  c.ip_mode = 'H'
  c.ip_mcanneal.sched = [
    [n_steps, init_temp],
  ]

  # measurement phase
  c.mode = 'H'
  c.steps = n_steps
  c.temp = init_temp

  c.do_prnstruct = 1
  c.plotenergy = 1
  c.do_avrg = 'Y'
  c.avrg_step = int(n_steps/3)
  c.do_cumu = 'Y'
  # c.cumu_step = int(n_steps/3)


  return c

def run_sim():
  material_dict = {
    'CoO': apply_config_CoO,
    'MnO': apply_config_MnO,
    'NiO': apply_config_NiO,
    'alphaUH3': apply_config_alphaUH3,
  }
  config = get_config(material_dict[sys.argv[1]], 1000)

  l = launcher.SDLauncher()

  n_points = 100
  res = l.run(config, os.path.join(sys.argv[2], "init/"))

  for temp in np.linspace(0.01, 500, n_points):
    print("temp: {}".format(temp))
    config.temp = temp
    config.ip_mcanneal.sched[0][1] = temp
    config.restartfile = res.restartfile()
    config.initmag = 4
    res = l.run(config, os.path.join(sys.argv[2], "{:2f}".format(temp)))

if __name__ == "__main__":
  run_sim()
