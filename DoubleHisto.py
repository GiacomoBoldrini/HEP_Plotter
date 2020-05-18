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
var1 = RandomFun(10000)
var2 = RandomFun(10000)

h = RootHisto()
h.fill(var1, name_of = ["Uniform", "firstVar"], ranges = [0,1],  markercolor=ROOT.kBlue) #fill first creating a dictionary named Uniform
h.addNewToColl(var2, merge_on="Uniform", to_merge="secondVar", markerstyle=23, markercolor=ROOT.kMagenta, ranges=[0,1])

h.printAttr("Uniform") #check if implementation went well should show {'firstVar': <ROOT.TH1F object ("firstVar") at 0x7fd5dc2db9a0>, 'secondVar': {'secondVar': <ROOT.TH1F object ("secondVar") at 0x7fd5de226640>}}

#retrieving collection:
h_coll = h.getHistoColl("Uniform")

#plotting
c = ROOT.TCanvas("c", "c", 1000, 700)
for index, key in enumerate(h_coll.keys()):
    if index == 0:
        h_coll[key].Draw("hist P")
    else:
        h_coll[key].Draw("hist P same")
c.Draw()
c.SaveAs(path + "TwoUniformHistos_1.png")

#Anotherway, just fill two collections

h.clearColl("Uniform")
h.fill(var1, name_of = ["Uniform1", "firstVar"], ranges = [0,1],  markercolor=ROOT.kBlue) #fill first creating a dictionary named Uniform
h.fill(var2, name_of = ["Uniform2", "secondVar"], ranges = [0,1], markerstyle=23, markercolor=ROOT.kMagenta, ) #fill first creating a dictionary named Uniform

var1hist = h.getSingleHisto("Uniform1", "firstVar")
var2hist = h.getSingleHisto("Uniform2", "secondVar")

c = ROOT.TCanvas("c", "c", 1000, 700)
var1hist.Draw("hist P")
var2hist.Draw("hist P same")
c.Draw()
c.SaveAs(path + "TwoUniformHistos_2.png")

#merge collection
h.mergeColl(["Uniform1", "Uniform2"], merge_on="Uniform", keep=False)
h.printAttr("Uniform") #should get the same config as first example line 35

