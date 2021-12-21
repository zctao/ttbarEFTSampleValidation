#!/usr/bin/env python3
import os
import sys

from modifyJO import modifyJO

pbs_header = """#!/bin/bash
#PBS -o {outdir}
#PBS -j oe
#PBS -m abe
#PBS -M {email}
#PBS -l nodes=1
#PBS -V
"""

setup_env = """
export FRONTIER="(http://frontier.triumf.ca:3128/ATLAS_frontier)(proxyurl=http://lcg-adm1.sfu.computecanada.ca:3128)(proxyurl=http://lcg-adm2.sfu.computecanada.ca:3128)(proxyurl=http://lcg-adm3.sfu.computecanada.ca:3128)"

echo HOSTNAME=$HOSTNAME

workDIR=/tmp/$USER/{label}/run
mkdir -p $workDIR
cd $workDIR
echo workDIR=$workDIR
echo PWD=$PWD
"""

run_prod = """
source {srcdir}/setup_gen.sh

outputDIR={outdir}/Gen
mkdir -p $outputDIR
echo outputDIR=$outputDIR

rngseed=$(date +"%N")
echo "randomSeed=$rngseed"

jobOption={joboption}
echo "Run sample production using JobOption $jobOption"

Gen_tf.py --ecmEnergy=13000. --firstEvent=1 --maxEvents=100000 --randomSeed=$rngseed --jobConfig $jobOption --outputEVNTFile $outputDIR/ttbar_SA_{label}_100k.EVNT.root
"""

run_deriv = """
source {srcdir}/setup_reco.sh

inputDIR={outdir}/Gen
echo inputDIR=$inputDIR

outputDIR={outdir}/Reco
mkdir -p $outputDIR
echo outputDIR=$outputDIR

echo "Run derivation"

Reco_tf.py --inputEVNTFile $inputDIR/ttbar_SA_{label}_100k.EVNT.root --outputDAODFile ttbar_{label}_100k.root --reductionConf TRUTH1
mv DAOD_TRUTH1.ttbar_{label}_100k.root $outputDIR/.
"""

clean_up = """
echo "Move working directory to output"
# TODO: zip?
mv $workDIR $outputDIR/.

if [ $? -ne 0 ]; then
    exit $?
fi
"""

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--coefficients", nargs='+', type=str,
                        help="List of Wilson coefficient names")
    parser.add_argument("-v", "--values", nargs='+', type=float,
                        help="Values of the Wilson coefficients")
    parser.add_argument("-t","--template-file", type=str,
                        default="template/mc_13TeV.MGPy8_tt_SMEFTsim_topmW_topX_StandAlone.py",
                        help="Path to the template job option file")
    parser.add_argument("-o", "--outdir", type=str,
                        help="Job output directory")
    parser.add_argument("-e", "--email", type=str,
                        default="os.getenv('USER')+'@phas.ubc.ca'")

    args = parser.parse_args()

    # source directory
    srcdir = os.getenv('SourceDIR')
    if srcdir is None:
        sys.exit("SoruceDIR not set. Abort.")

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

    jofname = os.path.basename(args.template_file).replace(".py", f"_{label}.py")
    jofname = os.path.join(jodir, jofname)

    modifyJO(args.template_file, args.coefficients, args.values, jofname)

    # write batch job scripts
    params_dict = {
        'outdir': outputdir,
        'email': eval(args.email),
        'srcdir': srcdir,
        'joboption': jodir,
        'label': label,
    }

    # sample production
    jobscripts_prod = pbs_header + setup_env + run_prod + clean_up
    jobscripts_prod = jobscripts_prod.format(**params_dict)

    # write to outputdir
    fname_prod = os.path.join(outputdir, 'submit_prod.sh')
    with open(fname_prod, 'w') as f_prod:
        f_prod.write(jobscripts_prod)

    # derivation
    jobscripts_deriv = pbs_header + setup_env + run_deriv + clean_up
    jobscripts_deriv = jobscripts_deriv.format(**params_dict)

    # write to outputdir
    fname_deriv = os.path.join(outputdir, 'submit_deriv.sh')
    with open(fname_deriv, 'w') as f_deriv:
        f_deriv.write(jobscripts_deriv)

    # chain the two steps together
    fname_chain = os.path.join(outputdir, 'submit_chain.sh')
    with open(fname_chain, 'w') as f_chain:
        f_chain.write("#!/bin/bash\n")
        f_chain.write(f"JOBPROD=$(qsub $@ {fname_prod})\n")
        f_chain.write(f"echo $JOBPROD\n")
        f_chain.write(f"qsub -W depend=afterok:$JOBPROD $@ {fname_deriv}")
