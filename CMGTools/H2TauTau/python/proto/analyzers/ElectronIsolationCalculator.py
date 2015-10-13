from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

from PhysicsTools.HeppyCore.utils.deltar import deltaR

from ROOT import heppy


class ElectronIsolationCalculator(Analyzer):

    '''Calculates different electron isolation values'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(ElectronIsolationCalculator, self).__init__(cfg_ana, cfg_comp, looperName)

    def attachPuppiIso(self, electron, puppi, name='puppi'):
        puppi_iso_cands = []
        puppi_iso_cands_04 = []
        puppi_iso_cands_03 = []
        electron_eta = electron.eta()
        electron_phi = electron.phi()

        for c_p in puppi:
            pdgId = c_p.pdgId()

            if abs(pdgId) not in [22, 130, 211]:
                continue

            eta = c_p.eta()
            phi = c_p.phi()
            # Neutral hadrons or photons
            inner_cone = 0.01
            if abs(pdgId) in [211]:
                inner_cone = 0.0001
            elif c_p.pt() < 0.5:
                continue

            if abs(electron_eta - eta) < 0.5:
                dr = deltaR(eta, phi, electron_eta, electron_phi)
                if inner_cone < dr:
                    if dr < 0.5:
                        puppi_iso_cands.append(c_p)
                    if dr < 0.4:
                        puppi_iso_cands_04.append(c_p)
                    if dr < 0.3:
                        puppi_iso_cands_03.append(c_p)


        setattr(electron, name+'_iso_pt', sum(c_p.pt() for c_p in puppi_iso_cands))
        setattr(electron, name+'_iso04_pt', sum(c_p.pt() for c_p in puppi_iso_cands_04))
        setattr(electron, name+'_iso03_pt', sum(c_p.pt() for c_p in puppi_iso_cands_03))

    def attachEffectiveArea(self, ele):
        aeta = abs(ele.eta())
        if   aeta < 0.800: ele.EffectiveArea03 = 0.0913
        elif aeta < 1.300: ele.EffectiveArea03 = 0.0765
        elif aeta < 2.000: ele.EffectiveArea03 = 0.0546
        elif aeta < 2.200: ele.EffectiveArea03 = 0.0728
        else:              ele.EffectiveArea03 = 0.1177
        if   aeta < 0.800: ele.EffectiveArea04 = 0.1564
        elif aeta < 1.300: ele.EffectiveArea04 = 0.1325
        elif aeta < 2.000: ele.EffectiveArea04 = 0.0913
        elif aeta < 2.200: ele.EffectiveArea04 = 0.1212
        else:              ele.EffectiveArea04 = 0.2085

    def attachMiniIsolation(self, ele):
        ele.miniIsoR = 10.0/min(max(ele.pt(), 50), 200)
        # -- version with increasing cone at low pT, gives slightly better performance for tight cuts and low pt leptons
        # ele.miniIsoR = 10.0/min(max(ele.pt(), 50),200) if ele.pt() > 20 else 4.0/min(max(ele.pt(),10),20)
        what = "ele" if (abs(ele.pdgId()) == 11) else ("eleB" if ele.isEB() else "eleE")
        if what == "ele":
            ele.miniAbsIsoCharged = self.IsolationComputer.chargedAbsIso(ele.physObj, ele.miniIsoR, {"ele": 0.0001, "eleB": 0, "eleE": 0.015}[what], 0.0)
        else:
            ele.miniAbsIsoCharged = self.IsolationComputer.chargedAbsIso(
                ele.physObj, ele.miniIsoR, {"ele": 0.0001, "eleB": 0, "eleE": 0.015}[what], 0.0, self.IsolationComputer.selfVetoNone)
        if what == "ele":
            ele.miniAbsIsoNeutral = self.IsolationComputer.neutralAbsIsoRaw(ele.physObj, ele.miniIsoR, 0.01, 0.5)
        else:
            ele.miniAbsIsoPho = self.IsolationComputer.photonAbsIsoRaw(ele.physObj, ele.miniIsoR, 0.08 if what == "eleE" else 0.0, 0.0, self.IsolationComputer.selfVetoNone)
            ele.miniAbsIsoNHad = self.IsolationComputer.neutralHadAbsIsoRaw(ele.physObj, ele.miniIsoR, 0.0, 0.0, self.IsolationComputer.selfVetoNone)
            ele.miniAbsIsoNeutral = ele.miniAbsIsoPho + ele.miniAbsIsoNHad

        if self.miniIsolationPUCorr == "rhoArea":
            ele.miniAbsIsoNeutral = max(0.0, ele.miniAbsIsoNeutral - ele.rho * ele.EffectiveArea03 * (ele.miniIsoR/0.3)**2)
        elif self.miniIsolationPUCorr != 'raw':
            raise RuntimeError, "Unsupported miniIsolationCorr name '" + \
                str(self.cfg_ana.miniIsolationCorr) + "'! For now only 'rhoArea', 'deltaBeta', 'raw', 'weights' are supported (and 'weights' is not tested)."

        ele.miniAbsIso = ele.miniAbsIsoCharged + ele.miniAbsIsoNeutral
        ele.miniRelIso = ele.miniAbsIso/ele.pt()

    def declareHandles(self):

        super(ElectronIsolationCalculator, self).declareHandles()
        self.handles['puppi'] = AutoHandle(('puppi'), 'std::vector<reco::PFCandidate>')
        self.handles['packedCandidates'] = AutoHandle('packedPFCandidates', 'std::vector<pat::PackedCandidate>')

        self.IsolationComputer = heppy.IsolationComputer()
        self.miniIsolationPUCorr = 'rhoArea'

    def beginLoop(self, setup):
        print self, self.__class__
        super(ElectronIsolationCalculator, self).beginLoop(setup)

    def process(self, event):
        self.readCollections(event.input)

        puppi = self.handles['puppi'].product()

        self.IsolationComputer.setPackedCandidates(self.handles['packedCandidates'].product())
        for lep in [event.diLepton.leg1(), event.diLepton.leg2()]:
            self.IsolationComputer.addVetos(lep.physObj)

        for electron in [event.diLepton.leg1()]:
            electron.rho = event.rho
            self.attachEffectiveArea(electron)
            self.attachMiniIsolation(electron)
            self.attachPuppiIso(electron, puppi)

        return True
