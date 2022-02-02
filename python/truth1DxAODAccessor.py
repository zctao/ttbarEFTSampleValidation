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
        return self.tree["AntiKt4TruthWZJetsAux.pt"].array(library=self.array_lib)

    ####
    # Parton history methods
    def getTruthTopP4(self, ievent, istbar, afterFSR):
        """
        Return the Lorentz vector (ROOT.Math.PxPyPzMVector) of the truth top
        """

        target_id = -6 if istbar else 6
        
        truth_particles = self.truth_particles_arr[ievent]

        for i, pid in enumerate(truth_particles["TruthParticlesAux.pdgId"]):
            if pid != target_id:
                continue

            # Check if it is the last (or first) top based on the status code
            # Pythia8 only
            status = truth_particles["TruthParticlesAux.status"][i]

            if afterFSR:
                if status != 62:
                    continue
            else:
                if status != 22:
                    continue

            # Construct Lorentz vector
            top_p4 = ROOT.Math.PxPyPzMVector(
                truth_particles["TruthParticlesAux.px"][i],
                truth_particles["TruthParticlesAux.py"][i],
                truth_particles["TruthParticlesAux.pz"][i],
                truth_particles["TruthParticlesAux.m"][i])

            return top_p4

        return None

    def getTruthTTbarP4(self, ievent, afterFSR):
        """
        Return the Lorentz vector of ttbar
        """

        t_p4 = self.getTruthTopP4(ievent, istbar=False, afterFSR=afterFSR)
        if t_p4 is None:
            print("Fail to find the required top quark in the truth particles")
            return None

        tbar_p4 = self.getTruthTopP4(ievent, istbar=True, afterFSR=afterFSR)
        if tbar_p4 is None:
            print("Fail to find the required anti-top quark in the truth particles")
            return None

        ttbar_p4 = t_p4 + tbar_p4

        return ttbar_p4
