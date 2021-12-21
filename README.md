# ttbarEFTSampleValidation
## Set up environment

    source setup_env.sh
  
## To produce samples

Generate job files:

    python script/createJobs.py -o <output_directory> -c <list of Wilson coefficients> -v <list of values for the WCs>

Also see an example script in

    test/run_production_2wc.sh
    
Submit jobs:

    source <output_directory>/submit_chain.sh [qsub options]
    
Or submit the generation and derivation steps separately:

    qsub [options] <output_directory>/submit_prod.sh
 
  and after it's done, then

    qsub [options] <output_directory>/submit_deriv.sh
