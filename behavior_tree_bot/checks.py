#from math import round
import logging

def benefit_check(state):
    
    total_planets = len(state.my_planets()) + len(state.neutral_planets()) + len(state.enemy_planets())
    stopping_point = int(total_planets / 10)
    
    logging.info("length of my_planets: " + str(len(state.my_planets())))
    logging.info("stopping_point: " + str(stopping_point))
    if len(state.my_planets()) >= stopping_point:
        return False
    #len(state.neutral_planets())
    #if len(state.neutral_planets()) <= 0:
    #    return False
    return True
   
    
def quicky_check(state):
    total_planets = len(state.my_planets()) + len(state.neutral_planets()) + len(state.enemy_planets())
    stopping_point = int(total_planets / 20)
    
    logging.info("length of my_planets: " + str(len(state.my_planets())))
    logging.info("stopping_point: " + str(stopping_point))
    if len(state.my_planets()) >= stopping_point:
        return False
    #len(state.neutral_planets())
    #if len(state.neutral_planets()) <= 0:
    #    return False
    return True
    
def checky_check(state):
    #logging.info("len(state.my_planets()) = " len(state.my_planets()))
    if len(state.my_planets()) < 3:
        return 1
    else:
        return 0


def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())
