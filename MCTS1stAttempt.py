#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: fnels
"""

from env_Cleaner import EnvCleaner
import random


    #https://github.com/hildensia/mcts
class Node1:
        """
        Node for the MCTS. Stores the move applied to reach this node from its parent,
        stats for the associated game position, children, parent and outcome
        (outcome==none unless the position ends the game).
        
        Args:
            move:
            parent:
            N (int): times this position was visited
            Q (int): average reward from this position
            children (dict):
        """
        def __init__(self, map_size, state, parent=None):
            self.visits = 1
            self.reward = 0.0
            self.state = state
            self.children = []
            self.parent = parent
            self.map_size = map_size
            
        def add_child(self, child_state):
            child = Node(child_state, self)
            self.children.append(child)
        
        def update(self, reward):
            self.reward += reward
            self.visits +=1
            
        def fully_expanded(self):
            if len(self.children) == 4: #all four moves are children
                return True
            else:
                return False
        def __repr__(self):
            s="Node; children: %d; visits: %d; reward: %f"%(len(self.children),self.visits,self.reward)
            return s
        
        def next_state(self):
            if self.children == []: #no children so next child should be up
                next_state = self.state - self.map_size
            elif len(self.children) == 1: #next child should be right
                next_state == self.state + 1
            elif len(self.children) == 2: #next child should be down
                next_state == self.state + self.map_size
            else: #next child should left
                next_state == self.state - 1
            
            return next_state
   
    
    def UCTSearch(budget, root):
        for iter in range(int(budget)): 
            if iter%10000 == 9999:
                logger.info("simulation: %d"%iter)
                logger.info(root)
                
            front = Tree_Policy(root)
            reward = Default_Policy(front.state)
            Backup(front, reward)
        return BestChild(root, 0)
    
    def Tree_Policy(node):
        #a hack to force 'exploitation' in a game where there are many options, and you may never/not want to fully expand first
    	while node.state.terminal()==False:
    		if len(node.children)==0: #node is currrently lasst in branch
    			return Expand(node)
    		elif random.uniform(0,1)<.5: #exploitation
    			node=BestChild(node,SCALAR)
    		else: #exploration
    			if node.fully_expanded()==False:	
    				return Expand(node)
    			else:
    				node=BestChild(node,SCALAR)
    	return node
    
    def Expand(node):
        tried_children = [c.state for c in node.children]
        new_state = node.next_state()
        
        while new_state in tried_children:
            new_state = node.next_state()
            node.add_child(new_state)
            
        return node.children[-1]
    
    def BestChild(node, scalar):
        bestscore=0.0
        bestchildren=[]
        for c in node.children:
            exploit = c.reward/c.visits
            explore = math.sqrt(2.0*math.log(node.visits)/float(c.visits))	
            score = exploit+scalar*explore
            if score == bestscore: #multiple best children
                bestchildren.append(c)
            if score>bestscore: # new best child
                bestchildren=[c]
                bestscore=score
        if len(bestchildren)==0:
            logger.warn("OOPS: no best child found, probably fatal")
        return random.choice(bestchildren)
    
    def Default_Policy(node, env):
        explore_env = EnvCleaner(env.N_agent, env.map_size, env.seed)
        explore_env.occupancy = env.occupancy
        explore_env.agt_pos_list = env.agt_pos_list.copy() 
        reward = 0
        
        count = 0 #count branch length
        parent = node.parent
        while parent != None:
            count += 1
            parent = parent.parent
        
        while count < 20: #random next choices
            action = random.randint(0,3)
            reward += explore_env([action])
            count +=1
            
        return reward
    
    def Backup(node, reward):
        while node != None:
            node.visits += 1
            node.reward += reward
            node = node.parent
        return
                
        
    class MCTS():
        
        def __init__ (self, env):
            self.env = env
        
        def search(self, time_budget):
            """
            Search and update the search tree for a specified amount of time in seconds
            time budget: int, how much time to think
            """
            #start_time = clock()
            return
   # parser = argparse.ArgumentParser(description='MCTS research code')
    #parser.add_argument('--num_sims', action="store", required=True, type=int)
   # parser.add_argument('--levels', action="store", required=True, type=int, choices=range(20))
   # args=parser.parse_args()
	
  #  current_node=Node1(1)
    #for l in range(args.levels):
        #current_node=UCTSearch(args.num_sims/(l+1),current_node)
        #print("level %d"%l)
        #print("Num Children: %d"%len(current_node.children))
        #for i,c in enumerate(current_node.children):
        #    print(i,c)
        #print("Best Child: %s"%current_node.state)
		
        #print("--------------------------------")	
			    
   