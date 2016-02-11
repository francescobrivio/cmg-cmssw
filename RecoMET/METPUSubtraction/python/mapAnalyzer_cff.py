import FWCore.ParameterSet.Config as cms
metstrings = []
postfixes = [ "Cov00", "Cov11", "Phi", "dPhi", "Pt", "sumEt", "sumEtFraction", "PerpZ", "LongZ"]
for met in ["patpfMET", "patpfTrackMET", "patpfNoPUMET", "patpfNoPUMETT1", "patpfPUCorrectedMET", "patpfPUMET", "patpfChargedPUMET", "patpfNeutralPUMET", "patpfNeutralPVMET", "patpfNeutralUnclusteredMET", "slimmedMETs", "slimmedMETsPuppi"]:
  for postfix in postfixes:
    metstrings.append("recoil" + met + "_" + postfix)

metstrings.extend([ 
                 "select",
                 "Jet0_Eta",
                 "Jet0_M",
                 "Jet0_Phi",
                 "Jet0_Pt",
                 "Jet1_Eta",
                 "Jet1_M",
                 "Jet1_Phi",
                 "Jet1_Pt",
                 "NCleanedJets",
                 "NVertex",
                 "Boson_Pt",
                 "Boson_Phi",
                 "Boson_M",
                 "Boson_Eta",
                 "Boson_sumET",
                 "Boson_daughter1",
                 "Boson_daughter2",
                 "nCombinations"
])

MAPAnalyzer =cms.EDAnalyzer('MAPAnalyzer',
                           srcVariables = cms.InputTag("MVAMET"),
                           srcVariableNames = cms.InputTag("MVAMET"),
                           variableNamesToSave = cms.vstring( metstrings ))
