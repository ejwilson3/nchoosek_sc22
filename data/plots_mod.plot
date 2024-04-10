set terminal png size 525,375 font ',12'
set output 'dwave_accuracy.png'
set xlabel 'Number of Qubits'
set ylabel 'Fraction of Optimal Results'
set key box top right
plot[:300]   '1_ocean_output.dat' using 4:5 with p ps 1.1 pt 4 title "Max Cut", \
             '0_ocean_output.dat' using 4:5 with p ps 1.1 pt 6 title "Vertex Cover", \
             '4_ocean_output.dat' using 4:5 with p ps 1.1 pt 8 title "Min Set", \
             '5_ocean_output.dat' using 4:1 with p ps 1.1 pt 9 title "Exact Set", \
             '2_ocean_output.dat' using 4:1 with p ps 1.1 pt 5 title "Clique Cover", \
             '3_ocean_output.dat' using 4:1 with p ps 1.1 pt 7 title "Map Color", \
             '6_ocean_output.dat' using 4:1 with p ps 1.1 pt 11 title "SAT3"

set output 'ibm_depth.png'
set key box top left
set xlabel 'Number of Constraints'
set ylabel 'Circuit Depth'
plot[:150]  '1_qiskit_output.dat' using 3:7 with p ps 1.1 pt 4 title "Max Cut", \
            '0_qiskit_output.dat' using 3:7 with p ps 1.1 pt 6 title "Vertex Cover", \
            '4_qiskit_output.dat' using 3:7 with p ps 1.1 pt 8 title "Min Set", \
            '5_qiskit_output.dat' using 3:7 with p ps 1.1 pt 9 title "Exact Set", \
            '2_qiskit_output.dat' using 3:7 with p ps 1.1 pt 5 title "Clique Cover", \
            '3_qiskit_output.dat' using 3:7 with p ps 1.1 pt 7 title "Map Color", \
            '6_qiskit_output.dat' using 3:7 with p ps 1.1 pt 11 title "3-SAT"

set output 'ibm_valid_depth.png'
set key box off
set ylabel 'Circuit Depth'
set xlabel ' '
set xtics ('Max Cut' 1, 'Vertex Cover' 2, 'Min Set' 3, 'Exact Set' 4, 'Clique Cover' 5, 'Map Color' 6, '3-SAT' 7) rotate by 45 right
plot[0:8][:400] '0_qiskit_output.dat' using 8:7 every :::1::1 with p ps 1.1 pt 6 lc 2 title "", \
                '0_qiskit_output.dat' using 8:7 every :::2::2 with p ps 1.1 pt 2 lc 8 title "", \
                '1_qiskit_output.dat' using 8:7 every :::1::1 with p ps 1.1 pt 4 lc 1 title "", \
                '1_qiskit_output.dat' using 8:7 every :::2::2 with p ps 1.1 pt 2 lc 8 title "", \
                '2_qiskit_output.dat' using 8:7 every :::1::1 with p ps 1.1 pt 5 lc 5 title "Optimal", \
                '2_qiskit_output.dat' using 8:7 every :::2::2 with p ps 1.1 pt 2 lc 8 title "Suboptimal", \
                '3_qiskit_output.dat' using 8:7 every :::1::1 with p ps 1.1 pt 7 lc 6 title "", \
                '3_qiskit_output.dat' using 8:7 every :::2::2 with p ps 1.1 pt 2 lc 8 title "", \
                '4_qiskit_output.dat' using 8:7 every :::1::1 with p ps 1.1 pt 8 lc 3 title "", \
                '4_qiskit_output.dat' using 8:7 every :::2::2 with p ps 1.1 pt 2 lc 8 title "", \
                '5_qiskit_output.dat' using 8:7 every :::1::1 with p ps 1.1 pt 9 lc 4 title "", \
                '5_qiskit_output.dat' using 8:7 every :::2::2 with p ps 1.1 pt 2 lc 8 title "", \
                '6_qiskit_output.dat' using 8:7 every :::1::1 with p ps 1.1 pt 11 lc 7 title "", \
                '6_qiskit_output.dat' using 8:7 every :::2::2 with p ps 1.1 pt 2 lc 8 title ""

set output 'ibm_valid_qubits.png'
set ylabel 'Number of Qubits Used'
plot[0:8]       '0_qiskit_output.dat' using 8:4 every :::1::1 with p ps 1.1 pt 6 lc 2  title "", \
                '0_qiskit_output.dat' using 8:4 every :::2::2 with p ps 1.1 pt 2 lc 8  title "", \
                '1_qiskit_output.dat' using 8:4 every :::1::1 with p ps 1.1 pt 4 lc 1  title "", \
                '1_qiskit_output.dat' using 8:4 every :::2::2 with p ps 1.1 pt 2 lc 8  title "", \
                '2_qiskit_output.dat' using 8:4 every :::1::1 with p ps 1.1 pt 5 lc 5  title "Optimal", \
                '2_qiskit_output.dat' using 8:4 every :::2::2 with p ps 1.1 pt 2 lc 8  title "Suboptimal", \
                '3_qiskit_output.dat' using 8:4 every :::1::1 with p ps 1.1 pt 7 lc 6  title "", \
                '3_qiskit_output.dat' using 8:4 every :::2::2 with p ps 1.1 pt 2 lc 8  title "", \
                '4_qiskit_output.dat' using 8:4 every :::1::1 with p ps 1.1 pt 8 lc 3  title "", \
                '4_qiskit_output.dat' using 8:4 every :::2::2 with p ps 1.1 pt 2 lc 8  title "", \
                '5_qiskit_output.dat' using 8:4 every :::1::1 with p ps 1.1 pt 9 lc 4  title "", \
                '5_qiskit_output.dat' using 8:4 every :::2::2 with p ps 1.1 pt 2 lc 8  title "", \
                '6_qiskit_output.dat' using 8:4 every :::1::1 with p ps 1.1 pt 11 lc 7 title "", \
                '6_qiskit_output.dat' using 8:4 every :::2::2 with p ps 1.1 pt 2 lc 8  title ""

