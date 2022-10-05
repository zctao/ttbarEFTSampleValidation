#!/usr/bin/env python3 
import os
import math
import time
from ROOT import TFile, TH1F, TCanvas, TRatioPlot, TLegend, TLatex

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
    histograms['weights'] = TH1F(f"h_weights_{label}", f"Event weights", 200, 350., 550.)
    histograms['weights'].GetXaxis().SetTitle("Event weight")

    histograms['weights_lowpt'] = TH1F(f"h_weights_lowpt_{label}", f"Event weights (top pT < 700 GeV)", 200, 350., 550.)
    histograms['weights_lowpt'].GetXaxis().SetTitle("Event weight")

    histograms['weights_highpt'] = TH1F(f"h_weights_highpt_{label}", f"Event weights (top pT > 700 GeV)", 200, 350., 550.)
    histograms['weights_highpt'].GetXaxis().SetTitle("Event weight")

    # Truth jet
    histograms['truthjet0_pt'] = TH1F(f"h_jet0_pt_{label}", f"Leading truth jet pT", 100, 0., 500.)
    histograms['truthjet0_pt'].GetXaxis().SetTitle("Leading truth jet p_{T} [GeV]")
    histograms['truthjet0_eta'] = TH1F(f"h_jet0_eta_{label}", f"Leading truth jet eta", 100, -5., 5.)
    histograms['truthjet0_eta'].GetXaxis().SetTitle("#eta^{leading truth jet}")

    histograms['truthjet1_pt'] = TH1F(f"h_jet1_pt_{label}", f"Sub-leading truth jet pT", 100, 0., 500.)
    histograms['truthjet1_pt'].GetXaxis().SetTitle("Sub-leading truth jet p_{T} [GeV]")
    histograms['truthjet1_eta'] = TH1F(f"h_jet1_eta_{label}", f"Sub-leading truth jet eta", 100, -5., 5.)
    histograms['truthjet1_eta'].GetXaxis().SetTitle("#eta^{subleading truth jet}")

    histograms['truthjet2_pt'] = TH1F(f"h_jet2_pt_{label}", f"Third truth jet pT", 100, 0., 500.)
    histograms['truthjet2_pt'].GetXaxis().SetTitle("3rd truth jet p_{T} [GeV]")
    histograms['truthjet2_eta'] = TH1F(f"h_jet2_eta_{label}", f"Third truth jet eta", 100, -5., 5.)
    histograms['truthjet2_eta'].GetXaxis().SetTitle("#eta^{3rd truth jet}")

    histograms['truthjet3_pt'] = TH1F(f"h_jet3_pt_{label}", f"Fourth truth jet pT", 100, 0., 500.)
    histograms['truthjet3_pt'].GetXaxis().SetTitle("4th truth jet p_{T} [GeV]")
    histograms['truthjet3_eta'] = TH1F(f"h_jet3_eta_{label}", f"Fourth truth jet eta", 100, -5., 5.)
    histograms['truthjet3_eta'].GetXaxis().SetTitle("#eta^{4th truth jet}")

    histograms['truthjet4_pt'] = TH1F(f"h_jet4_pt_{label}", f"Fifth truth jet pT", 100, 0., 500.)
    histograms['truthjet4_pt'].GetXaxis().SetTitle("5th truth jet p_{T} [GeV]")
    histograms['truthjet4_eta'] = TH1F(f"h_jet4_eta_{label}", f"Fifth truth jet eta", 100, -5., 5.)
    histograms['truthjet4_eta'].GetXaxis().SetTitle("#eta^{5th truth jet}")

    histograms['truthjet5_pt'] = TH1F(f"h_jet5_pt_{label}", f"Sixth truth jet pT", 100, 0., 500.)
    histograms['truthjet5_pt'].GetXaxis().SetTitle("6th truth jet p_{T} [GeV]")
    histograms['truthjet5_eta'] = TH1F(f"h_jet5_eta_{label}", f"Sixth truth jet eta", 100, -5., 5.)
    histograms['truthjet5_eta'].GetXaxis().SetTitle("#eta^{6th truth jet}")

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

    # W bosons
    histograms["Wp_pt"] = TH1F(f"h_Wp_pt_{label}", "W+ pT", 100, 0., 1000.)
    histograms["Wp_pt"].GetXaxis().SetTitle("p_{T}^{W^{+}} [GeV]")

    histograms["Wp_eta"] = TH1F(f"h_Wp_eta_{label}", "W+ eta", 100, -5, 5.)
    histograms["Wp_eta"].GetXaxis().SetTitle("#eta^{W^{+}}")

    histograms["Wp_phi"] = TH1F(f"h_Wp_phi_{label}", "W+ phi", 100, -math.pi, math.pi)
    histograms["Wp_phi"].GetXaxis().SetTitle("#phi^{W^{+}}")

    histograms["Wp_m"] = TH1F(f"h_Wp_m_{label}", "W+ mass", 100, 0., 250.)
    histograms["Wp_m"].GetXaxis().SetTitle("m^{W^{+}} [GeV]")

    histograms["Wm_pt"] = TH1F(f"h_Wm_pt_{label}", "W- pT", 100, 0., 1000.)
    histograms["Wm_pt"].GetXaxis().SetTitle("p_{T}^{W^{-}} [GeV]")

    histograms["Wm_eta"] = TH1F(f"h_Wm_eta_{label}", "W- eta", 100, -5, 5.)
    histograms["Wm_eta"].GetXaxis().SetTitle("#eta^{W^{-}}")

    histograms["Wm_phi"] = TH1F(f"h_Wm_phi_{label}", "W- phi", 100, -math.pi, math.pi)
    histograms["Wm_phi"].GetXaxis().SetTitle("#phi^{W^{-}}")

    histograms["Wm_m"] = TH1F(f"h_Wm_m_{label}", "W- mass", 100, 0., 250.)
    histograms["Wm_m"].GetXaxis().SetTitle("m^{W^{-}} [GeV]")

    #  electrons
    histograms["elec_pt"] = TH1F(f"h_elec_pt_{label}", "e pT", 100, 0., 100.)
    histograms["elec_pt"].GetXaxis().SetTitle("p_{T}^{e} [GeV]")

    histograms["elec_eta"] = TH1F(f"h_elec_eta_{label}", "e eta", 100, -5, 5.)
    histograms["elec_eta"].GetXaxis().SetTitle("#eta^{e}")

    histograms["elec_phi"] = TH1F(f"h_elec_phi_{label}", "e phi", 100, -math.pi, math.pi)
    histograms["elec_phi"].GetXaxis().SetTitle("#phi^{e}")

    histograms["elec_m"] = TH1F(f"h_elec_m_{label}", "e mass", 50, 0., 50.)
    histograms["elec_m"].GetXaxis().SetTitle("m^{e} [GeV]")

    histograms["next_elec_pt"] = TH1F(f"h_next_elec_pt_{label}", "e pT", 100, 0., 100.)
    histograms["next_elec_pt"].GetXaxis().SetTitle("p_{T}^{e} [GeV]")

    histograms["next_elec_eta"] = TH1F(f"h_next_elec_eta_{label}", "e eta", 100, -5, 5.)
    histograms["next_elec_eta"].GetXaxis().SetTitle("#eta^{e}")

    histograms["next_elec_phi"] = TH1F(f"h_next_elec_phi_{label}", "e phi", 100, -math.pi, math.pi)
    histograms["next_elec_phi"].GetXaxis().SetTitle("#phi^{e}")

    histograms["next_elec_m"] = TH1F(f"h_next_elec_m_{label}", "e mass", 50, 0., 50.)
    histograms["next_elec_m"].GetXaxis().SetTitle("m^{e} [GeV]")

    #muons
    histograms["muon_pt"] = TH1F(f"h_muon_pt_{label}", "#mu pT", 100, 0., 100.)
    histograms["muon_pt"].GetXaxis().SetTitle("p_{T}^{#mu} [GeV]")

    histograms["muon_eta"] = TH1F(f"h_muon_eta_{label}", "#mu eta", 100, -5, 5.)
    histograms["muon_eta"].GetXaxis().SetTitle("#eta^{#mu}")

    histograms["muon_phi"] = TH1F(f"h_muon_phi_{label}", "#mu phi", 100, -math.pi, math.pi)
    histograms["muon_phi"].GetXaxis().SetTitle("#phi^{#mu}")

    histograms["muon_m"] = TH1F(f"h_muon_m_{label}", "#mu mass", 50, 0., 50.)
    histograms["muon_m"].GetXaxis().SetTitle("m^{#mu} [GeV]")

    histograms["next_muon_pt"] = TH1F(f"h_next_muon_pt_{label}", "#mu pT", 100, 0., 100.)
    histograms["next_muon_pt"].GetXaxis().SetTitle("p_{T}^{#mu} [GeV]")

    histograms["next_muon_eta"] = TH1F(f"h_next_muon_eta_{label}", "#mu eta", 100, -5, 5.)
    histograms["next_muon_eta"].GetXaxis().SetTitle("#eta^{#mu}")

    histograms["next_muon_phi"] = TH1F(f"h_next_muon_phi_{label}", "#mu phi", 100, -math.pi, math.pi)
    histograms["next_muon_phi"].GetXaxis().SetTitle("#phi^{#mu}")

    histograms["next_muon_m"] = TH1F(f"h_next_muon_m_{label}", "#mu mass", 50, 0., 50.)
    histograms["next_muon_m"].GetXaxis().SetTitle("m^{#mu} [GeV]")

    #Both leptons
    histograms["lep_pt"] = TH1F(f"h_lep_pt_{label}", "lep pT", 100, 0., 100.)
    histograms["lep_pt"].GetXaxis().SetTitle("p_{T}^{lep} [GeV]")

    histograms["lep_eta"] = TH1F(f"h_lep_eta_{label}", "lep eta", 100, -5, 5.)
    histograms["lep_eta"].GetXaxis().SetTitle("#eta^{lep}")

    histograms["lep_phi"] = TH1F(f"h_lep_phi_{label}", "lep phi", 100, -math.pi, math.pi)
    histograms["lep_phi"].GetXaxis().SetTitle("#phi^{lep}")

    histograms["lep_m"] = TH1F(f"h_lep_m_{label}", "lep mass", 50, 0., 50.)
    histograms["lep_m"].GetXaxis().SetTitle("m^{lep} [GeV]")

    histograms["next_lep_pt"] = TH1F(f"h_next_lep_pt_{label}", "lep pT", 100, 0., 100.)
    histograms["next_lep_pt"].GetXaxis().SetTitle("p_{T}^{lep} [GeV]")

    histograms["next_lep_eta"] = TH1F(f"h_next_lep_eta_{label}", "lep eta", 100, -5, 5.)
    histograms["next_lep_eta"].GetXaxis().SetTitle("#eta^{lep}")

    histograms["next_lep_phi"] = TH1F(f"h_next_lep_phi_{label}", "lep phi", 100, -math.pi, math.pi)
    histograms["next_lep_phi"].GetXaxis().SetTitle("#phi^{lep}")

    histograms["next_lep_m"] = TH1F(f"h_next_lep_m_{label}", "lep mass", 50, 0., 50.)
    histograms["next_lep_m"].GetXaxis().SetTitle("m^{lep} [GeV]")


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
    truthjets_eta = tpa.truth_jets_eta()

    print("Loop over events")
    t_start = time.time()
    sumw = 0.
    for ievt in range( len(tpa) ):
        #if ievt > 2:
        #    break

        if not ievt%10000:
            print(f"Processing event #{ievt}")

        # event weight
        windex = getWeightIndex(weight_name)
        w = weights_arr[ievt][windex]
        hists_d['weights'].Fill(w)
        sumw += w

        # truth jets pt
        ntruthjets = len(truthjets_pt[ievt])

        if ntruthjets > 0:
            hists_d['truthjet0_pt'].Fill(truthjets_pt[ievt][0]/1000., w) # MeV to GeV
            hists_d['truthjet0_eta'].Fill(truthjets_eta[ievt][0], w)

        if ntruthjets > 1:
            hists_d['truthjet1_pt'].Fill(truthjets_pt[ievt][1]/1000., w)
            hists_d['truthjet1_eta'].Fill(truthjets_eta[ievt][1], w)

        if ntruthjets > 2:
            hists_d['truthjet2_pt'].Fill(truthjets_pt[ievt][2]/1000., w)
            hists_d['truthjet2_eta'].Fill(truthjets_eta[ievt][2], w)

        if ntruthjets > 3:
            hists_d['truthjet3_pt'].Fill(truthjets_pt[ievt][3]/1000., w)
            hists_d['truthjet3_eta'].Fill(truthjets_eta[ievt][3], w)

        if ntruthjets > 4:
            hists_d['truthjet4_pt'].Fill(truthjets_pt[ievt][4]/1000., w)
            hists_d['truthjet4_eta'].Fill(truthjets_eta[ievt][4], w)

        if ntruthjets > 5:
            hists_d['truthjet5_pt'].Fill(truthjets_pt[ievt][5]/1000., w)
            hists_d['truthjet5_eta'].Fill(truthjets_eta[ievt][5], w)

        # truth top, anti-top, ttbar
        # Before FSR
        t_p4_before = tpa.getTruthP4_top(ievt, afterFSR=False)
        tbar_p4_before = tpa.getTruthP4_antitop(ievt, afterFSR=False)
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
        t_p4_after = tpa.getTruthP4_top(ievt, afterFSR=True)
        tbar_p4_after = tpa.getTruthP4_antitop(ievt, afterFSR=True)
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

        # W bosons
        Wp_p4 = tpa.getTruthP4_Wp(ievt)
        Wm_p4 = tpa.getTruthP4_Wm(ievt)

        # W+
        hists_d['Wp_pt'].Fill(Wp_p4.Pt()/1000., w)
        hists_d['Wp_eta'].Fill(Wp_p4.Eta(), w)
        hists_d['Wp_phi'].Fill(Wp_p4.Phi(), w)
        hists_d['Wp_m'].Fill(Wp_p4.M()/1000., w)

        # W-
        hists_d['Wm_pt'].Fill(Wm_p4.Pt()/1000., w)
        hists_d['Wm_eta'].Fill(Wm_p4.Eta(), w)
        hists_d['Wm_phi'].Fill(Wm_p4.Phi(), w)
        hists_d['Wm_m'].Fill(Wm_p4.M()/1000., w)

        # Leptons
        #print('ievt = ', ievt)
        #print('weights =', w)
        elec_p4 = tpa.getTruthP4_elec(ievt)
        #print(ievt)            
        if elec_p4 is not None:
            #if len(elec_p4) != 0:
            Pt = []
            #print('No of entries = ', len(elec_p4))
            for idx in range(len(elec_p4)):
                Pt.append(elec_p4[idx].Pt())

            #print('Pt =', Pt)
            sorted_Pt = Pt.copy()
            sorted_Pt.sort(reverse=True)
            #print('Sorted Pt=',sorted_Pt)
            max_Pt = sorted_Pt[0]
            max_index = Pt.index(max_Pt)
            elec_maxPt_p4 = elec_p4[max_index]
            #print(elec_maxPt_p4)
            #global_count += 1 
            hists_d['elec_pt'].Fill(elec_maxPt_p4.Pt()/1000., w)
            hists_d['elec_eta'].Fill(elec_maxPt_p4.Eta(), w)
            hists_d['elec_phi'].Fill(elec_maxPt_p4.Phi(), w)
            hists_d['elec_m'].Fill(elec_maxPt_p4.M()/1000., w)

            if len(sorted_Pt) > 1:
                next_max_Pt = sorted_Pt[1]
                next_max_index = Pt.index(next_max_Pt)
                elec_next_maxPt_p4 = elec_p4[next_max_index]
                hists_d['next_elec_pt'].Fill(elec_next_maxPt_p4.Pt()/1000., w)
                hists_d['next_elec_eta'].Fill(elec_next_maxPt_p4.Eta(), w)
                hists_d['next_elec_phi'].Fill(elec_next_maxPt_p4.Phi(), w)
                hists_d['next_elec_m'].Fill(elec_next_maxPt_p4.M()/1000., w)  

        #muons
        muon_p4 = tpa.getTruthP4_muon(ievt)            
        if muon_p4 is not None:
            Pt = []
            for idx in range(len(muon_p4)):
                Pt.append(muon_p4[idx].Pt())

            sorted_Pt = Pt.copy()
            sorted_Pt.sort(reverse=True)
            max_Pt = sorted_Pt[0]
            max_index = Pt.index(max_Pt)
            muon_maxPt_p4 = muon_p4[max_index]
            hists_d['muon_pt'].Fill(muon_maxPt_p4.Pt()/1000., w)
            hists_d['muon_eta'].Fill(muon_maxPt_p4.Eta(), w)
            hists_d['muon_phi'].Fill(muon_maxPt_p4.Phi(), w)
            hists_d['muon_m'].Fill(muon_maxPt_p4.M()/1000., w)

            if len(sorted_Pt) > 1:
                next_max_Pt = sorted_Pt[1]
                next_max_index = Pt.index(next_max_Pt)
                muon_next_maxPt_p4 = muon_p4[next_max_index]
                hists_d['next_muon_pt'].Fill(muon_next_maxPt_p4.Pt()/1000., w)
                hists_d['next_muon_eta'].Fill(muon_next_maxPt_p4.Eta(), w)
                hists_d['next_muon_phi'].Fill(muon_next_maxPt_p4.Phi(), w)
                hists_d['next_muon_m'].Fill(muon_next_maxPt_p4.M()/1000., w)  


        #both
        both_p4 = tpa.getTruthP4_both(ievt)            
        if both_p4 is not None:
            Pt = []
            for idx in range(len(both_p4)):
                Pt.append(both_p4[idx].Pt())

            sorted_Pt = Pt.copy()
            sorted_Pt.sort(reverse=True)
            max_Pt = sorted_Pt[0]
            max_index = Pt.index(max_Pt)
            both_maxPt_p4 = both_p4[max_index]
            hists_d['lep_pt'].Fill(both_maxPt_p4.Pt()/1000., w)
            hists_d['lep_eta'].Fill(both_maxPt_p4.Eta(), w)
            hists_d['lep_phi'].Fill(both_maxPt_p4.Phi(), w)
            hists_d['lep_m'].Fill(both_maxPt_p4.M()/1000., w)

            if len(sorted_Pt) > 1:
                next_max_Pt = sorted_Pt[1]
                next_max_index = Pt.index(next_max_Pt)
                both_next_maxPt_p4 = both_p4[next_max_index]
                hists_d['next_lep_pt'].Fill(both_next_maxPt_p4.Pt()/1000., w)
                hists_d['next_lep_eta'].Fill(both_next_maxPt_p4.Eta(), w)
                hists_d['next_lep_phi'].Fill(both_next_maxPt_p4.Phi(), w)
                hists_d['next_lep_m'].Fill(both_next_maxPt_p4.M()/1000., w)               
            
                        
        

        # Event weights for low and high top pT
        if t_p4_before.Pt()/1000. < 700.:
            hists_d['weights_lowpt'].Fill(w)
        else:
            hists_d['weights_highpt'].Fill(w)

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

    # Compute Chi2/NDF between the two histograms
    chi2_per_ndf = hist1.Chi2Test(hist2, "WW OF UF CHI2/NDF")

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

    # Draw chi2/ndf to the canvas
    rp.GetUpperPad().cd()
    lt = TLatex()
    lt.SetTextSize(0.04)
    lt.DrawLatexNDC(0.7, 0.75, "#chi^{2}/NDF = "+f"{chi2_per_ndf:.3f}")

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

