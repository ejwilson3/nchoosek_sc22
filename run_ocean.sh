#!/bin/bash
date=$(date +%a%d%b_%H-%M)
echo '========================================='
echo 'Installing NchooseK'
echo '========================================='
cd NchooseK
python3 setup.py bdist_egg
cd ../
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 0_ocean_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 1_ocean_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 2_ocean_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 3_ocean_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 4_ocean_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 5_ocean_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 6_ocean_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 0_qiskit_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 1_qiskit_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 2_qiskit_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 3_qiskit_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 4_qiskit_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 5_qiskit_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 6_qiskit_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 0_z3_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 1_z3_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 2_z3_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 3_z3_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 4_z3_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 5_z3_output.dat
echo '# valid, vars, cons, qubits, optimal, jobs, depth, problem' > 6_z3_output.dat
echo '========================================='
echo 'Running with Ocean'
echo '========================================='
python3 run_problems.py ocean
echo 'Running with Qiskit'
echo '========================================='
python3 run_problems.py qiskit simulator
echo 'Running with Z3'
echo '========================================='
python3 run_problems.py z3
echo 'Creating Plots'
echo '========================================='
python3 rearrange.py
gnuplot plots.plot
mkdir run_$date
mv *.dat run_$date
mv *.png run_$date
echo 'Done!'
echo '========================================='
