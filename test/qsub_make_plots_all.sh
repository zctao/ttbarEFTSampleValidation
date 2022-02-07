#!/bin/bash
#PBS -t 0-26%10
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

#labels and samples
# A hash table for sample file paths
declare -A samples_standalone
# Also an array of labels to ensure the same order for job resubmission
labels_standalone=()

# 0
labels_standalone+=("cQd1_m1p0")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_cQd1_m1p0_100K.root"
# 1
labels_standalone+=("cQd8_p0p4")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_cQd8_p0p4_100K.root"
# 2
labels_standalone+=("cQj11_m0p3")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_cQj11_m0p3_100K.root"
# 3
labels_standalone+=("cQj18_p0p3")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_cQj18_p0p3_100K.root"
# 4
labels_standalone+=("cQj38_m0p8")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_cQj38_m0p8_100K.root"
# 5
labels_standalone+=("cQj31_p0p5")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_cQj31_p0p5_100K.root"
# 6
labels_standalone+=("cQu1_m1p0")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_cQu1_m1p0_100K.root"
# 7
labels_standalone+=("cQu8_p0p4")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_cQu8_p0p4_100K.root"
# 8
labels_standalone+=("ctd1_p0p6")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_ctd1_p0p6_100K.root"
# 9
labels_standalone+=("ctd8_m1p4")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_ctd8_m1p4_100K.root"
# 10
labels_standalone+=("ctGIm_p0p5")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_ctGIm_p0p5_100K.root"
# 11
labels_standalone+=("ctj1_p0p9")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_ctj1_p0p9_100K.root"
# 12
labels_standalone+=("ctj8_m1p4")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_ctj8_m1p4_100K.root"
# 13
labels_standalone+=("ctu8_p0p3")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_ctu8_p0p3_100K.root"
# 14
labels_standalone+=("ctu1_m0p15")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SA_ctu1_m0p15_100K.root"
# 15
labels_standalone+=("ctGRe_m0p4")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SMEFTsim_100k_ctGRe_m0p4_SA.root"
# Two WCs
# 16
labels_standalone+=("cQd1_p0p4_cQu1_p0p4")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SMEFTsim_100k_cQd1_cQu1_p0p4.root"
# 17
labels_standalone+=("cQj11_m0p3_cQj31_m0p3")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SMEFTsim_100k_cQj11_cQj31_m0p3.root"
# 18
labels_standalone+=("ctGRe_p0p4_cQu8_p0p4")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SMEFTsim_100k_ctGRe_cQu8_p0p4_SA.root"
# 19
labels_standalone+=("ctj8_p0p4_cQd8_p0p4")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SMEFTsim_100k_ctj8_cQd8_p0p4.root"
# 20
labels_standalone+=("ctu1_m0p3_cQj38_m0p3")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/NC/DAOD_TRUTH1.ttbar_SMEFTsim_100k_ctu1_cQj38_m0p3.root"
#
# 21
labels_standalone+=("ctGRe_p0p4_ctu8_p0p4")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/20211205/ctGRe_p0p4_ctu8_p0p4/DAOD_TRUTH1.ttbar_SA_ctGRe_p0p4_ctu8_p0p4_100k.root"
# 22
labels_standalone+=("ctGRe_m0p3_ctu8_m0p3")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/latest/ctGRe_m0p3_ctu8_m0p3/Reco/DAOD_TRUTH1.ttbar_ctGRe_m0p3_ctu8_m0p3_100k.root"
# 23
labels_standalone+=("ctGRe_p0p4_ctGIm_p0p4")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/latest/ctGRe_p0p4_ctGIm_p0p4/Reco/DAOD_TRUTH1.ttbar_ctGRe_p0p4_ctGIm_p0p4_100k.root"
# 24
labels_standalone+=("ctd1_p0p4_ctGIm_p0p4")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/latest/ctd1_p0p4_ctGIm_p0p4/Reco/DAOD_TRUTH1.ttbar_ctd1_p0p4_ctGIm_p0p4_100k.root"
# 25
labels_standalone+=("ctd8_m0p3_cQj31_m0p3")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/latest/ctd8_m0p3_cQj31_m0p3/Reco/DAOD_TRUTH1.ttbar_ctd8_m0p3_cQj31_m0p3_100k.root"
# 26
labels_standalone+=("ctj8_m0p3_cQj11_m0p3")
samples_standalone[${labels_standalone[-1]}]="${HOME}/data/topEFT/output/latest/ctj8_m0p3_cQj11_m0p3/Reco/DAOD_TRUTH1.ttbar_ctj8_m0p3_cQj11_m0p3_100k.root"

# check if all files exist
#for label in ${!samples_standalone[@]}; do
#    sample=${samples_standalone[${label}]}
#    if [[ ! -f "$sample" ]]; then
#        echo "Error: cannot find the sample for label ${label}: ${sample}"
#    fi
#done
#echo "Total number of samples: ${#samples_standalone[@]}"
#return

label_sa=${labels_standalone[${PBS_ARRAYID}]}
echo label=${label_sa}

sample_sa=${samples_standalone[${label_sa}]}

if [[ -f "${sample_sa}" ]]; then
    echo sample=${sample_sa}
else
    echo "Error: cannot find the sample for label ${label_sa}: ${sample_sa}"
    return 1
fi

echo "Making plots..."
source test/make_plots.sh ${label_sa} ${sample_sa} ${outdir}/${label_sa}

