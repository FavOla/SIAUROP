#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: fnels
"""

import numpy as np
import random



#https://www.youtube.com/watch?v=HGeI30uATws&list=PLZbbT5o_s2xoWNVdDudn51XM8lOuZ_Njv&index=9
def Q_agent(env):
        
      
        map_size = env.map_size - 2
        q_table = np.zeros((2**(map_size**2) * map_size,4)) #state space size, action space size
        print (q_table)
        
        num_episodes = 5000
        max_steps_per_episode = map_size**2 * 10 #size of grid * 10
        
        learning_rate = .1
        discount_rate = .99
        
        exploration_rate = 1
        max_exploration_rate = 1
        min_exploration_rate = .01
        exploration_decay_rate = .001
        
        rewards_all_episodes = []
        steps_all_episodes = []
        possible_states = generate_all_states(env)
        initial_state = state_to_index(env, 1, possible_states)
        
        #Q learning algorithm
        for episode in range(num_episodes): #for each episode
            env.reset()
            pos = 1
            state = initial_state
            
            done = False
            rewards_current_episode = 0
            
            
            
            for step in range(max_steps_per_episode): #for each time step within an episode
                # if episode%100 == 0:
                #     env.render()
                    
                
                #exploration-exploitation trade-off
                exploration_rate_threshold = random.uniform(0,1) #determiness if agent exploers or exploits in this time step
                if exploration_rate_threshold > exploration_rate: #agent exploits
                    action = np.argmax(q_table[state,:])
                else: #agent explorer
                    action = random.randint(0,3)
               
                
                
                reward = env.step([action]) 
                
                #determine new possition
                if reward == -1: #robot couldn't move/bumped into boundary
                    new_pos = pos
                elif action == 0: #up
                    new_pos = pos - env.map_size
                elif action == 1: #right
                    new_pos = pos + 1
                elif action == 2: #down
                    new_pos = pos + env.map_size
                else: #left
                    new_pos = pos - 1 
                
                done = env.is_room_clean()
                reward -= .2 #penalty forr taking an additional step
                
                
                new_state = state_to_index(env, new_pos, possible_states)
                
                
                #update Q-table for Q(s,a)
                q_table[state, action] = q_table[state, action] * (1 - learning_rate) + learning_rate * (reward + discount_rate * np.max(q_table[new_state,:]))
               
                pos = new_pos
                state = new_state
                rewards_current_episode += reward
                
                if done == True: #agent cleaned whole room, so stop time steps
                    steps_all_episodes.append(step)
                    if episode%1000 == 0:
                        print("Room Cleaned in", step, "steps")
                    break
                if step == max_steps_per_episode -1: #room not cleaned in max steps:
                    steps_all_episodes.append(max_steps_per_episode)
                
            #Exploration rate decay
            exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
            
            rewards_all_episodes.append(rewards_current_episode)
        
        #Calculate and print the average rewrad per thousand episodes
        # rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes),num_episodes/1000)
        # print(rewards_per_thousand_episodes)
        # count = 1000
        # print ("********Average reward per 1000 episodes********\n")
        # for r in rewards_per_thousand_episodes:
        #     print(count, ":", str(sum(r/1000))) 
        #     count += 1000     
        
        #Print update Q-table
        print("\n\n*****Q-table*******\n")
        print(q_table)
        print("Fastest time steps was: " + str(min(steps_all_episodes)))                                          
        
        return steps_all_episodes
    
def state_to_index(env, pos, possible_states):
                """
                
    
                Parameters
                ----------
                env : envCleaner
                    environment.
                pos : int 
                    tile number robot currently in.
    
                Returns
                -------
                index : int 
                    hashed index of state (both clean/dirty tile identification & position).
    
                """
                
                
                barriers = [] #number of the tile the barrier is located in
                
                occupancy = env.occupancy.copy()
                occupancy = np.delete(occupancy, 0, axis = 0) #delete top boundary
                occupancy = np.delete(occupancy, 0, axis = 1) #delete left boundary
                occupancy = np.delete(occupancy, env.map_size - 2, axis = 0) # delete bottom boundary
                occupancy = np.delete(occupancy, env.map_size - 2, axis = 1) #delete right boundary
                occupancy = occupancy.transpose()
                #print(occupancy)
                
                for r in range(len(occupancy)): #go through rows & columns to find the barriers
                    row = occupancy[r]
                    for column in range(len(row)):
                        if row[column] == 1 : #barrier
                            barrier = (r * (env.map_size - 2)) + column  #tile position of barrier
                            barriers.append(barrier)
                #print(barriers)
                for row in possible_states: #replace values of tile positions with barrriers with 1s     
                    for barrier in barriers:
                        row[barrier] = 1
            
                occupancy = occupancy.flatten() #make 1d array
                index = 0
                
                for state in range(len(possible_states)): #find index of state
                    if (possible_states[state] == occupancy).all():
                        index = state + 1 #number of that possibility
                        # print("this is the possible state\n", possible_states[state])
                        # print("this is the actual state\n", occupancy.flatten())
                        break
                
                if index == 0:
                    print ("This state not found in possible states")
                    return
                else: #hashing the state
                    index = index * (env.map_size - 2) + pos
                    return index   
                
def generate_all_states(env):
        """
        

        Parameters
        env : EnvCleaner
            number of rows/columns in the grid.

        Returns possible_states: np.array
            all possible combinations of clean/dirty tiles
            num columns will be grid size * grid size (grid is represented as long string of tiles)
        -------
        None.
        """
            
        grid_size = (env.map_size - 2) ** 2 #number of rows & columns in the grid
        possible_states = []
        num_zeros = 1 #number of zeros  that column should have before the pattern switches to 1s and vice versa
            
        for i in range(grid_size): #make the columns
            column = []
            num = 0 #tthe number that should fill that row/column spot
                
            for r in range(2**grid_size): #make the rows
                if r % num_zeros == 0: #time to switch to new digit (either 0 or 1)
                    if num == 0:
                        num = 2
                    else:
                        num = 0
                        
                column.append(num) 
                r += 1
                
            num_zeros *= 2 #next column should have twice as many 0s before switching tto 1s and vice versa
            possible_states.append(column)
                
        possible_states = np.array(possible_states)
        possible_states = possible_states.transpose() #make rows columns and columns rows
    
        return possible_states
    