#!/usr/bin/env python3
import os
import shutil
from datetime import datetime

from writeJO import writeJO_rw, writeJO_sa

pbs_header = """
#PBS -o {outdir}
#PBS -j oe
#PBS -m abe
#PBS -M {email}
#PBS -l nodes=1

export FRONTIER="(http://frontier.triumf.ca:3128/ATLAS_frontier)(proxyurl=http://lcg-adm1.sfu.computecanada.ca:3128)(proxyurl=http://lcg-adm2.sfu.computecanada.ca:3128)(proxyurl=http://lcg-adm3.sfu.computecanada.ca:3128)"
"""

slurm_header = """
#SBATCH -o {outdir}/slurm-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user={email}
#SBATCH --export=NONE
"""

setup_env = """
echo HOSTNAME=$HOSTNAME
"""

run_prod = """
source {srcdir}/setup_gen.sh

# output directory
outputDIR={outdir}/Gen
mkdir -p $outputDIR
echo outputDIR=$outputDIR

# run directory
workDIR=$outputDIR/run
mkdir -p $workDIR
echo workDIR=$workDIR
cd $workDIR
echo PWD=$PWD

# Random number generator seed
#rngseed=$(date +"%N")
rngseed={rng_seed}
echo "randomSeed=$rngseed"

jobOption={joboption}
echo "Run sample production using JobOption $jobOption"

Gen_tf.py --ecmEnergy=13000. --maxEvents={maxevents} --randomSeed=$rngseed --jobConfig $jobOption --outputEVNTFile $outputDIR/{filename_gen}
"""

run_deriv = """
source {srcdir}/setup_reco.sh

inputFile={outdir}/Gen/{filename_gen}
echo inputFile=$inputFile

outputDIR={outdir}/Reco
mkdir -p $outputDIR
echo outputDIR=$outputDIR

outputFile={filename_reco}

# run directory
workDIR=$outputDIR/run
mkdir -p $workDIR
echo workDIR=$workDIR
cd $workDIR
echo PWD=$PWD

echo "Run derivation"

Reco_tf.py --inputEVNTFile $inputFile --outputDAODFile $outputFile  --reductionConf TRUTH1

mv *.root $outputDIR/.
"""

clean_up = """
if [ $? -ne 0 ]; then
    exit $?
fi
"""

def writeJobScripts(params_d, batch_system=None):
    header = "#!/bin/bash"
    if batch_system == "pbs":
        header += pbs_header
    elif batch_system == "slurm":
        header += slurm_header

    # generation
    jobscripts_prod = header + setup_env + run_prod
    jobscripts_prod = jobscripts_prod.format(**params_d)

    # write the script to file
    fname_prod = os.path.join(params_d['outdir'], "run_prod.sh")
    with open(fname_prod, 'w') as f_prod:
        f_prod.write(jobscripts_prod)

    # derivation
    jobscripts_deriv = header + setup_env + run_deriv
    jobscripts_deriv = jobscripts_deriv.format(**params_d)

    # write the script to file
    fname_deriv = os.path.join(params_d['outdir'], "run_deriv.sh")
    with open(fname_deriv, 'w') as f_deriv:
        f_deriv.write(jobscripts_deriv)

def createJobs_rw(args):
    #label
    label = 'reweight'

    # output directory
    outputdir = os.path.join(args.outdir, label)
    if not os.path.isdir(outputdir):
        print(f"Create output directory {outputdir}")
        os.makedirs(outputdir)

    # job config
    jodir = os.path.join(outputdir, 'jobOption')
    if not os.path.isdir(jodir):
        print(f"Create job option directory {jodir}")
        os.makedirs(jodir)

    # write job options
    writeJO_rw(args.template_control, args.template_jo, jodir)

    # file names
    filename = f"ttbar_SMEFTsim_rw"
    filename_gen = filename+".EVNT.root"
    filename_reco = filename+".root"

    # for the job script
    params_dict = {
        'srcdir': args.srcdir,
        'email': args.email,
        'maxevents': args.max_events,
        'outdir': outputdir,
        'joboption': jodir,
        'filename_gen': filename_gen,
        'filename_reco': filename_reco,
        'rng_seed': datetime.now().strftime("%f")
    }

    writeJobScripts(params_dict, batch_system=args.batch_system)

def createJobs_sa(args):

    # label
    assert(len(args.coefficients)==len(args.values))
    label = ''
    for c, v in zip(args.coefficients, args.values):
        label += c+'_'
        label += 'p' if v > 0 else 'm'
        label += str(abs(v)).replace('.','p')+'_'
    label = label.rstrip('_')

    # output directory
    outputdir = os.path.join(args.outdir, label)
    if not os.path.isdir(outputdir):
        print(f"Create output directory {outputdir}")
        os.makedirs(outputdir)

    # job config
    jodir = os.path.join(outputdir, 'jobOption')
    if not os.path.isdir(jodir):
        print(f"Create job option directory {jodir}")
        os.makedirs(jodir)

    jofname = os.path.basename(args.template).replace(".py", f"_{label}.py")
    jofname = os.path.join(jodir, jofname)

    # write job option
    writeJO_sa(args.template, args.coefficients, args.values, jofname)

    # file names
    filename = f"ttbar_SMEFTsim_{label}"
    filename_gen = filename+".EVNT.root"
    filename_reco = filename+".root"

    # for the job script
    params_dict = {
        'srcdir': args.srcdir,
        'email': args.email,
        'maxevents': args.max_events,
        'outdir': outputdir,
        'joboption': jodir,
        'filename_gen': filename_gen,
        'filename_reco': filename_reco,
        'rng_seed': datetime.now().strftime("%f")
    }

    writeJobScripts(params_dict, batch_system=args.batch_system)

    # chain the two steps together
    #fname_chain = os.path.join(outputdir, 'submit_chain.sh')
    #with open(fname_chain, 'w') as f_chain:
    #    f_chain.write("#!/bin/bash\n")
    #    f_chain.write(f"JOBPROD=$(qsub $@ {fname_prod})\n")
    #    f_chain.write(f"echo $JOBPROD\n")
    #    f_chain.write(f"qsub -W depend=afterok:$JOBPROD $@ {fname_deriv}")

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # parser for generating reweighted sample
    parser_rw = subparsers.add_parser('rw', help="Generate reweighted sample")
    parser_rw.add_argument("-j", "--template-jo", type=str,
                            default="template/mc_13TeV.MGPy8_ttbar_SMEFTsim_reweighted_nonallhad.py.tmpl",
                            help="Job option template for generating reweighted sample")
    parser_rw.add_argument("-t", "--template-control", type=str,
                            default="template/Control_SMEFTsim_topU3lMw_ttbar_reweighted.py.tmpl",
                            help="Control file template for generating reweighted sample")
    parser_rw.set_defaults(func=createJobs_rw)

    # parser for generating standalone sample
    parser_sa = subparsers.add_parser('sa', help="Generate standalone sample")
    parser_sa.add_argument("-c", "--coefficients", nargs='+', type=str,
                            help="List of Wilson coefficient names")
    parser_sa.add_argument("-v", "--values", nargs='+', type=float,
                            help="Values of the Wilson coefficients")
    parser_sa.add_argument("-t","--template", type=str,
                            default="template/mc_13TeV.MGPy8_ttbar_SMEFTsim_topU3lMw_StandAlone_nonallhad.py.tmpl",
                            help="Template job option file for generating standalone sample")
    parser_sa.set_defaults(func=createJobs_sa)

    # common arguments
    parser.add_argument("-m", "--max-events", type=int, default=100000,
                        help="Max number of events to generate")
    parser.add_argument("-o", "--outdir", type=str, required=True,
                        help="Job output directory")
    parser.add_argument("-s", "--srcdir", type=str,
                        default="os.getenv('SourceDIR')",
                        help="Source directory")
    parser.add_argument("-e", "--email", type=str,
                        default="os.getenv('USER')+'@phas.ubc.ca'")
    parser.add_argument("-b", "--batch-system", choices=['pbs', 'slurm'])

    args = parser.parse_args()

    # check source directory
    srcdir = eval(args.srcdir)
    if srcdir is None or not os.path.isdir(srcdir):
        sys.exit("Soruce directory not set. Abort.")
    else:
        args.srcdir = srcdir

    # get the absolute path of the output directory
    args.outdir = os.path.abspath(args.outdir)

    # email
    args.email = eval(args.email)

    # call the selected function
    args.func(args)
