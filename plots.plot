set terminal png size 525,375 font ',12'
set output 'dwave_validity.png'
set xlabel 'Number of Qubits'
set ylabel 'Percent Valid'
set title 'DWave Validity by Qubits used'
set key box top right
plot        '0_ocean_output.dat' using 4:1 with p ps 2 title "Vertex Cover", \
            '1_ocean_output.dat' using 4:1 with p ps 2 title "Max Cut", \
            '2_ocean_output.dat' using 4:1 with p ps 2 title "Clique Cover"

set output 'ibm_depth.png'
set key box top left
set xlabel 'Number of Constraints'
set ylabel 'Circuit Depth'
set title 'IBM Circuit Depth Based on Number of NchooseK Constraints'
plot        '0_qiskit_output.dat' using 3:7 with p ps 2 title "Vertex Cover", \
            '1_qiskit_output.dat' using 3:7 with p ps 2 title "Max Cut", \
            '2_qiskit_output.dat' using 3:7 with p ps 2 title "Clique Cover"

set output 'ibm_valid_depth.png'
set xlabel 'Circuit Depth'
set ylabel 'Problem Performed'
set title 'IBM Physical Validity Based on Depth of Circuits'
plot[:350][0:4] '0_qiskit_output.dat' using 7:1 every :::1::1 with p ps 2 pt 1 lc 1 title "", \
                # '0_qiskit_output.dat' using 7:1 every :::2::2 with p ps 2 pt 2 lc 2 title "", \
                '1_qiskit_output.dat' using 7:1 every :::1::1 with p ps 2 pt 1 lc 1 title "", \
                # '1_qiskit_output.dat' using 7:1 every :::2::2 with p ps 2 pt 2 lc 2 title "", \
                '2_qiskit_output.dat' using 7:1 every :::1::1 with p ps 2 pt 1 lc 1 title "Valid"
                # '2_qiskit_output.dat' using 7:1 every :::2::2 with p ps 2 pt 2 lc 2 title "Invalid"

set output 'ibm_valid_qubits.png'
set xlabel 'Number of Qubits Used'
set title 'IBM Physical Validity Based on Number of Qubits'
plot[:][0:4]    '0_qiskit_output.dat' using 4:1 every :::1::1 with p ps 2 pt 1 lc 1 title "", \
                '0_qiskit_output.dat' using 4:1 every :::2::2 with p ps 2 pt 2 lc 2 title "", \
                '1_qiskit_output.dat' using 4:1 every :::1::1 with p ps 2 pt 1 lc 1 title "", \
                '1_qiskit_output.dat' using 4:1 every :::2::2 with p ps 2 pt 2 lc 2 title "", \
                '2_qiskit_output.dat' using 4:1 every :::1::1 with p ps 2 pt 1 lc 1 title "Valid", \
                '2_qiskit_output.dat' using 4:1 every :::2::2 with p ps 2 pt 2 lc 2 title "Invalid"
