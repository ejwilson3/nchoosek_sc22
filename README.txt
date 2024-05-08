# If accounts are set up and anaconda is installed, these lines should be enough to run everything:

    sudo apt install gnuplot
    conda env create -f nchoosek_sc22.yaml
    conda activate nchoosek_sc22
    bash run_complete.sh

This contains Programs to run graph problems in NchooseK on three different
architectures: IBM's circuit model machines, DWave's anealling model machines,
and the Microsoft Z3 constraint satisfaction module.

For full operation, you will need to register an account with both DWave and
IBM in order to have access to their physical machines. Replacement scripts can
be run without having accounts. The same type of results will be obtained by
the DWave simulating solver with the exception of number of physical qubits
used: the simulator has full connectivity, and so the number of qubits is the
same as the number of variables. Due to the nature of the Qiskit QAOA interface
(which hides the acutal circuits used), three key pieces of data are
unavailable from the Qiskit Aer simulator: number of physical qubits, circuit
depth, and number of jobs run. The figures in the paper were generated with
access to larger machines than are available to the public.

If you want to recreate the plots in the paper, you will need to install gnuplot. On Ubuntu, this will look something like
    sudo apt install gnuplot

If you want to inspect the data that was used in the paper or to recreate the exact figures, that can be found in the 'data' directory. running
    gnuplot plots_mod.plot
while in that directory will recreate the figures.

The next step is to install anaconda
(https://docs.anaconda.com/anaconda/install/index.html). After that, apply the
included environment, then activate it with the commands:
    conda env create -f nchoosek_sc22.yaml
    conda activate nchoosek_sc22

Next, if you need to register for the machines follow the instructions for IBM:
https://quantum-computing.ibm.com/
and DWave: https://cloud.dwavesys.com/leap/signup/

If you have greater access to IBM devices, search run_problems.py for #Change provider here# to set up your own hub/group/project, and #Change machine here# in order to select a larger device.

Finally, run the appropriate script:
    For both physical machines:
        bash run_complete.sh
    For IBM physical machine and DWave simulator:
        bash run_qiskit.sh
    For DWave physical machine and IBM simulator:
        bash run_ocean.sh
    For both simulators:
        bash run_simulated.sh

If the script exits normally, data and plots will be found in the directory run_[time of running]. If the script exits unexpectedly, they will be found in this directory.
NOTE: the plots might fail if there aren't enough data points for qiskit. This
is normal.
