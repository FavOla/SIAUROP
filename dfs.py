#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: fnels
"""
import time


#https://www.annytab.com/depth-first-search-algorithm-in-python/
class Node:
        
        def __init__(self, position:(), parent:()):
            self.position = position
            self.parent = parent
            self.g = 0 
            self.h = 0 # Distance to goal node
            self.f = 0 # Total cost
            
            
        # Compare nodes
        def __eq__(self, other):
            return self.position == other.position
        # Sort nodes
        def __lt__(self, other):
              return self.f < other.f
        # Print node
        def __repr__(self):
            return ('({0},{1})'.format(self.position, self.f))

    
    
def dfs_maze(env):
        
        #create lists for open nodes and closed nodes
        opened = []
        closed = []
        map_size = env.map_size - 2
        #create start and end goal node
        start_node = Node(1, None)
        end = (env.map_size - 2) ** 2
        goal_node = Node(end, None)
        
        #add the start node
        opened.append(start_node)
        
        #loop until the open list is empty
        while len(opened) > 0:
            #get the last node (LIFO)
            current_node = opened.pop(-1)
            
            #add the current node to closed list
            closed.append(current_node)
            #breakpoint()
            
            #check if goal reached, return the path
            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                #path.append(start)
                #return reversed path
                return path[::-1]
            
            #breakpoint()
            pos = current_node.position
            neighbors = [pos - map_size, pos - 1, pos + map_size, pos + 1 ] #up, left, down, right
            
            #loop neighbors:
            count = 0
            for next_one in neighbors:
                    
                #check if node is wall:
                occupancy = env.occupancy.transpose()
                
                print(occupancy)
                print((next_one // map_size + 1),(next_one % map_size + 1 ))
                if(occupancy[next_one // map_size + 1][next_one % map_size + 1] == 1): #illegible neighbor (boundarry)
                    print("continued")
                    continue
                
                #create neighbor node
                neighbor = Node(next_one, current_node)
                env.render()
                
                
                if count == 0: #up
                    env.step([0])
                if count == 1: #left
                    env.step([3])
                if count == 2: #down
                    env.step([2])
                else:
                    env.step([1])
                
                count +=1
                
                #check if the neighbor is in the closed list
                if (neighbor in closed):
                    continue
                    
                if (neighbor not in opened):
                    opened.append(neighbor)
                
                
            return None #no path found
    
    
 
#https://www.youtube.com/watch?v=VQp7pfij7_Q   
def dfs(env, pos, action, clean_tiles, time_steps ):
        '''
        Parameters
        ----------
        env : EnvCleaner
            cleaning environment.
        pos : tuple
            coordinates (x,y) where the robot is in the room.
        action : int
            direction it will move
        clean_tiles : list of tuples 
            list of clean tile coodinates.
        time_steps : number of iterations needed
    
        Returns reward: list [pos rewards for clean tiles, punishment for bumping into walls]
                
        -------
        None.
    
        '''
        
        env.render()
        
        # old = time.time()
        # while old - time.time() < 1000:
        #     f = 1+1
        
        # if time_steps > 10:
        #     return 
        #reward = env.step([action%4])
        time_steps +=1
        
        if pos in clean_tiles: #tile was already cleaned 
            env.step([action])
            return
        
        else: #tile was dirty and became clean
            
            # x = env.agt_pos_list[0][0]
            # y = env.agt_pos_list[0][1]
            # pos = (x, y)
            # env.occupancy[env.agt_pos_list[0][0]][env.agt_pos_list[0][1]] = 0
            reward = env.step([action%4]) #clean the tile
            clean_tiles.append(pos) #add current pos to clean tiles
        
        
        for i in range(4): #each branch surrounding current tile 
       
            if env.can_move([action]): #the robot can move in same direction
                #env.occupancy[env.agt_pos_list[0][0]][env.agt_pos_list[0][1]] = 2 #make it dirty again. Only wanted to know if it could move

                nextX = pos[0] #start with current x
                nextY = pos[1] #start with current y
                
                if action%4 == 0: #moving up
                    nextY -=1
                elif action%4 == 1: #moving right
                    nextX =+1
                elif action%4 == 2: #moving down
                    nextY +=1
                elif action%4 == 3: #moving left
                    nextX -=1
            
                new_pos = (nextX, nextY)  
                
               
        
                dfs(env, new_pos, action, clean_tiles, time_steps) #complete current direction path
                 
                #move but don't clean or change orientation
                action +=2 #turn 180 degrees 
                env.step([action%4]) 
                #env.occupancy[env.agt_pos_list[0][0]][env.agt_pos_list[0][1]] = 2 #make it dirty again
                action -=2
                 
            else: #can't move
                action +=1 #rotate 90 degrees cw
                
                
                
                
                