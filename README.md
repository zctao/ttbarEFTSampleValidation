# ttbarEFTSampleValidation
## Set up environment

    source setup_env.sh
  
## Generate job files

    python script/createJobs.py -o <output_directory> -c <list of Wilson coefficients> -v <list of values for the WCs>

Also see an example script in

    test/run_production_2wc.sh
