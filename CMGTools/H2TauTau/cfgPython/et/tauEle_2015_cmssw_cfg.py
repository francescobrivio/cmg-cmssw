import PhysicsTools.HeppyCore.framework.config as cfg

from CMGTools.H2TauTau.tauEle_2015_base_cfg import sequence, treeProducer

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
from CMGTools.RootTools.samples.samples_13TeV_74X import TT_pow, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf

from CMGTools.H2TauTau.proto.analyzers.FileCleaner import FileCleaner
from CMGTools.H2TauTau.proto.analyzers.TauIsolationCalculator import TauIsolationCalculator
from CMGTools.H2TauTau.proto.analyzers.ElectronIsolationCalculator import ElectronIsolationCalculator
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauEle  import mc_triggers as mc_triggers_et
from CMGTools.H2TauTau.htt_ntuple_base_cff import puFileData, puFileMC, eventSelector

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production')
production = True
pick_events = False
syncntuple = False

# Define extra modules
tauIsoCalc = cfg.Analyzer(
    TauIsolationCalculator,
    name='TauIsolationCalculator',
    getter=lambda event: [event.leg2]
)

electronIsoCalc = cfg.Analyzer(
    ElectronIsolationCalculator,
    name='ElectronIsolationCalculator',
    getter=lambda event: [event.leg1]
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)

treeProducer.addIsoInfo = True

sequence.insert(sequence.index(treeProducer), tauIsoCalc)
sequence.insert(sequence.index(treeProducer), electronIsoCalc)
sequence.append(fileCleaner)

if not syncntuple:
    module = [s for s in sequence if s.name == 'H2TauTauSyncTreeProducerTauEle'][0]
    sequence.remove(module)


# Define MC components
creator = ComponentCreator()

ggh2000 = creator.makeMCComponent("GGH2000", "/SUSYGluGluToHToTauTau_M-2000_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 1.0)
ggh160 = creator.makeMCComponent("GGH160", "/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 1.0)
ggh125 = creator.makeMCComponent("GGH125", "/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 1.0)
ggh1200 = creator.makeMCComponent("GGH1200", "/SUSYGluGluToBBHToTauTau_M-1200_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 1.0)


qcd_flat = creator.makeMCComponent("QCDflat", "/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISpring15DR74-Asympt25nsRaw_MCRUN2_74_V9-v3/MINIAODSIM", "CMS", ".*root", 1.0)

samples = [ggh160, qcd_flat, TT_pow, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf]
#samples = [qcd_flat, TT_pow, DYJetsToLL_M50, WJetsToLNu]
samples = [qcd_flat, TT_pow, WJetsToLNu, ggh125, ggh2000]
#samples = [WJetsToLNu]
#samples = [ggh125]
#samples = [ggh2000]
samples = [ggh1200]

split_factor = 2e4

for sample in samples:
    sample.triggers = mc_triggers_et
    sample.splitFactor = splitFactor(sample, split_factor)

# Assign PU to MC
for mc in samples:
    mc.puFileData = puFileData
    mc.puFileMC = puFileMC

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
selectedComponents = samples
# selectedComponents = [TT_pow]
# selectedComponents = mc_dict['HiggsGGH125']
# for c in selectedComponents : c.splitFactor *= 5


# Cherry-pick events
if pick_events:
    eventSelector.toSelect = [308041,191584,240060,73996]
    sequence.insert(0, eventSelector)

# Batch or local production
if not production:
    cache = True
    # comp = my_connect.mc_dict['HiggsSUSYGG160']
    # selectedComponents = [comp]
    # comp = selectedComponents[0]
    comp = ggh160
    selectedComponents = [comp]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    comp.files = comp.files[:1]


# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )

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
