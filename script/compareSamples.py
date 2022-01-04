#!/usr/bin/env python3
import uproot
import numpy as np
from ROOT import TFile, TH1F, TCanvas, TRatioPlot, TLegend

# weights map
from weightsMap import weights_map

def getWeightIndex(weight_name):
    try:
        return weights_map[weight_name]
    except KeyError:
        # try swapping the order of WCs
        wnarr = weight_name.split('_')
        if len(wnarr)==4:
            alt_weight_name = wnarr[2]+'_'+wnarr[3]+'_'+wnarr[0]+'_'+wnarr[1]
            try:
                return weights_map[alt_weight_name]
            except KeyError:
                pass
        raise

def makeHistogramsTRUTH1(
    filepath,
    label,
    weight_name = "Default",
    treename = "CollectionTree"
    ):

    print(f"Read TTree from input file {filepath}")
    tree = uproot.open(filepath+":"+treename)

    # event weights
    weights_arr = tree["EventInfoAuxDyn.mcEventWeights"].array()

    # variables to plot
    truthjets_pt = tree["AntiKt4TruthWZJetsAux.pt"].array()

    print("Making histograms")
    # define histograms
    h_weights = TH1F(f"h_weights_{label}", f"Event weights", 300, 300., 600.)
    h_weights.GetXaxis().SetTitle("Event weight")
    h_weights.Sumw2()

    h_truthjet0_pt = TH1F(f"h_jet0_pt_{label}", f"Leading AntiKt4TruthWZJets pT", 100, 0., 500.)
    h_truthjet0_pt.GetXaxis().SetTitle("truth jet0 p_{T} [GeV]")
    h_truthjet0_pt.Sumw2()

    sumw = 0.
    for ievt in range(len(weights_arr)):
        # event weight
        windex = getWeightIndex(weight_name)
        w = weights_arr[ievt][windex]
        h_weights.Fill(w)
        sumw += w

        # leading truth jet pt
        jet0_pt = truthjets_pt[ievt][0] / 1000. # MeV to GeV
        h_truthjet0_pt.Fill(jet0_pt, w)

    print(f"Total weights: {sumw}")

    return h_weights, h_truthjet0_pt

def plotHistograms(figname, histogram_list1, histogram_list2, label1, label2, title):
    canvas = TCanvas("c")
    canvas.Print(figname+'[')

    for hist1, hist2 in zip(histogram_list1, histogram_list2):
        ymax = max(hist1.GetMaximum(), hist2.GetMaximum())
        ymax *= 1.2

        hist1.SetStats(0)
        hist1.Rebin(4)
        hist1.SetLineColor(2) # red

        hist2.SetStats(0)        
        hist2.Rebin(4)
        hist2.SetLineColor(1) # black

        if title:
            hist1.SetTitle(title)

        rp = TRatioPlot(hist1, hist2)
        rp.SetH1DrawOpt("hist")
        rp.SetH2DrawOpt("hist")
        rp.SetGridlines([1.])
        rp.Draw()

        rp.GetUpperRefYaxis().SetTitle("Events")
        rp.GetLowerRefYaxis().SetTitle("Ratio")
        rp.GetLowerRefYaxis().CenterTitle()
        rp.GetLowYaxis().SetNdivisions(505)

        # legend
        leg = TLegend(0.68,0.80,0.88,0.90)
        leg.AddEntry(hist1, label1, "l")
        leg.AddEntry(hist2, label2, "l")
        leg.Draw("same")

        canvas.Print(figname)

    canvas.Print(figname+']')

def compareSamples(
    filepath_rw,
    filepath_sa,
    wc_name,
    output_name,
    tree_name="CollectionTree"
    ):

    # reweight sample
    histograms_rw = makeHistogramsTRUTH1(filepath_rw, f"rw_{wc_name}", wc_name, tree_name)

    # standalone sample
    histograms_sa = makeHistogramsTRUTH1(filepath_sa, f"sa_{wc_name}", "Default", tree_name)

    # plot histograms
    figname = output_name+'.pdf'
    print(f"Plot histograms to {figname}")
    plotHistograms(
        figname, histograms_rw, histograms_sa, 'Reweight', 'Standalone',
        title = wc_name
        )

    # save histograms to disk
    print(f"Create output file {output_name}")
    outfile = TFile.Open(output_name+'.root', "recreate")
    for hrw in histograms_rw:
        outfile.WriteTObject(hrw)

    for hsa in histograms_sa:
        outfile.WriteTObject(hsa)
    outfile.Close()

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infiles", nargs=2, type=str, required=True,
                        help="File paths to the reweight and standalone samples")
    parser.add_argument('-n', '--name', type=str, required=True,
                        help="Name of the Wilson cofficients and their value")
    parser.add_argument('-o', "--output", type=str, default="validation",
                        help="Output name")

    args = parser.parse_args()

    compareSamples(args.infiles[0], args.infiles[1], args.name, args.output)
