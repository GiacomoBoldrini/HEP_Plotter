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

#generate a sample dataset
def Phi(n):
    return np.random.uniform(-mt.pi, mt.pi, n)

def Smear(n, mu, sigma):
    return np.random.normal(mu, sigma, n)

#Building toys for signal and background. Not meaningful distributions
sig_Smear = Smear(10000, 0, 1)
bkg_Smear = Smear(10000, 0, 3)

sig_Phi = Phi(10000)
bkg_Phi = Phi(10000)

#create folder to save plots
path = "./plots"
mkdir(path)

#plotting the distributions with matplotlib
p = Plotter.SubPlots(1, 2, (10,5)) #instance of Plotter.Subplots arguments: (y subplots, x subplots , figsize=(dim_y, dim_x))
p.hist([sig_Smear, sig_Phi], label_ = "Signal", bins_=[50,20], range_=[(-10,10), (-mt.pi, mt.pi)]) #signal
p.hist([bkg_Smear, bkg_Phi], label_ = "Background", bins_=[50,20], range_=[(-10,10), (-mt.pi, mt.pi)], color_='blue') #background
p.addTextAll(0.105, 1.02, r"CMS $Preliminary$", size=8) #adding a text to all subplots in fixed position
p.xLabel([r"$\frac{p_{T}^{offline} - p_{T}}{p_{T}^{offline}}$", r"$\phi$"], s=10) #add xlabel to subplots
p.yLabel("Events", s=10, all_=True) #add fixed ylabel to all subplots
p.legend(all_=True, size=8, loc_=["upper left", "lower center"]) #add legend to all subplots with different positions 
p.setNotation(all_=True, ax='y') #Quickly set exponential notation where needed just by specifying axis
p.setTickSize(all_=True, size=5) #Tick size of axis for all of the subplots 
fig, ax = p.getAx() #return current figure and axes, we can also modify them in the main
fig.savefig(path + "/plt_subplot.png") #saving the subplots

#plotting same but with ROOT this time
ROOT.gStyle.SetOptStat(0) #off statistics
r = Plotter.RooPlot()
r.namedHistos(["sig_smear", "sig_phi", "bkg_smear", "bkg_phi"]) #creating named histos with default names
r.hist(val = [sig_Smear, bkg_Smear, sig_Phi, bkg_Phi], name = ["sig_smear", "bkg_smear", "sig_phi", "bkg_phi"], named=True,  bins_=[50,50, 20, 20], linecolor = [ROOT.kMagenta, ROOT.kBlue, ROOT.kMagenta, ROOT.kBlue], ranges=[[-10,10], [-10,10], [-mt.pi, mt.pi], [-mt.pi, mt.pi]])
r.histxlabels(["#frac{p_{T}^{offline} - p_{T}}{p_{T}^{offline}}", "#frac{p_{T}^{offline} - p_{T}}{p_{T}^{offline}}", "\phi", "\phi"], on='named', all_=True)
r.histylabels("Events", on='named', all_=True)
r.histTitle("", on='named', all_=True)
r.cmsText()
c = r.plotByName(names='all', same={1:["sig_smear", "bkg_smear"], 2:["bkg_phi", "sig_phi"]}, legend_=(0.89, 0.89, 0.6, 0.7), divide=(2,1), x_dim=2000, y_dim=800, reso=1000)
c.SaveAs(path + "/root_plot_divide.png")









