#!/usr/bin/env python3
import os

jo_reweighted = """
selected_operators = ['ctGRe', 'ctGIm', 'ctj1', 'cQd1', 'cQu1', 'ctj8', 'cQd8', 'cQu8', 'ctd1', 'ctu1', 'cQj11', 'cQj31', 'ctd8', 'ctu8', 'cQj38', 'cQj18']

process_definition = 'generate p p > t t~ QCD=2 NP=1 NPprop=0 SMHLOOP=0'

fixed_scale = 345. # ~ m(top)+m(top)

gridpack = False

evgenConfig.description = 'SMEFTsim 3.0 tt, top model, inclusive, reweighted, EFT vertices, no propagator correction'

include("{common_jo}")
"""

# import from somewhere instead?
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

def modifyJO(template_file, coefficients, values, output):
    assert(len(coefficients)==len(values))

    file_jo = open(template_file)
    lines = file_jo.readlines()

    for i in range(len(lines)):
        if lines[i].startswith("params['SMEFT']["):
            newline = ""
            for c, v in zip(coefficients, values):
                # look up the index of the Wilson coefficient
                wc_block, wc_id = eft_dict[c][:2]

                # in case of SMEFTcpv
                if wc_block == 'SMEFTcpv':
                    newline += f"params['SMEFTcpv'] = dict()\n"

                # add to the new line
                newline += f"params['{wc_block}']['{wc_id}'] = '{v}'\n"
            #print(newline)
            lines[i] = newline

    file_jo.close()
        
    # write to a new JO
    with open(output, 'w') as newfile_jo:
        newfile_jo.writelines(lines)

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a new job option by modifying the Wilson coefficients in a template job option file"
    )

    parser.add_argument("template_file", type=str,
                        help="File name of the job option to be modified")
    parser.add_argument("-c", "--coefficients", nargs='+', type=str, required=True,
                        help="List of Wilson coefficient names")
    parser.add_argument("-v", "--values", nargs='+', type=float, required=True,
                        help="Values of the Wilson coefficients")
    parser.add_argument("-o", "--output", type=str, required=True,
                        help="Output name")

    args = parser.parse_args()

    modifyJO(args.template_file, args.coefficients, args.values, args.output)
