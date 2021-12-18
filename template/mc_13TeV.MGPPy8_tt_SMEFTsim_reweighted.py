selected_operators = ['ctGRe', 'ctGIm', 'ctj1', 'cQd1', 'cQu1', 'ctj8', 'cQd8', 'cQu8', 'ctd1', 'ctu1', 'cQj11', 'cQj31', 'ctd8', 'ctu8', 'cQj38', 'cQj18']

# Note: the 4-quark operators ['cQj18','cQj38','ctu8','ctd8','cQj11','cQj31','ctj8','ctj1','ctu1','ctd1','cQd1','cQd8','cQu1','cQu8','cQQ1','cQQ8','cQt1','cQt8']
#       require QED=4, which includes SM EW corrections and is too CPU-intensive 

process_definition = 'generate p p > t t~ QCD=2 NP=1 NPprop=0 SMHLOOP=0\n'

fixed_scale = 345. # ~ m(top)+m(top)

gridpack = False

evgenConfig.description = 'SMEFTsim 3.0 tt, top model, inclusive, reweighted, EFT vertices, no propagator correction'

include("Common_SMEFTsim_topmW_topX_reweighted.py")
