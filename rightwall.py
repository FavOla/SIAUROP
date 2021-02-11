#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: fnels
"""


def right_turns(prev_action, env):
        if prev_action == None:
            prev_action = 1
        reward = env.step([(prev_action + 1) % 4]) #right
        action = (prev_action + 1) % 4
        if reward == - 1: #can't turn right
            reward2 = env.step([prev_action]) #go straight
            action = prev_action
            if reward2 == -1: #can't go straight
                reward3 = env.step([(prev_action + 3) % 4])
                action = (prev_action + 3) % 4
                if reward3 == -1: #must sswitch directions
                    reward4 = env.step([(prev_action + 2) % 4])
                    action = (prev_action + 2) % 4
        return action