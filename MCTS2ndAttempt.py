#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: fnels
"""

import logging
import argparse
import hashlib
import datetime
import copy
import math
import random
from collections import defaultdict
from random import choice, shuffle

#MCTS scalar.  Larger scalar will increase exploitation, smaller will increase exploration. 
SCALAR=1/math.sqrt(2.0)
    
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('MyLogger')


class UCBPolicy(object):
        C = math.sqrt(2)/2
        """ Calls for best child policy based on UCB bound v """
        def __init__(self, C = math.sqrt(2)):
            self.C = 1 / (2* math.sqrt(2)) 
            UCBPolicy.C = self.C
        
        def setParams(self,C):
            self.C = C
        
        @staticmethod
        def getScore(n):
            """Retturns UCB1 score for node (not root)"""
            return n.getExpectedValue() + UCBPolicy.C*math.sqrt(2*math.log(n.parent.N)/n.N)
        def bestChild(self, node):
            """ UCT Method: Assumes that all childs are expanded
            Implements given policy
            """
            L = [n.getExpectedValue() + self.C*math.sqrt(2*math.log(node.N)/n.N) for n in node.children]
            return node.children[L.index(max(L))]
        
class NodeMCTS:
        def __init__(self, env, action = None, parent_agent = None):
            self.env = env
            self.parent_agent_agent = parent_agent
            self.action = action
            #shuffle(self.actions_remaining)
            self.actions_remaining = [0,1,2,3]
            self.N = 0
            self.Q = 0.0
            self.parent = None
            self.children = []
            
        def getExpectedValue(self):
            """ returns expected value, if transposition option is on uses dict """
            return self.Q / float(self.N) + 1
        
        def isFullyExpanded(self):
            return len(self.children) == 4 #all four moves are children
        
        def isTerminal(self):
            return self.env.is_room_clean()

  
    #  
class MonteCarloAgent(object):
        def __init__(self, env, best_child_policy = UCBPolicy, **kwargs ):
            #Takes an instance of a room and optionally. Initializes the list of game states and the statistics tables.
            self.env = env
            self.runtime = datetime.timedelta(seconds = kwargs.get('runtime', .05 ))
            self.max_depth = kwargs.get('max_depth', 20)
            self.gamma = kwargs.get('gamma', .9)
            self.bestChild = best_child_policy().bestChild
            self.Qdict = defaultdict(float)
            self.Ndict = defaultdict(float)
            
            self.states = []
            
        def get_actions(self):
            #Calculate the best move from the current game state and return it
            root = NodeMCTS(copy.deepcopy(self.env), parent_agent = self)
            begin = datetime.datetime.utcnow()
            count = 0
            while datetime.datetime.utcnow() - begin < self.runtime:
                count += 1
                leaf = self.select_leaf(root)
                q = self.simulate(leaf)
                self.backup(leaf, q)
            
            L = [n.getExpectedValue() for n in root.children]
            
            actions = {0:'up', 1:'right', 2:'down', 3:'left'}
            print('.....', count, 'simulations')
            for n in root.children:
                print ('     ', actions[n.action], n.getExpectedValue())
               
            return (root.children[L.index(max(L))].action, root.children[L.index(max(L))])
            
        def pick_move_policy(self, env):
            #Policy for simulation, currently random
            return random.randint(0,3)
        
        def simulate(self, node):
            """ Simulate from the current node"""
            copy_env = copy.deepcopy(node.env)
            simulation_depth = 0
            rewards = []
            while simulation_depth <= self.max_depth:  #and not copy_env.inTerminalState():
                action = self.pick_move_policy(copy_env)
                reward = copy_env.step([action])
                rewards.append(reward)
                simulation_depth += 1
                
            discounted_rewards = [(self.gamma ** i) * r for i, r in zip(range(len(rewards)), rewards)]
            return sum(discounted_rewards)
        
        def select_leaf(self, node):
            """
            Find the leaf to expand
            node: node to start from
            return: child leaf or terminal node
            """
            
            while not node.isTerminal():
                if not node.isFullyExpanded():
                    return self.expand(node)
                else:
                    node = self.bestChild(node)
                return node
        
        def expand(self, node):
            """
            Expands node by one random step
            node: Node to expand
            return: child node
            """
            try:
                action = node.actions_remaining.pop()
            except:
                action = random.randint(0, 3)
            new_env = copy.deepcopy(node.env)
            new_env.step([action])
            child_node = NodeMCTS(new_env, action = action, parent_agent = self)
            child_node.parent = node
            node.children.append(child_node)
            return child_node
        
        def backup(self, node, q):
            """
            Backup and add all the new q values to the nodes, going upwards from the leaves
            """
            
            while node != None:
                node.Q = q
                node.N += 1
                node = node.parent