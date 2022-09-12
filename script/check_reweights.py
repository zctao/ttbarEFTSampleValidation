# A script from Noemi Cavalli to checked reweighted sample cross section relative errors based on log.generate

import sys

cutoff = 0.1 # maximum relative size of the uncertainty on the reweighted cross-section

infile = sys.argv[1]

data = []
orig_xsec = 1.

with open(infile,"r") as f:
    read_weight_names   = False
    read_cross_sections = False
    for line in f:
        if "cross-section from sum of weights:" in line:
            orig_xsec = float(line.split("cross-section from sum of weights: ")[1].split(")")[0])
        if not read_weight_names and len(data)==0:
            if "INFO reweight_card" in line:
                read_weight_names = True
        if read_weight_names:
            if "launch --rwgt_info=" in line:
                name = line.rstrip().split("launch --rwgt_info=")[1]
                data.append((name,[0,0]))
            if "INFO The parameters that will be updated are" in line or "INFO Found madevent/bin/gridrun, starting generation" in line:
                read_weight_names = False
        if not read_weight_names and len(data)>0:
            if "INFO: Computed cross-section" in line:
                read_cross_sections = True
        if read_cross_sections:
            if "INFO: rwgt_" in line:
                index = int(   line.split("INFO: rwgt_")[1].split(" ")[0] ) - 1
                xsec  = float( line.split("INFO: rwgt_")[1].split(":")[1].split("+-")[0] )
                err   = float( line.split("INFO: rwgt_")[1].split(":")[1].split("+-")[1].split("pb")[0] )
                name  = data[index][0]
                data[index] = (name,[xsec,err])

print("Reweight name"," "*(30-len("Reweight name")),"\t cross-section +- error","\t (relative size in %)")
print("-------------"," "*(30-len("Reweight name")),"\t ----------------------","\t --------------------")
print("")
for reweight in data:
    name = reweight[0]
    xsec = reweight[1][0]
    err  = reweight[1][1]

    if err > abs(xsec)*cutoff:
        print(name," "*(30-len(name)),"\t {:.6f} +- {:.6f}".format(xsec,err),"\t\t {:.0f}%".format(err/abs(xsec)*100),"\t--> {}".format("try to fix" if err/abs(xsec)*100 < 40 else "FIX!!!"))
    elif err <= abs(xsec)*cutoff:
        print(name," "*(30-len(name)),"\t {:.6f} +- {:.6f}".format(xsec,err),"\t\t {:.0f}%".format(err/abs(xsec)*100),"\t--> {}".format("this is nice!"))
    #if abs(1-xsec/orig_xsec)<0.0001:
        #print name," "*(30-len(name)),"\t {:.6f} +- {:.6f}".format(xsec,err),"\t\t {:.0f}%".format(err/abs(xsec)*100),"\t--> NO EFFECT!"
