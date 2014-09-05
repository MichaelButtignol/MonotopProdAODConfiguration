#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms

process = cms.Process("GEN")

process.source = cms.Source("MCFileSource",
    fileNames = cms.untracked.vstring('file:../../../ProductionToHepMC/prod_S4_mchi200p0_2/prod_0.hepmc')
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))


process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'

process.GEN = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('file:prod_S4_mchi200p0_2_HepMC.root')
)

process.outpath = cms.EndPath(process.GEN)
