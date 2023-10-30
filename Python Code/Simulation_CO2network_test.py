#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Xiao Gan
#
# Created:     13/06/2016
# Copyright:   (c) Xiao Gan 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


##import re
##import numpy as np
import networkx as nx
##import matplotlib.pyplot as plt
import copy
##import functions
##import Booleanops
##import StableMotif
##import itertools
import sys
import random
import time
import matplotlib.pyplot as plt
import xlsxwriter
import datetime
import itertools


def evalfunc(function, fullnodelist, cstate, fullstatelist):
    # copied from MultiQM.py
    # read a function, and return with its node and finds the nodes' states from a complete node level array
    # Note: only accept captalized operators e.g. 'AND'.
    nodelist = []
    statelist = []
    if '=' in function:
        function1 = function.split("=",1)[1].strip()
    else:
        function1 = function
##    print function1
    implicants = function1.split("OR")
##    print implicants
    no_brackets = str.maketrans('', '', '()') # remove brackets in the following 'for' loop
    for implicant in implicants:
        implicant1 = (implicant.strip()).translate(no_brackets)
        vnodes = implicant1.split("AND")
        for vnode in vnodes:
            node = vnode.split("$",1)[0].strip()
##            state = vnode.split("$",1)[1].strip()
            if node not in nodelist:
                nodelist.append(node)

    # evaluating the function
    str1 = function1
    for i in range(0,len(fullnodelist)):
    # replace occurences of state nodes with '1's and '0's
    # enumerate a state for this node: correspondent state node =>1, othere nodes =>0
        ON = str(fullnodelist[i]) + '$' + str(cstate[i])
##        print 'ON=',ON
        str1 = str1.replace(ON,'1')
        for state in fullstatelist[i]:
            if str(state) != str(cstate[i]):
                OFF = str(fullnodelist[i]) + '$' + str(state)
##                print 'OFF=',OFF
                str1 = str1.replace(OFF,'0')
    str1 = str1.replace('OR','|')
    str1 = str1.replace('AND','&')
    str1 = str1.replace('NOT','not')
##    print str1
    return eval(str1)


# test example

##y = Reduction.to_list('toy_example1.txt')
##y = 'A$0* = B$0 OR (C$1 AND B$1)'
##fullnodelist = ['A','B','C']
##cstate = [1,1,1]
##fullstatelist = [[0,1],[0,1],[0,1]]
##x = evalfunc(y,fullnodelist, cstate,fullstatelist)
##x = evalfunc('A$0* = B$0 OR (C$1 AND B$1)', ['A', 'B', 'C'], ['1', '0', '0'], [['0', '1', '2'], ['0', '1', '2'], ['0', '1']])
##x = evalfunc('C$0* = NOT (B$1 AND D$1)', ['A', 'B', 'C', 'D'], ['1', '0', '0', '0'], [['0', '1'], ['0', '1'], ['0', '1'], ['0', '1']])
##print x



def nodescan(functionlist,mode=0,subzero=0):
    # find how many original node there is, and how many states each has;
    # (Obsolete) subzero=1: substitute any 'N$0' state nodes with the negation of other node, e.g 'not N$1 and not N$2'
    # TBD: mode=1: show warning of node function errors/issues

    # TBD: replacesib=1: replace undetermined nodes whose sibling nodes are identified. Will not run if replacesib=0.

    # return a list of nodes,a list of states and a list of # states for the corresponding node

    nodelist=[]
    nodestates=[]
    nodestatenumber=[]
    nodehigheststate=[] #record the highest state given in the node name
    newfunctionlist=[]
    Flags=[]
    for words in functionlist:
        vnode = words.split("*",1)[0].strip()
        node = vnode.split("$",1)[0].strip()
        state = vnode.split("$",1)[1].strip()
        function = words.split("=",1)[1].strip()

        if node not in nodelist:
            nodelist.append(node)
            nodestates.append([state])
            nodestatenumber.append(1)
            nodehigheststate.append(state)
            Flags.append(0)
        else:
            # corresponding nodestatenumber +1
            x = nodelist.index(node)
            nodestates[x].append(state)
            nodestatenumber[x] += 1
            if nodehigheststate[x] < state:
                nodehigheststate[x] = state
##                print 'node=',node
##                print 'nodehigheststate=',nodehigheststate
##        if replacesib==1 and not function.isdigit():
##        # check if all sibling nodes has their states identified
##            Flag2=0
##            for words2 in functionlist:
##                vnode2 = words2.split("*",1)[0].strip()
##                node2 = vnode2.split("$",1)[0].strip()
##                state2 = vnode2.split("$",1)[1].strip()
##                function2 = words2.split("=",1)[1].strip()
##                if node ==node2 and state != state2:
##                    # only continues if Flag2<=1
##                    if function2==1:
##                        Flag2 +=1
##                        if Flag2 >=2:
##                            break
##                    elif not function2.isdigit():
##                        Flag2 = 'x'
##                        break
##            if Flag2 ==0 :
##            # reconstruct the function
##                result= vnode + '* = ' + function
##            elif Flag2==1 :
##                result= vnode + '* = ' + 1
##            newfunctionlist.append(result)


##    print nodelist
    if mode==1:
        for i in range(0,len(nodelist)):
##            print i
##            print 'node=',nodelist[i]
##            print nodehigheststate[i]
##            print nodestatenumber[i]
            if int(nodehigheststate[i]) != (nodestatenumber[i]-1):
                print ('warning: node {} has number of states that does not match: max state {}, total states {}'.format(nodelist[i],nodehigheststate[i],nodestatenumber[i]-1))
##            print '------'
    # substituting zero states (not needed anymore)
    if subzero ==1:
        removable = ['(',')',' ']
        for words in functionlist:
            # put a space before each '(', if there hasn't been a space
            str2 = ''
            if len(words)>=1:
                for i in range(0,len(words)):
                    if str2 != '':
                        if (words[i]=='(') and (str2[i-1] != ' '):
                            str2 += ' '
                    str2 += words[i]
                words = str2

            vnode = words.split("*",1)[0].strip()
            node = vnode.split("$",1)[0].strip()
            state = vnode.split("$",1)[1].strip()
            function = words.split("=",1)[1].strip()
    ##        print 'state=',state
            if state != 0: # always true
    ##            print function
                # find zero states in the function
                result= vnode + '* = '
                for item in function.split():
    ##                print item
                    result1=''
                    end=''
                    if len(item)>=2:
                        while item[0] in removable:  # remove symbols in 'removable' category
                            result += item[0]
                            item = item[1:len(item)]
                        while item[len(item)-1] in removable:
                            end += item[len(item)-1]
                            item = item[0:len(item)-1]
                        # substitute zero after found
                        if '$' in item:
    ##                        print item
                            nodex = item.split("$",1)[0]
                            statex = item.split("$",1)[1]
                            if not statex.isdigit():
                                print ('ERROR! state is not digit')
                            elif statex =='0':
                                index1 = nodelist.index(nodex)
                                result1 += '('
                                for j in range (0,nodestatenumber[index1]):
                                    if nodestates[index1][j]!='0':
                                        result1 += 'not '
                                        result1 += nodelist[index1]
                                        result1 += '$'
                                        result1 += nodestates[index1][j]
                                        result1 += ' AND '

                                result1 = result1[:len(result1)-5]
                                result1 += ')'
                            else:
                                result1 = item

                            result += result1

                            result += end
                            if result[len(result)-1] != ' ':
                                result += ' '
                        else:
                            result += item
                            if result[len(result)-1] != ' ':
                                result += ' '
                    else:
                        result += item
                        if result[len(result)-1] != ' ':
                            result += ' '
    ##                print 'result=',result
                newfunctionlist.append(result.strip())

    return [nodelist, nodestates, nodestatenumber, nodehigheststate, newfunctionlist]


# test example:
##y = Reduction.to_list('toy_example1.txt')
##print y
##x = nodescan(y,mode=1)
##print x


def to_list(file1): # convert a functions file into a list of strings/functions
    list1=[]
    f = open(file1, 'r')

    words = f.readline()
    while (words[0]==('#')) or (words==''):
        words = f.readline()
    while (words.find("=")!=(-1)):
        list1.append(words.strip())
        words = f.readline()
    return list1


def perturb(functionlist, perturbations):
    # apply perturbations to a functionlist by modifying the corresponding functions. E.g. node A KO => A$0=1, A$1=0
    # functionlist is a list of functions <string>
    # "perturbations" is a list of perturbed states <string>, e.g. ['A$0', 'B$1'] means A KO and B CA (in Boolean).
    if perturbations==[]:
        return functionlist
    # redundant case of no perturbations

    # pre-process the perturbations: create a dictionary to store nodenames (as dictionary keys) and their states.
    nodedict={}
    for item in perturbations:
        node = item.split("$",1)[0].strip()
        state = item.split("$",1)[1].strip()
        nodedict[node]=state

    # Applying perturbation
    newfunctionlist=[]
    for words in functionlist:
        # if function node is present, set perturbation
        vnode = words.split("*",1)[0].strip()
        node = vnode.split("$",1)[0].strip()
        state = vnode.split("$",1)[1].strip()
        function = words
        if node in nodedict: # modify functions
            if nodedict[node]==state:
                function = vnode + '*=' + '1'
            else:
                function = vnode + '*=' + '0'
        newfunctionlist.append(function)
    return newfunctionlist

def pertb_generator(input_list1=[],input_list2=[], mode=0):
    # generator certain mode(s) of perturbation
    # always return an empty set as 1st item, representing unperturbed case
    # if input_list is empty, no inconsistency.
    #
    # mode: 0: single. generate a single perturbation for each item in a perturbationlist, used in a systematic perturbation test
    # mode: 1: combinatorial. Generate perturbation combinations from each combinatorial pair of elements in input list 1&2.
    # mode: 2: combinatorial + all combi of list2. First generate perturbation combinations from each combinatorial pair of elements in input list 2; then combine this list with list1
    perturbationlist=[]
    if mode == 0:
        perturbationlist.append([])
        for item in input_list1:
            perturbationlist.append([item])
    if mode >= 1:
        combi_list2 = []
        if mode ==2:
            for L in range(0, min(3,len(input_list2)+1)): # limit upper limit of L (# perturbation combinations) to 2
                for subset in itertools.combinations(input_list2, L):
                    combi_list2.append(list(subset))
                    # make combinations of elements in list2 up to L (default L=2)
        elif mode==1:
            # make combinations across list 1&2
            combi_list2.append([])
            for item_list2 in input_list2:
                combi_list2.append([item_list2])
##        print combi_list2
        for item_list2 in combi_list2:
            perturbationlist.append(item_list2)
        for item1 in input_list1:
            for item_list2 in combi_list2:
                perturbationlist.append([item1]+item_list2)

    return perturbationlist

# test
##y = to_list('toy_model_XLG_Cac.txt')
##    perturbations = []
##pertb_list1 = []
##pertb_list1 = ['GPA1$0', 'XLG$0']
##pertb_list2 = ['ROS$0', 'CaIM$1','ABI1$0']
##print pertb_generator(input_list1=pertb_list1,input_list2=pertb_list2, mode=2)


def simulate (functionlist_input,timestep,outputmode=0,istates=[],updatescheme=0,stop=0,printresult=0, ABAsignal=[], CO2signal=[]):
    # simulate the trajectory of a model
    # inputs:
    # output mode 0: print ss or trajectory in format: [t (int,timestep; t=-1 means no ss was found), ss state/trajectory (a list)]
    # output mode 1: print in words a steady state or trajectory is found
    # istates is a designated initial state list (as a list of lists). Its default is an empty list, in which case a random initial state will be generated.

    # updatescheme: =0: General async,default; =1: random order async
    # Unchecked: Random-order asynchronous update
    # stop: =1: stop if a steady state is reached.

    # working: ABA and CO2 signal: a list of ABA and CO2 states, used to simulate when the signals are time-dependent

    # TBD perturbationlist: a list of nodes whose states are kept in a perturbation test. E.g. node A knockout is ['A$0']

    functionlist = functionlist_input
    x = nodescan(functionlist)
##    print x
    nodes = x[0]
    fullstatelist =x[1]
    initial_state = []

    if istates ==[]:
        # generate an initial state
        for i in range (0,len(x[0])):
            y = random.choice(x[1][i])
            initial_state.append(y)
    else:
        # generate initial state by randomly choosing states for each '*' state
        for istate in istates:
            for i in range (0,len(x[0])):
                if isinstance(istate[i],int):
##                if  istate[i] == 1 or istate[i] == 0:
                    initial_state.append(str(istate[i]))
                elif istate[i] == '*':
                    # randomly generate a state
                    initial_state.append(random.choice(x[1][i]))
                else:
                    print ('Error in istate format')
                    return

##        initial_state = random.choice(istates)
##    print 'initial state:',initial_state

    trajectory =[initial_state]
    reducedlist = functionlist
    # (Optional TBD) reduction / QM transformation of functions

    cstate = copy.copy(initial_state)

    for t in range(0, timestep):
    # Simulation of: effective trajectory:
    # 1. randomly select a original node index (i,e, a set of functions corresponding to the same node), then simulate
   	# 2. if result is same, remove this index (i.e. this set of functions), then go to 1
	# 3. if all results are same (no function left), reached a steady state attractors

##        print cstate
        list1 = reducedlist
        indexrange1 = list(range(len(nodes)))
        # pre-determin the perturbed nodes:

        Flag1 = 0
##        trajectory.append(cstate)
        states = []
        for i in indexrange1:
            states.append(nodes[i]+'$'+cstate[i])
            if nodes[i]=='ABA' and ABAsignal!=[]:
                states[i]= nodes[i]+'$'+ABAsignal[t]
            if nodes[i]=='high_CO2' and CO2signal!=[]:
                states[i]= nodes[i]+'$'+CO2signal[t]
##        print states

        if updatescheme==0:
        # General Async
            while (Flag1==0 and indexrange1 !=[]):
                index1 = random.choice(indexrange1)
    ##            print 'index1=',index1, 'node:', nodes[index1]
    ##            newstate = '@'

                # evaluate new state, by first accessing the correspondent functions
                for words in reducedlist:
                    vnode = words.split("*",1)[0].strip()
                    node = vnode.split("$",1)[0].strip()
                    state1 = vnode.split("$",1)[1].strip()
                    function1 = words.split("=",1)[1].strip()
                    if node == nodes[index1]:
    ##                    print words
                        # find the new state of this node
    ##                    print 'eval:',words,nodes, cstate,fullstatelist
                        new = evalfunc(words,nodes, cstate,fullstatelist)
    ##                    print node,state1,new,type(new)
                        if new == '1' or new == True or new == 1:
                            newstate = state1
                            states[index1] = nodes[index1]+'$'+cstate[index1]
    ##            if newstate == '@': print 'Error:', nodes[index1]
    ##            print newstate,cstate[index1]
                if newstate != cstate[index1]:
                    Flag1=1
                    cstate[index1] = newstate
                else:
                    # remove this index
                    indexrange1.remove(index1)
            if indexrange1 == []:
            # reached a steady state
                if outputmode ==0:
                    return [t,cstate]
                if outputmode ==1:
                    return 'steady state in {} steps:{}; trajectory: {}'.format(t,cstate,trajectory)
            else:
                trajectory.append(copy.copy(cstate))

        if updatescheme==1:
        # Random Order Async
            #removing perturbed nodes
            if ABAsignal!=[]:
                indexrange1.remove(nodes.index('ABA'))
                cstate[nodes.index('ABA')]= ABAsignal[t]
            if CO2signal!=[]:
                indexrange1.remove(nodes.index('high_CO2'))
                cstate[nodes.index('high_CO2')]= CO2signal[t]
##            print indexrange1

            Nodechange_Flag1=0
            while (indexrange1 !=[]):
                index1 = random.choice(indexrange1)
##                print 'index1=',index1, 'node:', nodes[index1]
                newstate = '@'
                # evaluate new state, by first accessing the correspondent functions
##                print 'start'
                for words in reducedlist:
                    vnode = words.split("*",1)[0].strip()
                    node = vnode.split("$",1)[0].strip()
                    state1 = vnode.split("$",1)[1].strip()
                    function1 = words.split("=",1)[1].strip()
                    if node == nodes[index1]:
##                        print words
                        # find the new state of this node
##                        print 'eval:',words,nodes, cstate,fullstatelist
                        new = evalfunc(words,nodes, cstate,fullstatelist)
##                        print node,state1,new,type(new)
                        if new == '1' or new == True or new == 1:
                            newstate = state1
                            states[index1] = nodes[index1]+'$'+cstate[index1]
                if newstate == '@': print ('Error:', nodes[index1])
                # raise error if node doesn't get updated
##                print newstate,cstate[index1]
                if newstate != cstate[index1]:
                    Nodechange_Flag1=1
                    cstate[index1] = newstate
                # remove this index
                indexrange1.remove(index1)

            if Nodechange_Flag1==0:
            # reached a steady state
                if printresult==1:
                    print ('steady state in {} steps:{}'.format(t,cstate))
                if stop==1:
                    if outputmode ==0:
                        return [t,cstate]
                    if outputmode ==1:
                        return [t,trajectory,cstate]
##                        return 'steady state in {} steps:{}; trajectory: {}'.format(t,cstate,trajectory)
                else:
                    trajectory.append(copy.copy(cstate))
            else:
                trajectory.append(copy.copy(cstate))

    if outputmode ==0:
        return [-1,trajectory]
    if outputmode ==1:
        if printresult==1:
            print
##            print '!!!FLag!!!'
            print ('Did not reach steady state.')
            print ('Trajectory:', trajectory)
        return ['trajectory:',trajectory]


def write_trajectory(trajectory_list, iteration, nodeindexlist, export2excel=0, global_iterator1=0, global_iterator2=0,global_iterator3=0,perturbation_mode=0,nodelist=[]):
    # 2019-0505 update: use 'nodeindexlist' as a list of nodes to be monitored, instead of 1 node.
    # take the 'nodeindex' node's value from each trajectory, and average them
    y=[]
    x=range(0,len(trajectory_list[0]))
    for i in range (0,len(nodeindexlist)):
        y.append([0]*len(trajectory_list[0]))

##    iteration = len (trajectory_list) # Length of traj_list is simulation iteration
##    print 'length:',len (trajectory_list)

        for trajectory in trajectory_list:
    ##        print 'trajectory:', trajectory
            t=0
            for state in trajectory:
    ##            print 'state', state, type(state),t
                y[i][t] += eval(state[nodeindexlist[i]])
                t+=1
    ##    print y
        for j in range(0,len(y[i])):
    ##        print y[i],iteration
            y[i][j] = float(y[i][j])/iteration

    # exporting data to excel
        if export2excel==1:
            if nodelist!=[]:
                ws1.write(0,2+i, nodelist[nodeindexlist[i]])
                ws2.write(0,2+i, nodelist[nodeindexlist[i]])
            for j in range (0,len(x)):
                ws1.write(j+1,1,x[j])
                ws1.write(j+1,global_iterator3+1+i,y[i][j])
            ws2.write(global_iterator3,2+i, y[i][j])
            if perturbation_mode==1:
                ws3.write(global_iterator1+2,global_iterator2+i, y[i][j])
    return

# TBD list:
# print attractor with node names;

def full_perturbation_list(nodescan, inlist=[], outlist=[]):
    # take the nodescan result as input and create a full list of perturbations, i.e. a list of all single node states. E.g. ['ABA$0', 'ABA$1', ...]
    # inlist is the list of nodes we want to keep. outlist is the list of nodes that we do not want to keep. In other words, only nodes in inlist but not in outlist are chosen to create perturbation states. Default inlist is the full list (though shown as [] in parameters)..
    result_list=[]
    if inlist==[]:
        inlist = nodescan[0]
    for node in nodescan[0]:
        if node in inlist and node not in outlist:
            for state in nodescan[1][nodescan[0].index(node)]:
                result_list.append(node+'$'+state)
    return result_list


def sub_istate(istate, perturbationlist, nodelist):
    # substitute contradicting initial states to be consistent with perturbations. E.g. if CO2 is perturbed to be 0, then initial state will be subbed to 0, too.
    # istate is a list of state numbers in the sequence of nodes; perturbationlist is the list of perturbations (a list of strings e.g. 'A$0'); nodelist is the list of nodes obtained from 'nodescan' function (order of the nodes are important)
    # return an updated istate (list of numbers)
    new_istate= copy.deepcopy(istate)
##    print 'new_istate',new_istate
##    print perturbationlist
    for vnode in perturbationlist:
##        if vnode != []:
        node = vnode.split("$",1)[0].strip()
        state = vnode.split("$",1)[1].strip()
##        print vnode, node, state, nodelist.index(node)
        new_istate[0][nodelist.index(node)]=eval(state)
    return new_istate

# test
##y = to_list('toy_model_XLG_0128.txt')
##nodelist = nodescan(y)[0]
##perturbationlist=['high_CO2$0']
##istatelist=[[0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,'*','*','*','*',0]]
##istatelist=sub_istate(istatelist, perturbationlist, nodelist)
##print istatelist

# initial state converter
# converts a list of virtual nodes (list of strings) to the corresponding list of their states (list of numbers)
# if nodelist (reference list of node name (strings)) is not empty. return states in the same order as the nodelist
# put in defaultstate ('*') if a node's state is not specified

def istate_convert(istate, nodelist=[],defaultstate='*'):
    statelist=[]
    if nodelist == []:
        for vnode in istate:
            statelist.append(int(vnode.split("$",1)[1].strip()))
    else:
        for node in nodelist:
            statelist.append(defaultstate)
        for vnode in istate:
            node1 = vnode.split("$",1)[0].strip()
            state1 = vnode.split("$",1)[1].strip()
            statelist[nodelist.index(node1)]= int (state1)

    return statelist
# note: this function can give a state that is not allowed by the nodelist itself, e.g. give ROS$3 while ROS is Boolean

#test
##y = to_list('toy_model_HT1_0419.txt')
##nodelist = nodescan(y)[0]
##testlist = ['ABA$1','closure$2','ROS$3']
##print istate_convert(testlist,nodelist)


# simulation
test = 1 # A master switch to turn the simulation ON or OFF
if test ==1:
    y = to_list("CO2model_2023_0726.txt") # s

##    print y
    nodelist = nodescan(y)[0]
##    print nodescan(y)

    # for a full CPC simulation, one needs to set monitor to closure (-1), perturb_mode = 0, perturbation_list to full_perturbation_list

    print (nodelist)
    iteration1 = 20 # set simulation iteration. According to the manuscript, this should be set to 1000
    timesteps = 30 # set timestep. According to the manuscript, this should be set to 30
    stop_flag=0 # default value
    prtresult=0 # default value

    # create a monitor list from node names
    monitorlist = [-1] # Default: minotoring closure
##    monitorlist = [nodelist.index('AnionEM')] # minotoring AnionEM represening SLAC1 (since SLAC1 is now split into two nodes)

    # create monitor list for specific nodes
##    listx1 = ['HCO3','GHR1','HT1','ABI1','ABI2','ROS','MPKs_kinase','OST1_basal','CaIM','Cac','H+_ATPase','KOUT','Depolarization','SLAC1_CO2','SLAC1_nonCO2','AnionEM','CPKs','K+_efflux','H+_ATPase','Closure'] # single SLAC1
##    monitorlist = [nodelist.index(i) for i in listx1]

##    monitorlist = range(0,len(nodelist)) # monitor everything

    pertb_mode =0 #default value
    pertb_list2 =[] #default value

    nname=''
    if nname!='':
        if nname not in nodelist:
          sys.exit('Error! Node name does not exist.')
        else:
            nindex = nodelist.index(nname)

    print ('Monitoring:'),
    for nindex in monitorlist:
        print (nodelist[nindex], nindex,)
##    print (len(nodelist))
    print

    export2excel1=1 # export to excel file. This needs to be set to 1, so an output excel file will be generated.
    perturbationlist = [] # setting perturbations for simulation
    perturbationlist = full_perturbation_list(nodescan(y), inlist=[], outlist=[]) # full list for systematic perturbations, for e.g. CPC values
##    perturbationlist = ['high_CO2$1']*200 # for generating a default distribution of CPC values under CO2

    global_iter1=0 # global iterators used to control which row or column in excel to write into between different perturbations
    global_iter2=0
    global_iter3=0

    # generating ABA and CO2 signal, and initial condition
    ABAsignal1=[]
    CO2signal1=[]
    start_time = time.time()
    list1 = ['high_CO2$0','CO2_porins$1','CA14$1','MPKs$1','CBC12$1','ABI2$1','ABI1$1','HAB1$1','HT1$1','ABA$0','H+_ATPase$1'] # define initial state. All specified nodes are initialized ON; other nodes are initialized OFF.
    istatelist = [istate_convert(list1,nodelist,defaultstate=0)]
##    print (len(istatelist[0]),istatelist)

    # create excel file
    if export2excel1==1:
        wb = xlsxwriter.Workbook('sample.xlsx')
        ws2 = wb.add_worksheet('simulation')
        ws1 = wb.add_worksheet('response_curve')
        ws1.write(0,1,'timestep')
    else:
        ws1=[]

    # perturbations
    if pertb_mode==0:
        perturbations = pertb_generator(input_list1=perturbationlist,input_list2=pertb_list2, mode=pertb_mode)
##        print 'Perturbations:',perturbations
        for item in perturbations:
            global_iter3+=1
            traj_list = []
            resultlist=[]
            print
            print ('Perturbed:', item)
            ws2.write(0,1,'Perturbation')
##            ws2.write(0,2,'Final average closure')
            y1 = perturb(y, item)
            ws2.write(global_iter3,1, str(item))
            ws1.write(0,global_iter3+1,str(item))
            istatelist1=sub_istate(istatelist, item, nodelist)
##            print y1
        # iterating single pertubations (E.g. systematic single node KO)

            for i in range(0,iteration1):
                z = simulate (y1,timestep=timesteps,outputmode=1,istates=istatelist1,updatescheme=1,stop=stop_flag,printresult=prtresult,ABAsignal=ABAsignal1, CO2signal=CO2signal1)
                traj_list.append(z[1])

            # create final state representation, and put into resultlist
                fstate=copy.copy(z[1][-1])
                attractor=[]
                for j in range(0,len(fstate)):
                    attractor.append(str(nodelist[j]+'='+str(fstate[j])))
                #print (attractor)
    ##            if export2excel1==1:
    ##                ws2.write(i+1,3,str(attractor))
                resultlist.append(attractor)

                write_trajectory(trajectory_list=traj_list, iteration=iteration1, nodeindexlist=monitorlist,export2excel=export2excel1,global_iterator1=global_iter1,global_iterator2=global_iter2,global_iterator3=global_iter3,perturbation_mode=pertb_mode,nodelist=nodelist)
                    #Showing trajectory figure of designated node

    if pertb_mode>=1:
        ws3 = wb.add_worksheet('perturbation Combinations')

        perturbations1 = pertb_generator(input_list1=perturbationlist,input_list2=[], mode=0)
        if perturbations1[0]!=[]:
            perturbations1.insert(0,[])
##        print ('Perturbations1:',perturbations1)
        perturbations2 = pertb_generator(input_list1=[],input_list2=pertb_list2, mode=pertb_mode)
##        print (perturbations2)
        global_iter2 =1
##        for item2_0 in perturbations2:
##            global_iter2+=1
        for item1 in perturbations1:
            global_iter1+=1
            global_iter2=1
##            traj_list = []
            resultlist=[]
            ws2.write(0,1,'Perturbation')
            ws2.write(0,2,'Final average closure')
            if pertb_mode>=1:
                ws3.write(1,1,'mutant')
                ws3.write(0,2,'Perturbation')
                ws3.write(0,3,'inital state'+str(list1))
                ws3.write(0,1,'Final average closure')
                ws3.write(global_iter1+2,1, str(item1))

            for item2 in perturbations2:
                traj_list = []
                global_iter2+=1
                global_iter3+=1
                ws3.write(2,global_iter2, str(item2))
                ws2.write(global_iter3,1, str(item1 + item2))
                ws1.write(0,global_iter3+1,str(item1 + item2))
                print
                print ('Perturbed:', item1+item2)
                y1 = perturb(y, item1 + item2)
##                print y1
##                print istatelist
                istatelist1=sub_istate(istatelist, item1 + item2, nodelist)
##                print istatelist1
##                print
                for i in range(0,iteration1):
                    z = simulate (y1,timestep=timesteps,outputmode=1,istates=istatelist1,updatescheme=1,stop=stop_flag,printresult=prtresult,ABAsignal=ABAsignal1, CO2signal=CO2signal1)
                    traj_list.append(z[1])

                # create final state representation, and put into resultlist
                    fstate=copy.copy(z[1][-1])
                    attractor=[]
                    for j in range(0,len(fstate)):
                        attractor.append(str(nodelist[j]+'='+str(fstate[j])))
                    #print (attractor)
        ##            if export2excel1==1:
        ##                ws2.write(i+1,3,str(attractor))
                    resultlist.append(attractor)
##                print traj_list
                    write_trajectory(trajectory_list=traj_list, iteration=iteration1, nodeindexlist=monitorlist,export2excel=export2excel1,global_iterator1=global_iter1,global_iterator2=global_iter2,global_iterator3=global_iter3,perturbation_mode=pertb_mode,nodelist=nodelist)
                    #Showing trajectory figure of designated node

    wb.close()

    print ("--- %s seconds ---" % (time.time() - start_time))

    now = datetime.datetime.now()

    print ("Current time: ")
    print (now.strftime("%H:%M:%S"))

# display result sheet
""""""
import pandas as pd
df= pd.read_excel('sample.xlsx') # read the output file just generated by the above program
print (df.dropna(axis=1))
""""""
