#!/usr/bin/env python3
import os
import sys
import re
import uproot
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def rebin(ngroup, edges, values, errors):
    new_edges = edges[::ngroup].copy()
    if new_edges[-1] != edges[-1]:
        new_edges.append(edges[-1])

    new_values = np.convolve(values, np.ones(ngroup), mode='full')[(ngroup-1)::ngroup]

    variances = errors * errors
    new_variances = np.convolve(variances, np.ones(ngroup), mode='full')[(ngroup-1)::ngroup]
    new_errors = np.sqrt(new_variances)

    assert(len(new_values) == len(new_errors))
    assert(len(new_values)+1 == len(new_edges))

    return new_edges, new_values, new_errors

def plotRatio(ax, hist1, hist2, merge_every_nbins=4, title='', xlabel='', ylabel='', compute_chi2=False):

    bin_edges = hist1.axis().edges()
    assert(np.all(bin_edges == hist2.axis().edges()))

    value1 = hist1.values()
    error1 = hist1.errors()

    value2 = hist2.values()
    error2 = hist2.errors()
    
    if merge_every_nbins is not None:
        bin_edges_rb, value1_rb, error1_rb = rebin(merge_every_nbins, bin_edges, value1, error1)
        _, value2_rb, error2_rb = rebin(merge_every_nbins, bin_edges, value2, error2)

        bin_edges = bin_edges_rb
        value1 = value1_rb
        error1 = error1_rb
        value2 = value2_rb
        error2 = error2_rb

    if compute_chi2:
        # number of degress of freedom
        ndf = len(value1)

        # loop over bins
        chi2 = 0.
        for v1, v2, e1, e2 in zip(value1, value2, error1, error2):
            if v1 == 0 and v2 == 0:
                ndf -= 1 # Skip empty bin
                continue
            chi2 += (v1-v2)*(v1-v2) / (e1*e1+e2*e2)

        pvalue = 1. - stats.chi2.cdf(chi2, ndf)

        # add to title
        if title:
            title += "\n"
        title += "[$\chi^{2}$/NDF" + f" = {chi2:.2f}/{ndf} (p-value = {pvalue:.2f})]"

    relerr2 = np.zeros_like(error2)
    np.divide(error2, value2, out=relerr2, where=value2!=0)

    # draw denominator error band
    # append the relerr array with its last entry so its length is the same as bin edges
    relerr2 = np.append(relerr2, relerr2[-1])
    ax.fill_between(
        bin_edges, 1+relerr2, 1-1*relerr2, step='post',
        edgecolor='none', facecolor='black', alpha=0.3)

    # draw a horizontal line at y=1
    ax.axhline(y=1, color='grey', linestyle='-', alpha=0.5, label='Reweight')

    # draw ratio
    ratio = np.zeros_like(value1)
    np.divide(value1, value2, out=ratio, where=value2!=0)

    ratio_err = np.zeros_like(error1)
    np.divide(error1, value2, out=ratio_err, where=value2!=0)

    bin_center = (bin_edges[1:] + bin_edges[:-1]) / 2
    bin_width = bin_edges[1:] - bin_edges[:-1]

    ax.errorbar(
        bin_center, ratio, xerr = bin_width/2, yerr = ratio_err,
        marker='', drawstyle= 'steps-mid', linestyle='-', color='tab:red',
        label='Standalone')

    if title:
        ax.set_title(title, fontsize=6)

    if xlabel:
        ax.set_xlabel(xlabel)

    if ylabel:
        ax.set_ylabel(ylabel)

    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

def makeSummaryPlots(
        input_dir,
        label_list,
        outname,
        helF_suffix=None,
        histfile='histograms.root'
        ):

    # list of input file names
    infiles = []
    for l in label_list:
        label = l if helF_suffix is None else f"{l}_{helF_suffix}"
        infiles.append(os.path.join(input_dir, label, histfile))

    print(f"Reading histograms from {infiles}")

    assert(len(infiles))

    # get the list of available histogram names from the first input file
    hist_prefix = []
    with uproot.open(infiles[0]) as file0:
        label0 = label_list[0]

        for name, class_type in file0.classnames().items():
            if not 'TH1' in class_type:
                continue

            # get only the reweighted histogram to avoid duplicates
            if not '_rw_' in name:
                continue

            # get the prefix
            hprefix = name.replace(f'_rw_{label0}','')
            hist_prefix.append(hprefix)

    for hpre in hist_prefix:
        print(f"{hpre}")
        figname = outname + hpre.lstrip('h') + '.png'

        nlabels = len(label_list)
        fig, axes = plt.subplots(nlabels, figsize=(6, 1.5*nlabels), sharex=True)
        plt.subplots_adjust(hspace = 0.5)

        for l, fn, ax in zip(label_list, infiles, axes):
            print(f" {l}")

            f = uproot.open(fn)

            hist_sa = f[f'{hpre}_sa_{l}']
            hist_rw = f[f'{hpre}_rw_{l}']

            plotRatio(
                ax, hist_sa, hist_rw,
                title=l, compute_chi2=True)

        # x-axis label
        xlabel = hist_sa.axis().member('fTitle')
        newlabels = []
        for xl in re.split(r"\s(?![^{]*})", xlabel):
            # add '$' for latex expressions
            if '#' in xl or '{' in xl or '}' in xl:
                newlabels.append('$'+xl.replace("#","\\")+'$')
            else:
                newlabels.append(xl)

        axes[-1].set_xlabel(' '.join(newlabels))

        # legend
        axes[0].legend(bbox_to_anchor=(1.05, 1.01), loc="lower right", ncol=1, fontsize='small')

        print(f"Create plot {figname}")
        fig.savefig(figname, dpi=300)
        plt.close(fig)            

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('input_dir', type=str,
                        help="Top directory to read histogram files")
    parser.add_argument('-l', '--labels', nargs='+', required=True,
                        help="List of Wilson coefficiencts and values to plot")
    parser.add_argument('-s', '--suffix', type=str,
                        help="Suffix to be added to labels for accessing files")
    parser.add_argument('-o', '--output', type=str, default="valiations",
                        help="Output plot name")
    parser.add_argument('--filename', type=str, default='histograms.root',
                        help="Name of the file that contains histograms")

    args = parser.parse_args()

    # check input directory
    if not os.path.isdir(args.input_dir):
        print(f"Can not read from directory {args.input_dir}")
        sys.exit(1)

    # output directory
    outdir = os.path.dirname(args.output)
    if outdir and not os.path.isdir(outdir):
        print(f"Create output directory {outdir}")
        os.makedirs(outdir)

    makeSummaryPlots(
        args.input_dir, args.labels, args.output,
        helF_suffix = args.suffix,  histfile = args.filename)
