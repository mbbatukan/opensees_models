#%%
import numpy as np
import openseespy.opensees as ops
import opsvis as opsv
import matplotlib.pyplot as plt
# %matplotlib widget
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats('svg')

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)

width = 7.5/4
height = 2.5

ops.node(1, 0.0, 0.0)
ops.node(2, 0.0, height)
ops.node(3, width, 0.0)
ops.node(4, width, height)
ops.node(5, 2*width, 0.0)
ops.node(6, 2*width, height)
ops.node(7, 3*width, 0.0)
ops.node(8, 3*width, height)
ops.node(9, 4*width, 0.0)
ops.node(10, 4*width, height)

ops.fix(1, 1, 1, 0)
ops.fix(3, 1, 1, 1)
ops.fix(5, 1, 1, 1)
ops.fix(7, 1, 1, 1)
ops.fix(9, 1, 1, 0)

# uniaxialMaterial('Concrete01', matTag, fpc, epsc0, fpcu, epsU)
ops.uniaxialMaterial('Concrete01', 1, -30e3, -0.002, -30e3, -0.002)
# uniaxialMaterial('Steel01', matTag, Fy, E0, b, a1, a2, a3, a4)
ops.uniaxialMaterial('Steel01', 2, 420e3, 2e8, 0.00001)

As20 = 0.25*np.pi*(0.020**2)
As22 = 0.25*np.pi*(0.022**2)
As28 = 0.25*np.pi*(0.028**2)

Bcol = 0.35
Hcol = 0.35

c = 0.04  # cover

y1col = Hcol/2.0
z1col = Bcol/2.0

y2col = 0.5*(Hcol-2*c)/3.0
num_bars = 2
nFibZ = 1
nFib = 20
nFibCover, nFibCore = 2, 16

ops.section('Fiber', 1)
ops.patch('rect', 1, nFibCore, nFibZ, *[c-y1col, c-z1col], *[y1col-c, z1col-c])
ops.patch('rect', 1, nFib, nFibZ, *[-y1col, -z1col], *[y1col, c-z1col])
ops.patch('rect', 1, nFib, nFibZ, *[-y1col, z1col-c], *[y1col, z1col])
ops.patch('rect', 1, nFibCover, nFibZ, *[-y1col, c-z1col], *[c-y1col, z1col-c])
ops.patch('rect', 1, nFibCover, nFibZ, *[y1col-c, c-z1col], *[y1col, z1col-c])
ops.layer('straight', 2, num_bars, As20, *[y1col-c, z1col-c], *[y1col-c, c-z1col])
ops.layer('straight', 2, num_bars, As20, *[c-y1col, z1col-c], *[c-y1col, c-z1col])

ops.section('Fiber', 2)
ops.patch('rect', 1, nFibCore, nFibZ, *[c-y1col, c-z1col], *[y1col-c, z1col-c])
ops.patch('rect', 1, nFib, nFibZ, *[-y1col, -z1col], *[y1col, c-z1col])
ops.patch('rect', 1, nFib, nFibZ, *[-y1col, z1col-c], *[y1col, z1col])
ops.patch('rect', 1, nFibCover, nFibZ, *[-y1col, c-z1col], *[c-y1col, z1col-c])
ops.patch('rect', 1, nFibCover, nFibZ, *[y1col-c, c-z1col], *[y1col, z1col-c])
ops.layer('straight', 2, num_bars, As22, *[y1col-c, z1col-c], *[y1col-c, c-z1col])
ops.layer('straight', 2, num_bars, As22, *[c-y1col, z1col-c], *[c-y1col, c-z1col])

ops.section('Fiber', 3)
ops.patch('rect', 1, nFibCore, nFibZ, *[c-y1col, c-z1col], *[y1col-c, z1col-c])
ops.patch('rect', 1, nFib, nFibZ, *[-y1col, -z1col], *[y1col, c-z1col])
ops.patch('rect', 1, nFib, nFibZ, *[-y1col, z1col-c], *[y1col, z1col])
ops.patch('rect', 1, nFibCover, nFibZ, *[-y1col, c-z1col], *[c-y1col, z1col-c])
ops.patch('rect', 1, nFibCover, nFibZ, *[y1col-c, c-z1col], *[y1col, z1col-c])
ops.layer('straight', 2, num_bars, As28, *[y1col-c, z1col-c], *[y1col-c, c-z1col])
ops.layer('straight', 2, num_bars, As28, *[c-y1col, z1col-c], *[c-y1col, c-z1col])

ops.geomTransf('PDelta', 1)
ops.geomTransf('Linear', 2)

N = 10
# beamIntegration('Lobatto', tag, secTag, N)
ops.beamIntegration('Lobatto', 1, 1, N)
ops.beamIntegration('Lobatto', 2, 2, N)
ops.beamIntegration('Lobatto', 3, 3, N)
# element('forceBeamColumn', eleTag, *eleNodes, transfTag, integrationTag, '-iter', maxIter=10, tol=1e-12, '-mass', mass=0.0)
ops.element('forceBeamColumn', 1, *[1, 2], 1, 1, '-iter', 100)
ops.element('forceBeamColumn', 2, *[3, 4], 1, 1, '-iter', 100)
ops.element('forceBeamColumn', 3, *[5, 6], 1, 3, '-iter', 100)
ops.element('forceBeamColumn', 4, *[7, 8], 1, 2, '-iter', 100)
ops.element('forceBeamColumn', 5, *[9, 10], 1, 2, '-iter', 100)
# element('dispBeamColumn', eleTag, *eleNodes, transfTag, integrationTag, '-cMass', '-mass', mass=0.0)
# ops.element('dispBeamColumn', 1, *[1, 2], 1, 1)
# ops.element('dispBeamColumn', 2, *[3, 4], 1, 1)
# ops.element('dispBeamColumn', 3, *[5, 6], 1, 3)
# ops.element('dispBeamColumn', 4, *[7, 8], 1, 2)
# ops.element('dispBeamColumn', 5, *[9, 10], 1, 2)

# Beams and shit
# element('elasticBeamColumn', eleTag, *eleNodes, Area, E_mod, Iz, transfTag, <'-mass', mass>, <'-cMass'>, <'-release', releaseCode>)
ops.element('elasticBeamColumn', 6, *[2, 4], 1e3, 2e8, 1e3, 2)
ops.element('elasticBeamColumn', 7, *[4, 6], 1e3, 2e8, 1e3, 2)
ops.element('elasticBeamColumn', 8, *[6, 8], 1e3, 2e8, 1e3, 2)
ops.element('elasticBeamColumn', 9, *[8, 10], 1e3, 2e8, 1e3, 2)

opsv.plot_model()

ops.loadConst('-time', 0.0)
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)

lat_load = 1000
ops.load(2, lat_load, 0.0, 0.0)
ops.load(4, lat_load, 0.0, 0.0)
ops.load(6, lat_load, 0.0, 0.0)
ops.load(8, lat_load, 0.0, 0.0)
ops.load(10, lat_load, 0.0, 0.0)


# create SOE
Nsteps = 1000
ops.constraints("Plain")
ops.numberer("RCM")
ops.system("BandGeneral")
ops.test('NormUnbalance',1e-6, 1000)
ops.algorithm("Newton")
dU = 0.0001  # Displacement increment
# integrator('DisplacementControl', nodeTag, dof, incr, numIter=1, dUmin=incr, dUmax=incr
ops.integrator('DisplacementControl', 2, 1, dU)
ops.analysis("Static")

arr_disp = np.zeros((0,5), dtype=float)
arr_react = np.zeros((0,5), dtype=float)

for j in range(Nsteps):
    ops.analyze(1)
    ops.reactions()
    D2, D4, D6, D8, D10 = ops.nodeDisp(2, 1), ops.nodeDisp(4, 1), ops.nodeDisp(6, 1), ops.nodeDisp(8, 1), ops.nodeDisp(10, 1)
    R1, R3, R5, R7, R9 = ops.nodeReaction(1, 1), ops.nodeReaction(3, 1), ops.nodeReaction(5, 1), ops.nodeReaction(7, 1), ops.nodeReaction(9, 1)
    arr_disp = np.append(arr_disp, [[D2, D4, D6, D8, D10]], axis=0)
    arr_react = np.append(arr_react, [[R1, R3, R5, R7, R9]], axis=0)


plt.figure()
plt.plot(arr_disp[:,0]*1e3, -arr_react.sum(axis=1), color='coral')
plt.xlabel('Displacement (mm)')
plt.ylabel('Base Shear (kN)')
plt.grid()
plt.title('Pushover curve of RC Frame')