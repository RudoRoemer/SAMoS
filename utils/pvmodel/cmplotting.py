#!/usr/bin/env python

import numpy as np
import ioutils as io
#from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import pyplot as plt
import time
from glob import glob
import os.path as path

# is building a class on top of matplotlib which manages the graph formatting 
#overengineering the problem?

# i.e.
#class Extfigure(object):
    #def __init__(self, ddump):
        #self.ddump = ddump


def makename(num, fn):
    fn = '_'.join([fn, justifynum(num)])  + '.npz'
    return fn
def justifynum(num):
    return '{:0>10}'.format(num)

# we are using numpys .npz now
def plot_radial(*fils):
    fig = plt.figure()
    axi = fig.add_subplot(111)
    #axi.show()
    axi = plt
    for fi in fils:
        data = np.load(fi)
        xs = data['rspace']
        assert len(xs) > 1
        xdiff = xs[1] - xs[0]
        x = xs[:-1] + xdiff/2
        rad = data['radial_pressure']
        axi.plot(x, rad, marker='o')
        #axi.draw()
        axi.show()
        time.sleep(0.05)

## we are using numpys .npz now
#def plot_radial_all(fglob, *fdirs):
    #fig = plt.figure()
    ##axi = fig.add_subplot(111)
    #npzset = []
    #for fd in fdirs:
        #npzset.append([])
    #npzset.append( sorted(glob(path.join(fd, fglob))) )

    #axi = plt
    #for i, fi in enumerate(npzset[0]):
        #data = np.load(fi)
        #xs = data['rspace']
        #assert len(xs) > 1
        #xdiff = xs[1] - xs[0]
        #x = xs[:-1] + xdiff/2
        #rad = data['radial_pressure']
        #axi.plot(x, rad, marker='o')
        ##axi.draw()
        #time.sleep(0.05)

def plot_radial_all(num, fname):
    fname = makename(num, fname)
    plt.xlabel('radial distance')
    data = np.load(fname)
    xs = data['simple_rspace']
    xsh = data['hardy_rspace']
    xdiff = xsh[1] - xsh[0]
    xh = xsh[:-1] + xdiff/2
    xdiff = xs[1] - xs[0]
    x = xs[:-1] + xdiff/2
    for k in data:
        if 'rspace' in k: continue
        if 'simple' in k:
            plt.plot(x, data[k], label=k, marker='o', alpha=0.5)
        if 'hardy' in k:
            plt.plot(xh, data[k], label=k, marker='x', alpha=0.5)
        
    plt.legend()
    #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           #ncol=2, mode="expand", borderaxespad=0.)
    plt.show()

def outnum(name):
    name = path.basename(name)
    bname, _ = path.splitext(name)
    return int(bname.split('_')[-1])

def plot_avg_pressures(fglob):
    stfiles = sorted(glob(fglob))
    plt.xlabel('step')
    plt.ylabel('average_pressure')
    stdatas = [np.load(st) for st in stfiles]
    xsteps = map(outnum, stfiles)
    spressure = [np.mean(data['simple_radial_pressure']) for data in stdatas]
    plt.plot(xsteps, spressure, label='simple pressure', marker='o')
    vpressure = [np.mean(data['virial_radial_pressure']) for data in stdatas]
    plt.plot(xsteps, vpressure, label='virial pressure', marker='o')
    hpressure = [np.mean(data['hardy_radial_pressure']) for data in stdatas]
    plt.plot(xsteps, hpressure, label='hardy pressure', marker='o')
    plt.show()


def plot_wls(yname='radial_pressure', fglob='stress_wl*.npz'):
    #fname = makename(num, fname)
    npzl = sorted(glob(fglob))
    plt.xlabel('radial distance')
    plt.ylabel('radial pressure')
    print npzl
    for npz in npzl:
        data = np.load(npz)
        xs = data['rspace']
        xdiff = xs[1] - xs[0]
        x = xs[:-1] + xdiff/2
        y= data[yname]
        plt.plot(x, y, label=npz, marker='o')

    plt.legend()
    plt.show()


#cmplotting.py compare_radial 4000 stress_st . ../../rA_2.5/pressure_test/ ../../vpotential_only/pressure_test/
def compare_radial(num, fname, *fdirs):
    plt.clf()
    fname = '_'.join([fname, justifynum(num)])  + '.npz'
    paths = [path.join(fd, fname) for fd in fdirs]
    plt.xlabel('radial distance')
    plt.ylabel('pressure')
    for fi in paths:
        data = np.load(fi)
        xs = data['rspace']
        assert len(xs) > 1
        xdiff = xs[1] - xs[0]
        x = xs[:-1] + xdiff/2
        rad = data['radial_pressure']
        plt.plot(x, rad, marker='o', label=fi)
    #http://matplotlib.org/users/legend_guide.html
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.show()

def readdotplot(fi):
        ddump = io.readdump(fi, firstc=float)
        return ddump
def testspace():
    rs1 = np.linspace(0, 2, 100)
    y1 = map(lambda x:x*x, rs1)
    rs2 = np.linspace(0.1, 2.5, 100)
    y2 = rs2
    plt.plot(rs1, y1)
    plt.plot(rs2, y2)
    plt.show()


if __name__=='__main__':

    import sys
    import argparse

    # This is a cute command line function that takes the first argument to be the name
    #  of a function defined locally and any other arguments as arguments to the function
    args = sys.argv[1:]
    nargs = len(args)
    if nargs is 0:
        print 'cmplotting <function> [arguments]'
        sys.exit()

    fname = args[0]
    print 'using function ', fname
    fargs = args[1:]
    try:
        f_using = locals()[fname]
    except KeyError:
        print 'I don\'t have a function \'%s\'', fname
        raise

    if len(fargs) is 0:
        print 'No arguments given to cmplotting.%s' % fname

        if hasattr(f_using, 'defaults'):
            fargs = f_using.defaults
            print 'Using defaults ', f_using.defaults
        else:
            fargs = []

    print fargs
    #print map(eval, fargs)
    #ff = map(eval, fargs)
    ff = fargs
    outd = f_using(*ff)



