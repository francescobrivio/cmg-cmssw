import PhysicsTools.HeppyCore.framework.config as cfg

from CMGTools.H2TauTau.tauMu_2015_base_cfg import sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
from CMGTools.RootTools.samples.samples_13TeV_74X import TT_pow, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, SingleTop
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import SingleMuon_Run2015B_17Jul, SingleMuon_Run2015B
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauMu import mc_triggers as mc_triggers_mt
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauMu import data_triggers as data_triggers_mt
from CMGTools.H2TauTau.proto.samples.spring15.higgs import HiggsGGH125, HiggsVBF125, HiggsTTH125

from CMGTools.H2TauTau.htt_ntuple_base_cff import puFileData, puFileMC, eventSelector

from CMGTools.H2TauTau.proto.analyzers.TriggerEfficienciesAnalyzer import TriggerEfficienciesAnalyzer

# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production')
production = False
pick_events = False
syncntuple = True

creator = ComponentCreator()
ggh160 = creator.makeMCComponent("GGH160", "/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 1.0)

qcd_flat = creator.makeMCComponent("QCDflat", "/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISpring15DR74-Asympt25nsRaw_MCRUN2_74_V9-v3/MINIAODSIM", "CMS", ".*root", 2022100000.)

ggh125 = creator.makeMCComponent("GGH125", "/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 1.0)



#samples = [qcd_flat, TT_pow, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf]

#samples = [TT_pow, DYJetsToLL_M50, WJetsToLNu, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8]

# samples = [HiggsGGH125, HiggsVBF125, HiggsTTH125] + SingleTop

samples = [ggh125, ggh160]

split_factor = 1e5

for sample in samples:
    sample.triggers = ['HLT_IsoMu24_eta2p1_v1']#mc_triggers_mt
    #sample.triggers = ['HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v1']#mc_triggers_mt
    sample.splitFactor = splitFactor(sample, split_factor)

data_list = [SingleMuon_Run2015B_17Jul, SingleMuon_Run2015B]

for sample in data_list:
    sample.triggers = data_triggers_mt
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_v2.txt'
    sample.lumi = 40.03


### Define mu-tau specific modules

triggEfficiency = cfg.Analyzer(
    TriggerEfficienciesAnalyzer,
    name='TriggerEfficienciesAnalyzer',
    common_trigger='HLT_IsoMu24_eta2p1_v1',
    specific_trigger='HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v1',
    #addTriggerObjects=True,
    #requireTrigger=True
)


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
# selectedComponents = samples


###################################################
###             CHERRY PICK EVENTS              ###
###################################################

if pick_events:
    eventSelector.toSelect = [1017413, 1033114]
    sequence.insert(0, eventSelector)

if not syncntuple:
    module = [s for s in sequence if s.name == 'H2TauTauSyncTreeProducerTauMu'][0]
    sequence.remove(module)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    cache = True
    # comp = my_connect.mc_dict['HiggsSUSYGG160']
    # selectedComponents = [comp]
    # comp = selectedComponents[0]
    # comp = data_list[0]
    #comp = QCD_Mu15
    comp = ggh125
    #selectedComponents = [comp]
    selectedComponents = samples
    comp.splitFactor = 1
    comp.fineSplitFactor = 10
    # comp.files = comp.files[]

###################################################
###                  SEQUENCE                   ###
###################################################
# Adding specific mutau analyzers to the sequence

# Loop on sequence to have the requireTrigger=False and to add the triggEffAnalyzer
# right after the MuTauAnalyzer
for i in range(0,len(sequence)):

    if sequence[i].name is 'TriggerAnalyzer':
        sequence[i].requireTrigger = True
        #sequence[i].requireTrigger = False
        #sequence[i].extraTrig = ['HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v1']
        sequence[i].extraTrig = ['HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v1']
        sequence[i].verbose = True
        sequence[i].saveFlag = True

    '''if sequence[i].name is 'TauMuAnalyzer':
        sequence.insert(i+1,triggEfficiency)
    else:
        continue'''

# Print the sequence (just a check to see if everything is ok)
print '----> SEQUENCE <----'
print sequence

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

