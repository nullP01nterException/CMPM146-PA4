import sys, logging
from math import inf
sys.path.insert(0, '../')
from planet_wars import issue_order

# The objective is the planet easier to be conquered: the lowest product between 
# the distance from the planet that executes the tree and the number of ships in the objective planet
def attack_quickest(state): # lowest product: distance * num_ships to conquer
    
    target_planets = [planet for planet in state.not_my_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    my_planets = [planet for planet in state.my_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    if len(my_planets) == 0:
        return False
    my_sender = my_planets[0]
    quickest_planet = target_planets[0]
    lowest_product = inf
    
    for j in range(len(target_planets)):
        for i in range(len(my_planets)):
            logging.info("my_sender: " + str(my_sender))
            logging.info("distance: " + str(state.distance(my_planets[i].ID, target_planets[j].ID)))
            current_product =  state.distance(my_planets[i].ID, target_planets[j].ID) * target_planets[j].num_ships+1
            logging.info("current_product" + str(current_product))
            if current_product < lowest_product and my_planets[i].num_ships/2 > target_planets[j].num_ships +1:
                lowest_product = current_product
                quickest_planet = target_planets[j]
                my_sender = my_planets[i]
    
    return issue_order(state, my_sender.ID, quickest_planet.ID, quickest_planet.num_ships + 1)
    #return False
    
def attack_beneficial(state): # attack_beneficial for neutral planets
    #if len(state.neutral_planets()) <= 20:
    #    return False
    logging.info("state.neutral_planets(): " + str(len(state.neutral_planets())))
    neutral_target_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
                      
    my_planets = [planet for planet in state.my_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
                      
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    
    highest_product = 0
    if len(neutral_target_planets) == 0:
        return False
    beneficialest_planet = neutral_target_planets[0]
    if len(my_planets) == 0:
        return False
    my_sender = my_planets[0]
    #quickest_planet = neutral_target_planets[0]
    lowest_product = inf
    
    for j in range(len(my_planets)):
        
        for i in range(len(neutral_target_planets)):
            distance_product =  state.distance(my_planets[j].ID, neutral_target_planets[i].ID) * neutral_target_planets[i].num_ships+1
            
            current_product = neutral_target_planets[i].growth_rate / distance_product
            
            if current_product > highest_product: # and?
                highest_product = current_product
                beneficialest_planet = neutral_target_planets[i]
                my_sender = my_planets[j]
                
    logging.info("highest_product: " + str(highest_product))
    # might want to check if we have any planets
    return issue_order(state, my_sender.ID, beneficialest_planet.ID, beneficialest_planet.num_ships + 1)
                      
    #return False

def spread_to_fattest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False
    #logging.info("len(state.my_planets()) = " len(state.my_planets()))
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    
    target_planets = [planet for planet in state.not_my_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    target_planets = iter(sorted(target_planets, key=lambda p: p.num_ships, reverse=True))
    if target_planets is None:
        return False    
    fattest_planet = max(state.neutral_planets(), key=lambda p: p.growth_rate, default=None)
    if fattest_planet is None:
        return False
    fattest_planets_sorted_list = [planet for planet in state.not_my_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    fattest_planets_sorted_list = sorted(fattest_planets_sorted_list, key=lambda p: p.growth_rate, reverse=True)
 
    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    # enemy_planets = iter(sorted(enemy_planets, key=lambda p: p.num_ships, reverse=True))

    my_planets = [planet for planet in state.my_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())
                      ]
    # my_planets = iter(sorted(my_planets, key=lambda p: p.num_ships, reverse=True))
        
    #dist_next_my_planet = distance(next(my_planets), fattest_planet)
    
    # STATE.DISTANCE FIX STATE.DISTANCE FIX STATE.DISTANCE FIX STATE.DISTANCE FIX STATE.DISTANCE FIX STATE.DISTANCE FIX STATE.DISTANCE FIX
    #next_my_planet = 
    logging.info("len(fattest_planets_sorted_list: " + str(len(fattest_planets_sorted_list)))
    for j in range(len(fattest_planets_sorted_list)):
        dist_my_closest_to_fattest = inf 
        for i in range(len(my_planets)):
            dist_next_my_planet = state.distance(my_planets[i].ID, fattest_planets_sorted_list[j].ID)
            if dist_next_my_planet < dist_my_closest_to_fattest and my_planets[i].num_ships/2 > fattest_planets_sorted_list[j].num_ships:
               dist_my_closest_to_fattest = dist_next_my_planet
    
        dist_enemy_closest_to_fattest = inf
        for i in range(len(enemy_planets)):
            dist_next_enemy_planet = state.distance(enemy_planets[i].ID, fattest_planets_sorted_list[j].ID)
            if dist_next_enemy_planet < dist_enemy_closest_to_fattest: # distance between two planets
                dist_enemy_closest_to_fattest = dist_next_enemy_planet
        
        if dist_enemy_closest_to_fattest < dist_my_closest_to_fattest:
            break
    
    if not strongest_planet or not fattest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        #return issue_order(state, strongest_planet.ID, fattest_planet.ID, strongest_planet.num_ships / 2)
        return issue_order(state, strongest_planet.ID, fattest_planet.ID, fattest_planet.num_ships + 1)


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def aggressive_attack(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return

def defensive_defense(state):
        my_planets = [planet for planet in state.my_planets()]
        if not my_planets:
            return

        def strength(p):
            return p.num_ships \
                   + sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == p.ID) \
                   - sum(fleet.num_ships for fleet in state.enemy_fleets() if fleet.destination_planet == p.ID)

        avg = sum(strength(planet) for planet in my_planets) / len(my_planets)

        weak_planets = [planet for planet in my_planets if strength(planet) < avg]
        strong_planets = [planet for planet in my_planets if strength(planet) > avg]

        if (not weak_planets) or (not strong_planets):
            return

        weak_planets = iter(sorted(weak_planets, key=strength))
        strong_planets = iter(sorted(strong_planets, key=strength, reverse=True))

        try:
            weak_planet = next(weak_planets)
            strong_planet = next(strong_planets)
            while True:
                need = int(avg - strength(weak_planet))
                have = int(strength(strong_planet) - avg)

                if have >= need > 0:
                    issue_order(state, strong_planet.ID, weak_planet.ID, need)
                    weak_planet = next(weak_planets)
                elif have > 0:
                    issue_order(state, strong_planet.ID, weak_planet.ID, have)
                    strong_planet = next(strong_planets)
                else:
                    strong_planet = next(strong_planets)

        except StopIteration:
            return