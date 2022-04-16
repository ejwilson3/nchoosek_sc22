#!/bin/bash
echo '========================================='
echo 'Installing NchooseK'
echo '========================================='
cd NchooseK
python setup.py install
cd ../
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 0_ocean_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 1_ocean_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 2_ocean_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 0_qiskit_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 1_qiskit_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 2_qiskit_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 0_z3_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 1_z3_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 2_z3_output.dat
echo '========================================='
echo 'Running with Ocean'
echo '========================================='
python run_problems.py ocean simulator
echo 'Running with Qiskit'
echo '========================================='
python run_problems.py qiskit simulator
echo 'Running with Z3'
echo '========================================='
python run_problems.py z3
echo 'Creating Plots'
echo '========================================='
python rearrange.py
gnuplot plots.plot
echo 'Done!'
echo '========================================='
