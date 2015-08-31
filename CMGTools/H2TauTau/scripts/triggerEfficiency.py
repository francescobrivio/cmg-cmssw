#!/bin/env python

import argparse
import ROOT
import numpy as np

parser = argparse.ArgumentParser(description = 'Trigger tun-ons fitter. Pass me the ntuple location and a bunch of options')

parser.add_argument('ntuplePath', type = str, nargs = 1, help = 'path to the ntuple')
parser.add_argument('-t', '--tree', type = str, default = 'tree', help = 'name of the tree')
parser.add_argument('-s', '--selection', type = list, default = ['tag > 0',
                                                                'l2_byCombinedIsolationDeltaBetaCorr3Hits < 2.', 
                                                                'l1_charge * l2_charge < 0.',
                                                                'l2_eta < 2.3',
                                                                'l2_eta > -2.3',
                                                                'l2_pt > 20'], help = 'offline selection')
parser.add_argument('-b', '--binning', default = [0., 10., 15., 20., 25., 30., 35., 40., 50., 70., 100., 200.], help = 'binning')
parser.add_argument('-f', '--doFit', action = 'store_true', help = 'perform the fit')
parser.add_argument('-r', '--fitRange', default = [20., 200.], help = 'fit range')
parser.add_argument('-F', '--fitFunction', default = '[0]*TMath::Erf((x-[1])/[2])', help = 'define the function to be used in the fit')
parser.add_argument('-p', '--initialParameters', type = list, default = [(0, .8), (1, 20.), (2, 10.)], help = 'initial parameters of the fit')
parser.add_argument('-o', '--saveOutput', default = '', help = 'pass name of the root file where the efficiency TH1 is to be saved. If left blank no file is saved')

args = parser.parse_args()

fileName  = args.ntuplePath[0]
selection = args.selection
treeName  = args.tree

ROOT.TH1.SetDefaultSumw2()
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)

f1 = ROOT.TFile.Open(fileName)
f1.cd()
t1 = f1.Get(treeName)

bins = np.array(args.binning)

h_den = ROOT.TH1F('h_den', 'h_den', len(bins)-1, bins)
h_num = ROOT.TH1F('h_num', 'h_num', len(bins)-1, bins)

sel_den = ' && '.join(selection)
sel_num = sel_den + '&& probe > 0'

t1.Draw('l2_pt>>h_den', sel_den)
t1.Draw('l2_pt>>h_num', sel_num)

c1 = ROOT.TCanvas('', '', 700, 700)

ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()

h_num.Divide(h_den)
h_num.GetXaxis().SetTitle('offline #tau p_{T} [GeV]')
h_num.GetYaxis().SetTitle('L1 + HLT efficiency')
h_num.GetXaxis().SetTitleOffset(1.3)
h_num.GetYaxis().SetTitleOffset(1.3)
h_num.SetTitle('')
h_num.SetMarkerStyle(8)
h_num.SetLineWidth(2)
h_num.Draw('E')

if args.doFit:
    func = ROOT.TF1('func', args.fitFunction, args.fitRange[0], args.fitRange[1])
    for pair in args.initialParameters:
        func.SetParameter(pair[0], pair[1])

    h_num.Fit('func')
    func.Draw('SAME')

c1.SaveAs('eff.pdf')

if len(args.saveOutput):
    o1 = ROOT.TFile(args.saveOutput, 'recreate')
    o1.cd()
    h_num.Write()
    c1.Write()
    o1.Close()
    


