for filename in ['0_ocean_output.dat', '1_ocean_output.dat', '2_ocean_output.dat', '0_qiskit_output.dat','1_qiskit_output.dat', '2_qiskit_output.dat', '0_z3_output.dat','1_z3_output.dat','2_z3_output.dat']:
    file = open(filename, 'r')
    lines = file.read().splitlines()
    file.close()
    if len(lines) > 0:
        good = []
        bad = []
        file = open(filename, 'w')
        for line in lines:
            if line:
                if line[0] == '0':
                    bad.append(line + "\n")
                elif line[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    good.append(line + "\n")
        file.write(lines[0] + "\n")
        file.write("\n")
        for line in good:
            file.write(line)
        file.write("\n")
        for line in bad:
            file.write(line)
        file.close()
