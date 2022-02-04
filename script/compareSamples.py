#!/usr/bin/env python3
import os
import math
import time
from ROOT import TFile, TH1F, TCanvas, TRatioPlot, TLegend

from truth1DxAODAccessor import TruthParticleAccessor

# weights map
from weightsMap import weights_map

def compute_dphi(phi1, phi2):
    dphi = phi1 - phi2

    while( dphi > math.pi):
        dphi -= 2*math.pi

    while( dphi < -math.pi ):
        dphi += 2*math.pi

    return dphi

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

def setupHistograms(label):
    print("Creating histograms")
    histograms = dict()

    # Event weights
    h_weights = TH1F(f"h_weights_{label}", f"Event weights", 300, 300., 600.)
    h_weights.GetXaxis().SetTitle("Event weight")
    histograms['weights'] = h_weights

    # Leading truth jet
    h_truthjet0_pt = TH1F(f"h_jet0_pt_{label}", f"Leading AntiKt4TruthWZJets pT", 100, 0., 500.)
    h_truthjet0_pt.GetXaxis().SetTitle("truth jet0 p_{T} [GeV]")
    histograms['truthjet0_pt'] = h_truthjet0_pt

    ###
    for s in ['before', 'after']:
        # ttbar
        histograms[f'ttbar_{s}FSR_pt'] = TH1F(f"h_ttbar_{s}FSR_pt_{label}", f"TTbar ({s} FSR) pT", 100, 0., 1000.)
        histograms[f'ttbar_{s}FSR_pt'].GetXaxis().SetTitle("p_{T}^{t#bar{t}} [GeV]"+f" ({s} FSR)")

        histograms[f'ttbar_{s}FSR_eta'] = TH1F(f"h_ttbar_{s}FSR_eta_{label}", f"TTbar ({s} FSR) eta", 100, -5., 5.)
        histograms[f'ttbar_{s}FSR_eta'].GetXaxis().SetTitle("#eta^{t#bar{t}}"+f" ({s} FSR)")

        histograms[f'ttbar_{s}FSR_phi'] = TH1F(f"h_ttbar_{s}FSR_phi_{label}", f"TTbar ({s} FSR) phi", 100, -math.pi, math.pi)
        histograms[f'ttbar_{s}FSR_phi'].GetXaxis().SetTitle("#phi^{t#bar{t}}"+f" ({s} FSR)")

        histograms[f'ttbar_{s}FSR_m'] = TH1F(f"h_ttbar_{s}FSR_m_{label}", f"TTbar ({s} FSR) mass", 100, 0., 2000.)
        histograms[f'ttbar_{s}FSR_m'].GetXaxis().SetTitle("m^{t#bar{t}} [GeV]"+f" ({s} FSR)")

        histograms[f'ttbar_{s}FSR_dphi'] = TH1F(f"h_ttbar_{s}FSR_dphi_{label}", f"TTbar ({s} FSR) dphi", 100, 0., math.pi)
        histograms[f'ttbar_{s}FSR_dphi'].GetXaxis().SetTitle("|#Delta#phi(t,#bar{t})|"+f" ({s} FSR)")

        # t
        histograms[f't_{s}FSR_pt'] = TH1F(f"h_t_{s}FSR_pt_{label}", f"Top ({s} FSR) pT", 100, 0., 1000.)
        histograms[f't_{s}FSR_pt'].GetXaxis().SetTitle("p_{T}^{t} [GeV]"+f" ({s} FSR)")

        histograms[f't_{s}FSR_eta'] = TH1F(f"h_t_{s}FSR_eta_{label}", f"Top ({s} FSR) eta", 100, -5., 5.)
        histograms[f't_{s}FSR_eta'].GetXaxis().SetTitle("#eta^{t}"+f" ({s} FSR)")

        histograms[f't_{s}FSR_phi'] = TH1F(f"h_t_{s}FSR_phi_{label}", f"Top ({s} FSR) phi", 100, -math.pi, math.pi)
        histograms[f't_{s}FSR_phi'].GetXaxis().SetTitle("#phi^{t}"+f" ({s} FSR)")

        histograms[f't_{s}FSR_m'] = TH1F(f"h_t_{s}FSR_m_{label}", f"Top ({s} FSR) mass", 100, 0., 500.)
        histograms[f't_{s}FSR_m'].GetXaxis().SetTitle("m^{t} [GeV]"+f" ({s} FSR)")

        # tbar
        histograms[f'tbar_{s}FSR_pt'] = TH1F(f"h_tbar_{s}FSR_pt_{label}", f"Tbar ({s} FSR) pT", 100, 0., 1000.)
        histograms[f'tbar_{s}FSR_pt'].GetXaxis().SetTitle("p_{T}^{#bar{t}} [GeV]"+f" ({s} FSR)")

        histograms[f'tbar_{s}FSR_eta'] = TH1F(f"h_tbar_{s}FSR_eta_{label}", f"Tbar ({s} FSR) eta", 100, -5., 5.)
        histograms[f'tbar_{s}FSR_eta'].GetXaxis().SetTitle("#eta^{#bar{t}}"+f" ({s} FSR)")

        histograms[f'tbar_{s}FSR_phi'] = TH1F(f"h_tbar_{s}FSR_phi_{label}", f"Tbar ({s} FSR) phi", 100, -math.pi, math.pi)
        histograms[f'tbar_{s}FSR_phi'].GetXaxis().SetTitle("#phi^{#bar{t}}"+f" ({s} FSR)")

        histograms[f'tbar_{s}FSR_m'] = TH1F(f"h_tbar_{s}FSR_m_{label}", f"Tbar ({s} FSR) mass", 100, 0., 500.)
        histograms[f'tbar_{s}FSR_m'].GetXaxis().SetTitle("m^{#bar{t}} [GeV]"+f" ({s} FSR)")

    # end of for s in ['before', 'after']:

    for hkey, hobj in histograms.items():
        hobj.Sumw2()

    return histograms

def makeHistogramsTRUTH1(
    filepath,
    label,
    weight_name = "Default",
    treename = "CollectionTree"
    ):

    tpa = TruthParticleAccessor(filepath, treename)

    # define histograms
    hists_d = setupHistograms(label)

    # arrays
    weights_arr = tpa.event_weights()
    truthjets_pt = tpa.truth_jets_pt()

    print("Loop over events")
    t_start = time.time()
    sumw = 0.
    for ievt in range( len(tpa) ):
        if not ievt%10000:
            print(f"Processing event #{ievt}")

        # event weight
        windex = getWeightIndex(weight_name)
        w = weights_arr[ievt][windex]
        hists_d['weights'].Fill(w)
        sumw += w

        # leading truth jet pt
        truthjet0_pt = truthjets_pt[ievt][0] / 1000. # MeV to GeV
        hists_d['truthjet0_pt'].Fill(truthjet0_pt, w)

        # truth top, anti-top, ttbar
        # Before FSR
        t_p4_before = tpa.getTruthTopP4(ievt, istbar=False, afterFSR=False)
        tbar_p4_before = tpa.getTruthTopP4(ievt, istbar=True, afterFSR=False)
        ttbar_p4_before = t_p4_before + tbar_p4_before

        hists_d['ttbar_beforeFSR_pt'].Fill(ttbar_p4_before.Pt()/1000., w)
        hists_d['ttbar_beforeFSR_eta'].Fill(ttbar_p4_before.Eta(), w)
        hists_d['ttbar_beforeFSR_phi'].Fill(ttbar_p4_before.Phi(), w)
        hists_d['ttbar_beforeFSR_m'].Fill(ttbar_p4_before.M()/1000., w)

        hists_d['ttbar_beforeFSR_dphi'].Fill(abs(compute_dphi(t_p4_before.Phi(), tbar_p4_before.Phi())), w)

        hists_d['t_beforeFSR_pt'].Fill(t_p4_before.Pt()/1000., w)
        hists_d['t_beforeFSR_eta'].Fill(t_p4_before.Eta(), w)
        hists_d['t_beforeFSR_phi'].Fill(t_p4_before.Phi(), w)
        hists_d['t_beforeFSR_m'].Fill(t_p4_before.M()/1000., w)

        hists_d['tbar_beforeFSR_pt'].Fill(tbar_p4_before.Pt()/1000., w)
        hists_d['tbar_beforeFSR_eta'].Fill(tbar_p4_before.Eta(), w)
        hists_d['tbar_beforeFSR_phi'].Fill(tbar_p4_before.Phi(), w)
        hists_d['tbar_beforeFSR_m'].Fill(tbar_p4_before.M()/1000., w)

        # After FSR
        t_p4_after = tpa.getTruthTopP4(ievt, istbar=False, afterFSR=True)
        tbar_p4_after = tpa.getTruthTopP4(ievt, istbar=True, afterFSR=True)
        ttbar_p4_after = t_p4_after + tbar_p4_after

        hists_d['ttbar_afterFSR_pt'].Fill(ttbar_p4_after.Pt()/1000., w)
        hists_d['ttbar_afterFSR_eta'].Fill(ttbar_p4_after.Eta(), w)
        hists_d['ttbar_afterFSR_phi'].Fill(ttbar_p4_after.Phi(), w)
        hists_d['ttbar_afterFSR_m'].Fill(ttbar_p4_after.M()/1000., w)

        hists_d['ttbar_afterFSR_dphi'].Fill(abs(compute_dphi(t_p4_after.Phi(), tbar_p4_after.Phi())), w)

        hists_d['t_afterFSR_pt'].Fill(t_p4_after.Pt()/1000., w)
        hists_d['t_afterFSR_eta'].Fill(t_p4_after.Eta(), w)
        hists_d['t_afterFSR_phi'].Fill(t_p4_after.Phi(), w)
        hists_d['t_afterFSR_m'].Fill(t_p4_after.M()/1000., w)

        hists_d['tbar_afterFSR_pt'].Fill(tbar_p4_after.Pt()/1000., w)
        hists_d['tbar_afterFSR_eta'].Fill(tbar_p4_after.Eta(), w)
        hists_d['tbar_afterFSR_phi'].Fill(tbar_p4_after.Phi(), w)
        hists_d['tbar_afterFSR_m'].Fill(tbar_p4_after.M()/1000., w)

    print(f"Total weights: {sumw}")

    t_done = time.time()
    print(f"Total processing time: {t_done - t_start:.2f} seconds")

    return hists_d

def plotHistograms(figname, hist1, hist2, label1, label2, title, canvas=None):
    if canvas is None:
        canvas = TCanvas("canvas")

    hist1.SetStats(0)
    hist1.Rebin(4)
    hist1.SetLineColor(2) # red

    hist2.SetStats(0)
    hist2.Rebin(4)
    hist2.SetLineColor(1) # black

    ymax = max(hist1.GetMaximum(), hist2.GetMaximum())
    hist1.SetMaximum(ymax*1.2)
    hist2.SetMaximum(ymax*1.2)
    hist1.SetMinimum(0)
    hist2.SetMinimum(0)

    if title:
        hist1.SetTitle(title)

    rp = TRatioPlot(hist1, hist2, 'divsym')
    rp.SetH1DrawOpt("hist")
    rp.SetH2DrawOpt("hist")
    rp.SetGridlines([1.])
    rp.Draw()

    rp.GetUpperRefYaxis().SetTitle("Weighted events")
    rp.GetUpperRefYaxis().SetMaxDigits(3)
    rp.GetLowerRefYaxis().SetTitle("Ratio")
    rp.GetLowerRefYaxis().CenterTitle()
    rp.GetLowYaxis().SetNdivisions(505)

    # legend
    leg = TLegend(0.68,0.80,0.88,0.90)
    leg.AddEntry(hist1, label1, "l")
    leg.AddEntry(hist2, label2, "l")
    leg.Draw("same")

    canvas.SaveAs(figname)

def plotHistograms_ErrOpt2(figname, hist1, hist2, label1, label2, title, canvas=None):
    if canvas is None:
        canvas = TCanvas("canvas")

    hist1.SetStats(0)
    hist1.Rebin(4)
    hist1.SetLineColor(2) # red

    hist2.SetStats(0)
    hist2.Rebin(4)
    hist2.SetLineColor(1) # black

    ymax = max(hist1.GetMaximum(), hist2.GetMaximum())
    hist1.SetMaximum(ymax*1.2)
    hist2.SetMaximum(ymax*1.2)
    hist1.SetMinimum(0)
    hist2.SetMinimum(0)

    if title:
        hist1.SetTitle(title)

    # hist2 but with zero bin errors
    hist2_noberr = hist2.Clone()
    nbins = hist2_noberr.GetNbinsX()
    for ibin in range(nbins+2): # include underflow and overflow bins
        hist2_noberr.SetBinError(ibin, 0.)

    # For displaying hist2 error bars on the ratio plot
    rp2 = TRatioPlot(hist2, hist2_noberr, 'divsym')
    rp2.Draw() # need to call Draw() first
    gr = rp2.GetLowerRefGraph()
    canvas.Clear()

    # Draw the actual ratio plot
    rp = TRatioPlot(hist1, hist2_noberr, 'divsym')
    rp.SetH1DrawOpt("hist")
    rp.SetH2DrawOpt("hist")
    rp.SetGraphDrawOpt("apz")
    rp.SetGridlines([1.])
    rp.Draw()

    rp.GetUpperRefYaxis().SetTitle("Events")
    rp.GetUpperRefYaxis().SetMaxDigits(3)
    rp.GetLowerRefYaxis().SetTitle("Ratio")
    rp.GetLowerRefYaxis().CenterTitle()
    rp.GetLowYaxis().SetNdivisions(505)

    rp.GetLowerPad().cd()
    gr.SetFillColorAlpha(1, 0.35)
    gr.Draw("same 2")

    # legend
    rp.GetUpperPad().cd()
    leg = TLegend(0.68,0.80,0.88,0.90)
    leg.AddEntry(hist1, label1, "l")
    leg.AddEntry(hist2, label2, "l")
    leg.Draw("same")

    canvas.SaveAs(figname)

def compareSamples(
    filepath_rw,
    filepath_sa,
    wc_name,
    output_dir,
    tree_name="CollectionTree"
    ):

    # reweight sample
    histograms_rw = makeHistogramsTRUTH1(filepath_rw, f"rw_{wc_name}", wc_name, tree_name)

    # standalone sample
    histograms_sa = makeHistogramsTRUTH1(filepath_sa, f"sa_{wc_name}", "Default", tree_name)

    # save histograms to disk
    fname_root = os.path.join(output_dir, 'histograms.root')
    print(f"Save histograms to {fname_root}")
    outfile = TFile.Open(fname_root, "recreate")
    for hkey, hrw in histograms_rw.items():
        outfile.WriteTObject(hrw)

    for hkey, hsa in histograms_sa.items():
        outfile.WriteTObject(hsa)
    outfile.Close()

    # plot histograms
    print("Plot histograms")
    for hkey in histograms_rw:
        #plotHistograms(
        plotHistograms_ErrOpt2(
            os.path.join(output_dir, f'{hkey}.pdf'),
            histograms_sa[hkey], histograms_rw[hkey],
            'Standalone', 'Reweight',
            title = wc_name
        )

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--infiles", nargs=2, type=str, required=True,
                        help="File paths to the reweight and standalone samples")
    parser.add_argument('-n', '--name', type=str, required=True,
                        help="Name of the Wilson cofficients and their value")
    parser.add_argument('-o', "--outputdir", type=str, default="validation",
                        help="Output name")

    args = parser.parse_args()

    if not os.path.isdir(args.outputdir):
        os.makedirs(args.outputdir)

    compareSamples(args.infiles[0], args.infiles[1], args.name, args.outputdir)
