from MadGraphControl.MadGraphUtils import *
from MCJobOptionUtils.JOsupport import get_physics_short

# TO USE THIS CONTROL FILE:
# - create a separate JO for your process, e.g. mc.MGPy8_ttll_SMEFTsim_reweighted.py
# - declare "selected_operators", a list of SMEFTsim operators that is a subset of the keys of the "eft_dict" below
# - declare "process_definition", a string that will be appended to "process" below and MUST contain at least the relevant MG generate command
# - declare "fixed_scale", a float to fix muR=muF (because MG doesn't run the WCs). Recommended: = sum(masses)_{final state particles}
# - declare "gridpack", a bool indicating whether generation (and possibly reweighting) is to be run from a gridpack
# - declare "evgenConfig.description", a sufficiently descriptive string for the sample metadata,
#                                      e.g. 'SMEFTsim 3.0 tt+ll, top model, inclusive, reweighted, EFT vertices, no propagator correction'
# - include this file, using the appropriate relative path

# general parameters
nevents     = runArgs.maxEvents if runArgs.maxEvents>0 else evgenConfig.nEventsPerJob
nevents    *= 1.1 # safety factor
mllcut      = 5
lhe_version = 3

fixed_scale = 345. # ~ m(top)+m(top)
gridpack = False
evgenConfig.description = 'SMEFTsim 3.0 tt, top model, inclusive, standalone, EFT vertices, no propagator correction'

# process definition
model = "SMEFTsim_top_MwScheme_UFO-massless_topX"
if "_prop" in get_physics_short():
    model = "SMEFTsim_top_MwScheme_PropCorr_UFO-massless_topX"

process = '''
import model ''' + model + '''
define p = g u c d s b u~ c~ d~ s~ b~
define j = g u c d s b u~ c~ d~ s~ b~
define w = w+ w-
define l+ = e+ mu+ ta+
define l- = e- mu- ta-
define wdec = l+ l- vl vl~ j
''' + 'generate p p > t t~ QCD=2 NP=1 NPprop=0 SMHLOOP=0\n' + '''
output -f
'''
process_dir = new_process(process)

# run card settings
settings = {
    'nevents'               : nevents,
    'maxjetflavor'          : 5,
    'pdlabel'               : 'lhapdf',
    'lhaid'                 : 262000,
    'use_syst'              : 'False',
    'ptj'                   : '0.0',
    'ptl'                   : '0.0',
    'etaj'                  : '-1.0',
    'etal'                  : '-1.0',
    'drjj'                  : '0.0',
    'drll'                  : '0.0',
    'drjl'                  : '0.0',
    'mmll'                  : mllcut,
    'dynamical_scale_choice': '0',
    'fixed_ren_scale'       : 'True',
    'fixed_fac_scale'       : 'True',
    'scale'                 : fixed_scale,
    'dsqrt_q2fact1'         : fixed_scale,
    'dsqrt_q2fact2'         : fixed_scale,
}

modify_run_card(process_dir=process_dir,
                runArgs=runArgs,
                settings=settings)

# SM param card settings
params = dict()
params['mass'] = dict()
params['mass']['6'] = '1.725000e+02'
params['mass']['23'] = '9.118760e+01'
params['mass']['24'] = '8.039900e+01'
params['mass']['25'] = '1.250000e+02'
params['yukawa'] = dict()
params['yukawa']['6'] = '1.725000e+02'
params['DECAY'] = dict()
params['DECAY']['23'] = 'DECAY  23   2.495200e+00'
params['DECAY']['24'] = '''DECAY  24   2.085000e+00
   3.377000e-01   2   -1   2
   3.377000e-01   2   -3   4
   1.082000e-01   2  -11  12
   1.082000e-01   2  -13  14
   1.082000e-01   2  -15  16'''
params['DECAY']['25'] = 'DECAY  25   6.382339e-03'

modify_param_card(process_dir=process_dir,params=params)

# EFT param card settings
params = dict() 
params['SMEFTcutoff'] = dict()
params['SMEFTcutoff']['1'] = '1.000000e+03'

# set the WCs
params['SMEFT'] = dict()
params['SMEFT']['8'] = '0.5'

modify_param_card(process_dir=process_dir,params=params)

# build a dictionary of EFT operators: dict[operator name] = (block, id, [values])
eft_dict = {
    'ctGRe':  ('SMEFT', 15, [-0.4,-0.2,0.3,0.5]),
    'ctWRe':  ('SMEFT', 17, [-1.1,-0.7,0.7,1.1]),
    'ctBRe':  ('SMEFT', 19, [-0.9,-0.3,0.3,0.9]),
    'cHQ1':   ('SMEFT', 27, [-5,-1,1,5]),
    'cHQ3':   ('SMEFT', 29, [-5,-1,1,5]),
    'cHt':    ('SMEFT', 31, [-5,-1,1,5]),
    'cQj11':  ('SMEFT', 40, [-0.5,-0.3,0.3,0.5]),
    'cQj18':  ('SMEFT', 41, [-1.3,-0.9,0.3,0.7]),
    'cQj31':  ('SMEFT', 42, [-0.5,-0.4,0.3,0.5]),
    'cQj38':  ('SMEFT', 43, [-0.8,-0.4,0.4,0.8]),
    'cQQ1':   ('SMEFT', 44, [-1.4,-1,0.4,0.9]),
    'cQQ8':   ('SMEFT', 45, [-1.4,-1,0.4,0.9]),
    'ctu1':   ('SMEFT', 49, [-0.3,-0.15,0.1,0.3]),
    'ctu8':   ('SMEFT', 50, [-0.5,-0.3,0.3,0.5]),
    'ctd1':   ('SMEFT', 58, [-0.6,-0.3,0.3,0.6]),
    'ctd8':   ('SMEFT', 62, [-1.4,-1,0.4,0.9]),
    'cQu1':   ('SMEFT', 67, [-1.4,-1,0.4,0.9]),
    'cQu8':   ('SMEFT', 69, [-1.4,-1,0.4,0.9]),
    'ctj1':   ('SMEFT', 70, [-1.4,-1,0.4,0.9]),
    'ctj8':   ('SMEFT', 71, [-1.4,-1,0.4,0.9]),
    'cQt1':   ('SMEFT', 72, [-1.4,-1,0.4,0.9]),
    'cQt8':   ('SMEFT', 73, [-1.4,-1,0.4,0.9]),
    'cQd1':   ('SMEFT', 76, [-1.4,-1,0.4,0.9]),
    'cQd8':   ('SMEFT', 77, [-1.4,-1,0.4,0.9]),
    'cQl111': ('SMEFT', 133, [-5,-1,1,5]),
    'cQl122': ('SMEFT', 134, [-5,-1,1,5]),
    'cQl133': ('SMEFT', 135, [-5,-3,3,5]),
    'cQl311': ('SMEFT', 136, [-5,-1,1,5]),
    'cQl322': ('SMEFT', 137, [-1.1,-0.6,0.6,1.1]),
    'cQl333': ('SMEFT', 138, [-5,-1,1,3,5]),
    'cte11':  ('SMEFT', 148, [-2.4,-1,1,3]),
    'cte22':  ('SMEFT', 149, [-3,-1,1,5]),
    'cte33':  ('SMEFT', 150, [-5,-1,1,5]),
    'cQe11':  ('SMEFT', 160, [-2.4,-1,1,3]),
    'cQe22':  ('SMEFT', 161, [-3,-1,1,5]),
    'cQe33':  ('SMEFT', 162, [-5,-1,1,5]),
    'ctl11':  ('SMEFT', 166, [-2.4,-1,1,3]),
    'ctl22':  ('SMEFT', 167, [-3,-1,1,5]),
    'ctl33':  ('SMEFT', 168, [-5,-1,1,5]),
    'ctGIm':  ('SMEFTcpv', 8, [-0.4,-0.3,0.3,0.5]),
    'ctWIm':  ('SMEFTcpv', 10, [-1.4,-0.8,0.6,1.2]),
    'ctBIm':  ('SMEFTcpv', 12, [-1.8,-0.6,0.6,1.8]),
}


print_cards()

generate(process_dir=process_dir,
         grid_pack=gridpack,
         gridpack_compile=False,
         required_accuracy=0.001,
         runArgs=runArgs)

outputDS = arrange_output(process_dir=process_dir,
                          runArgs=runArgs,
                          saveProcDir=True,
                          lhe_version=lhe_version)

evgenConfig.contact          = ['noemi.cavalli@cern.ch']
evgenConfig.generators       = ['MadGraph','EvtGen','Pythia8']

check_reset_proc_number(opts)
include("Pythia8_i/Pythia8_A14_NNPDF23LO_EvtGen_Common.py")
include("Pythia8_i/Pythia8_MadGraph.py")

#new lines to avoid crash when no pythia
#theApp.finalize()
#theApp.exit()
