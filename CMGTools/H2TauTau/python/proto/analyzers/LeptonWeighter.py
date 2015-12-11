from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.statistics.average import Average

from CMGTools.H2TauTau.proto.TriggerEfficiency import TriggerEfficiency
from CMGTools.H2TauTau.proto.analyzers.RecEffCorrection import recEffMapEle, recEffMapMu

import ROOT
import math

def _crystalballPositiveAlpha( x, alpha, n, mu, sigma):
    '''
    https://en.wikipedia.org/wiki/Crystal_Ball_function
    ''' 
    
    expArg = -0.5 * ROOT.TMath.Power(abs(alpha), 2.)
    gauss  = ROOT.TMath.Exp(expArg)
        
    A = ROOT.TMath.Power( (n/abs(alpha)), n) * gauss
    B = n / abs(alpha) - abs(alpha)
    C = n / (abs(alpha) * (n - 1.)) * gauss
    D = math.sqrt(math.pi/2.) * (1. + ROOT.TMath.Erf(abs(alpha)/math.sqrt(2.))) 
    N = 1. / (sigma * (C + D))

    pull = (x - mu)/sigma 
        
    if pull > -alpha:
        func = N * ROOT.TMath.Gaus(x, mu, sigma)
    else:
        func = N * A * ROOT.TMath.Power( (B - pull), -n )

    return func

def _crystalball( x, alpha, n, mu, sigma, scale ):
    
    if alpha > 0.:
        return scale * _crystalballPositiveAlpha( x, alpha, n, mu, sigma ) 
    else:
        x1     = 2 * mu - x
        alpha1 = -alpha
        return scale * _crystalballPositiveAlpha( x1, alpha1, n, mu, sigma ) 


def crystalball(x, par):
    x     = x[0]
    alpha = par[0]
    n     = par[1]
    mu    = par[2]
    sigma = par[3]
    scale = par[4]
    return _crystalball(x, alpha, n, mu, sigma, scale)


class LeptonWeighter( Analyzer ):
    '''Gets lepton efficiency weight and puts it in the event'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(LeptonWeighter,self).__init__(cfg_ana, cfg_comp, looperName)

        self.leptonName = self.cfg_ana.lepton
        # self.lepton = None
        self.weight = None
        # self.weightFactor = 1.
        self.trigEff = None
        if (self.cfg_comp.isMC or self.cfg_comp.isEmbed) and \
               not ( hasattr(self.cfg_ana,'disable') and self.cfg_ana.disable is True ):
                self.trigEff = TriggerEfficiency()
                self.trigEff.lepEff = getattr( self.trigEff,
                                               self.cfg_ana.effWeight )
                self.trigEff.lepEffMC = None
                if hasattr( self.cfg_ana, 'effWeightMC'):
                    self.trigEff.lepEffMC = getattr( self.trigEff,
                                                     self.cfg_ana.effWeightMC )

            
    def beginLoop(self, setup):
        print self, self.__class__
        super(LeptonWeighter,self).beginLoop(setup)
        self.averages.add('weight', Average('weight') )
        self.averages.add('triggerWeight', Average('triggerWeight') )
        self.averages.add('eff_data', Average('eff_data') )
        self.averages.add('eff_MC', Average('eff_MC') )
        self.averages.add('recEffWeight', Average('recEffWeight') )
        self.averages.add('idWeight', Average('idWeight') )
        self.averages.add('isoWeight', Average('isoWeight') )


    def process(self, event):
        self.readCollections( event.input )
        lep = getattr( event, self.leptonName )
        lep.weight = 1
        lep.triggerWeight = 1
        lep.triggerEffData = 1
        lep.triggerEffMC = 1 
        lep.recEffWeight = 1
        lep.idWeight = 1
        lep.isoWeight = 1

        if (self.cfg_comp.isMC or self.cfg_comp.isEmbed) and \
           not ( hasattr(self.cfg_ana,'disable') and self.cfg_ana.disable is True ) and lep.pt() < 9999.:
            assert( self.trigEff is not None )
            lep.triggerEffData = self.trigEff.lepEff( lep.pt(),
                                                      lep.eta() )
            lep.triggerWeight = lep.triggerEffData

            # JAN: Don't apply MC trigger efficiency for embedded samples
            if not self.cfg_comp.isEmbed and self.trigEff.lepEffMC is not None and \
                   len(self.cfg_comp.triggers)>0:
                lep.triggerEffMC = self.trigEff.lepEffMC( lep.pt(),
                                                          lep.eta() )
                if lep.triggerEffMC>0:
                    lep.triggerWeight /= lep.triggerEffMC
                else:
                    lep.triggerWeight = 1.                    

            if hasattr( self.cfg_ana, 'idWeight'):
                lep.idWeight = self.cfg_ana.idWeight.weight(lep.pt(), abs(lep.eta()) ).weight.value
            # JAN: Do not apply iso weight for embedded sample
            if hasattr( self.cfg_ana, 'isoWeight'):
                if not self.cfg_comp.isEmbed:
                    lep.isoWeight = self.cfg_ana.isoWeight.weight(lep.pt(), abs(lep.eta()) ).weight.value
                else:
                    print 'Not applying isolation weights for embedded samples, to be reconsidered in 2015!'
            
        lep.recEffWeight = lep.idWeight * lep.isoWeight
        lep.weight = lep.triggerWeight * lep.recEffWeight

        # FRANCESCO: Adding a weighter fot the DYsample. As the DYJets do not have the correct trigger
        #            the are reweighted with a CrystalBall
        DYweight = 1.
        if hasattr(self.cfg_ana, 'DYweighter') and self.cfg_ana.DYweighter is True:
            #print '--------HAS ATTR --------'
            #print 'lep.pt()', lep.pt()
            par = [2.07990, 89.9997, 35.8956, 5.11556, 0.968286]
            x = [lep.pt()]
            DYweight = crystalball(x, par)
            #print 'DYweight', DYweight
        #print 'before lep.weight', lep.weight
        #print 'lep.weight*DYweight', lep.weight * DYweight
        lep.weight *= DYweight
        #print 'after lep.weight', lep.weight


        event.eventWeight *= lep.weight
	if not hasattr(event,"triggerWeight"): event.triggerWeight=1.0
        event.triggerWeight *= lep.triggerWeight
        self.averages['weight'].add( lep.weight )
        self.averages['triggerWeight'].add( lep.triggerWeight )
        self.averages['eff_data'].add( lep.triggerEffData )
        self.averages['eff_MC'].add( lep.triggerEffMC )
        self.averages['recEffWeight'].add( lep.recEffWeight )
        self.averages['idWeight'].add( lep.idWeight )
        self.averages['isoWeight'].add( lep.isoWeight )
                
