import os
import sys
import qiskit
from qiskit.utils import QuantumInstance
import datetime
import nchoosek
import re
from dimod import SimulatedAnnealingSampler

def min_vert_cover(V, E):
    env = nchoosek.Environment()
    for vert in V:
        env.register_port(vert)
    for edge in E:
        env.nck([edge[0], edge[1]], {1, 2})
    env.minimize(V)
    return env

def max_cut(V, E):
    env = nchoosek.Environment()
    for vert in V:
        env.register_port(vert)
    for edge in E:
        env.different(edge[0], edge[1], soft=True)
    return env

def clique_cover(V, E, nCliques):
    env = nchoosek.Environment()
    # One hot encoding: each vertex is part of one clique.
    for vert in V:
        N = []
        for clique in range(nCliques):
            var = vert + str(clique)
            env.register_port(var)
            N.append(var)
        env.nck(N, {1})
    # Check every vertex pair; if they aren't connected, add nCliques constraints
    for idx, vert1 in enumerate(V[:-1]):
        for vert2 in V[idx+1:]:
            if ((vert1, vert2) not in E) and ((vert2, vert1) not in E):
                for clique in range(nCliques):
                    var1 = vert1 + str(clique)
                    var2 = vert2 + str(clique)
                    env.nck([var1, var2], {0, 1})
    return env

def run_graph(V, E, nCliques, solver, simulator=False, time_filename='times.dat', results_filename='results.dat', data_filename='output.dat', quantum_instance=None, nQubs=2000, num_reads=100):
    # list of environments
    envs = []
    # list of lists of results
    results = []
    # list of lists of how often the result showed up; relevant only to ocean solver
    total_counts = []
    # list of environments for comparing soft constraints
    check_envs = []
    # list of results for comparing soft constraints
    check = []
    # list of times used in the solver; used primarily for qiskit solver in order to collect the jobs
    times = []
    # list of how many results satisfied all hard constraints. The number will only be more than one for the ocean solver
    good_counts = []
    # list of how many results had the maximum number of soft constraints met. The number will only be more than one for the ocean solver
    opt_counts = []
    # list of number of physical qubits used
    n_qubs = []
    # list of number of jobs used for qiskit solver
    n_jobs = []
    # list of circuit depths used for qiskit solver
    depths = []
    job_ids = []
    envs.append(min_vert_cover(V, E))
    check_envs.append(min_vert_cover(V, E))
    envs.append(max_cut(V, E))
    check_envs.append(max_cut(V, E))
    # clique cover uses more qubits than the others
    if len(V)*nCliques <= nQubs:
        envs.append(clique_cover(V, E, nCliques))
        check_envs.append(clique_cover(V, E, nCliques))
    else:
        envs.append(None)
        check_envs.append(None)
    times.append(datetime.datetime.now())

    # Run all the problems and record the results
    for idx, env in enumerate(envs):
        # Add None to the lists in order to keep indices in line
        if not env:
            results.append(None)
            total_counts.append(None)
            opt_counts.append(None)
            good_counts.append(None)
            n_qubs.append(None)
            times.append(datetime.datetime.now())
            continue
        # Run the actual problem and add it to the lists
        if solver == 'qiskit':
            res = env.solve(solver=solver, quantum_instance=quantum_instance)
        elif solver == 'ocean':
            if simulator:
                res = env.solve(solver=solver, sampler=SimulatedAnnealingSampler(), num_reads=num_reads)
            else:
                res = env.solve(solver=solver, num_reads=num_reads)
        else:
            res = env.solve(solver=solver)
        results.append(res.solutions)
        total_counts.append(res.tallies)
        # Get the classically optimized solution; this is needed in order to test whether our result is the actual maximum or minimum
        ch = check_envs[idx].solve(solver='z3')
        check.append(ch.solutions[0])
        # This checks how many runs satisfied the constraints
        v = 0
        # This checks how many runs optimized the constraints
        count = 0
        # Compare the quality of the results to this value
        check_quality = check_envs[idx].quality(check[idx])
        for r_idx, result in enumerate(res.solutions):
            if res.tallies:
                add = res.tallies[r_idx]
            else:
                add = 1
            if env.valid(result):
                v += add
            if env.quality(result) == check_quality:
                count += add
        opt_counts.append(count)
        good_counts.append(v)
        n_qubs.append(res.qubits)
        depths.append(res.depth)
        n_jobs.append(res.jobs)
        job_ids.append(res.jobIDs)
        times.append(datetime.datetime.now())

    # Qiskit solver needs to inspect the jobs

    with open(time_filename, 'a') as f:
        f.write(str(len(V)) + ", " + str(len(V) * nCliques) + ", " + str(len(E)) + '\n')
        for time in times:
            f.write(str(time) + "\n")
    with open(results_filename, 'a') as f:
        for idx, result in enumerate(results):
            f.write(str(result) + "\n")
            f.write(str(total_counts[idx]) + "\n")
    for idx, env in enumerate(envs):
        good = []
        bad = []
        name = str(idx%3)
        if env:
            item =  str(good_counts[idx]) + ", " + \
                    str(len(env.ports())) + ", " + \
                    str(len(env.constraints())) + ", " + \
                    str(n_qubs[idx]) + ", " + \
                    str(opt_counts[idx]) + ", " + \
                    str(n_jobs[idx]) + ", " + \
                    str(depths[idx]) + ", " + \
                    str(int(name) + 1) + "\n"
            if good_counts[idx] > 0:
                good.append(item)
            else:
                bad.append(item)
        with open(name + '_' + solver + '_' + data_filename, 'a') as f:
            f.write("\n")
            for item in good:
                f.write(item)
            f.write("\n")
            for item in bad:
                f.write(item)

    return envs
        
if len(sys.argv) == 1:
    solver = 'z3'
else:
    solver = str(sys.argv[1])
    if solver != 'qiskit' and solver != 'ocean' and solver != 'z3':
        print(str(sys.argv[1]) + " solver not implemented; using z3 solver")
        solver = 'z3'
if len(sys.argv) < 4:
    simulator = True
else:
    simulator = False

if solver == 'qiskit':    
    qiskit.IBMQ.load_account()
    # provider = qiskit.IBMQ.get_provider(hub='ibm-q-ncsu', group='nc-state', project='noise')
    provider = qiskit.IBMQ.get_provider(hub='ibm-q', group='open', project='main')
    if simulator:
        device = qiskit.Aer.get_backend('qasm_simulator')
        # device = provider.get_backend('ibmq_qasm_simulator')
    else:
#########################Change machine here####################################
        device = provider.get_backend('ibmq_guadalupe')
################################################################################
    nqubs = device.configuration().n_qubits
    quantum_instance = QuantumInstance(device)
else:
    quantum_instance = None
    if solver == 'ocean':
        nqubs = 3000
    else:
        nqubs = 1000

nqubs=6
V = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
     'n', 'o', 'p', 'q', 'r', 'x', 'y', 'z', 's', 't', 'u', 'v', 'w',
     'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 
     'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz',
     'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am', 'an',
     'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az',
     'ba', 'bc', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bk', 'bl', 'bm', 'bn',
     'bo', 'bp', 'bq', 'br', 'bs', 'bt', 'bu', 'bv', 'bw', 'bx', 'by', 'bz',
     'ca', 'cb', 'cd']
E = [('a', 'b'), ('a', 'c'), ('b', 'c'), ('d', 'e'), ('d', 'f'), 
     ('e', 'f'), ('a', 'd'), ('b', 'e'), ('g', 'h'), ('h', 'i'),
     ('g', 'i'), ('g', 'b'), ('h', 'c'), ('j', 'k'), ('j', 'l'),
     ('k', 'l'), ('j', 'c'), ('k', 'a'), ('m', 'n'), ('n', 'o'),
     ('m', 'o'), ('m', 'f'), ('n', 'f'), ('p', 'r'), ('p', 'q'),
     ('q', 'r'), ('p', 'i'), ('q', 'i'), ('x', 'p'), ('x', 'q'),
     ('x', 'r'), ('y', 'm'), ('y', 'n'), ('y', 'o'), ('z', 'j'),
     ('z', 'k'), ('z', 'l'), ('s', 'n'), ('t', 'i'), ('s', 't'),
     ('s', 'u'), ('t', 'u'), ('v', 'w'), ('v', 'aa'), ('w', 'aa'),
     ('v', 'a'), ('w', 'k'), ('bb', 'cc'), ('bb', 'dd'), ('cc', 'dd'),
     ('bb', 'aa'), ('cc', 's'), ('ee', 'ff'), ('ee', 'gg'), ('ff', 'gg'),
     ('ee', 'h'), ('ff', 'r'), ('hh', 'ii'), ('ii', 'jj'), ('jj', 'kk'),
     ('kk', 'hh'), ('jj', 'j'), ('kk', 'll'), ('ll', 'mm'), ('mm', 'nn'),
     ('nn', 'oo'), ('oo', 'll'), ('pp', 'qq'), ('qq', 'rr'), ('rr', 'ss'),
     ('ss', 'pp'), ('qq', 'z'), ('tt', 'uu'), ('vv', 'ww'), ('ww', 'xx'),
     ('uu', 'vv'), ('xx', 'tt'), ('tt', 'ww'), ('vv', 'r'), ('xx', 'o'),
     ('yy', 'zz'), ('zz', 'ab'), ('ab', 'ac'), ('ac', 'ad'), ('ad', 'yy'),
     ('yy', 'ab'), ('yy', 'ad'), ('zz', 'ac'), ('ab', 'b'), ('ad', 'l'),
     ('ae', 'af'), ('af', 'ag'), ('ag', 'ah'), ('ah', 'ai'), ('ai', 'ae'),
     ('ae', 'ag'), ('ae', 'ah'), ('af', 'ai'), ('ag', 'g'), ('ah', 'h'),
     ('aj', 'ak'), ('ak', 'al'), ('al', 'am'), ('am', 'an'), ('an', 'aj'),
     ('aj', 'al'), ('aj', 'am'), ('al', 'll'), ('am', 'mm'), ('ak', 'an'),
     ('ao', 'ap'), ('ap', 'aq'), ('aq', 'ar'), ('ar', 'as'), ('at', 'au'),
     ('au', 'av'), ('aw', 'ax'), ('av', 'aw'), ('ax', 'ao'), ('as', 'at'),
     ('ao', 'ar'), ('ap', 'as'), ('aq', 'at'), ('ar', 'au'), ('as', 'av'),
     ('at', 'aw'), ('au', 'ax'), ('av', 'ao'), ('aw', 'ap'), ('ax', 'aq'),
     ('ao', 'oo'), ('aq', 'qq'), ('as', 'ss'), ('au', 'uu'), ('aw', 'ww'),
     ('ay', 'az'), ('az', 'ba'), ('ba', 'bc'), ('bc', 'bd'), ('bi', 'ay'),
     ('bd', 'be'), ('be', 'bf'), ('bf', 'bg'), ('bg', 'bh'), ('bh', 'bi'),
     ('ay', 'bc'), ('az', 'bd'), ('ba', 'be'), ('bc', 'bf'), ('bd', 'bg'),
     ('be', 'bh'), ('bf', 'bi'), ('bg', 'ay'), ('bh', 'az'), ('bi', 'bc'),
     ('ay', 'yy'), ('ba', 'aa'), ('bd', 'dd'), ('bf', 'ff'), ('bh', 'hh'),
     ('bj', 'bk'), ('bk', 'bl'), ('bl', 'bm'), ('bm', 'bn'), ('bn', 'bo'),
     ('bo', 'bp'), ('bp', 'bq'), ('bq', 'br'), ('br', 'bs'), ('bs', 'bj'),
     ('bj', 'bm'), ('bk', 'bn'), ('bl', 'bo'), ('bm', 'bp'), ('bn', 'bq'),
     ('bo', 'br'), ('bp', 'bs'), ('bq', 'bj'), ('br', 'bk'), ('bs', 'bl'),
     ('bj', 'jj'), ('bl', 'al'), ('bn', 'an'), ('bp', 'ap'), ('bs', 'as'),
     ('bt', 'bu'), ('bu', 'bv'), ('bv', 'bw'), ('bw', 'bx'), ('bx', 'by'),
     ('by', 'bz'), ('bz', 'ca'), ('ca', 'cb'), ('cb', 'cd'), ('cd', 'bt'),
     ('bt', 'bw'), ('bu', 'bx'), ('bv', 'by'), ('bw', 'bz'), ('bx', 'ca'),
     ('by', 'cb'), ('bz', 'cd'), ('ca', 'bt'), ('cb', 'bu'), ('cd', 'bv'),
     ('bt', 'at'), ('bv', 'av'), ('bx', 'ax'), ('bz', 'az'), ('cb', 'ab')]
edge_length = [3, 8, 13, 18, 23, 28, 37, 42, 47, 52, 57, 62, 67, 72, 80, 90, 100, 110, 135, 160, 185, 210]
for i, j in enumerate([3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 37, 41, 45, 50, 55, 60, 65, 75, 85, 95, 105]):
    if j > nqubs:
        break 
    run_graph(V[:j], E[:edge_length[i]], i+1, solver, simulator=simulator, quantum_instance=quantum_instance, nQubs=nqubs)

E = [('a', 'b'), ('a', 'c'), ('b', 'c'), ('d', 'e'), ('d', 'f'), 
     ('e', 'f'), ('a', 'd'), ('b', 'e'), ('g', 'h'), ('h', 'i'),
     ('g', 'i'), ('g', 'b'), ('h', 'c'), ('j', 'k'), ('j', 'l'),
     ('k', 'l'), ('j', 'c'), ('k', 'a'), ('i', 'l'), ('f', 'l'),
     ('f', 'i'), ('j', 'd'), ('j', 'g'), ('g', 'd'), ('k', 'e'),
     ('k', 'h'), ('e', 'h'), ('l', 'a'), ('c', 'd'), ('f', 'g'), 
     ('i', 'j'), ('a', 'i'), ('b', 'l'), ('c', 'f'), ('b', 'h'),
     ('b', 'k'), ('e', 'g'), ('l', 'c'), ('f', 'h'), ('i', 'k'),
     ('a', 'g'), ('d', 'i'), ('j', 'e'), ('j', 'b'), ('a', 'e'),
     ('c', 'g'), ('g', 'k'), ('g', 'l'), ('d', 'h'), ('f', 'a'),
     ('i', 'c'), ('d', 'k'), ('b', 'f'), ('l', 'h'), ('b', 'i'),
     ('c', 'k'), ('i', 'e'), ('f', 'j'), ('b', 'd'), ('c', 'e'),
     ('f', 'k'), ('l', 'd'), ('l', 'e')]
edge_length = [24, 31, 37, 43, 48, 54, 60, 63]
for i, j in enumerate([12, 12, 12, 12, 12, 12, 12, 12]):
    if j > nqubs:
        break 
    run_graph(V[:j], E[:edge_length[i]], 4, solver, simulator=simulator, quantum_instance=quantum_instance, nQubs=nqubs)
