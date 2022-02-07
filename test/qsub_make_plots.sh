#!/bin/bash
#PBS -o /home/ztao/data/topEFT/plot
#PBS -j oe
#PBS -m abe
#PBS -M ztao@phas.ubc.ca
#PBS -V

export FRONTIER="(http://frontier.triumf.ca:3128/ATLAS_frontier)(proxyurl=http://lcg-adm1.sfu.computecanada.ca:3128)(proxyurl=http://lcg-adm2.sfu.computecanada.ca:3128)(proxyurl=http://lcg-adm3.sfu.computecanada.ca:3128)"

# set up environment
echo HOSTNAME=$HOSTNAME
source /home/ztao/topEFT/ttbarEFTSampleValidation/setup_env.sh
echo "SourceDIR = $SourceDIR"
echo "PWD = $PWD"
cd ${SourceDIR}

outdir=/home/ztao/data/topEFT/plot

label_sa=ctGRe_m0p4
sample_sa=/home/ztao/data/topEFT/test_sample/DAOD_TRUTH1.ttbar_SMEFTsim_100k_ctGRe_m0p4_SA.root

source test/make_plots.sh ${label_sa} ${sample_sa} ${outdir}/${label_sa}
