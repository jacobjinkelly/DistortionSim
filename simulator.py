# -*- coding: utf-8 -*-
"""Overall class for running the simulations.

Contains the Simulator class, which holds all of the matching algorithms and calculates the distortion. Also logs the outcomes of the experiments for analysis and
visualization.

"""

import argparse
import os

import networkx as nx
import pandas as pd

import instance_generator
import solver


class Simulator:
    """Object that solves instances of matching problems given to it and aggregates the results in a pretty manner.

    Attributes:
        instance_generator (InstanceGenerator): InstanceGenerator for creating problem instances for simulation
        history (dict): history of all results, stored in a dictionary for later conversion to pd.DataFrame
    """

    def __init__(self, instance_generate):
        """Initializes a new Simulator.

        Args:
            instance_generate (InstanceGenerator): InstanceGenerator for creating problem instances for simulation
        """
        self.instance_generator = instance_generate
        self.history = {'id': [], 'val_index': [], 'size': [], 'valuation':[], 'algo': [], 'distortion': []}
        self.id = 1

    def serial_dictatorship_experiment(self, val_index, val_type, G, size=None, agent_cap=None):
        """Finds the distortion of running serial dictatorship on the given input.
        
        Args:
            val_index (int): The id of the valuation in self.instance_generator.
            val_type (string): The method by which the valuation was generated.
            G (nx.Graph): The actual matching input. Must be a weighted bipartite graph with numerical node labels.
            size (int): The number of agents in the input. Defaults to half the size of G.nodes if not given.
            agent_cap (int): An integer value i such that for all nodes with label <= i, those nodes are agents. Defaults to len(G.nodes//2) if not given.
            
        """
        if size is None:
            size = len(G.nodes)//2

        M = solver.serial_dictatorship(G,agent_cap)

        self.history['id'].append(self.id)
        self.id += 1
        self.history['val_index'].append(val_index)
        self.history['size'].append(size)
        self.history['valuation'].append(val_type)
        self.history['algo'].append('serial_dictatorship')
        self.history['distortion'].append(solver.calculate_modified_distortion(G,M,prio='pareto'))

    def partial_max_matching_experiment(self, val_index, val_type, G, m, size=None, agent_cap=None):
        """Finds the distortion of running PartialMaxMatching on the given input.
        
        Args:
            val_index (int): The id of the valuation in self.instance_generator.
            val_type (string): The method by which the valuation was generated.
            G (nx.Graph): The actual matching input. Must be a weighted bipartite graph with numerical node labels.
            m (int): The number of buckets, used as input to PartialMaxMatching.
            size (int): The number of agents in the input. Defaults to half the size of G.nodes if not given.
            agent_cap (int): An integer value i such that for all nodes with label <= i, those nodes are agents. Defaults to len(G.nodes//2) if not given.
            
        """
        if size is None:
            size = len(G.nodes)//2

        M = solver.partial_max_matching(G,m,agent_cap)
        H = solver.reassign_labels(G, M)
        M_0 = solver.top_trading_cycles(H)

        self.history['id'].append(self.id)
        self.id += 1
        self.history['val_index'].append(val_index)
        self.history['size'].append(size)
        self.history['valuation'].append(val_type)
        self.history['algo'].append('partial_max_matching' + '_' + str(m))
        self.history['distortion'].append(solver.calculate_distortion(G, M_0))

    def modified_max_matching_experiment(self, val_index, val_type, G, prio='pareto', size=None, agent_cap=None):
        """Finds the distortion of running ModifiedMaxMatching on the given input.
        
        Args:
            val_index (int): The id of the valuation in self.instance_generator.
            val_type (string): The method by which the valuation was generated.
            G (nx.Graph): The actual matching input. Must be a weighted bipartite graph with numerical node labels.
            size (int): The number of agents in the input. Defaults to half the size of G.nodes if not given.
            agent_cap (int): An integer value i such that for all nodes with label <= i, those nodes are agents. Defaults to len(G.nodes//2) if not given.
            
        """
        if size is None:
            size = len(G.nodes)//2

        M_0 = solver.modified_max_matching(G,prio=prio,agent_cap=agent_cap)

        self.history['id'].append(self.id)
        self.id += 1
        self.history['val_index'].append(val_index)
        self.history['size'].append(size)
        self.history['valuation'].append(val_type)
        self.history['algo'].append('modified_max_matching')
        self.history['distortion'].append(solver.calculate_modified_distortion(G,M_0,prio))

    def top_trading_cycles_experiment(self, val_index, val_type, G, size=None, agent_cap=None):
        """Finds the distortion of running top trading cycles on the given input.
        
        Args:
            val_index (int): The id of the valuation in self.instance_generator.
            val_type (string): The method by which the valuation was generated.
            G (nx.Graph): The actual matching input. Must be a weighted bipartite graph with numerical node labels.
            size (int): The number of agents in the input. Defaults to half the size of G.nodes if not given.
            agent_cap (int): An integer value i such that for all nodes with label <= i, those nodes are agents. Defaults to len(G.nodes//2) if not given.
        """
        if size is None:
            size = len(G.nodes)//2

        M = solver.top_trading_cycles(G,agent_cap)

        self.history['id'].append(self.id)
        self.id += 1
        self.history['val_index'].append(val_index)
        self.history['size'].append(size)
        self.history['valuation'].append(val_type)
        self.history['algo'].append('ttc_matching')
        self.history['distortion'].append(solver.calculate_modified_distortion(G,M,prio='pareto'))
    
    def epsilon_max_matching_experiment(self, val_index, val_type, G, epsilon, size=None, agent_cap=None):
        """Finds the distortion of running epsilon max matching on the given input.
        
        Args:
            val_index (int): The id of the valuation in self.instance_generator.
            val_type (string): The method by which the valuation was generated.
            G (nx.Graph): The actual matching input. Must be a weighted bipartite graph with numerical node labels.
            size (int): The number of agents in the input. Defaults to half the size of G.nodes if not given.
            agent_cap (int): An integer value i such that for all nodes with label <= i, those nodes are agents. Defaults to len(G.nodes//2) if not given.
        """
        if size is None:
            size = len(G.nodes)//2

        M = solver.epsilon_max_matching(G, epsilon, agent_cap=agent_cap)
        H = solver.reassign_labels(G, M)
        M_0 = solver.top_trading_cycles(H)

        self.history['id'].append(self.id)
        self.id += 1
        self.history['val_index'].append(val_index)
        self.history['size'].append(size)
        self.history['valuation'].append(val_type)
        self.history['algo'].append('epsilon_max_matching'+str(epsilon))
        self.history['distortion'].append(solver.calculate_distortion(G,M_0))

    def epsilon_max_matching_prio_experiment(self, val_index, val_type, G, epsilon, prio='pareto', size=None, agent_cap=None):
        """Finds the distortion of running epsilon max matching on the given input.
        
        Args:
            val_index (int): The id of the valuation in self.instance_generator.
            val_type (string): The method by which the valuation was generated.
            G (nx.Graph): The actual matching input. Must be a weighted bipartite graph with numerical node labels.
            prio (String): String in ['rank_maximal', 'max_cardinality_rank_maximal', 'fair'] that represents the priority vector used for this problem. Defaults to 'rank_maximal'.
            size (int): The number of agents in the input. Defaults to half the size of G.nodes if not given.
            agent_cap (int): An integer value i such that for all nodes with label <= i, those nodes are agents. Defaults to len(G.nodes//2) if not given.
        """
        if size is None:
            size = len(G.nodes)//2

        M = solver.epsilon_max_matching(G, epsilon, prio, agent_cap)

        self.history['id'].append(self.id)
        self.id += 1
        self.history['val_index'].append(val_index)
        self.history['size'].append(size)
        self.history['valuation'].append(val_type)
        self.history['algo'].append('epsilon_max_matching '+prio+str(epsilon))
        self.history['distortion'].append(solver.calculate_modified_distortion(G,M,prio))

    # TODO fix inconsistent casing
    def twothirds_max_matching_experiment(self, val_index, val_type, G, prio, size=None, agent_cap=None):
        """Finds the distortion of twothirds_max_matching on the given input.
        
        Args:
            val_index (int): The id of the valuation in self.instance_generator.
            val_type (string): The method by which the valuation was generated.
            G (nx.Graph): The actual matching input. Must be a weighted bipartite graph with numerical node labels.
            prio (String): String in ['rank_maximal', 'max_cardinality_rank_maximal', 'fair'] that represents the priority vector used for this problem. Defaults to 'rank_maximal'.
            size (int): The number of agents in the input. Defaults to half the size of G.nodes if not given.
            agent_cap (int): An integer value i such that for all nodes with label <= i, those nodes are agents. Defaults to len(G.nodes//2) if not given.
        """
        M = solver.twothirds_max_matching(G, prio, agent_cap)

        self.history['id'].append(self.id)
        self.id += 1
        self.history['val_index'].append(val_index)
        self.history['size'].append(size)
        self.history['valuation'].append(val_type)
        self.history['algo'].append('twothirds_max_matching '+prio)
        self.history['distortion'].append(solver.calculate_modified_distortion(G,M,prio))

    def updated_hybrid_max_matching_experiment(self, val_index, val_type, G, size=None, agent_cap=None):
        """Finds the distortion of running updated HybridMaxMatching on the given input.
        
        Args:
            val_index (int): The id of the valuation in self.instance_generator.
            val_type (string): The method by which the valuation was generated.
            G (nx.Graph): The actual matching input. Must be a weighted bipartite graph with numerical node labels.
            size (int): The number of agents in the input. Defaults to half the size of G.nodes if not given.
            agent_cap (int): An integer value i such that for all nodes with label <= i, those nodes are agents. Defaults to len(G.nodes//2) if not given.
            
        """
        if size is None:
            size = len(G.nodes)//2

        M = solver.updated_hybrid_max_matching(G,agent_cap=agent_cap)
        H = solver.reassign_labels(G, M)
        M_0 = solver.top_trading_cycles(H)

        self.history['id'].append(self.id)
        self.id += 1
        self.history['val_index'].append(val_index)
        self.history['size'].append(size)
        self.history['valuation'].append(val_type)
        self.history['algo'].append('updated_hybrid_max_matching')
        self.history['distortion'].append(solver.calculate_modified_distortion(G,M_0,prio='pareto'))


if __name__ == '__main__':
    instantiator = instance_generator.InstanceGenerator(True)
    sim = Simulator(instantiator)

    parser = argparse.ArgumentParser("big boi Bhomas")
    parser.add_argument("--scale", type=str, default="1.", choices=["0.2", "1", "5"])
    parser.add_argument("--norm", type=str, default="range", choices=["range", "sum"])
    parser.add_argument("--save_dir", type=str, default="./")
    parser.add_argument("--ckpt_path", type=str, default="./")

    args = parser.parse_args()

    val_type = f"theta{args.scale}unit{args.norm}"

    for size in [5, 10, 20, 50, 100]:
        filename = f"rdata/ord_n{size}_theta{args.scale}.txt"
        print('current n value is', size)

        G_list = instantiator.generate_list_from_ordinal_preferences(filename, size, 100, f"unit_{args.norm}")
        val_index = instantiator.index - 100

        for i in range(len(G_list)):
            G = G_list[i]

            # adjust experiments here
            sim.serial_dictatorship_experiment(val_index, val_type, G)
            sim.top_trading_cycles_experiment(val_index, val_type, G)
            sim.epsilon_max_matching_prio_experiment(val_index, val_type, G, 1, prio='pareto')
            sim.epsilon_max_matching_prio_experiment(val_index, val_type, G, 0.1, prio='pareto')
            sim.updated_hybrid_max_matching_experiment(val_index, val_type, G)

            val_index += 1

    # adjust naming conventions here
    data_dir = os.path.join(args.save_dir, "ijcaidata")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    s = os.path.join(data_dir, val_type + ".csv")
    s_instances = os.path.join(data_dir, val_type + "instances.csv")

    df = pd.DataFrame(sim.history)
    df.to_csv(s)

    df = pd.Series(sim.instance_generator.history)
    df.to_csv(s_instances)
