import PhysicsTools.HeppyCore.framework.config as cfg

from CMGTools.H2TauTau.tauMu_2015_base_cfg import sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence

from CMGTools.H2TauTau.proto.analyzers.L1TriggerAnalyzer     import L1TriggerAnalyzer

from PhysicsTools.HeppyCore.framework.config                 import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop             import getHeppyOption

from CMGTools.RootTools.utils.splitFactor                    import splitFactor
from CMGTools.RootTools.samples.ComponentCreator             import ComponentCreator
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauMu import mc_triggers   as mc_triggers_mt
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauMu import data_triggers as data_triggers_mt

from CMGTools.H2TauTau.htt_ntuple_base_cff import puFileData, puFileMC, eventSelector

# Get all heppy options; set via '-o production' or '-o production=True'
# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production')

production  = True
pick_events = False
syncntuple  = False

json25ns = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-257599_13TeV_PromptReco_Collisions15_25ns_JSON.txt'

creator = ComponentCreator()
run2015D = creator.makeDataComponent(
    'DataRun2015D'                       ,
    '/SingleMuon/Run2015D-PromptReco-v3/MINIAOD',
#     '/Tau/Run2015D-PromptReco-v3/MINIAOD', # need to run on the dataset that contains the *tag* trigger
    'CMS'                                , 
    '.*root'                             , 
    json25ns
)


samples = []

split_factor = 1e5

for sample in samples:
    sample.triggers = ['HLT_IsoMu17_eta2p1_v1', 'HLT_IsoMu17_eta2p1_v2', 'HLT_IsoMu17_eta2p1_v3', 'HLT_IsoMu18_v1', 'HLT_IsoMu18_v2', 'HLT_IsoMu18_v3']
    sample.splitFactor = splitFactor(sample, split_factor)

data_list = [run2015D]

for sample in data_list:
    #sample.triggers    = ['HLT_IsoMu17_eta2p1_v1', 'HLT_IsoMu17_eta2p1_v2', 'HLT_IsoMu17_eta2p1_v3', 'HLT_IsoMu18_v1', 'HLT_IsoMu18_v2', 'HLT_IsoMu18_v3']
    sample.triggers    = ['HLT_IsoMu18_v1', 'HLT_IsoMu18_v2', 'HLT_IsoMu18_v3']
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.json = json25ns
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
# selectedComponents = samples + data_list
selectedComponents = data_list
# selectedComponents = samples


###################################################
###          AD HOC L1 TRIGGER ANALYZER         ###
###################################################
L1TriggerAnalyzer = cfg.Analyzer(
    L1TriggerAnalyzer,
    name='L1TriggerAnalyzer',
    collections=['IsoTau', 'Tau', 'Muon'],
    #label='hltL1extraParticles',
    label='l1extraParticles',
    dR=0.5
)

###################################################
###             CHERRY PICK EVENTS              ###
###################################################

if pick_events:
    eventSelector.toSelect = [178036, 1254835, 227759, 1290544, 228758, 214782, 752109, 1279542, 1448477, 767598, 735715, 738503, 1422548, 534428]
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
    comp = run2015D
    selectedComponents = [comp]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    comp.files = comp.files[:2]

###################################################
###                  SEQUENCE                   ###
###################################################
# Adding specific mutau analyzers to the sequence
for i, module in enumerate(sequence):
  
    if module.name == 'TriggerAnalyzer':
#         module.usePrescaled = True
        module.requireTrigger = True
#         module.extraTrig = ['HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v2']
#         module.extraTrig = ['HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1_v2']
        module.extraTrig = ['HLT_IsoMu17_eta2p1_MediumIsoPFTau35_Trk1_eta2p1_Reg_v1', 'HLT_IsoMu17_eta2p1_MediumIsoPFTau35_Trk1_eta2p1_Reg_v2']
        # module.verbose = False
        module.saveFlag = True
#         module.triggerResultsHandle = ('TriggerResults', '', 'HLT25NSV4L1V5')
#         module.triggerObjectsHandle = ('selectedPatTriggerCustom', '', 'HLT25NSV4L1V5')
#         module.triggerPrescalesHandle = ('patTrigger', '', 'RECO')
    
    if module.name == 'H2TauTauTreeProducerTauMu':
        module.addTnPInfo = True
        
    if module.name == 'TauMuAnalyzer':
        sequence.insert(i+1, L1TriggerAnalyzer)
    
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

