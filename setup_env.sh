#!/bin/bash
lcgVersion=${1:-LCG_101}

arch=x86_64-centos7-gcc8-opt

if command -v lsetup &> /dev/null
then
    lsetup "views $lcgVersion $arch"
else
    source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh ${lcgVersion} ${arch}
fi

export SourceDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export PYTHONPATH=$SourceDIR/python:$SourceDIR/script:$SourceDIR:$PYTHONPATH
