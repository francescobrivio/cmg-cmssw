import operator

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

import PhysicsTools.HeppyCore.framework.config as cfg

'''class TriggerInfo(object):
    def __init__(self, name, index, fired=True):
        self.name = name
        self.index = index
        self.fired = fired
        self.objects = []
        self.objIds = set()

    def __str__(self):
        return 'TriggerInfo: name={name}, fired={fired}, n_objects={n_o}'.format(
            name=self.name, fired=self.fired, n_o=len(self.objects))'''

class TriggerEfficienciesAnalyzer(Analyzer):

    def declareHandles(self):
        super(TriggerEfficienciesAnalyzer, self).declareHandles()

        self.handles['triggerResultsHLT'] = AutoHandle(
            ('TriggerResults', '', 'HLT'),
            'edm::TriggerResults'
            )

        self.handles['triggerObjects'] =  AutoHandle(
            'selectedPatTrigger',
            'std::vector<pat::TriggerObjectStandAlone>'
            )

    # Loop on the events
    def beginLoop(self, setup):
        super(TriggerEfficienciesAnalyzer,self).beginLoop(setup)

        self.triggerList = self.cfg_comp.triggers

        # Counters definition        
        self.counters.addCounter('TriggerEff')
        self.counters.counter('TriggerEff').register('All events')
        self.counters.counter('TriggerEff').register('trigger passed')
        self.counters.counter('TriggerEff').register('Passed Single_Muon trigger')
        self.counters.counter('TriggerEff').register('Passed MuTau trigger')

    def process(self, event):
        self.readCollections(event.input)

        # Adding new configurable points to the analyzer
        # the two triggers are defined in order to calculate efficiency,
        # the common_trigger is used for the denominator (e.g. singleMu trigger),
        # the specific_trigger is used for the numerator (e.g. MuTau trigger)
        self.cfg_ana.common_trigger
        self.cfg_ana.specific_trigger
        #self.cfg_ana.addTriggerObjects

        # Begining of the trigMatching scheme
        triggerBits = self.handles['triggerResultsHLT'].product()
        names = event.input.object().triggerNames(triggerBits)

        self.counters.counter('TriggerEff').inc('All events')

        singleMu_passed = False
	tauMu_passed = False
        trigger_passed = False
	#import pdb; pdb.set_trace()
        #trigger_infos = []
        for trigger_name in self.triggerList:
            index = names.triggerIndex(trigger_name)
            if index == len(triggerBits):
                continue
            fired = triggerBits.accept(index)

            #trigger_infos.append(TriggerInfo(trigger_name, index, fired))

            if fired:
                trigger_passed = True


	for i in event.trigger_infos:
           #print 'i name: ', i.name
           #print 'common trigger: ', self.cfg_ana.common_trigger
           if i.name == self.cfg_ana.common_trigger:
              #print 'different names'
              #singleMu_passed = False
           #else :
              #print 'name is the same'
              if i.fired:
                  #print 'is also fired'
                  singleMu_passed = True
           else:
		#import pdb; pdb.set_trace()
                print 'i name: ', i.name

	for j in event.trigger_infos:
           if j.name is self.cfg_ana.specific_trigger:
              if j.fired:
                  tauMu_passed = True

        '''if self.cfg_ana.addTriggerObjects:
            triggerObjects = self.handles['triggerObjects'].product()
            for to in triggerObjects:
                to.unpackPathNames(names)
                for info in trigger_infos:
                    if to.hasPathName(info.name, True):
                        info.objects.append(to)
                        info.objIds.add(abs(to.pdgId()))

        event.trigger_infos = trigger_infos'''

	#import pdb; pdb.set_trace()

        if not trigger_passed:
           return False

        self.counters.counter('TriggerEff').inc('trigger passed')

        if not singleMu_passed:
           return False

        self.counters.counter('TriggerEff').inc('Passed Single_Muon trigger')

        if not tauMu_passed:
           return False

        self.counters.counter('TriggerEff').inc('Passed MuTau trigger')

        #import pdb; pdb.set_trace()

        # e se li passa mettere delle flag (event.example_flag = True)

        return True

'''setattr(TriggerEfficienciesAnalyzer, 'defaultConfig', 
    cfg.Analyzer(
        class_object=TriggerEfficienciesAnalyzer,
        requireTrigger=True,
        usePrescaled=False,
        addTriggerObjects=True,
        # vetoTriggers=[],
    )
)'''

