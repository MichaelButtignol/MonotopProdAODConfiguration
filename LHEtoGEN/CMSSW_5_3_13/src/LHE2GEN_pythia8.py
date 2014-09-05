import FWCore.ParameterSet.Config as cms

process = cms.Process('GEN')


# import general service
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.EventContent.EventContent_cff')


# import standard sequences
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration/StandardSequences/Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')


# Number of events
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))


# Summary veto
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )


# LHE input file
process.source = cms.Source("LHESource",
        fileNames = cms.untracked.vstring('file:../../../../../Prod_LHE/Prod_S1/prod_S1_mres1000p0_mchi825p0_100/prod_S1_mres1000p0_mchi825p0_100.lhe')
	)


# Other statements
process.GlobalTag.globaltag = 'START53_V29::All'


# Generation
#from Configuration.Generator.PythiaUEZ2Settings_cfi import *

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    SLHAFileForPythia8 = cms.string('Monotop_config.slha'),   # Makes pythia8 understand that it has to use the QNumbers 
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(8000.),
    PythiaParameters = cms.PSet(
        processParameters = cms.vstring(
        'Tune:pp 5',                         # Tune 4C
        'Tune:ee 3',                         # Tune 4C
        'Main:timesAllowErrors    = 10000', 
        'Main:showAllSettings = on',         # print all flags/modes/parameters
        'Main:showAllParticleData = on',     # print all particle and decay data

        #'Init:showChangedSettings = on',      # list changed settings
        #'Init:showChangedParticleData = on',  # list changed particle data
        #'Init:showChangedResonanceData = on', # also print changed resonance data
        'ExtraDimensionsG*:all = off',
        'PartonLevel:MPI = on',
        'HadronLevel:Hadronize = on',
        'PartonLevel:ISR = on',
        'PartonLevel:FSR = on',
        'ParticleDecays:limitTau0 = on',
        'ParticleDecays:tauMax = 10'
        ),
        parameterSets = cms.vstring('processParameters')
    )
)



# Output definition
process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string('prod_S1_mres1000p0_mchi825p0_100_GEN.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-RAW')
    ),
    SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('generation_step') )                                        
)


# Path and EndPath definitions
process.generation_step       = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step       = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)


# Schedule definition
process.schedule = cms.Schedule(process.generation_step,
              		        process.genfiltersummary_step)
process.schedule.extend([process.endjob_step,process.RAWSIMoutput_step])


# special treatment in case of production filter sequence
for path in process.paths:
    getattr(process,path)._seq = process.generator*getattr(process,path)._seq

