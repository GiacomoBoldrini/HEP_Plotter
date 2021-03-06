from Engine import RootHisto
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


file_path_1 = "../323725_37_57_PU50.root"
file_path_2 = "../ggMCRAW_GenJets.root"

#create folder to save plots
path = "./plots/"
mkdir(path)
path = path + "FullROOTtree/"
mkdir(path)

h = RootHisto()
ranges = {"pt": [0, 400], "eta": [-5,5], "phi":[-mt.pi, mt.pi], "btag":[-1,1]}
h.rangeDefiner(ranges)

h.fillROOT(path=[file_path_1, file_path_2], tree=["SaveAllJets/Jets"]*2, n_ev = 200, name_of=["323725", "MC"], branches='all',  bins = 30, linestyle=1, linecolor = [ROOT.kBlue, ROOT.kMagenta], fillcolor = 0, fillstyle = 0, ranges=False)
h.printAttr("MC") #print content of "MC" dictionary
h.printAttr("323725") #print content of "323725" dictionary

MC_pf_pt = h.getSingleHisto("MC", "pf_pt")
c = ROOT.TCanvas("c", "c", 1000, 700)
MC_pf_pt.Draw("hist")
c.Draw()
c.Print(path + "bins30.png")

h.rebinCollection(bins_=5, coll_name="MC", branches='pf_pt') #rebinning only previous histo with 5 bins

MC_pf_pt = h.getSingleHisto("MC", "pf_pt")
c = ROOT.TCanvas("c", "c", 1000, 700)
MC_pf_pt.Draw("hist")
c.Draw()
c.Print(path + "bins5.png")

h.markerstyleCollection(markerstyle=22, coll_name="MC", branches='all')
h.markercolorCollection(markercolor=ROOT.kMagenta, coll_name="MC", branches='all')
h.xlabelsCollection(labels='branch', coll_name="MC", branches='all')

MC_pf_pt = h.getSingleHisto("MC", "calo_pt")
c = ROOT.TCanvas("c", "c", 1000, 700)
MC_pf_pt.Draw("hist P")
c.Draw()
c.Print(path + "Star.png")


