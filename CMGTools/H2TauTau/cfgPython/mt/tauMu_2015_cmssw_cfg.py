import PhysicsTools.HeppyCore.framework.config as cfg

from CMGTools.H2TauTau.tauMu_2015_base_cfg import sequence, treeProducer, tauMuAna

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
from CMGTools.H2TauTau.proto.analyzers.FileCleaner import FileCleaner

from CMGTools.H2TauTau.proto.analyzers.TauIsolationCalculator import TauIsolationCalculator
from CMGTools.H2TauTau.proto.analyzers.MuonIsolationCalculator import MuonIsolationCalculator

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, SingleTop, WJetsToLNu_LO, QCD_Mu5, DYJetsToLL_M50_LO
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow_ext, WJetsToLNu_LO, DYJetsToLL_M50_LO, TBar_tWch, T_tWch, ST_tchan_anti, ST_tchan_top, VVTo2L2Nu, WWTo1L1Nu2Q, ZZTo2L2Q, ZZTo4L, WWToLNuQQ, WWTo2L2Nu, WZTo2L2Q, WZTo3L, WZTo1L3Nu, WZTo1L1Nu2Q
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import SingleMuon_Run2015D_05Oct, SingleMuon_Run2015B_05Oct, SingleMuon_Run2015D_Promptv4
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauMu import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauMu import data_triggers, data_triggerfilters
from CMGTools.H2TauTau.proto.samples.spring15.higgs import HiggsGGH125, HiggsVBF125, HiggsTTH125
from CMGTools.H2TauTau.proto.samples.spring15.higgs_susy import HiggsSUSYGG160 as ggh160

from CMGTools.H2TauTau.htt_ntuple_base_cff import puFileData, puFileMC, eventSelector

# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production')
production = False
pick_events = False
syncntuple = True

# Define extra modules
tauIsoCalc = cfg.Analyzer(
    TauIsolationCalculator,
    name='TauIsolationCalculator',
    getter=lambda event: [event.leg2]
)

muonIsoCalc = cfg.Analyzer(
    MuonIsolationCalculator,
    name='MuonIsolationCalculator',
    getter=lambda event: [event.leg1]
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)

sequence.insert(sequence.index(treeProducer), muonIsoCalc)
sequence.insert(sequence.index(treeProducer), tauIsoCalc)
sequence.append(fileCleaner)

treeProducer.addIsoInfo = True
tauMuAna.from_single_objects = False

ggh125 = HiggsGGH125

# DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, 

# Minimal list of samples
#samples = [TT_pow, ggh125, ggh160]
#samples += [WJetsToLNu_LO, DYJetsToLL_M50_LO]
#samples += [WWTo2L2Nu, ZZp8, WZp8]
#samples += [QCD_Mu15, HiggsGGH125, HiggsVBF125, HiggsTTH125] + SingleTop

# Samples for Sync 2015 datacard
samples = [ggh160, TT_pow_ext, WJetsToLNu_LO, DYJetsToLL_M50_LO]
samples += [TBar_tWch, T_tWch, ST_tchan_anti, ST_tchan_top]
samples += [VVTo2L2Nu, ZZTo2L2Q, ZZTo4L, WWTo1L1Nu2Q, WZTo2L2Q, WZTo3L, WZTo1L3Nu, WZTo1L1Nu2Q]

split_factor = 1e5

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)

data_list = [SingleMuon_Run2015D_05Oct, SingleMuon_Run2015D_Promptv4]#SingleMuon_Run2015B_05Oct, 

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
selectedComponents = samples + data_list
selectedComponents = data_list
selectedComponents = samples


###################################################
###             CHERRY PICK EVENTS              ###
###################################################

if pick_events:
    eventSelector.toSelect = [72752, 433276, 316483, 453194, 318491, 418480, 54085, 352085]
    sequence.insert(0, eventSelector)

if not syncntuple:
    module = [s for s in sequence if s.name == 'H2TauTauSyncTreeProducerTauMu'][0]
    sequence.remove(module)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    cache = True
    # comp = samples[0]
    #comp = ggh160
    #comp = WJetsToLNu_LO
    comp = TT_pow_ext
    #comp = DYJetsToLL_M50_LO
    #comp = TBar_tWch
    #comp = T_tWch
    #comp = ST_tchan_anti
    #comp = ST_tchan_top
    selectedComponents = [comp]
    #selectedComponents = samples
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    #comp.splitFactor = 20
    #comp.fineSplitFactor = 10
    # comp.files = comp.files[]

preprocessor = CmsswPreprocessor("$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_cfg.py", addOrigAsSecondary=False)

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    preprocessor=preprocessor,
                    events_class=Events
                    )

printComps(config.components, True)

def modCfgForPlot(config):
    config.components = []
