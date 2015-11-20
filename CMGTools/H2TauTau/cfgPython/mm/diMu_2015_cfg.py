import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.MuMuAnalyzer import MuMuAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerMuMu import H2TauTauTreeProducerMuMu
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.SVfitProducer import SVfitProducer

from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, WJetsToLNu_LO, QCD_Mu5, DYJetsToLL_M50_LO, TBar_tWch, T_tWch
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import SingleMuon_Run2015D_05Oct, SingleMuon_Run2015B_05Oct, SingleMuon_Run2015D_Promptv4
from CMGTools.H2TauTau.proto.samples.spring15.higgs import HiggsGGH125, HiggsVBF125, HiggsTTH125
from CMGTools.H2TauTau.proto.samples.spring15.higgs_susy import HiggsSUSYGG160 as ggh160

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.spring15.triggers_muMu import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.spring15.triggers_muMu import data_triggers, data_triggerfilters


# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, genAna, dyJetsFakeAna, puFileData, puFileMC, eventSelector

# mu-mu specific configuration settings

syncntuple = False
pick_events = False
computeSVfit = False
production = False

# When ready, include weights from CMGTools.H2TauTau.proto.weights.weighttable

# mc_tauEffWeight_mc = 'effTau_muTau_MC_2012ABCDSummer13'
# mc_muEffWeight_mc = 'effMu_muTau_MC_2012ABCD'
# mc_tauEffWeight = 'effTau_muTau_Data_2012ABCDSummer13'
# mc_muEffWeight = 'effMu_muTau_Data_2012ABCDSummer13'

mc_tauEffWeight_mc = None
mc_muEffWeight_mc = None
mc_tauEffWeight = None
mc_muEffWeight = None

dyJetsFakeAna.channel = 'mt'

# Define mu-tau specific modules

MuMuAna = cfg.Analyzer(
    MuMuAnalyzer,
    name='MuMuAnalyzer',
    pt1=20,
    eta1=2.3,
    iso1=0.1,
    pt2=20,
    eta2=2.3,
    iso2=0.1,
    m_min=10,
    m_max=99999,
    dR_min=0.5,
    # triggerMap = pathsAndFilters,
    from_single_objects=True,
    verbose=True
)

muonWeighter1 = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_mu_1',
    effWeight=None,
    effWeightMC=None,
    lepton='leg1',
    verbose=True,
    disable=True,
)

muonWeighter2 = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_mu_2',
    effWeight=None,
    effWeightMC=None,
    lepton='leg2',
    verbose=True,
    disable=True,
    idWeight=None,
    isoWeight=None
)

treeProducer = cfg.Analyzer(
    H2TauTauTreeProducerMuMu,
    name='H2TauTauTreeProducerMuMu'
)

syncTreeProducer = cfg.Analyzer(
    H2TauTauTreeProducerMuMu,
    name='H2TauTauSyncTreeProducerMuMu',
    varStyle='sync'
)

svfitProducer = cfg.Analyzer(
    SVfitProducer,
    name='SVfitProducer',
    integration='VEGAS',
    # integration='MarkovChain',
    # debug=True,
    l1type='muon',
    l2type='muon'
)


# Minimal list of samples
samples = [TT_pow, HiggsGGH125, ggh160]
samples += [WJetsToLNu_LO, DYJetsToLL_M50_LO]
samples += [ZZp8, WZp8]
samples += [QCD_Mu15, HiggsGGH125, HiggsVBF125, HiggsTTH125]
samples += [TBar_tWch, T_tWch, WWTo2L2Nu]

# Additional samples

split_factor = 1e5

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)

data_list = [SingleMuon_Run2015D_05Oct, SingleMuon_Run2015D_Promptv4, SingleMuon_Run2015B_05Oct]

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt'
    sample.lumi = 40.03

###################################################
###              ASSIGN PU to MC                ###
###################################################
for mc in samples:
    mc.puFileData = puFileData
    mc.puFileMC = puFileMC

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
selectedComponents = [ggh160]
# for c in selectedComponents : c.splitFactor *= 5

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = commonSequence
sequence.insert(sequence.index(genAna), MuMuAna)
sequence.append(muonWeighter1)
sequence.append(muonWeighter2)
if computeSVfit:
    sequence.append(svfitProducer)
sequence.append(treeProducer)
if syncntuple:
    sequence.append(syncTreeProducer)

###################################################
###             CHERRY PICK EVENTS              ###
###################################################
if pick_events:
    eventSelector.toSelect = []
    sequence.insert(0, eventSelector)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp = DYJetsToLL_M50_LO
    selectedComponents = [comp]
    comp.splitFactor = 1


# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )

printComps(config.components, True)


def modCfgForPlot(config):
    config.components = []
