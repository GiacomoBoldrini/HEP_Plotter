import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import sys
import ROOT

class Plotter:

    class Figure:
        """
            Generate figure matplotlib
        """
        
        def __init__(size, dpi_=100):
            """
                Initialize object with size = (,) ex (10,10) and dpi_ by default 100
            """
            self.size = size 
            self.dpi = dpi_
            self.figure = plt.figure(figsize=size, dpi= dpi_)

        def getFig(self):
            """
                Return current figure
            """
            return self.figure
            
    
    class SubPlots:
        """
            Matplotlib.pyplot helper for subplots
        """

        def __init__(self, n, m, size, dpi_=100):
            """
                Initialize with member attributes: 
                n: number of subplots x dimension
                m: number of subplots y dimension (tot subplots = nxm)
                size: size of the figure as (,) ex (10,10)
                dpi_: resolution, by default 100
            """
            self.n = n
            self.m = m 
            self.size = size 
            self.dpi = dpi_
            self.figure, self.axes = plt.subplots(n,m, figsize=size, dpi= dpi_)

        def getAx(self):
            """
                Return current axes and figure
            """
            return self.figure, self.axes

        def hist(self, val, n=1, m=1, label_="histo",  histtype_='step', color_='fuchsia', bins_=50, ret=False, density_=True, range_=(0,0)):
            """
                Plot histograms on subplots. Different ways to plot:
                val: single list/numpy/pd.series of values to be histogrammed. Can also be a list of list
                n: x coordinate of the subplot. Must be integer. By default = 1 but not needed when val is type nested list
                m: y coordinate of the subplot. Must be integer. By default = 1 but not needed when val is type nested list
                label_: label of histograms. By default "histo", can be a list of dimension equal to val dimension
                hissttype_ : type of plotting hystos. By default step for everyone, can be a list of dimension equal to val dimension
                color_: color of histograms. By default = 'fuchsia' for everyone, can be a list of dimension equal to val dimension
                bins_: number of bins. By default 50 for everyone, can be a list of dimension equal to val dimension
                ret: if you want current figure or axis after plot
                density_ : Normalize to unit area all histos in input
                range_: range of histograms. By default min(val), max(val) for every item in val, otherwise can be a list of dimension equal to val dimension
            """
            if isinstance(val[0],(list,pd.core.series.Series,np.ndarray)):
                if not isinstance(range_, list):
                    range_ = []
                    for v in val:
                        if type(v) == list:
                            range_.append((min(v), max(v)))
                        else:
                            range_.append((v.min(), v.max()))

                if not isinstance(label_, list):
                    label_ = [label_]*len(val)

                if not isinstance(histtype_, list):
                    histtype_ = [histtype_]*len(val)
                
                if not isinstance(color_, list):
                    color_ = [color_]*len(val)

                for v, ax, col, lab, ra, ht in zip(val, self.axes.flat, color_, label_, range_, hissttype_ ):
                    ax.hist(v, histtype=ht, color=col, label=lab, range=ra)

            else:
                    
                if range_[0] == range_[1]:
                    if type(val) == list:
                        range_ = (min(val), max(val))
                    else:
                        range_ = (val.min(), val.max())
                
                self.axes[n,m].hist(val, histtype=histtype_, color=color_, label=label_, density=density_, range=range_)

            if ret:
                return self.figure, self.axes

        def scatter(self, val, n=1, m=1, label_="scatter", color_='fuchsia', alpha=1, ret=False, marker_='o'):

            """
                Plot scatter on subplots. Different ways to plot:
                val: single list/numpy/pd.series of values to be scattered. Can also be a list of list of type [[x,y], [x,y], ...] where x and y are list/numpy..
                n: x coordinate of the subplot. Must be integer. By default = 1 but not needed when val is type nested list
                m: y coordinate of the subplot. Must be integer. By default = 1 but not needed when val is type nested list
                label_: label of scatter. By default "scatter", can be a list of dimension equal to val dimension
                color_: color of histograms. By default = 'fuchsia' for everyone, can be a list of dimension equal to val dimension
                alpha: trasparency. By default = 1, can be a list of the same dimension of val
                ret: if you want current figure or axis after plot
                marker_: marker for the scatter. Default is 'o', can be a list of the same dimension of val
            """
            
            if isinstance(val[0],(list,pd.core.series.Series,np.ndarray)):

                if not isinstance(label_, list):
                    label_ = [label_]*len(val)
                
                if not isinstance(alpha, list):
                    alpha = [alpha]*len(val)

                if not isinstance(marker_, list):
                    marker_ = [marker_]*len(val)
                
                if not isinstance(color_, list):
                    color_ = [color_]*len(val)

                for v, ax, al, col, lab, m in zip(val, self.axes.flat, alpha, color_, label_, marker_ ):
                    ax.scatter(v[0], v[1], marker=m, color=col, alpha=al, label=lab)

            else:
                self.axes[n,m].scatter(val[0], val[1], color=color_, label=label_)

            if ret:
                return self.figure, self.axes

        def xLabel(self, lab, n=1, m=1, s=13, all_=False):
            """
                Label the x axis of the subplots.
                lab: label of the x axis. can be a list of the same dimension of the axes created
                n: x position of the subplot to be labelled. By default = 1, Not needed if lab is a list
                m: y position of the subplot to be labelled. By default = 1, Not needed if lab is a list
                s: Size of the label. It is equal to all subplots (Who wants different size for labels???). By default = 13, musgt be integer
                all_: lab must be a string. Assign same xlabel to all subplots in the class
            """
            if isinstance(lab, list):
                for l, ax in zip(lab, self.axes.flat):
                    ax.set_xlabel(l, size=s)
            else:
                if all_:
                    for ax in self.axes.flat:
                        ax.set_xlabel(lab, size=s)
                else:
                    self.axes[n,m].set_xlabel(l, size=s)

        def yLabel(self, lab, n=1, m=1, s=13, all_=False):
            """
                Label the y axis of the subplots.
                lab: label of the y axis. can be a list of the same dimension of the axes created
                n: x position of the subplot to be labelled. By default = 1, Not needed if lab is a list
                m: y position of the subplot to be labelled. By default = 1, Not needed if lab is a list
                s: Size of the label. It is equal to all subplots (Who wants different size for labels???). By default = 13, musgt be integer
                all_: lab must be a string. Assign same ylabel to all subplots in the class
            """
            if isinstance(lab, list):
                for l, ax in zip(lab, self.axes.flat):
                    ax.set_ylabel(l, size=s)
            else:
                if all_:
                    for ax in self.axes.flat:
                        ax.set_ylabel(lab, size=s)
                else:
                    self.axes[n,m].set_ylabel(l, size=s)



        def addText(self, x, y, s, n, m, size=13, ax_Frac=True):
            """
                Add text on subplot by method ax.text of subplot 
                x: x position of the text. Must be integer
                y: y position of the text. Must be integer
                s: string with the text to be plotted
                n: x index of the subplot on which we want to write
                m: y index of the subplot on which we want to write
                size: size of the text. By default is 13
                ax_Frac: x and y coordinates are intended as fraction of the relative axis (so x,y in [0,1])
            """
            if(ax_Frac):
                self.axes[n,m].text(x, y, s, fontsize=size,transform=self.axes[n,m].transAxes)
            else:
                self.axes[n,m].text(x, y, s, fontsize=size)

        def addTextAll(self, x, y, s, size=13, font_=52, ax_Frac=True):
            """
                Add same text on all subplots by method ax.text of subplot 
                x: x position of the text. Must be integer
                y: y position of the text. Must be integer
                s: string with the text to be plotted
                n: x index of the subplot on which we want to write
                m: y index of the subplot on which we want to write
                size: size of the text. By default is 13
                ax_Frac: x and y coordinates are intended as fraction of the relative axis (so x,y in [0,1]) ->
                        text will be drawn at the same position in each of the subplots
            """
            if(ax_Frac):
                for ax in self.axes.flat:
                    ax.text(x, y, s, fontsize=size,transform=ax.transAxes)
            else:
                for ax in self.axes.flat:
                    ax.text(x, y, s, fontsize=size)

        
        def legend(self, n=1, m=1, loc_ = "upper center", size= 15, bordersize=0.0, all_=False ):
            """
                Add Legend to subplots.
                n: x index of the subplot on which we want to write
                m: y index of the subplot on which we want to write
                loc_: position of the legend in the subplot. can be a list for each of the subplots only if all_=True
                size: size of the text in the legend, by default 15
                bordersize: size of the border of the legend, by default 0 (no border)
                all_: if True assign legend to all subplots with same parameters except for location that can be a list of positions
            """
            if not all_:
                leg = self.axes[n,m].legend(loc = loc_, prop={'size': size})
                leg.get_frame().set_linewidth(bordersize)
            else:
                if isinstance(loc_, list):
                    for l, ax in zip(loc_, self.axes.flat):
                        leg = ax.legend(loc = l, prop={'size': size})
                        leg.get_frame().set_linewidth(bordersize)
                else:
                    for ax in self.axes.flat:
                        leg = ax.legend(loc = loc_, prop={'size': size})
                        leg.get_frame().set_linewidth(bordersize)



        def setTickSize(self,n=1,m=1,size=11, all_=False, axis_="both"):
            """
                Tick size of axes in subplot.
                n: x index of the subplot on which we want to write
                m: y index of the subplot on which we want to write
                size: size of the Tick text in the axis, by default 11
                all_: if True assign same tick dimension to all subplots.
                axis_: change dimension of tick on specified axis: 'x', 'y' or 'both'. By default 'both'.
            """
            if not all_:
                self.axes[n,m].tick_params(axis='both', which='major', labelsize=size)
            else:
                for ax in self.axes.flat:
                    ax.tick_params(axis=axis_, which='major', labelsize=size)

        def setNotation(self, ax, n=1, m=1, all_=False ):
            """
                Mathematical notation of axis (ex 1000 -> 10^3).
                ax: can be 'x', 'y' or 'both
                n: x index of the subplot on which we want to write
                m: y index of the subplot on which we want to write
                all_: if True assign same notation to all specified axis on all subplots.
            """
            if not all_: 
                self.axes[n,m].ticklabel_format(style='sci', axis=ax, scilimits=(0,0))
            else:
                for axes in self.axes.flat:
                    axes.ticklabel_format(style='sci', axis=ax, scilimits=(0,0))

        def save(self, output="./subplots.png"):
            """
                Save current figure
                output: output path for figure by default "./subplots.png"
            """
            self.fig.savefig(output)



    class RooPlot:
        """
            Class meant to manage Root plots
        """
        def __init__(self):
            """
                Nothing needed at initialization. 5 objects will be created:
                histos: list of ROOT.TH1F to be filled
                graphs: list of ROOT.TGraph to be filled
                namedhistos: dict of named ROOT.TH1F to be filled
                keys: list of names of the above
                texts: list of text to be plotted on canvas as ROOT.TLatex
            """

            self.histos = []
            self.graphs = []
            self.namedhistos = {}
            self.keys = []
            self.texts = []

        def addText(self, coord, s):
            """
                Add text to list.
                coord: meant to be (x,y), coordinate of the text on canvas
                s: text to be plotted
            """
            self.texts.append([coord, s])
        
        def cmsText(self):
            """
                Add "CMS Preliminary" at top left outside canvas in your plot
            """
            self.texts.append([(.1, .92), "#scale[1.]{ #font[62]{CMS} #font[52]{Preliminary} }"])

        def namedHistos(self, names):
            """
                Initialize the keys of the namedhistograms.
                This method does not fill the named histograms only initialize the keys of self.namedhistos
                and assign names to self.keys.
                names: str or list of str with names of the histos

            """
            print("...Initialize names histo dictionary")
            if not isinstance(names, list):
                names = [names]
            self.namedhistos.fromkeys(names)
            self.keys = names

        def isNameInDict(self, name):
            """
                Check if a desired name is in the current dict ()so the histo is present). Does not work
                if we did not initialize self.keys with the namedHisto method.
                name: str with name to be searched
            """
            if len(self.keys):
                print("...Keys empty, fill with namedHistos(names)")
                return
            if len(self.namedhistos) == 0 and len(keys) != 0:
                print("...Initialized keys but histos are empty. Fill with hist(named=True) function")
                return

            if not isinstance(name, list):
                name = [name]

            for n in name:
                if n in self.keys:
                    print("...{} is present".format(n))
        
        def hist(self, val, name, named=False, bins_=30, linestyle = 1, linecolor = ROOT.kBlack, fillcolor = 0, fillstyle = 0, ranges=False ):
            """
                Method to fill ROOT.TH1F histograms. Works for both self.histos and self.namedhistos as follows:
                val: single list or nested list/np.array/pd.Series with arrays to be histogrammed.
                name: list of str names to give to histos. Importantg to give different names to avoid memory leaks (can be random names)
                named: Here we select which type of histograms we want to fill. If named=True self.namedhistos will be filled -> name parameter must be equal to self.keys!!!
                      By default named=False so self.histos will be filled.
                bins_: number of bins of the histograms. Can be a list if we want different binnings, dimension equal to val dimension.
                        By default bins=30 for every histo.
                linestyle: Linestyle for TH1F. Default = 1 (full line) can be a list of same dimension of val.
                linecolor: Linecolor for TH1F. Default = ROOT.kBlack, can be a list like [ROOT.kBlack, ROOT.kRed,...] of same dimension of val dimension
                fillcolor: Fillcolor of TH1F. Default = 0, can be a list like [ROOT.kBlack, ROOT.kRed, ...] fo same dimension of val dimension.
                fillstyle: FillStyle of TH1F. Default = 0, can be a list like [0, 30003, 3004, ...] of same dimension of val dimension.
                ranges: X axis range for histograms. By default range = (min(v), max(v)) for every item in v, but can be a list like [(0,100), (0,400), ...]
                        of the same dimension of val dimension, if 'all' in list then the range in that position will be (minn(val), max(val))

            """

            if ranges == False:
                ranges = []
                for v in val:
                    ranges.append([min(v), max(v)])
            else:
                if len(ranges) != len(val):
                    sys.exit("Number of ranges must be equal to number of variables being plotted")
                else:
                    ind = [i for i,x in enumerate(ranges) if x == 'all']
                    for i in ind:
                        ranges[i] = [min(val[i]), max(val[i])]

            if not named: #if not named then just fill self.histos, otherwise fill the dict
                if isinstance(val[0], (list,pd.core.series.Series,np.ndarray)):

                    if not isinstance(linecolor, list):
                        linecolor = [linecolor]*len(val)

                    if not isinstance(bins_, list):
                        bins_ = [bins_]*len(val)
                    
                    if not isinstance(fillcolor, list):
                        fillcolor = [fillcolor]*len(val)

                    if not isinstance(fillstyle, list):
                        fillstyle = [fillstyle]*len(val)

                    if not isinstance(linestyle, list):
                        linestyle = [linestyle]*len(val)

                    if not isinstance(name, list):
                        print("...Same Names for multiple TH1F possible memory leaks. Suggestying name = []")
                        name = [name]*len(val)
                        
                    for v, n, fc, fs, lc, ls, r, b in zip(val, name, fillcolor, fillstyle, linecolor, linestyle, ranges, bins_):
                        max_, min_ = r[1], r[0]
                        h = ROOT.TH1F(n, n, b, min_, max_)
                        h.SetFillStyle(fs)
                        h.SetFillColor(fc)
                        h.SetLineColor(lc)
                        h.SetLineStyle(ls)
                        for value in v:
                            h.Fill(value)
                        
                        self.histos.append(h)
                else:
                    max_, min_ = ranges[0][1], ranges[0][0]
                    h = ROOT.TH1F(name, name, bins_, min_, max_)
                    h.SetFillStyle(fillstyle)
                    h.SetFillColor(fillcolor)
                    h.SetLineColor(linecolor)
                    h.SetLineStyle(linestyle)
                    for value in val:
                        h.Fill(value)
                    
                    self.histos.append(h)

            else:
                if len(self.keys) == 0:
                    sys.exit("First fill the keys using namedHistos(self, names) function")

                if isinstance(val[0], (list,pd.core.series.Series,np.ndarray)):

                    if not isinstance(linecolor, list):
                        linecolor = [linecolor]*len(val)

                    if not isinstance(bins_, list):
                        bins_ = [bins_]*len(val)
                    
                    if not isinstance(fillcolor, list):
                        fillcolor = [fillcolor]*len(val)

                    if not isinstance(fillstyle, list):
                        fillstyle = [fillstyle]*len(val)

                    if not isinstance(linestyle, list):
                        linestyle = [linestyle]*len(val)

                    if not isinstance(name, list):
                        sys.exit("You cannot require multiple histograms with same names while filling with named=True. Switch to name=False")

                    for v, n, fc, fs, lc, ls, r, b in zip(val, name, fillcolor, fillstyle, linecolor, linestyle, ranges, bins_):
                        max_, min_ = r[1], r[0]
                        h = ROOT.TH1F(n, n, b, min_, max_)
                        h.SetFillStyle(fs)
                        h.SetFillColor(fc)
                        h.SetLineColor(lc)
                        h.SetLineStyle(ls)
                        for value in v:
                            h.Fill(value)
                        
                        self.namedhistos[n] = h
                else:
                    max_, min_ = ranges[0][1], ranges[0][0]
                    h = ROOT.TH1F(name, name, bins_, min_, max_)
                    h.SetFillStyle(fillstyle)
                    h.SetFillColor(fillcolor)
                    h.SetLineColor(linecolor)
                    h.SetLineStyle(linestyle)
                    for value in val:
                        h.Fill(value)
                    
                    self.namedhistos[name] = h
                

        def histTitle(self, title, n=0, all_=False, on='named'):
            """
                Define Title for Histograms:
                title: str or list with titles for histos
                n: index of single histo that we want to give title inside self.histos
                all_: if all_ all histos will be titled. if title = str then all histos will have the same title
                      otherwise title = list must be of the same dimension of histos dimension
                on: can be 'named' to act on self.namedhistos or 'list' to act on self.histos. note that n parameter works only if on='list'
            """
            if on=='named':
                if not all_:
                    #assign title only to one named histo with n = key 
                    if not isinstance(n, str):
                        sys.exit("check your inputs. if on=='named' then n is a string with key")
                    self.namedhistos[n].SetTitle(title)
                else:
                    #assign titles to all histograms in keys. If title = str then all histo will have the same title
                    if not isinstance(title, list):
                        title = [title]*len(self.namedhistos.keys())
                    for key, t in zip(self.namedhistos.keys(), title):
                        self.namedhistos[key].SetTitle(t)

            elif on=='list':
                if isinstance(title, list):
                    if len(title) == len(self.histos) :
                        for h, t in zip(self.histos, title):
                            h.SetTitle(t)
                    elif isinstance(n, list):
                        for index, t in zip(n, title):
                            self.histos[index].SetTitle(t)
                
                elif all_ and isinstance(title, str):
                    for h in self.histos:
                        h.SetTitle(title)

                else:
                    self.histos[n].GetXaxis().SetTitle(xlabel)

        def histxlabels(self, xlabel, n=0, all_=False, on='named'):
            """
                Assign xlabel to histograms:
                xlabel: str or list(str) with labels
                n: index or key or list of index for histogram to be assigned xlabels
                all_: if all al histo will be considered
                on: can be 'named' if self.namedhistos or 'list' if we want to act on self.histos
            """
            if on=='named':
                if not all_:
                    if not isinstance(n, str):
                        sys.exit("check your inputs. if on=='named' then n is a string with key")
                    self.namedhistos[n].GetXaxis().SetTitle(title)
                else:
                    if not isinstance(xlabel, list):
                        xlabel = [xlabel]*len(self.namedhistos.keys())
                    for key, l in zip(self.namedhistos.keys(), xlabel):
                        self.namedhistos[key].GetXaxis().SetTitle(l)

            elif on=='list':
                if isinstance(xlabel, list):
                    if len(xlabel) == len(self.histos) :
                        for h, l in zip(self.histos, xlabel):
                            h.GetXaxis().SetTitle(l)
                    elif isinstance(n, list):
                        for index, lab in zip(n, xlabel):
                            self.histos[index].GetXaxis().SetTitle(lab)
                
                elif all_ and isinstance(xlabel, str):
                    for h in self.histos:
                        h.GetXaxis().SetTitle(xlabel)

                else:
                    self.histos[n].GetXaxis().SetTitle(xlabel)

        def histylabels(self, ylabel, n=0, all_=False, on='named'):
            """
                Assign ylabel to histograms:
                ylabel: str or list(str) with labels
                n: index or key or list of index for histogram to be assigned ylabels
                all_: if all al histo will be considered
                on: can be 'named' if self.namedhistos or 'list' if we want to act on self.histos
            """
            if on=='named':
                if not all_:
                    if not isinstance(n, str):
                        sys.exit("check your inputs. if on=='named' then n is a string with key")
                    self.namedhistos[n].GetYaxis().SetTitle(ylabel)
                else:
                    if not isinstance(ylabel, list):
                        ylabel = [ylabel]*len(self.namedhistos.keys())

                    for key, l in zip(self.namedhistos.keys(), ylabel):
                        self.namedhistos[key].GetYaxis().SetTitle(l)

            elif on=='list':
                if isinstance(ylabel, list):
                    if len(ylabel) == len(self.histos) :
                        for h, l in zip(self.histos, ylabel):
                            h.GetYaxis().SetTitle(l)
                    elif isinstance(n, list):
                        for index, lab in zip(n, ylabel):
                            self.histos[index].GetYaxis().SetTitle(lab)
                
                elif all_ and isinstance(ylabel, str):
                    for h in self.histos:
                        h.GetYaxis().SetTitle(ylabel)

                else:
                    self.histos[n].GetYaxis().SetTitle(ylabel)

        def createLegend(self, loc):
            """
                Create legend for canvases
                loc: ( , , , ) with coordinates, fixed for each canvas otherwise predefined location 
                    like pyplot "upper center", "lower center", ...
            """
            if loc == "upper center": loc = (0.4, 0.89, 0.6, 0.7)
            if loc == "upper left" : loc = ()
            if loc == "upper right": loc = ()
            if loc == "lower center": loc = ()
            if loc == "lower left" : loc = ()
            if loc == "lower right": loc = ()

            self.legend = ROOT.TLegend(loc[0], loc[1], loc[2], loc[3])
            self.legend.SetBorderSize(0)

        def AddEntry(self, h, name):
            """
                Add entry to legend. Usually used in plot but can be used from main script.
                h: an element
                name: name to be plotted on the legend
            """
            self.legend.AddEntry(h, name)


        def plotAllHistos(self, x_dim=1000, y_dim=700, reso=1000, same=False):
            """
                Plot histos from self.histos.
                x_dim: x dimension of the ROOT.TCanvas. Default = 1000
                y_dim: y dimension of the ROOT.TCanvas. Default = 700
                reso: resolution for both x and y. Default = 1000
                same: plot all histos on the same Canvas? Default = False
            """
            if not same:
                canvas = []
                for ind, h in enumerate(self.histos):
                    c = ROOT.TCanvas("c"+str(ind), "c"+str(ind), reso, reso, x_dim, y_dim)
                    h.Draw("hist")
                    if len(self.texts) != 0:
                            for coord, text in self.texts:
                                T = ROOT.TLatex()
                                T.DrawLatexNDC(coord[0], coord[1], text)
                    c.Draw()
                    canvas.append(c)
                return canvas
            else:
                c = ROOT.TCanvas("c", "c", reso, reso, x_dim, y_dim)
                for ind, h in enumerate(self.histos):
                    if ind == 0:
                        h.Draw("hist")
                    else:
                        h.Draw("hist same")
                if len(self.texts) != 0:
                            for coord, text in self.texts:
                                T = ROOT.TLatex()
                                T.DrawLatexNDC(coord[0], coord[1], text)
                c.Draw()
                return c

        def plotByName(self, names, x_dim=1000, y_dim=700, reso=1000, same=False, legend_=False):
            """
                Plot histograms by name from self.nameshistos.
                names: list of keys to be plot. if 'all' in names then all self.keys() will  be plotted.
                x_dim: x dimension of the ROOT.TCanvas. Default = 1000
                y_dim: y dimension of the ROOT.TCanvas. Default = 700
                reso: resolution for both x and y. Default = 1000
                same: plot all histos on the same Canvas? Default = False
                legend_: do you want to plot the legend on the canvas? if same one big legend in not same
                        all canvases will have its own legend. Specify in input the position of the legend ex: legend_= "upper center"
                        or legend_ = ( , , , ).

            """
            if 'all' in names:
                names = self.keys

            if all(n in self.keys for n in names ) and len(self.namedhistos) != 0:
                if not same:
                    canvas = []
                    for n in names:
                        c = ROOT.TCanvas("c"+str(n), "c"+str(n), reso, reso, x_dim, y_dim)
                        if legend_: 
                            self.createLegend(legend_) #create legend, here legend_ = (,,,) coordinates
                            self.AddEntry(self.namedhistos[n], n)
                        self.namedhistos[n].Draw("hist")
                        if len(self.texts) != 0:
                            for coord, text in self.texts:
                                T = ROOT.TLatex()
                                T.DrawLatexNDC(coord[0], coord[1], text)
                        
                        if legend_:
                            self.legend.Draw()
                        c.Draw()
                        canvas.append(c)
                    return canvas
                else:
                    c = ROOT.TCanvas("c", "c", reso, reso, x_dim, y_dim)
                    if legend_: self.createLegend(legend_) #create legend, here legend_ = (,,,) coordinates
                    for ind, n in enumerate(names):
                        if ind == 0:
                            self.namedhistos[n].Draw("hist")
                            if legend_: self.AddEntry(self.namedhistos[n], n)
                        else:
                            self.namedhistos[n].Draw("hist same")
                            if legend_: self.AddEntry(self.namedhistos[n], n)
                    if len(self.texts) != 0:
                            for coord, text in self.texts:
                                T = ROOT.TLatex()
                                T.DrawLatexNDC(coord[0], coord[1], text)

                    if legend_:
                        self.legend.Draw()
                    c.Draw()
                    return c


        def getHistos(self, n=0, all_=False):
            """
                Get self.histos by index
                n: list of indeces to be returned
                all_: to return all histos
            """
            if all_:
                return self.histos
            else:
                if not isinstance(n,list): n = [n]
                return [self.histos[i] for i in n]

        def getHistosByName(self, names, all_=False):
            """
                Get self.namedhistos by name
                n: list of names to be returned
                all_: to return all histos
            """
            if all_:
                return self.namedhistos
            else:
                if not isinstance(names, list):
                    names = [names]
                return [self.namedhistos[key] for key in names]

        def scale(self, scale, n=0, all_=False):
            """
                Normalize the self.histos by a scale value.
                scale: can be float number or 'density' to normalize to unit area
                n: index of self.histos or list of indices
                all_: decide to apply the normalizations to all histos
            """
            if all_:
                if scale=='density': 
                    for h in self.histos:
                        h.Scale(1./h.Integral())
                else:
                    for h in self.histos:
                        h.Scale(1./scale)
            else:
                if not isinstance(n, list):
                    n = [n]
                if scale == 'density':
                    for idx in n:
                        self.histos[n].Scale(1./self.histos[n].Integral())
                else:
                    for idx in n:
                        self.histos[n].Scale(1./scale)

        def scaleByName(self, scale, name, all_=False):
            """
                Normalize the self.namedhistos by a scale value.
                scale: can be float number or 'density' to normalize to unit area
                name: can be str or list of str with keys of histos to be normalized
                all_: decide to apply the normalizations to all histos
            """
            if all_:
                if scale=='density':
                    for key in self.keys:
                        self.namedhistos[key].Scale(1./self.namedhistos[key].Integral())
                else:
                    if not isinstance(scale, list):
                        scale = [scale]*len(self.keys)
                    for key, s in zip(self.keys, scale):
                        self.namedhistos[key].Scale(1./s)

            else:
                if not isinstance(name, list): name = [name]
                if not all(n in self.keys for n in name): 
                    sys.exit("names not present in keys, Check consistency")
                if len(name) != len(scale) and scale != 'density': 
                    sys.exit("Same number of scales for names otherwise specify scale='density'")
                
                if scale =='density':
                    for key in name:
                        self.namedhistos[key].Scale(1./self.namedhistos[key].Integral())
                else:
                    if not isinstance(scale, list): scale = [scale]
                    for key, s in zip(name, scale):
                        self.namedhistos[key].Scale(1./s)
    