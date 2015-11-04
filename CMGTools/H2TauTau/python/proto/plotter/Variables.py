from CMGTools.H2TauTau.proto.plotter.PlotConfigs import VariableCfg

from CMGTools.H2TauTau.proto.plotter.binning import binning_svfitMass_finer

all_vars = [    
    VariableCfg(name='mvis', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{vis}'),
    VariableCfg(name='mt', binning={'nbinsx':50, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T}'),
    VariableCfg(name='mt_leg2', binning={'nbinsx':50, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T} #tau'),
    VariableCfg(name='n_vertices', binning={'nbinsx':51, 'xmin':-0.5, 'xmax':50.5}, unit=None, xtitle='N_{vertices}'),
    VariableCfg(name='n_jets', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets}'),
    VariableCfg(name='n_jets_20', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets} (20 GeV)'),
    VariableCfg(name='n_bjets', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{b jets}'),
    VariableCfg(name='met_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='E_{T}^{miss} #Phi'),
    VariableCfg(name='met_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':150.}, unit='GeV', xtitle='E_{T}^{miss}'),
    VariableCfg(name='delta_eta_l1_l2', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta#eta(#tau, #mu)'),
    VariableCfg(name='delta_r_l1_l2', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta R(#tau, #mu)'),
    VariableCfg(name='vbf_mjj', binning={'nbinsx':40, 'xmin':0, 'xmax':1000.}, unit='GeV', xtitle='m_{jj}'),
    VariableCfg(name='vbf_deta', binning={'nbinsx':40, 'xmin':-7., 'xmax':7.}, unit=None, xtitle='#Delta#eta (VBF)'),
    VariableCfg(name='jet1_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='jet 1 p_{T}'),
    VariableCfg(name='jet2_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='jet 2 p_{T}'),
    VariableCfg(name='jet1_eta', binning={'nbinsx':40, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 1 #eta'),
    VariableCfg(name='jet2_eta', binning={'nbinsx':40, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 2 #eta'),
    VariableCfg(name='l1_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='muon p_{T}'),
    VariableCfg(name='l2_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau p_{T}'),
    VariableCfg(name='l1_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='muon #eta'),
    VariableCfg(name='l2_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='tau #eta'),
    VariableCfg(name='l2_decayMode', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='tau decay mode'),
    VariableCfg(name='l2_mass', binning={'nbinsx':40, 'xmin':0., 'xmax':3.}, unit='GeV', xtitle='tau mass'),
    VariableCfg(name='l2_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='tau gen match PDG ID'),
    VariableCfg(name='l1_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='muon gen match PDG ID'),
    VariableCfg(name='log_l1_dxy', drawname='log(abs(l1_dxy))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(muon d_{xy})'),
    VariableCfg(name='log_l2_dxy', drawname='log(abs(l2_dxy)+0.00001)', binning={'nbinsx':40, 'xmin':-18., 'xmax':0.5}, unit='log(cm)', xtitle='log(tau d_{xy})'),
    VariableCfg(name='l1_dxy_sig', drawname='log(abs(l1_dxy/l1_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='muon log(d_{xy}/#sigma(d_{xy}))'),
    VariableCfg(name='l2_dxy_sig', drawname='log(abs(l2_dxy/l2_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='tau log(d_{xy}/#sigma(d_{xy}))'),

    VariableCfg(name='log_l1_dz', drawname='log(abs(l1_dz))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(muon d_{z})'),
    VariableCfg(name='log_l2_dz', drawname='log(abs(l2_dz)+0.00001)', binning={'nbinsx':40, 'xmin':-18., 'xmax':0.5}, unit='log(cm)', xtitle='log(tau d_{z})'),
    VariableCfg(name='l1_dz_sig', drawname='log(abs(l1_dz/l1_dz_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='muon log(d_{z}/#sigma(d_{z}))'),
    VariableCfg(name='l2_dz_sig', drawname='log(abs(l2_dz/l2_dz_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='tau log(d_{z}/#sigma(d_{z}))'),

    VariableCfg(name='l1_reliso05_04', drawname='log(abs(l1_reliso05_04)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(muon relative isolation cone 0.4)'),
    VariableCfg(name='l1_reliso05', drawname='log(abs(l1_reliso05)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(muon relative isolation cone 0.3)'),

    VariableCfg(name='l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', binning={'nbinsx':100, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau delta-beta corr. 3-hit isolation'),

    VariableCfg(name='_norm_', drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),

]

dict_all_vars = {}
for v in all_vars:
    dict_all_vars[v.name] = v

def getVars(names):
    return [dict_all_vars[n] for n in names]
    
