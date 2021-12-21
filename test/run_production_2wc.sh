outdir=$HOME/data/topEFT/output/latest

python script/createJobs.py -o $outdir -c ctGRe ctu8 -v -0.3 -0.3
python script/createJobs.py -o $outdir -c ctd8 cQj31 -v -0.3 -0.3
python script/createJobs.py -o $outdir -c ctGRe ctGIm -v 0.4 0.4
python script/createJobs.py -o $outdir -c ctj8 cQj11 -v -0.3 -0.3
python script/createJobs.py -o $outdir -c ctd1 ctGIm -v 0.4 0.4
