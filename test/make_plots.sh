#!/bin/bash
label_sa=${1}
sample_sa=${2}
output_dir=${3:-valout}

# reweight sample
sample_rw=/home/ztao/data/topEFT/test_sample/DAOD_TRUTH1.ttbarEFT_full_default_rw_100K.root
sample_rw_helF=/home/ztao/data/topEFT/test_sample/DAOD_TRUTH1.ttbarEFT_full_default_rw_helF_100K.root

# standalone sample
echo "label: ${label_sa}"

# check if file exists
if [ ! -f ${sample_sa} ]; then
    echo "${sample_sa} does not exist"
    return 1
else
    echo "Standalone sample: ${sample_sa}"
fi

echo "Reweight sample: ${sample_rw}"
python script/compareSamples.py -i ${sample_rw} ${sample_sa} -n ${label_sa} -o ${output_dir}

echo "Reweight sample: ${sample_rw_helF}"
python script/compareSamples.py -i ${sample_rw_helF} ${sample_sa} -n ${label_sa} -o ${output_dir}_helF
