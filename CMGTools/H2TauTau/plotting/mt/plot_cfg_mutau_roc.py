from collections import namedtuple

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram

from CMGTools.H2TauTau.proto.plotter.ROCPlotter import histsToRoc, makeROCPlot

from CMGTools.H2TauTau.proto.plotter.Samples import samples, sampleDict

int_lumi = 1560.
pt1 = 19
pt1 = 40
pt2 = 20

inc_cut = '!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_againstMuon3>1.5 && l2_againstElectronMVA5>0.5 && l2_pt>{pt2} && l2_decayModeFinding'.format(pt2=pt2)

vars_tau = [
    VariableCfg(name='l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='db corr. 3-hit iso'),
    VariableCfg(name='l2_puppi_iso_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.5'),
    VariableCfg(name='l2_puppi_iso04_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.4'),
    VariableCfg(name='l2_puppi_iso03_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.3'),
    VariableCfg(name='l2_byIsolationMVA3newDMwLTraw', binning={'nbinsx': 10000, 'xmin': -1., 'xmax': 1.001}, unit='GeV', xtitle='MVA new DM'),
    VariableCfg(name='l2_byIsolationMVA3oldDMwLTraw', binning={'nbinsx': 10000, 'xmin': -1., 'xmax': 1.001}, unit='GeV', xtitle='MVA old DM')
]

vars_mu = [
    VariableCfg(name='l1_reliso05', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='dB iso cone 0.3'),
    VariableCfg(name='l1_reliso05_04', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='dB iso cone 0.4'),
    VariableCfg(name='l1_mini_reliso', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='Mini iso'),
    VariableCfg(name='l1_puppi_iso_pt', drawname='l1_puppi_iso_pt/l1_pt',  binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.5'),
    VariableCfg(name='l1_puppi_iso04_pt', drawname='l1_puppi_iso04_pt/l1_pt',  binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.4'),
    VariableCfg(name='l1_puppi_iso03_pt', drawname='l1_puppi_iso03_pt/l1_pt',  binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.3'),
    VariableCfg(name='l1_puppi_no_muon_iso_pt', drawname='l1_puppi_no_muon_iso_pt/l1_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI n/l cone 0.5'),
    VariableCfg(name='l1_puppi_no_muon_iso04_pt', drawname='l1_puppi_no_muon_iso04_pt/l1_pt',  binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI n/l cone 0.4'),
    VariableCfg(name='l1_puppi_no_muon_iso03_pt', drawname='l1_puppi_no_muon_iso03_pt/l1_pt',  binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI n/l cone 0.3'),
    VariableCfg(name='l1_puppi_ave_iso_pt', drawname='(l1_puppi_iso_pt + l1_puppi_no_muon_iso_pt)/l1_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI ave cone 0.5'),
    VariableCfg(name='l1_puppi_ave_iso04_pt', drawname='(l1_puppi_iso04_pt + l1_puppi_no_muon_iso04_pt)/l1_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI ave cone 0.4'),
    VariableCfg(name='l1_puppi_ave_iso03_pt', drawname='(l1_puppi_iso03_pt + l1_puppi_no_muon_iso03_pt)/l1_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI ave cone 0.3'),

]

VarSet = namedtuple('VariableSet', ['name', 'vars', 'cut_s', 'cut_b'])

var_sets = [
    # VarSet('tau_iso', vars_tau, '&& l2_gen_match == 5', '&& l2_gen_match == 6'),
    VarSet('muon_iso', vars_mu, '&& (l2_gen_match == 2 || l2_gen_match == 4)', '&& l2_gen_match == 6')
]

# samples = [sampleDict['TTJets']]#, sampleDict['QCD']]

cfg_signal = HistogramCfg(name='signal', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight='1.')
cfg_bg = HistogramCfg(name='bg', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight='1.')


for var_set in var_sets:
    print 'Variable set', var_set.name

    cfg_signal.cut += var_set.cut_s
    cfg_bg.cut += var_set.cut_b

    rocs = []
    for var in var_set.vars:
        print '  variable:', var
        cfg_signal.var = var
        cfg_bg.var = var

        plot_signal = createHistogram(cfg_signal, verbose=False)
        plot_bg = createHistogram(cfg_bg, verbose=False)

        h_signal = plot_signal.GetStack().totalHist
        h_bg = plot_bg.GetStack().totalHist

        roc = histsToRoc(h_signal.weighted, h_bg.weighted)
        roc.title = var.xtitle
        roc.name = var.name

        rocs.append(roc)

    allrocs = makeROCPlot(rocs, var_set.name, xmin=0.8, ymin=0.1, logy=True)
