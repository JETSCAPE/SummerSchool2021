import numpy as np
import argparse
import sys
import os
import smash_basic_scripts as sb
from multiprocessing import Pool

class HadronHistory():
    def __init__(self):
        self.history = {}

    def add_reaction(self, block):
        nin = block['nin']
        nout = block['nout']
        pdgin = block['incoming']['pdgid']
        pdgout = block['outgoing']['pdgid']
        idin = block['incoming']['id']
        idout = block['outgoing']['id']
        t = sb.get_block_time(block)
        is_elastic = sb.is_elastic22(block)
        if (is_elastic):
            for i, particle_id in enumerate(idout):
                if not particle_id in self.history: self.history[particle_id] = {}
                self.history[particle_id]["pdg"] = block['outgoing']['pdgid'][i]
                if not "t_el" in self.history[particle_id]: self.history[particle_id]["t_el"] = []
                self.history[particle_id]["t_el"].append(t)
                self.history[particle_id]["p"] = block['outgoing']['p'][i]
            return
        for i, particle_id in enumerate(idin):
            if not particle_id in self.history: self.history[particle_id] = {}
            self.history[particle_id]["t_end"] = t
            self.history[particle_id]["pdg"] = block['incoming']['pdgid'][i]
            self.history[particle_id]["r_end_pdg"] = (pdgin,pdgout)
            self.history[particle_id]["r_end_id"] = (idin,idout)
            self.history[particle_id]["p"] = block['incoming']['p'][i]
        for i, particle_id in enumerate(idout):
            if not particle_id in self.history: self.history[particle_id] = {}
            self.history[particle_id]["t_start"] = t
            self.history[particle_id]["r_start_pdg"] = (pdgin,pdgout)
            self.history[particle_id]["r_start_id"] = (idin,idout)
            self.history[particle_id]["pdg"] = block['outgoing']['pdgid'][i]
            self.history[particle_id]["p"] = block['outgoing']['p'][i]

    def print_statistics(self):
        k = self.history.keys()
        v = self.history.values()
        pdg = [x["pdg"] for x in v]
        ids = np.array(k)
        pdg = np.array(pdg)
        print(ids.size, "unique ids, min id = ", ids.min(), ", max id = ", ids.max())
        print("Total number of rho0 tracks: ", (pdg == 113).sum())
        rho0_ids = ids[pdg == 113]
        v_is_final = np.vectorize(self.is_final)
        final_rho0_ids = rho0_ids[v_is_final(rho0_ids)]
        print(final_rho0_ids.size, " of them are measurable experimentally")
        p = np.array([self.history[pid]["p"] for pid in final_rho0_ids])
        y = np.array([0.5 * np.log((x[0] + x[3]) / (x[0] - x[3]) ) for x in p])
        y_selector = (np.abs(y) < 1.0)
        print(y_selector.sum(), " of them are at midrapidity")

    def destiny_matrix_rho0(self):
        M = np.zeros((5, 5), dtype = np.int)
        rho0pdg = 113
        midrapidity_cut = 0.5

        k = list(self.history.keys())
        v = list(self.history.values())
        pdg = [x["pdg"] for x in v]
        ids = np.array(k)
        pdg = np.array(pdg)
        rho0_ids = ids[pdg == rho0pdg]
        p = np.array([self.history[pid]["p"] for pid in rho0_ids])
        y = np.array([0.5 * np.log((x[0] + x[3]) / (x[0] - x[3]) ) for x in p])
        y_selector = (np.abs(y) < midrapidity_cut)
        midrapidity_rho0_ids = rho0_ids[y_selector]
        for rho0_id in midrapidity_rho0_ids:
            if ("r_start_id" not in self.history[rho0_id]):
                # born from hydro directly
                index_born = 0
            elif (self.history[rho0_id]["r_start_id"][0].size > 1 and self.history[rho0_id]["r_start_id"][1].size == 1):
                # born from resonance formation
                index_born = 1
            elif (self.history[rho0_id]["r_start_id"][0].size > 1 and self.history[rho0_id]["r_start_id"][1].size > 1):
                # born from some inelastic 2 -> n >=2 interaction
                index_born = 2
            elif (self.history[rho0_id]["r_start_id"][0].size == 1):
                # born from decay
                parent_id = self.history[rho0_id]["r_start_id"][0][0]
                if ("r_start_id" not in self.history[parent_id]):
                    # parent resonance born from hydro
                    index_born = 3
                else:
                    # parent resonance born not from hydro
                    index_born = 4
            else:
                print("Error, broken logic")

            if (self.is_final(rho0_id)):
                # ended up being detectable
                index_die = 0
            elif (self.history[rho0_id]["r_end_id"][1].size == 1):
                # formed a resonance
                index_die = 1
            elif (self.history[rho0_id]["r_end_id"][0].size > 1 and self.history[rho0_id]["r_end_id"][1].size > 1):
                # got into some inelastic reaction, 2->2 or 2->n > 2
                index_die = 2
            elif (self.history[rho0_id]["r_end_id"][0].size == 1 and self.history[rho0_id]["r_end_id"][1].size > 1):
                # decayed, but decay products collided and Lambda ended up undetectable
                index_die = 3
            else:
                # shouldn't get here, indicates some broken logic
                print("logic error, index_die", self.history[rho0_id])
            M[index_born, index_die] += 1
        return M
        

    def distributions(self):
        Lambda1520pdg = 3124
        f2_1525_pdg = 335
        Kstar0_892_pdg = 313
        Sigma0_1775_pdg = 3216
        phi2010_pdg = 333
        rho0_pdg = 113
        Sigma1385pl_pdg = 3224
        Sigma1385mi_pdg = 3114
        Xi1530 = 3314
        Xi1690 = 203312
        Xi1950 = 103316
        Sigma1670 = 13214
        La1405 = 13122
        La1690 = 13124
        La1800 = 43122
        Deltapp = 2224
        Delta1620pp = 2222 
        N1520 = 1214
        N1680 = 12116
        K2st1430 = 315
        K1st_1270 = 10313
        b1_1235 = 10113
        pdgs_of_interest = [rho0_pdg]

        #pdgs_of_interest = [
        #    9000221, 113, 223, 331, 9010221, 9000111, 333, 10223, 10113, 20113, 225, 20223,
        #    100221, 100111, 115, 10221, 9000113, 9020221, 20333, 100223, 10111, 100113,
        #    100331, 9030221, 335, 9010113, 10225, 30223, 227, 10115, 100333, 117, 30113,
        #    10331, 9010111, 337, 9050225, 9060225, 119, 229, 9080225, 9090225, 313, 10313,
        #    20313, 100313, 10311, 315, 30313, 10315, 317, 20315, 319, 12112, 1214, 22112,
        #    32112, 2116, 12116, 21214, 42112, 31214, 9902114, 9952112, 9962112, 9912114,
        #    9902118, 9922116, 9922114, 9972112, 9932114, 1218, 19922119, 19932119, 1114,
        #    1112, 11114, 11112, 1116, 21112, 21114, 11116, 1118, 13122, 3124, 23122, 33122,
        #    13124, 43122, 53122, 3126, 13126, 23124, 3128, 23126, 19903129, 3114, 13112,
        #    13114, 23112, 3116, 13116, 23114, 3118, 9903118, 3314, 203312, 13314, 103316,
        #    203316, 203338]
        ybins = np.linspace(-4.0, 4.0, 41)
        ptbins = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0, 4.4, 4.8, 6.0, 8.0, 10.0, 15.0])
        midrapidity_cut = 0.5

        k = list(self.history.keys())
        v = list(self.history.values())
        pdg = [x["pdg"] for x in v]
        ids = np.array(k)
        pdg = np.array(pdg)
        results = {}
        for pdg_of_interest in pdgs_of_interest:
            pdg_of_interest_ids = ids[pdg == pdg_of_interest]
            if (pdg_of_interest_ids.size == 0):
                results[pdg_of_interest] = \
                       {'y': np.histogram([], bins = ybins),
                       'pt': np.histogram([], bins = ptbins),
                       'cos2phi': np.histogram([], bins = ptbins),
                       'midrap_yield': 0}
                continue
            v_is_final = np.vectorize(self.is_final)
            final_pdg_of_interest_ids = pdg_of_interest_ids[v_is_final(pdg_of_interest_ids)]
            p = np.array([self.history[pid]["p"] for pid in final_pdg_of_interest_ids])
            y = np.array([0.5 * np.log((x[0] + x[3]) / (x[0] - x[3]) ) for x in p])
            y_selector = (np.abs(y) < midrapidity_cut)
            pt = np.array([np.sqrt(x[1]*x[1] + x[2]*x[2]) for x in p])
            tmp = np.array([(x[1]*x[1] - x[2]*x[2]) for x in p])
            cos2phi = np.where(pt > 0.0, tmp / (pt*pt), 0.0)
            if pdg_of_interest == rho0_pdg:
                for pid in final_pdg_of_interest_ids[y_selector]:
                    tstart = self.history[pid]["t_start"] if "t_start" in self.history[pid] else -1.0
                    tend = self.history[pid]["t_end"] if "t_end" in self.history[pid] else 101.0
                    if not "r_end_id" in self.history[pid]:
                        # print("x ", self.history[pid])
                        continue
                    ids_out =  self.history[pid]["r_end_id"][1]
                    #for id_out in ids_out:
                        # print(self.history[id_out]["pdg"],)
                    #print()
                    #print(tstart, tend)
 
            results[pdg_of_interest] = \
                {'y': np.histogram(y, bins = ybins),
                'pt': np.histogram(pt[y_selector], bins = ptbins),
                'cos2phi': np.histogram(pt[y_selector], bins = ptbins, weights = cos2phi[y_selector]),
                'midrap_yield': y_selector.sum()}
        return results

    def is_final(self, res_id):
        """
        Returns true if particle can be retrieved experimentally.
        This means that the particle only decayed, possibly in many stages,
        but decay products never collided, elastically or inelastically.
        """
        # True if particle never participated in any reactions. Although
        # it might also mean that res_id is wrong and particle never existed,
        # but it's impossible to check only from reaction list.
        if (not res_id in self.history):
            print(res_id, " is final, never participated in reactions")
            return True
        # True if particle is a product of reaction, but never participated in a reaction
        if (not "r_end_id" in self.history[res_id]):
            #print(res_id, " is final, never decayed or collided inelastically")
            return True
        # True if particle decayed, decay products are final and never collided elastically
        elif (self.history[res_id]["r_end_id"][0].size == 1 and \
              self.history[res_id]["r_end_id"][1].size == 2):
            assert(self.history[res_id]["r_end_id"][0][0] == res_id)
            daughter1_id = self.history[res_id]["r_end_id"][1][0]
            daughter2_id = self.history[res_id]["r_end_id"][1][1]
            d1_collided_elastically = ((daughter1_id in self.history) and ("t_el" in self.history[daughter1_id]))
            d2_collided_elastically = ((daughter2_id in self.history) and ("t_el" in self.history[daughter2_id]))
            if (d1_collided_elastically or d2_collided_elastically):
                #print("One of ", res_id, " decay products (", daughter1_id, daughter2_id, ") collided elastically")
                return False
            else:
                #print("Let's check if decay products ", daughter1_id, daughter2_id, " are final")
                return self.is_final(daughter1_id) and self.is_final(daughter2_id)
        else:
            #print(res_id, " collided inelastically", self.history[res_id]["r_end_pdg"])
            return False

def analyze_file(path):
    if not os.path.exists(path):
        print('WARN: ignored non-existing file "{}"'.format(path))
        return {}
    #print(path)

    hadron_history = HadronHistory()

    intcounter = 0  # any interactions counter
    event_num = 0  # event counter
    destiny_matrix_rho0 = np.zeros((5, 5), dtype = np.int)
    yhist = {}
    pthist = {}
    dndy = {}
    cos2phi = {}

    with sb.BinaryReader(path) as reader:
        for block in reader:
            if (block['type'] == b'f'):  # end of event
                distr = hadron_history.distributions()
                pdgs_of_interest = distr.keys()
                for pdg_of_interest in pdgs_of_interest:
                    if (event_num == 0):
                        ybins = distr[pdg_of_interest]['y'][1]
                        yhist[pdg_of_interest] = distr[pdg_of_interest]['y'][0]
                        ptbins = distr[pdg_of_interest]['pt'][1]
                        pthist[pdg_of_interest] = distr[pdg_of_interest]['pt'][0]
                        cos2phi[pdg_of_interest] = distr[pdg_of_interest]['cos2phi'][0]
                        dndy[pdg_of_interest] = distr[pdg_of_interest]['midrap_yield']
                    else:
                        yhist[pdg_of_interest] += distr[pdg_of_interest]['y'][0]
                        pthist[pdg_of_interest] += distr[pdg_of_interest]['pt'][0]
                        np.add(cos2phi[pdg_of_interest], distr[pdg_of_interest]['cos2phi'][0], out = cos2phi[pdg_of_interest], casting = 'unsafe')
                        dndy[pdg_of_interest] += distr[pdg_of_interest]['midrap_yield']
                destiny_matrix_rho0 += hadron_history.destiny_matrix_rho0()
                event_num += 1
                hadron_history = HadronHistory()
                #print(event_num)
                #if (event_num > 6):
                #    print(yhist, pthist, dndy, event_num)
                #    break
            if (block['type'] == b'i'):  # interaction
                intcounter += 1
                hadron_history.add_reaction(block)

    return {'ybins': ybins,
            'yhist': yhist,
            'ptbins': ptbins,
            'pthist': pthist,
             'v2':    cos2phi,
             'dndy':  dndy,
             'nev':   event_num,
             'destiny_matrix': destiny_matrix_rho0}

if __name__ == '__main__':
    input_files = sys.argv[1:]
    pool = Pool(processes=1)
    results = pool.map_async(analyze_file, input_files)
    #results = [analyze_file(input_file) for input_file in input_files]
    pdgs_of_interest = list(results.get()[0]['yhist'].keys())
    pdgs_of_interest.sort()
    # print(pdgs_of_interest)
    ybins = results.get()[0]['ybins']
    ptbins = results.get()[0]['ptbins']
    yhist = results.get()[0]['yhist']
    pthist = results.get()[0]['pthist']
    v2 = results.get()[0]['v2']
    dndy = results.get()[0]['dndy']
    nev = results.get()[0]['nev']
    destiny_matrix_rho0 = results.get()[0]['destiny_matrix']
    for i in results.get()[1:]:
        for pdg_of_interest in pdgs_of_interest:
            yhist[pdg_of_interest] += i['yhist'][pdg_of_interest]
            pthist[pdg_of_interest] += i['pthist'][pdg_of_interest]
            dndy[pdg_of_interest] += i['dndy'][pdg_of_interest]
            np.add(v2[pdg_of_interest], i['v2'][pdg_of_interest], out = v2[pdg_of_interest], casting = 'unsafe')
        nev += i['nev']
        destiny_matrix_rho0 += i['destiny_matrix']
    #print(yhist, pthist, dndy, nev)
    #print(destiny_matrix_rho0)

    with open('resonances_yspectrum.txt', 'w') as f:
        f.write("# MUSIC + SMASH simulation, PbPb at 5.02 TeV, measurable rho0 rapidity spectrum\n")
        f.write("# \"Measurable\" rho0 definition: none of its decay products ever collided, el or inel\n")
        f.write("# number of events: %d\n" % nev)
        f.write("# y   dN/dy for pdg  ")
        for pdg_of_interest in pdgs_of_interest:
            f.write("%d " % pdg_of_interest)
        f.write("\n")
        ybin_centers = 0.5 * (ybins[1:] + ybins[:-1])
        for i, y in enumerate(ybin_centers):
            f.write("%5.2f" % y)
            for pdg_of_interest in pdgs_of_interest:
                f.write("%12d " % yhist[pdg_of_interest][i])
            f.write("\n")

    with open('resonances_ptspectrum.txt', 'w') as f:
        f.write("# MUSIC + SMASH simulation, PbPb at 5.02 TeV, measurable rho0 transverse momentum spectrum\n")
        f.write("# \"Measurable\" rho0 definition: none of its decay products ever collided, el or inel\n")
        f.write("# |y| < 0.5 cut\n")
        f.write("# number of events: %d\n" % nev)
        f.write("# pt   counts for pdg  ")
        for pdg_of_interest in pdgs_of_interest:
            f.write("%d " % pdg_of_interest)
        f.write("\n")
        ptbin_centers = 0.5 * (ptbins[1:] + ptbins[:-1])
        for i, pt in enumerate(ptbin_centers):
            f.write("%5.2f" % pt)
            for pdg_of_interest in pdgs_of_interest:
                f.write("%12d " % pthist[pdg_of_interest][i])
            f.write("\n")

    with open('resonances_dndy.txt', 'w') as f:
        f.write("# MUSIC + SMASH simulation, PbPb at 5.02 TeV, measurable rho0 dn/dy\n")
        f.write("# \"Measurable\" rho0 definition: none of its decay products ever collided, el or inel\n")
        f.write("# |y| < 0.5 cut\n")
        f.write("# number of events: %d\n" % nev)
        f.write("# dndy   counts for pdg  ")
        for pdg_of_interest in pdgs_of_interest:
            f.write("%d " % pdg_of_interest)
        f.write("\n")
        for pdg_of_interest in pdgs_of_interest:
            f.write("%12d " % dndy[pdg_of_interest])
        f.write("\n")

    with open('resonances_v2.txt', 'w') as f:
        f.write("# MUSIC + SMASH simulation, PbPb at 5.02 TeV, measurable rho0 v2\n")
        f.write("# \"Measurable\" rho0 definition: none of its decay products ever collided, el or inel\n")
        f.write("# |y| < 0.5 cut\n")
        f.write("# number of events: %d\n" % nev)
        f.write("# pt[GeV] v2(pt) for pdg  ")
        for pdg_of_interest in pdgs_of_interest:
            f.write("%d " % pdg_of_interest)
        f.write("\n")
        ptbin_centers = 0.5 * (ptbins[1:] + ptbins[:-1])
        for i, pt in enumerate(ptbin_centers):
            f.write("%5.2f" % pt)
            for pdg_of_interest in pdgs_of_interest:
                if (pthist[pdg_of_interest][i] != 0):
                    f.write("%12.6f " % (float(v2[pdg_of_interest][i]) / float(pthist[pdg_of_interest][i])) )
                else:
                    f.write("%12.6f " % 0)
            f.write("\n")


    np.savetxt('destiny_matrix.txt', destiny_matrix_rho0)
