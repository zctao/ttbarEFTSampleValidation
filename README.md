# ttbarEFTSampleValidation
## Set up environment

    source setup_env.sh
  
## To produce samples

Generate job files for reweight sample:

    python script/createJobs.py -o <output_directory> rw

Generate job files for standalone samples:

    python script/createJobs.py -o <output_directory> sa -c <list of Wilson coefficients> -v <list of values for the WCs>

See examples in

    test/run_production_example.sh

To run sample productions on a cluster, add ```-b slurm``` if for Slurm or ```-b pbs``` if for PBS to ```script/createJobs.py```.

To submit the production job:

    sbatch --time=<hh:mm:ss> <output_directory>/run_prod.sh

or

    qsub -l walltime=<hh:mm:ss> <output_directory>/run_prod.sh

To submit the derivation job after the sample production is done:

    sbatch --time=<hh:mm:ss> <output_directory>/run_deriv.sh
  
or

    qsub -l walltime=<hh:mm:ss> <output_directory>/run_deriv.sh

## To make comparison plot

    python script/compareSamples.py -i <filepath to the reweight sample> <filepath to the standalone sample> -n <label> -o <output_name>
