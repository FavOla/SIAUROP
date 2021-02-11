#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: fnels
"""

#heavily based on https://github.com/saschaschramm/MonteCarloTreeSearch

from env_Cleaner import EnvCleaner
import random
import uuid
import math

class Node:

        def __init__(self, state, action, action_space, reward, terminal):
            self.identifier = str(uuid.uuid1())
            self.parent_identifier = None
            self.children_identifiers = []
            self.untried_actions = list(range(action_space))
            self.state = state
            self.total_simulation_reward = 0
            self.num_visits = 0
            self.performance = 0
            self.action = action
            self.reward = reward
            self.terminal = terminal
    
        def __str__(self):
            return "{}: (action={}, visits={}, reward={:d}, ratio={:0.4f})".format(self.state, self.action, self.num_visits, int(self.total_simulation_reward), self.performance)
    
        def untried_action(self):
            action = random.choice(self.untried_actions)
            self.untried_actions.remove(action)
            return action
        
        def vertical_lines(self,last_node_flags):
            vertical_lines = []
            vertical_line = '\u2502'
            for last_node_flag in last_node_flags[0:-1]:
                if last_node_flag == False:
                    vertical_lines.append(vertical_line + ' ' * 3)
                else:
                    # space between vertical lines
                    vertical_lines.append(' ' * 4)
            return ''.join(vertical_lines)
        
        def horizontal_line(self,last_node_flags):
            horizontal_line = '\u251c\u2500\u2500 '
            horizontal_line_end = '\u2514\u2500\u2500 '
            if last_node_flags[-1]:
                return horizontal_line_end
            else:
                return horizontal_line
    
class Tree:
    
        def __init__(self):
            self.nodes = {}
            self.root = None
    
        def is_expandable(self, node):
            if node.terminal:
                return False
            if len(node.untried_actions) > 0:
                return True
            return False
    
        def iter(self, identifier, depth, last_node_flags):
            if identifier is None:
                node = self.root
            else:
                node = self.nodes[identifier]
    
            if depth == 0:
                yield "", node
            else:
                yield node.vertical_lines(last_node_flags) + node.horizontal_line(last_node_flags), node
    
            children = [self.nodes[identifier] for identifier in node.children_identifiers]
            last_index = len(children) - 1
    
            depth += 1
            for index, child in enumerate(children):
                last_node_flags.append(index == last_index)
                for edge, node in self.iter(child.identifier, depth, last_node_flags):
                    yield edge, node
                last_node_flags.pop()
    
        def add_node(self, node, parent=None):
            self.nodes.update({node.identifier: node})
    
            if parent is None:
                self.root = node
                self.nodes[node.identifier].parent = None
            else:
                self.nodes[parent.identifier].children_identifiers.append(node.identifier)
                self.nodes[node.identifier].parent_identifier=parent.identifier
    
        def children(self, node):
            children = []
            for identifier in self.nodes[node.identifier].children_identifiers:
                children.append(self.nodes[identifier])
            return children
    
        def parent(self, node):
            parent_identifier = self.nodes[node.identifier].parent_identifier
            if parent_identifier is None:
                return None
            else:
                return self.nodes[parent_identifier]
    
        def show(self):
            lines = ""
            for edge, node in self.iter(identifier=None, depth=0, last_node_flags=[]):
                lines += "{}{}\n".format(edge, node)
            print(lines)
    
    
class MonteCarloTreeSearch():
        
        def __init__(self, env, tree):
            self.env = env
            self.tree = tree
            self.action_space = 4
            state = self.env.reset()
            self.tree.add_node(Node(state = state, action = None, action_space=self.action_space, reward=0, terminal=False))
        
        def expand(self, node):
            action = node.untried_action()
            reward = self.env.step([action])
            done = self.env.is_room_clean()
            state = self.env.occupancy
            new_node = Node(state = state, action = action, action_space=self.action_space, reward=reward, terminal=done)
            self.tree.add_node(new_node, node)
            return node #NOTT THERE IN USUAL CODE
        
        def default_policy(self, node, show = False):
            if node.terminal:
                return node.reward
            steps = 0
            while True: #loop until room is cleaned from this branch
                action = random.randint(0, self.action_space -1)
                reward= self.env.step([action])
                steps += 1
                if show:
                    self.env.render()
                state = self.env.occupancy
                done = self.env.is_room_clean()
                
                if done:
                    return (reward, steps)
        
        def compute_value(self, parent, child, exploration_constant):
                try: 
                    exploitation_term = child.total_simulation_reward / child.num_visits
                except:
                    exploitation_term = 0
                try: 
                    exploration_term = exploration_constant * math.sqrt(2 * math.log(parent.num_visits) / child.num_visits)
                except:
                    exploration_term = 0
                return exploitation_term + exploration_term            
        
        def best_child(self, node, exploration_constant):
            best_child = self.tree.children(node)[0]
            best_value = self.compute_value(node, best_child, exploration_constant)
            iter_children = iter(self.tree.children(node))
            next(iter_children)
            for child in iter_children: #go through each child to determine the best one
                value = self.compute_value(node, child, exploration_constant)
                for child in iter_children:
                    value = self.compute_value(node, child, exploration_constant)
                if value > best_value:
                    best_child = child
                    best_value = value
                    
            return best_child
        
        def tree_policy(self, show = False):
            node = self.tree.root
            
           
            while not node.terminal:
                if self.tree.is_expandable(node):
                   
                    return self.expand(node)
                else:
                    node = self.best_child(node, exploration_constant = 1.0/math.sqrt(2))
                    #reward = self.env.step([action])
                    
                    if(show):
                        print("entered")
                        self.env.render()
                    state = self.env.occupancy
                    done = self.env.is_room_clean()
                    node.state = self.env.occupancy
                    assert (node.state == state).all()
          
            return node
        
        def backward(self, node, value):
            while node:
                node.num_visits +=1
                node.total_simulation_reward += value
                node.performance = node.total_simulation_reward/node.num_visits
                node = self.tree.parent(node)
        
        def forward(self):
            self._forward(self.tree.root)
            
        def _forward(self, node):
            best_child = self.best_child(node, exploration_constant = 0)
            
            print("****** {} ******".format(best_child.state))
            
            for child in self.tree.children(best_child):
                print("{}: {:0.4f}".format(child.state, child.performance))

            if len(self.tree.children(best_child)) > 0:
                self._forward(best_child)
