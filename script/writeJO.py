#!/usr/bin/env python3
import os

from eft_dict import eft_dict

def cleanup_template_filename(fname):
    # remove template file extension e.g. ".tmpl" and add the extension ".py"
    newfname = os.path.splitext(fname)[0]

    if not newfname.endswith(".py"):
        newfname += ".py"

    return newfname

def read_lines_and_replace(filename, target_str_list, new_str_list):

    with open(filename) as f_in:
        lines = f_in.readlines()

    for i in range(len(lines)):
        # search and replace
        for target, newstr in zip(target_str_list, new_str_list):
            if target in lines[i]:
                lines[i] = lines[i].replace(target, newstr)

    return lines

def writeJO_rw(template_control, template_jo, outdir):

    # Modify template_control
    assert(os.path.isfile(template_control))
    # Add eft_dict to template_control
    # search and replace "TEMPLATE_INSERT_EFT_DICT" in template_control
    lines_ctrl = read_lines_and_replace(
        template_control, ["TEMPLATE_INSERT_EFT_DICT"], [f"{eft_dict=}"]
        )

    # write to a new file
    fname_ctrl = os.path.basename( cleanup_template_filename(template_control) )
    with open(os.path.join(outdir, fname_ctrl), 'w') as new_fctrl:
        new_fctrl.writelines(lines_ctrl)

    # Modify template_jo
    assert(os.path.isfile(template_jo))
    # Add control file to the job option
    lines_jo = read_lines_and_replace(
        template_jo, ["TEMPLATE_INSERT_CONTROL_PY"], [fname_ctrl]
        )

    # write to a new file
    fname_jo = os.path.basename( cleanup_template_filename(template_jo) )
    with open(os.path.join(outdir, fname_jo), 'w') as new_jo:
        new_jo.writelines(lines_jo)

def writeJO_sa(template_file, coefficients, values, output):
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
    output = cleanup_template_filename(output)
    with open(output, 'w') as newfile_jo:
        newfile_jo.writelines(lines)

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')

    # For reweight sample
    parser_rw = subparsers.add_parser('rw', help="Generate job options for reweighted sample")
    parser_rw.add_argument("-t", "--template-control", type=str, required=True,
                            help="Template for control file")
    parser_rw.add_argument("-j", "--template-jo", type=str, required=True,
                            help="Job option tempalte")
    parser_rw.add_argument("-o", "--outdir", type=str, required=True,
                            help="Output directory")

    # For standalone sample
    parser_sa = subparsers.add_parser('sa', help="Generate a new job option by modifying the Wilson coefficients in a template job option file")
    parser_sa.add_argument("template_file", type=str,
                            help="File name of the job option to be modified")
    parser_sa.add_argument("-c", "--coefficients", nargs='+', type=str, required=True,
                            help="List of Wilson coefficient names")
    parser_sa.add_argument("-v", "--values", nargs='+', type=float, required=True,
                            help="Values of the Wilson coefficients")
    parser_sa.add_argument("-o", "--output", type=str, required=True,
                            help="Output name")

    args = parser.parse_args()

    # call the corresponding function
    if args.subparser_name == "rw":
        if not os.path.isdir(args.outdir):
            os.makedirs(args.outdir)
        writeJO_rw(
            args.template_control, args.template_jo, args.outdir
            )
    elif args.subparser_name == "sa":
        writeJO_sa(
            args.template_file, args.coefficients, args.values, args.output
            )
