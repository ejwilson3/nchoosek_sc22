import sys
sys.path.append('/Users/ejwilson/nchoosek/NchooseK')
import nchoosek
import qiskit
from nchoosek import solver
from nchoosek.solver import construct_qubo
import qiskit
import datetime
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
from qiskit.utils import QuantumInstance
from typing import Optional

import logging

class COBYLA_wrapper(COBYLA):
    
    def __init__(
        self,
        time_vector1,
        time_vector2,
        maxiter: int = 1000,
        disp: bool = False,
        rhobeg: float = 1.0,
        tol: Optional[float] = None,
        options: Optional[dict] = None,
        **kwargs,
    ) -> None:
    
        self._time_vector1 = time_vector1
        self._time_vector2 = time_vector2
        super().__init__(maxiter=maxiter, disp=disp, rhobeg=rhobeg, tol=tol, options=options, **kwargs)

    def minimize(self, fun, x0, jac=None, bounds=None):
        # print(self.get_support_level())
        self._time_vector1.append(datetime.datetime.now())
        # print(type(super()))
        ret = super().minimize(fun, x0, jac=jac, bounds=bounds)
        self._time_vector2.append(datetime.datetime.now()) 
        return ret

def time_run(env, quantum_instance):
    # If there is no quantum_instance given, run it on a simulator on the
    # computer running the program.
    if not quantum_instance:
        backend = qiskit.Aer.get_backend('qasm_simulator')
        quantum_instance = QuantumInstance(backend)

    # Convert the environment to a QUBO.
    construct_time_start = datetime.datetime.now()
    qubo = construct_qubo(env, None)

    # Set up a QuadraticProgram for Qiskit.
    prog = QuadraticProgram('nck')
    for var in {e for qs in qubo for e in qs}:
        prog.binary_var(var)
    prog.minimize(quadratic=qubo)
    construct_time_end = datetime.datetime.now()
    print("Construction time:")
    print(construct_time_end - construct_time_start)

    time1 = datetime.datetime.now()
    time_starts = []
    time_ends = []
    optimizer = COBYLA_wrapper(time_starts, time_ends)
    # This runs the problem as a QAOA.
    qaoa = MinimumEigenOptimizer(QAOA(optimizer=COBYLA_wrapper(time_starts, time_ends), reps=1,
    # qaoa = MinimumEigenOptimizer(QAOA(optimizer=COBYLA(), reps=1,
                                 quantum_instance=quantum_instance))
    result = qaoa.solve(prog)
    ret = solver.QiskitResult()

    ret.solutions = []
    ret.solutions.append({k: v != 0 for k, v in result.variables_dict.items() if k in env.ports()})
    # Record this time now to ensure that the QAOA is done running first.
    time2 = datetime.datetime.now()
    ret.times = (time1, time2)
    ret.tallies = [1]
    ret.quantum_instance = quantum_instance

    # Convert the result to a mapping from port names to Booleans and
    # return it.
    ports = env.ports()
    # print(optimizer._time_vector1)
    print("Optimization time:")
    for i in range(len(optimizer._time_vector1)):
        print(optimizer._time_vector2[i] - optimizer._time_vector1[i])
    return ret

if __name__ == '__main__':
    from run_problems import min_vert_cover
    logging.basicConfig(filename='log.log', level=logging.DEBUG)
    qiskit.IBMQ.load_account()
    provider = qiskit.IBMQ.get_provider(hub='ibm-q', group='open', project='main')
    # device = qiskit.Aer.get_backend('aer_simulator')
    device = provider.get_backend('ibm_perth')
    quantum_instance = QuantumInstance(device)
    V = ['a', 'b', 'c', 'd', 'e', 'f']
    # V = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    E = [('a', 'b'), ('a', 'c'), ('b', 'c'), ('d', 'e'), ('d', 'f'), 
        ('e', 'f'), ('a', 'd'), ('b', 'e')]
    env = min_vert_cover(V, E)
    res = time_run(env, quantum_instance)
    print(res)
    tdict = {}
    for ID in res.jobIDs():
        job = res.quantum_instance.backend.retrieve_job(ID)
        times = job.time_per_step()
        typ = set()
        for key in times:
            typ.add(key)
            for key2 in times:
                if key2 in typ:
                    continue
                timename = key2 + "-" + key
                if timename not in tdict:
                    tdict[timename] = 0
                tdict[timename] += (times[key2] - times[key]).total_seconds()
    f = open("time.dat", 'a')
    f.write(str(res))
    f.write(tdict)
    f.close()
