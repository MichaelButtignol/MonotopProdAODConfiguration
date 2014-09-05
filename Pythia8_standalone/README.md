To change the version of pythia8 (local)  CMSSW will use, you have to: 

        - install a release of CMSSW (outside pythia8 repository) which is compatible with the version of pythia you want to use. Typically, CMSSW_5_3_X (slc5_amd64_gcc462) works pretty fine under pythia8153. To use pythia8170 or pythia8175 you may need to install CMSSW_5_3_13 (slc6_amd64_gcc462) or higher. Then, to use pythia8186, you need to switch to CMSSW_6_X_Y or even CMSSW_7_X_Y (I do not really know actually).
        - move to 'CMSSW_X_Y_Z/src/'
        - edit a 'pythia8.xml' file with: (you also can dl the template here: '/opt/exp_soft/cms/slc5_amd64_gcc462/cms/cmssw/CMSSW_5_3_11/config/toolbox/slc5_amd64_gcc462/tools/selected/pythia8.xml')

(example adapted to pythia8153)
#############################################
<tool name="pythia8" version="153-michael">
  <lib name="pythia8"/>
  <lib name="hepmcinterface"/>
  <client>
    <environment name="PYTHIA8_BASE" default="/opt/sbg/data/data1/cms/mbuttign/THESE/Monotop/Prod/Prod_AOD/pythia8153"/>
    <environment name="LIBDIR" default="$PYTHIA8_BASE/lib"/>
    <environment name="INCLUDE" default="$PYTHIA8_BASE/include"/>
  </client>
  <runtime name="PYTHIA8DATA" value="$PYTHIA8_BASE/xmldoc"/>
  <use name="cxxcompiler"/>
  <use name="hepmc"/>
  <use name="pythia6"/>
  <use name="clhep"/>
  <use name="lhapdf"/>
</tool>
#############################################
       
        - you may need to enable shared libraries: scram setup enable-shared 
        - compile with: scram setup pythia8.xml
        - check that the right pythia8 is linked: echo $PYTHIA8DATA
        - edit a 'init.sh' file with:

############################################
export LD_LIBRARY_PATH=/'absolute path to your pythia8'/pythia8153/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/'absolute path to your pythia8'/pythia8153/lib:$LIBRARY_PATH
export CMSSW_SEARCH_PATH=/'absolute path to your pythia8'/pythia8153/lib:$CMSSW_SEARCH_PATH
export CMSSW_FWLITE_INCLUDE_PATH=/'absolute path to your pythia8'/pythia8153/include:$CMSSW_FWLITE_INCLUDE_PATH
export CMSSW_FWLITE_INCLUDE_PATH=/'absolute path to your pythia8'/pythia8153/include/Pythia8:$CMSSW_FWLITE_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=/'absolute path to your pythia8'/pythia8153/include:$CPLUSLUDE_PATH
export CPLUS_INCLUDE_PATH=/'absolute path to your pythia8'/pythia8153/include/Pythia8:$CPLUSLUDE_PATH
############################################

        - run your file: source init.sh
        - clean your area: scram b clean 
        - compile your area: scram b
        - check the 'libPythia8.so' is well linked: ldd ../lib/slc5_amd64_gcc462/pluginGeneratorInterfacePythia8Interface.so
        - add the package needed to make your local version of pythia8 understand the instructions of CMSSW: 'git cms-addpkg GeneratorInterface/Pythia8Interface'
        - READY to use pythia8!! Use 'cmsRun myGENconfig.py' ... 

##########################################
#                                        #
#                                        #
#####  ENJOY THE BEUGS OF PYTHIA8 :D #####
#                                        #
#                                        #
##########################################
