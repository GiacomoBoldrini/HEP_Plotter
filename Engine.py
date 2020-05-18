import ROOT
import pandas as pd 
import numpy as np 
import sys
import matplotlib.pyplot as plt
import math as mt


class RootHisto:

    def __init__(self):
        self.attributes = []
        self.filepaths = []
        self.trees = []

    def rangeDefiner(self, rangedict = {"pt": [0, 400], "eta": [-5,5], "phi":[-mt.pi, mt.pi], "btag":[-1,1]}):
        """
            As TH1F do not allow dynamical rebinning after object innitialization, 
            it is important to define the ranges of variables a priori.
            Arguments:
            rangedict: a dictionary of type {var:[min, max], ...} where var can be a full name to avoid 
                        ambiguity or just a fragment for general use -> it will check if branches have this fragment
            
            rangedict will be stored in an attribute self.ranges used only when filling histos. Can be changed 
            when filling new histograms at any time.
        """
        self.ranges = rangedict

    def clearRange(self):
        """
            Clear attribute self.ranges
        """

        del self.ranges

    def clearColl(self, coll_name):
        """
            Clear collection by name
        """

        delattr(self, coll_name)

    def addNewToColl(self, var, merge_on='namedhisto', to_merge = 'namedhisto', bins=30, linestyle=1, linecolor = ROOT.kBlack, fillcolor = 0, fillstyle = 0, ranges=False, markerstyle = 22, markercolor = ROOT.kBlack):
        """
            Add single histogram to collection
            Arguments:
            styles/bins: See fill method 
            var: list/np.ndarray unidimensional with values to be histogrammed
            merge_on: Collection we want to append the new instance
            to_merge: Name of the key the object will have in self.merge_on attribute

        """
        print(to_merge)
        histo_coll = self.fill(var, name_of = to_merge, set_=False, bins=bins, linestyle=linestyle, linecolor=linecolor, fillcolor=fillcolor, fillstyle=fillstyle, ranges=ranges, markerstyle=markerstyle, markercolor=markercolor)
        histo = histo_coll[to_merge]
        coll_ = getattr(self, merge_on)
        coll_[to_merge] = histo
        setattr(self, merge_on, coll_)

    def mergeColl(self, coll_names, merge_on='new_merged_coll', keep=False ):
        """
            Merging two collections into a single one. Pay attention to keys to avoid overwriting
            Arguments:
            coll_names: list/np.ndarray of attribute names to be searched in self.
            merge_on: The name of the newly created merged collection
            keep: Allows to keep originary collections or free them to save memory
        """
        assert len(coll_names) >= 2, "[ERROR] not enough coll_names to merge"
        
        new_h_dict = {}
        for name in coll_names:
            h_dict = getattr(self, name)
            for key in h_dict.keys():
                new_h_dict[key] = h_dict[key]
            if not keep:
                delattr(self, name) #free memory

        setattr(self, merge_on, new_h_dict)



    def fill(self, val, name_of='namehisto', bins=30, linestyle=1, linecolor = ROOT.kBlack, fillcolor = 0, fillstyle = 0, ranges=False, markerstyle = 22, markercolor = ROOT.kBlack, set_=True ):
        """
            fill will fill named dictionaries starting from list/np.ndarrays.
            Arguments:
            val: list/ np.ndarray of values
            name_of: list [coll, key] or str [key, key]. This names will be the attributes names of the class. Avoid redefinitions to avoid 
                    overwriting. To access attributes like name_of='namehisto' just type self.namehisto. This objects
                    will be dictionaries of branches and relative histos like self.namehisto = {"branch_name": TH1F}
            bins: list or nested list of binnings. If int (list) all the histograms (related to tree list position) will have the same 
                    binning
            linestyle: same as above, linecolor of TH1F
            linecolor: same as above, linecolor of TH1F
            fillcolor: same as above, fillcolor of TH1F
            fillstyle: same as above, fillstyle of TH1F
            ranges: list or nested list of ranges. Will be overrided if self.ranges is present (more specific)
            set_: Set this dictionary as attribute of the class. Default = False will return the dictionary created
        """

        assert isinstance(val, list) or isinstance(val, np.ndarray), "[ERROR] input argument is not a list/np.array"
        if hasattr(self, "ranges") and ranges: 
            print("[INFO]: Ranges from rangeDefiner will shadow input ranges")
            ranges = False
        else:
            assert len(ranges)==2, "[ERROR] multiple ranges for single histo, check your inputs"

        if isinstance(name_of, list) or isinstance(name_of, np.ndarray):
            assert len(name_of) == 2, "[ERROR] name_of list contains too many elements"
            coll_name = name_of[0]
            histo_name = name_of[1]
        else:
            coll_name = name_of
            histo_name = name_of


        if coll_name in self.attributes:
            sys.exit("[ERROR] name of collection already in class, change name_of")
        else:
            self.attributes.append(coll_name)

        namedhisto = {}

        if ranges == False:
            if hasattr(self, "ranges"):
                for range_key in self.ranges.keys():
                    r = self.ranges[range_key]
            else:
                r = [min(var), max(var)]

        else:
            if ranges == 'all':
                r = [min(var), max(var)]
            else:
                r = ranges

        max_, min_ = r[1], r[0]
        h = ROOT.TH1F(histo_name, histo_name, bins, min_, max_)
        h.SetFillStyle(fillstyle)
        h.SetFillColor(fillcolor)
        h.SetLineColor(linecolor)
        h.SetLineStyle(linestyle)
        h.SetMarkerStyle(markerstyle)
        h.SetMarkerColor(markercolor)
        for value in val:
            h.Fill(value)
        
        namedhisto[histo_name] = h

        if set_:
            setattr(self, coll_name, namedhisto)
        else:
            return namedhisto


    def fillROOT(self, path, tree, n_ev, name_of='namehisto', branches='all',  bins = 30, linestyle=1, linecolor = ROOT.kBlack, fillcolor = 0, fillstyle = 0, ranges=False):
        """
            fillROOT will fill named dictionaries starting from .root files and trees.
            Arguments:
            path: list of paths to .root files
            tree: list of trees to pairwise reading root files
            n_ev: list of maximum number of events to read from all files. if n_ev='all' all events will be red from all files,
                    if 'all' in n_ev then it will red all the entries from pairwise file
            name_of: list of names. This names will be the attributes names of the class. Avoid redefinitions to avoid 
                    overwriting. To access attributes like name_of='namehisto' just type self.namehisto. This objects
                    will be dictionaries of branches and relative histos like self.namehisto = {"branch_name": TH1F}
            branches: list or nested list of branches to read from pairwise trees. If 'all' all branches of all files will be filled,
                        if 'all' in branches all branches of pairwise tree will be filled.
            bins: list or nested list of binnings. If int (list) all the histograms (related to tree list position) will have the same 
                    binning
            linestyle: same as above, linecolor of TH1F
            linecolor: same as above, linecolor of TH1F
            fillcolor: same as above, fillcolor of TH1F
            fillstyle: same as above, fillstyle of TH1F
            ranges: list or nested list of ranges. Will be overrided if self.ranges is present (more specific)
        """
        
        assert len(path) == len(tree), "[ERROR] Dimension of root files and trees does not match"
        assert len(path) == len(name_of), "[ERROR] Dimension of names and files does not match"

        if hasattr(self, "ranges") and ranges: 
            print("[INFO]: Ranges from rangeDefiner will shadow input ranges")
            ranges = False

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

            if ranges_ and not self.ranges:
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
                    if hasattr(self, "ranges"):
                        for range_key in self.ranges.keys():
                            if range_key in branch:
                                r = self.ranges[range_key]
                    else:
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
        """
            Print the content of an attribute of the class.
            Arguments:
            name: name  of the attribute such as "namehisto"
        """
        if name not in self.attributes:
            sys.exit("[ERROR] Name not in collection, change name")
        print(getattr(self, name))

    def getHistoColl(self, coll_name):
        """
            Return a collection of histograms from attributes.
            Attributes:
            coll_name: name of the attribute such as "namehisto"
        """
        if not isinstance(coll_name, list): coll_name  = [coll_name]
        assert all([names in self.attributes for names in coll_name]), "[ERROR] given names not in attributes"

        dicts = []
        for name in coll_name:
            dicts.append(getattr(self, name))
        
        if len(dicts) == 1: return dicts[0]
        else: return dicts

    def getSingleHisto(self, coll_name, br_name):
        """
            Get a single histo from one of collection.
            Attributes:
            coll_name: name of the attribute such as "namehisto"
            br_name: name of the key of the dictionary
        """
        assert not isinstance(coll_name, list), "[ERROR] only one col name allowed"

        h_dict = getattr(self, coll_name)

        assert br_name in h_dict.keys(), "[ERROR] {}  not in collection required: {} ".format(br_name, coll_name)

        return h_dict[br_name]
    

    def rebinCollection(self, bins_, coll_name, branches='all'):
        """
            Rebinning of TH1F is possible with fixed range and for one collection.
            Arguments:
            bins_: list of bins to pairwise binning with collection.keys()
            coll_name: name of the collection such as "namehisto"
            branches: name of the branches to  be modified, pairwise with bins_ entries
        """

        if not isinstance(bins_, list):
            bins_ = [bins_]*len(branches)

        else:
            assert len(bins_) == len(branches), "[ERROR] Same number of bins for number of branches"

        assert not isinstance(coll_name, list), "[ERROR] Parameter coll_name: {} was found to be list, only one name accepted".format(coll_name)
        
        if branches == 'all':
            branches = getattr(self, coll_name).keys()
        else:
            if not isinstance(branches, list): branches = [branches]

        h_dict = getattr(self, coll_name)

        for br, bi in zip(branches, bins_):
            h_dict[br].Rebin(bi)

        setattr(self, coll_name, h_dict) #overload the attribute with new dictionary

        return

    def linestyleCollection(self, linestyle=1, coll_name='all', branches='all'):
        """
            Change Linestyle of a collection
        """

        if coll_name == 'all': coll_name = self.attributes
        if not isinstance(coll_name, list) and coll_name != 'all': coll_name = [coll_name]
        if not isinstance(branches, list) and branches != 'all': branches = [branches]
        for name in coll_name:
            h_dict = getattr(self, name)
            if branches == 'all': branches = h_dict.keys()
            if not isinstance(linestyle, list):
                linestyle = [linestyle]*len(branches)
            else:
                assert len(linestyle) == len(branches), "[ERROR] Same number of styles for number of branches"

            for branch, ls in zip(branches, linestyle):
                h_dict[branch].SetLineStyle(ls)
            setattr(self, branch, h_dict)

    def markerstyleCollection(self, markerstyle=20, coll_name='all', branches='all'):
        """
            Change markerstyle of collection
        """ 

        if coll_name == 'all': coll_name = self.attributes
        if not isinstance(coll_name, list) and coll_name != 'all': coll_name = [coll_name]
        if not isinstance(branches, list) and branches != 'all': branches = [branches]
        for name in coll_name:
            h_dict = getattr(self, name)
            if branches == 'all': branches = h_dict.keys()
            if not isinstance(markerstyle, list):
                markerstyle = [markerstyle]*len(branches)
            else:
                assert len(markerstyle) == len(branches), "[ERROR] Same number of styles for number of branches"

            for branch, ms in zip(branches, markerstyle):
                h_dict[branch].SetMarkerStyle(ms)
            setattr(self, branch, h_dict)

    def markercolorCollection(self, markercolor=20, coll_name='all', branches='all'):
        """
            Change marker color for collection
        """

        if coll_name == 'all': coll_name = self.attributes
        if not isinstance(coll_name, list) and coll_name != 'all': coll_name = [coll_name]
        if not isinstance(branches, list) and branches != 'all': branches = [branches]
        for name in coll_name:
            h_dict = getattr(self, name)
            if branches == 'all': branches = h_dict.keys()
            if not isinstance(markercolor, list):
                markercolor = [markercolor]*len(branches)
            else:
                assert len(markercolor) == len(branches), "[ERROR] Same number of styles for number of branches"

            for branch, mc in zip(branches, markercolor):
                h_dict[branch].SetMarkerColor(mc)
            setattr(self, branch, h_dict)


    def xlabelsCollection(self, labels='branch', coll_name='all', branches='all'):
        """
            Label X axis of a collection
        """

        if coll_name == 'all': coll_name = self.attributes
        if not isinstance(coll_name, list) and coll_name != 'all': coll_name = [coll_name]
        if not isinstance(branches, list) and branches != 'all': branches = [branches]
        for name in coll_name:
            h_dict = getattr(self, name)
            if branches == 'all': branches = h_dict.keys()
    
            if not isinstance(labels, list) and labels != 'branch':
                labels = [labels]*len(branches)
            elif labels == 'branch': labels = h_dict.keys()
            else:
                assert len(labels) == len(branches), "[ERROR] Same number of styles for number of branches"


            for branch, label in zip(branches, labels):
                h_dict[branch].GetXaxis().SetTitle(label)
            setattr(self, branch, h_dict)

        







    

