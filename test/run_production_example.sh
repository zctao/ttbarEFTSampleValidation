outdir=$HOME/data/topEFT/output/latest

# Reweight sample
python script/createJobs.py -o $outdir rw

# Standalone samples
# One WC
python script/createJobs.py -o $outdir sa -c ctGRe -v 0.5

# Two WCs
python script/createJobs.py -o $outdir sa -c ctGRe ctu8 -v -0.3 -0.3
python script/createJobs.py -o $outdir sa -c ctd8 cQj31 -v -0.3 -0.3
python script/createJobs.py -o $outdir sa -c ctGRe ctGIm -v 0.4 0.4
python script/createJobs.py -o $outdir sa -c ctj8 cQj11 -v -0.3 -0.3
python script/createJobs.py -o $outdir sa -c ctd1 ctGIm -v 0.4 0.4
