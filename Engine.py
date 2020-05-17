import ROOT
import pandas as pd 
import numpy as np 
import sys
import matplotlib.pyplot as plt


class RootHisto:

    def __init__(self):
        self.attributes = []
        self.filepaths = []
        self.trees = []
        #self.filename = self.path.split(".")[-2][1:] + "_" #will be added to TH1F name to avoid memory leaks

    def fillROOT(self, path, tree, n_ev, name_of='namehisto', branches='all',  bins = 30, linestyle=1, linecolor = ROOT.kBlack, fillcolor = 0, fillstyle = 0, ranges=False):
        
        assert len(path) == len(tree), "[ERROR] Dimension of root files and trees does not match"
        assert len(path) == len(name_of), "[ERROR] Dimension of names and files does not match"

        if not isinstance(branches, list):
                branches = [branches]*len(path)
        else:
            assert len(branches) == len(path), "[ERROR] Branches does not match dimension of path"
        
        if not isinstance(linecolor, list):
                linecolor = [linecolor]*len(path)
        else:
            assert len(linecolor) == len(path), "[ERROR] Linecolor does not match dimension of path"

        if not isinstance(bins, list):
            bins = [bins]*len(path)
        else:
            assert len(bins_) == len(path), "[ERROR] Bins does not match dimension of path"
        
        if not isinstance(fillcolor, list):
            fillcolor = [fillcolor]*len(path)
        else:
            assert len(fillcolor) == len(path), "[ERROR] Fillcolor does not match dimension of path"

        if not isinstance(fillstyle, list):
            fillstyle = [fillstyle]*len(path)
        else:
            assert len(fillstyle) == len(path), "[ERROR] Fillstyle does not match dimension of path"

        if not isinstance(linestyle, list):
            linestyle = [linestyle]*len(path)
        else:
            assert len(linestyle) == len(path), "[ERROR] Linestyle does not match dimension of path"

        if not isinstance(ranges, list):
            ranges = [ranges]*len(path)
        else:
            assert len(ranges) == len(path), "[ERROR] Ranges does not match dimension of path"

        if not isinstance(n_ev, list):
            n_ev = [n_ev]*len(path)
        else:
            assert len(n_ev) == len(path), "[ERROR] Number of events does not match dimension of path"

        for path_, tree_, n_ev_, name, branches_,  bins_, linestyle_, linecolor_, fillcolor_, fillstyle_, ranges_  in zip(path, tree, n_ev, name_of, branches,  bins, linestyle, linecolor, fillcolor, fillstyle, ranges):
            
            if name in self.attributes:
                sys.exit("[ERROR] name of collection already in class, change name_of")
            else:
                self.attributes.append(name)

            self.filepaths.append(path_)
            self.trees.append(tree_)
            namedhistos = {}

            f = ROOT.TFile(path_)
            t = f.Get(tree_)

            filename = path_.split(".")[-2][1:] + "_" #will be added to TH1F name to avoid memory leaks

            if branches_ == 'all':
                branches_ = [i.GetName() for i in t.GetListOfBranches()] #branch names

            if n_ev_ == 'all':
                n_ev_ = t.GetEntries()

            f.Close()

            if ranges_:
                if len(ranges_) != len(branches_) and ranges_ != 'all':
                    sys.exit("Number of ranges must be equal to number of variables being plotted")

            if not isinstance(linecolor_, list):
                linecolor_ = [linecolor_]*len(branches_)

            if not isinstance(bins_, list):
                bins_ = [bins_]*len(branches_)
            
            if not isinstance(fillcolor_, list):
                fillcolor_ = [fillcolor_]*len(branches_)

            if not isinstance(fillstyle_, list):
                fillstyle_ = [fillstyle_]*len(branches_)

            if not isinstance(linestyle_, list):
                linestyle_ = [linestyle_]*len(branches_)

            if not isinstance(ranges_, list):
                ranges = [ranges_]*len(branches_)

            idx = 0

            print("...Filling Named Histograms")

            for branch, fc, fs, lc, ls, b in zip(branches_, fillcolor_, fillstyle_, linecolor_, linestyle_, bins_):
                print(branch)
                f = ROOT.TFile(path_)
                t = f.Get(tree_)
                var = []
                print("@Filling: ", branch)
                #filling single variables = multiple scan of tree but less memory employment -> Quicker
                #appending to list to list [[event1], [event2], ...] takes O(1) while appending everything 
                #into one list [1,2,3,...] makes everything very expensive.
                var = []
                ind_to_stop = 0
                for event in t:
                    if ind_to_stop == n_ev_ : break
                    try:
                        var.append(list(getattr(event, branch)))
                    except:
                        var.append([getattr(event, branch)])
                    ind_to_stop += 1

                var = [item for sublist in var for item in sublist]

                f.Close()

                if ranges[idx] == False:
                    r = [min(var), max(var)]

                else:
                    if ranges[idx] == 'all':
                        r = [min(var), max(var)]
                    else:
                        r = ranges[idx]
            
                max_, min_ = r[1], r[0]
                h = ROOT.TH1F(filename + branch, filename + branch, b, min_, max_)
                h.SetFillStyle(fs)
                h.SetFillColor(fc)
                h.SetLineColor(lc)
                h.SetLineStyle(ls)
                for value in var:
                    h.Fill(value)
                
        
                namedhistos[branch] = h

                idx += 1
            
            setattr(self, name, namedhistos)


    def printAttr(self, name):
        if name not in self.attributes:
            sys.exit("[ERROR] Name not in collection, change name")
        print(getattr(self, name))

    def getHistoColl(self, coll_name):
        if not isinstance(coll_name, list): coll_name  = [coll_name]
        assert all([names in self.attributes for names in coll_name]), "[ERROR] given names not in attributes"

        dicts = []
        for name in coll_name:
            dicts.append(getattr(self, name))

        return dicts

    def getSingleHisto(self, coll_name, br_name):
        assert not isinstance(coll_name, list), "[ERROR] only one col name allowed"

        h_dict = getattr(self, coll_name)

        assert br_name in h_dict.keys(), "[ERROR] {}  not in collection required: {} ".format(br_name, coll_name)

        return h_dict[br_name]






    

