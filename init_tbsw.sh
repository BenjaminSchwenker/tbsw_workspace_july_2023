#!/bin/bash
#tbsw commit SHA-1: 8d02ba535314c7e2a2fe60339a04666783a72000 
#--------------------------------------------------------------------------------
#    ROOT                                                                        
#--------------------------------------------------------------------------------
export ROOTSYS=/home/benjamin/root_install
export PATH=/home/benjamin/root_install/bin:$PATH
export LD_LIBRARY_PATH=/home/benjamin/root_install/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/benjamin/root_install/lib:/home/benjamin/tbsw/source:$PYTHONPATH
export ROOT_INCLUDE_PATH=/home/benjamin/tbsw/build

#--------------------------------------------------------------------------------
#    TBSW                                                                        
#--------------------------------------------------------------------------------
export PATH=/home/benjamin/tbsw/build/bin:$PATH
export LD_LIBRARY_PATH=/home/benjamin/tbsw/build/lib:$LD_LIBRARY_PATH
export MARLIN_DLL=/home/benjamin/tbsw/build/lib/libTBReco.so:/home/benjamin/tbsw/build/lib/libEudaqInput.so:
export MARLIN=/home/benjamin/tbsw/build

