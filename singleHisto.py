from Engine import RootHisto
import matplotlib.pyplot as plt 
import ROOT
import math as mt 
import numpy as np 
import os
import sys

def RandomFun(n):
    return np.random.uniform(0, 1, n)

#simple function to create folder to save plots
def mkdir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Folder %s already present / failed creation" % path)
    else:
        print ("Successfully created the directory %s " % path)

#create folder to save plots
path = "./plots/"
mkdir(path)
path = path + "FullROOTtree/"
mkdir(path)

#generate uniform numbers
vars = RandomFun(10000)

#define a histo object
h = RootHisto()
h.fill(vars, name_of = ["Uniform", "myHisto"], ranges = [0,1])
h.printAttr("Uniform") #simply shows the object created

#retrieving histo
histo = h.getSingleHisto("Uniform", "myHisto")
c = ROOT.TCanvas("c", "c", 1000, 700)
histo.Draw("hist")
c.Draw()
c.SaveAs(path + "singleHisto.png")

#changing fancy stuffs
h.markerstyleCollection(markerstyle=22, coll_name="Uniform", branches='myHisto')
h.markercolorCollection(markercolor=ROOT.kMagenta, coll_name="Uniform", branches='myHisto')
h.xlabelsCollection(labels='branch', coll_name="Uniform", branches='myHisto')

#retrieving histo
histo = h.getSingleHisto("Uniform", "myHisto")
c = ROOT.TCanvas("c", "c", 1000, 700)
histo.Draw("hist P")
c.Draw()
c.SaveAs(path + "singleHistoFancy.png")




