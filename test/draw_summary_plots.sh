#!/bin/bash
result_dir=${HOME}/data/topEFT/plot/

labels1='cQd1_m1p0 cQd8_p0p4 cQj11_m0p3 cQj18_p0p3 cQj38_m0p8 cQj31_p0p5 cQu1_m1p0 cQu8_p0p4'
labels2='ctd1_p0p6 ctd8_m1p4 ctGIm_p0p5 ctj1_p0p9 ctj8_m1p4 ctu8_p0p3 ctu1_m0p15 ctGRe_m0p4'

labels_2wc='cQd1_p0p4_cQu1_p0p4 cQj11_m0p3_cQj31_m0p3 ctGRe_p0p4_cQu8_p0p4 ctj8_p0p4_cQd8_p0p4 ctu1_m0p3_cQj38_m0p3 ctGRe_p0p4_ctu8_p0p4 ctGRe_m0p3_ctu8_m0p3 ctGRe_p0p4_ctGIm_p0p4 ctd1_p0p4_ctGIm_p0p4 ctd8_m0p3_cQj31_m0p3 ctj8_m0p3_cQj11_m0p3'

# helicity true
outputname=valtest/helT/summary
python script/makeSummaryPlots.py ${result_dir} -l ${labels1} -o ${outputname}1
python script/makeSummaryPlots.py ${result_dir} -l ${labels2} -o ${outputname}2
python script/makeSummaryPlots.py ${result_dir} -l ${labels_2wc} -o ${outputname}_2wc

# helicity false
outputname=valtest/helF/summary
python script/makeSummaryPlots.py ${result_dir} -l ${labels1} -s helF -o ${outputname}1_helF
python script/makeSummaryPlots.py ${result_dir} -l ${labels2} -s helF -o ${outputname}2_helF
python script/makeSummaryPlots.py ${result_dir} -l ${labels_2wc} -s helF -o ${outputname}_2wc_helF
