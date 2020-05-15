from plotter import Plotter
import matplotlib.pyplot as plt 
import ROOT
import math as mt 
import numpy as np 
import os
import sys

#simple function to create folder to save plots
def mkdir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Folder %s already present / failed creation" % path)
    else:
        print ("Successfully created the directory %s " % path)


file_path = "../323725_37_57_PU50.root"

#create folder to save plots
path = "./plots/"
mkdir(path)
path = path + "FullROOTtree/"
mkdir(path)

ROOT.gStyle.SetOptStat(0) #off statistics
r = Plotter.RooPlot()
#r.namedHistos(['l1_pt', 'l1_et'])
r.histFromRoot(path=file_path , tree="SaveAllJets/Jets", named=True)
r.print()
c = r.plotByName(names='all', legend_=(0.89, 0.89, 0.6, 0.7))
ky = r.getKeys()

for name, canvas in zip(ky, c):
    save_path = path + name + ".png"
    canvas.SaveAs(save_path)

