This is the python code for simulating high CO2 induced closure model, by Xiao Gan.
This code uses the multi-level formalism proposed in Gan, X and Albert, R. "General method to find the attractors of discrete dynamic models of biological systems." Physical Review E 97(4): 042308 (2018). 
Notation "$" indicate the state of a node/variable. In a Boolean model such as the high CO2 induced closure model, nodes states are limited to "$0" for OFF and "$1" for ON. 
The multi-level formalism is less computationally efficient in simulating Boolean models. Thus, we also recommend Cubewalker (ref: arxiv preprint), as a more recent and more efficient simulation tool for Boolean dynamic models.

"Simulation_CO2network_test.py" is the main simulation file. Python environment and some packages are necessary to run this simulation. 
A sample input file, "CO2model_2023_0726.txt", is included in the code folder. The code will generate an output file "sample.xlsx". A sample output file with explanations how to read it, "sample_output.xlsx", is also included in the code folder. 

Possible important lines in the code:
#613: input file
#622: set the number of iterations (default value mentioned in the paper is 1000; I set it to 20 for a quick demo), #623: timestep as mentioned in the paper (default=30)
#628: set the node being monitored. The default is the node "closure", with value "-1". This number is determined from the ordered number of the nodes in the input file. Closure is the last node in the input file, so its corresponding value is -1. 
#655: set the simulation to be full perturbation list of all nodes. This lead to the simulated CPC values. 
#656: set the simulation to repeat 200 iterations of high CO2 induced closure. This simulation is used to determine the "Close to Wildtype" category of closure response. 
#666: This line defines the initial condition of the nodes in a simulation. Any unspecified node will initialize at "$0", i.e. "OFF"

A full perturbation simulation may take many hours, or longer, depending on computational hardware.

Sample output with iteration1=20 and timestep=30 (using Pythonscript):

>>> 
*** Remote Interpreter Reinitialized ***
['high_CO2', 'CA14', 'CO2_porins', 'CO2_entry_of_cell', 'HCO3', 'RHC1', 'MPKs', 'MPKsHT1complex', 'HT1', 'CBC12', 'ABA', 'OST1_basal', 'OST1_activated', 'GHR1', 'MPKs_kinase', 'ABI1', 'ABI2', 'HAB1', 'RbohDF', 'CIS', 'cADPR', 'ADPRc', '8nitro_cGMP', 'cGMP', 'NOGC', 'NIA1/2', 'NO', 'ROS', 'CaIM', 'Cac', 'Ca_ATPase', 'CPKs', 'SLAC1_CO2', 'SLAC1_nonCO2', 'AnionEM', 'QUAC1', 'H+_ATPase', 'KEV', 'Depolarization', 'KOUT', 'K+_efflux', 'Aquaporins', 'H2O_Efflux', 'Closure']
Monitoring:
Closure -1
Perturbed: []
Perturbed: ['high_CO2$0']
Perturbed: ['high_CO2$1']
Perturbed: ['CA14$0']
Perturbed: ['CA14$1']
Perturbed: ['CO2_porins$0']
Perturbed: ['CO2_porins$1']
Perturbed: ['CO2_entry_of_cell$0']
Perturbed: ['CO2_entry_of_cell$1']
Perturbed: ['HCO3$0']
Perturbed: ['HCO3$1']
Perturbed: ['RHC1$0']
Perturbed: ['RHC1$1']
Perturbed: ['MPKs$0']
Perturbed: ['MPKs$1']
Perturbed: ['MPKsHT1complex$0']
Perturbed: ['MPKsHT1complex$1']
Perturbed: ['HT1$0']
Perturbed: ['HT1$1']
Perturbed: ['CBC12$0']
Perturbed: ['CBC12$1']
Perturbed: ['ABA$0']
Perturbed: ['ABA$1']
Perturbed: ['OST1_basal$0']
Perturbed: ['OST1_basal$1']
Perturbed: ['OST1_activated$0']
Perturbed: ['OST1_activated$1']
Perturbed: ['GHR1$0']
Perturbed: ['GHR1$1']
Perturbed: ['MPKs_kinase$0']
Perturbed: ['MPKs_kinase$1']
Perturbed: ['ABI1$0']
Perturbed: ['ABI1$1']
Perturbed: ['ABI2$0']
Perturbed: ['ABI2$1']
Perturbed: ['HAB1$0']
Perturbed: ['HAB1$1']
Perturbed: ['RbohDF$0']
Perturbed: ['RbohDF$1']
Perturbed: ['CIS$0']
Perturbed: ['CIS$1']
Perturbed: ['cADPR$0']
Perturbed: ['cADPR$1']
Perturbed: ['ADPRc$0']
Perturbed: ['ADPRc$1']
Perturbed: ['8nitro_cGMP$0']
Perturbed: ['8nitro_cGMP$1']
Perturbed: ['cGMP$0']
Perturbed: ['cGMP$1']
Perturbed: ['NOGC$0']
Perturbed: ['NOGC$1']
Perturbed: ['NIA1/2$0']
Perturbed: ['NIA1/2$1']
Perturbed: ['NO$0']
Perturbed: ['NO$1']
Perturbed: ['ROS$0']
Perturbed: ['ROS$1']
Perturbed: ['CaIM$0']
Perturbed: ['CaIM$1']
Perturbed: ['Cac$0']
Perturbed: ['Cac$1']
Perturbed: ['Ca_ATPase$0']
Perturbed: ['Ca_ATPase$1']
Perturbed: ['CPKs$0']
Perturbed: ['CPKs$1']
Perturbed: ['SLAC1_CO2$0']
Perturbed: ['SLAC1_CO2$1']
Perturbed: ['SLAC1_nonCO2$0']
Perturbed: ['SLAC1_nonCO2$1']
Perturbed: ['AnionEM$0']
Perturbed: ['AnionEM$1']
Perturbed: ['QUAC1$0']
Perturbed: ['QUAC1$1']
Perturbed: ['H+_ATPase$0']
Perturbed: ['H+_ATPase$1']
Perturbed: ['KEV$0']
Perturbed: ['KEV$1']
Perturbed: ['Depolarization$0']
Perturbed: ['Depolarization$1']
Perturbed: ['KOUT$0']
Perturbed: ['KOUT$1']
Perturbed: ['K+_efflux$0']
Perturbed: ['K+_efflux$1']
Perturbed: ['Aquaporins$0']
Perturbed: ['Aquaporins$1']
Perturbed: ['H2O_Efflux$0']
Perturbed: ['H2O_Efflux$1']
Perturbed: ['Closure$0']
Perturbed: ['Closure$1']
--- 278.3234586715698 seconds ---
Current time: 
20:38:31
        Perturbation  Closure
0                 []        0
1     ['high_CO2$0']        0
2     ['high_CO2$1']        1
3         ['CA14$0']        0
4         ['CA14$1']        0
..               ...      ...
84  ['Aquaporins$1']        0
85  ['H2O_Efflux$0']        0
86  ['H2O_Efflux$1']        1
87     ['Closure$0']        0
88     ['Closure$1']        1

[89 rows x 2 columns]
>>> 


