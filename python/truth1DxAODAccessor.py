import uproot
import ROOT

class TruthParticleAccessor():
    """
    """

    def __init__(
        self,
        filepath, # file path to DxAOD TRUTH1 root file
        treename="CollectionTree", # tree name
        library="ak" # type of array uproot retures. Default: Awkward array; Use "np" for Numpy array
    ):
        print(f"Read TTree from input file {filepath}")
        self.tree = uproot.open(filepath+":"+treename)

        print(f"Load truth particle arrays ...")
        self.truth_particles_arr = self.tree.arrays([
            "TruthParticlesAux.pdgId",
            "TruthParticlesAux.status",
            "TruthParticlesAux.px",
            "TruthParticlesAux.py",
            "TruthParticlesAux.pz",
            "TruthParticlesAux.e",
            "TruthParticlesAux.m"
            ], library=library)
        print("... done!")

        self.array_lib=library

    def __len__(self):
        return self.tree.num_entries

    def event_weights(self):
        return self.tree["EventInfoAuxDyn.mcEventWeights"].array(library=self.array_lib)

    def truth_jets_pt(self):
        return self.tree["AntiKt4TruthJetsAux.pt"].array(library=self.array_lib)

    def truth_jets_eta(self):
        return self.tree["AntiKt4TruthJetsAux.eta"].array(library=self.array_lib)

    ####
    # Parton history methods
    def getTruthParticleP4(self, ievent, pdgid, status):
        """
        Return the Lorentz vector of the specified truth particle
        (ROOT.Math.PxPyPzMVector)
        """
        truth_particles = self.truth_particles_arr[ievent]

        for i, pid in enumerate(truth_particles["TruthParticlesAux.pdgId"]):
            if pid != pdgid:
                continue

            # check status
            st = truth_particles["TruthParticlesAux.status"][i]
            if st != status:
                continue

            # found the particle
            # construct Lorentz Vector
            p4 = ROOT.Math.PxPyPzMVector(
                truth_particles["TruthParticlesAux.px"][i],
                truth_particles["TruthParticlesAux.py"][i],
                truth_particles["TruthParticlesAux.pz"][i],
                truth_particles["TruthParticlesAux.m"][i]
                )

            return p4

        return None

    def getTruthP4_top(self, ievent, afterFSR):
        status = 62 if afterFSR else 22 # Pythia 8 only
        return self.getTruthParticleP4(ievent, 6, status)

    def getTruthP4_antitop(self, ievent, afterFSR):
        status = 62 if afterFSR else 22  # Pythia 8 only
        return self.getTruthParticleP4(ievent, -6, status)

    def getTruthP4_Wp(self, ievent):
        status = 22 # Pythia 8 only
        return self.getTruthParticleP4(ievent, 24, status)

    def getTruthP4_Wm(self, ievent):
        status = 22 # Pythia 8 only
        return self.getTruthParticleP4(ievent, -24, status)

    def getTruthTTbarP4(self, ievent, afterFSR):
        """
        Return the Lorentz vector of ttbar
        """

        t_p4 = self.getTruthP4_top(ievent, afterFSR=afterFSR)
        if t_p4 is None:
            print("Fail to find the required top quark in the truth particles")
            return None

        tbar_p4 = self.getTruthP4_antitop(ievent, afterFSR=afterFSR)
        if tbar_p4 is None:
            print("Fail to find the required anti-top quark in the truth particles")
            return None

        ttbar_p4 = t_p4 + tbar_p4

        return ttbar_p4
