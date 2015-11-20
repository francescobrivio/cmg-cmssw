from CMGTools.H2TauTau.proto.plotter.PlotConfigs import SampleCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import setSumWeights

from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow, DYJetsToLL_M50_LO, WJetsToLNu_LO, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, T_tWch, TBar_tWch, TToLeptons_tch_amcatnlo, TToLeptons_sch_amcatnlo

def createSampleLists(analysis_dir='/afs/cern.ch/user/s/steggema/work/public/mt/NewProd', 
                      tree_prod_name='H2TauTauTreeProducerTauMu', 
                      ztt_cut='(l2_gen_match == 5)', zl_cut='(l2_gen_match < 5)',
                      zj_cut='(l2_gen_match == 6)'):
    # -> Possibly from cfg like in the past, but may also make sense to enter directly
    samples_essential = [
        SampleCfg(name='ZTT', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=ztt_cut),
        SampleCfg(name='ZL', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=zl_cut),
        SampleCfg(name='ZJ', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=zj_cut),
        SampleCfg(name='W', dir_name='WJetsToLNu_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WJetsToLNu_LO.xSection, sumweights=WJetsToLNu_LO.nGenEvents, weight_expr='1.'),
        SampleCfg(name='TT', dir_name='TT_pow', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TT_pow.xSection, sumweights=TT_pow.nGenEvents),
        SampleCfg(name='T_tWch', dir_name='T_tWch', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=T_tWch.xSection, sumweights=T_tWch.nGenEvents),
        SampleCfg(name='TBar_tWch', dir_name='TBar_tWch', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TBar_tWch.xSection, sumweights=TBar_tWch.nGenEvents),
        SampleCfg(name='ZZ', dir_name='ZZp8', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=ZZp8.xSection, sumweights=ZZp8.nGenEvents),
        SampleCfg(name='WZ', dir_name='WZ', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WZp8.xSection, sumweights=WZp8.nGenEvents),
        SampleCfg(name='WW', dir_name='WWTo2L2Nu', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WWTo2L2Nu.xSection, sumweights=WWTo2L2Nu.nGenEvents),
        SampleCfg(name='QCD', dir_name='QCD_Mu15', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=QCD_Mu15.xSection)
    ]

    samples_data = [
        SampleCfg(name='Data', dir_name='SingleMuon_Run2015D_v4', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='Data', dir_name='SingleMuon_Run2015D_05Oct', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='Data', dir_name='SingleMuon_Run2015B_05Oct', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True)
    ]

    samples_additional = [
        SampleCfg(name='TToLeptons_tch', dir_name='TToLeptons_tch_amcatnlo', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TToLeptons_tch_amcatnlo.xSection, sumweights=TToLeptons_tch_amcatnlo.nGenEvents),
        SampleCfg(name='TToLeptons_sch', dir_name='TToLeptons_sch', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TToLeptons_sch_amcatnlo.xSection, sumweights=TToLeptons_sch_amcatnlo.nGenEvents),
    ]

    samples_mc = samples_essential + samples_additional
    samples = samples_essential + samples_data
    all_samples = samples_mc + samples_data
    # -> Can add cross sections for samples either explicitly, or from file, or from cfg
    for sample in samples_mc:
        setSumWeights(sample)

    sampleDict = {s.name:s for s in all_samples}

    return samples_mc, samples_data, samples, all_samples, sampleDict

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists()

