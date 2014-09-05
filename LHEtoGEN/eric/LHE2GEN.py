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
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(2))


# Summary veto
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )


# LHE input file
process.source = cms.Source("LHESource", fileNames = cms.untracked.vstring(
	#"/../econte/FCNC/WZjets/WZjets_matchup2_1_unweighted_events.lhe",
	"file:../../Configuration/Test/prod_S1_mres1000p0_mchi825p0.lhe",
	))


# Other statements
process.GlobalTag.globaltag = 'START53_V29::All'


# Generation
from Configuration.Generator.PythiaUEZ2Settings_cfi import *
process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(8000.0),
    maxEventsToPrint = cms.untracked.int32(0),
    UseExternalGenerators = cms.untracked.bool(True),
    PythiaParameters = cms.PSet(
	pythiaUESettingsBlock,
        processParameters = cms.vstring(
	    'MSEL=0          ! User defined processes', 
            'MSTJ(1)=1       ! Fragmentation/hadronization on or off',
            'MSTP(61)=1      ! Parton showering on or off',
	    'MSTP(71)=1      !',
            'MSTP(7)=6       ! flavour = top', 
            'PMAS(6,1)=172.  ! top quark mass'),
        parameterSets = cms.vstring('pythiaUESettings','processParameters')
    ),
    jetMatching = cms.untracked.PSet(
        scheme          = cms.string("Madgraph"),
        mode            = cms.string("auto"),
        MEMAIN_etaclmax = cms.double(5.0),
        MEMAIN_qcut     = cms.double(0),
        MEMAIN_minjets  = cms.int32(0),
        MEMAIN_maxjets  = cms.int32(3),
        MEMAIN_showerkt = cms.double(0),
        MEMAIN_nqmatch  = cms.int32(5),
        MEMAIN_excres   = cms.string(""),        
        outTree_flag    = cms.int32(0) 
      )
)


# Output definition
process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string('GEN.root'),
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


