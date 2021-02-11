#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: fnels
"""
# problem statement: robot can see in tiles immediately next to it before moving, but nothing else.
from env_Cleaner import EnvCleaner
import random
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
import math
import logging
import argparse
import hashlib
import datetime
import copy
import math
from collections import defaultdict
from random import choice, shuffle

import Qagent as Q
import dfs
import rightwall
import randomAgent
import MCTS


if __name__ == '__main__':
    
     
    
    ###############################
    #running the tests    
    
    env = EnvCleaner(2, 5, 0)
    max_iter = 20000
    reward = None
    action = [0,1,2,3] #up, right, down, left
    #env.step([0, 1])
    env.render()
    
    move = 0
    total_reward = 0
    #print(dfs_maze(env))
    
    
    """Testing Q-agent"""
    # steps_all_episodes = Q.Q_agent(env)
    
    # x = []
    # for i in range(1, len(steps_all_episodes)+1):
    #     x.append(i)
    # plt.plot(x,steps_all_episodes,'b.') #blue dots of actual values
    # plt.xlabel("Episode")
    # plt.ylabel("Steps")       
    # plt.title("Q agent steps per episode " )     
    # plt.show()
    
    
    "Testing MCTS Agent"
    # tree = MCTS.Tree()
    # monteCarloTreeSearch = MCTS.MonteCarloTreeSearch(env=env, tree=tree)
    # steps = 1000
    
    # for i in range(0, steps):
    #     env.reset()
    #     node = monteCarloTreeSearch.tree_policy()
    #     reward = monteCarloTreeSearch.default_policy(node)[0]
    #     monteCarloTreeSearch.backward(node, reward)
    
    # env.reset()
    # node = monteCarloTreeSearch.tree_policy(True)
    # reward, step = monteCarloTreeSearch.default_policy(node, True)
    # if env.is_room_clean():
    #     print("room clean in", step, "steps")
        
    # print("reward is", reward)
    # monteCarloTreeSearch.tree.show()
    # monteCarloTreeSearch.forward()

    
    
    """Testing MCTS Agent 1st attempt"""
    # MCTS_agent = MonteCarloAgent(env)
    # print(MCTS_agent.bestChild)
    # node = NodeMCTS(env)
    # for step in range(1000):
    #     #env.render()
        
    #     for i in range(4):
    #         child = MCTS_agent.expand(node)
            
    #         q = MCTS_agent.simulate(child)
    #         MCTS_agent.backup(child, q)
            
    #         MCTS_agent.backup(node, q)
        
    #     best_child = MCTS_agent.select_leaf(node) #choose the mostst promising node
    #     action = best_child.action
    #     env.step ([action])
  
    
 
    
    """ testing random actions"""
    # for i in range(1,max_iter +1):
        
        
    #     #env.render()
    #     action = randomAgent.random_actions()
    #     reward = env.step(action)
    #     if env.is_room_clean():
    #         print("room cleaned in", i, "steps")
    #         break
    #     elif i == max_iter: #room not clean after max iterations
    #       print("room not cleaned in", i, " (max) time steps")
    
    
    
    """ testing right turns """
    # action = 1 
    # for i in range(1,max_iter +1):
        
        
    #     env.render()
    #     action = rightwall.right_turns(action, env)
    #     if env.is_room_clean():
    #         print("room cleaned in", i, "steps")
    #         break
    #     elif i == max_iter: #room not clean after max iterations
    #       print("room not cleaned in", i, " (max) time steps")
  
    
    """testing dfs"""
    # dfs(env, (0,0), 0, [], 0)
            

    

        
   