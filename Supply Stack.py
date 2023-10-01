# this script will create a simple 3 generator supply stack with PyPSA
# The idea is that lopf will determine the optimal output of each source given some (fixed) demand
# the next challenge can be to have demand vary with time
# finally, the script will print a visual supply stack (supply curve)
# In our hypothetical scenario, the grid demand will be 850 MW


import os
import pypsa
glpk_path = "/usr/local/bin/glpsol"
os.environ["PATH"] += os.pathsep + os.path.dirname(glpk_path)

network = pypsa.Network()

network.add("Bus", "bus1")

# 3 generators, varying outputs and MCs

network.add("Generator", "coal_plant", bus="bus1", p_nom=1000, marginal_cost=100)
network.add("Generator", "wind_farm", bus="bus1", p_nom=750, marginal_cost=50)
network.add("Generator", "solar_farm", bus="bus1", p_nom=400, marginal_cost=10)

# add demand
network.add("Load", "load1", bus="bus1", p_set=900)

# linear optimization with glpk

network.lopf(network.snapshots, solver_name="glpk")

print(network.generators_t.p)

# try to create a visual supply curve using matplotlib

import pypsa
import matplotlib.pyplot as plt

# Relist the network, bus, generators, and the load (demand)
network = pypsa.Network()
network.add("Bus", "bus1")
network.add("Generator", "coal_plant", bus="bus1", p_nom=1000, marginal_cost=100)
network.add("Generator", "wind_farm", bus="bus1", p_nom=750, marginal_cost=50)
network.add("Generator", "solar_farm", bus="bus1", p_nom=400, marginal_cost=10)
network.add("Load", "load1", bus="bus1", p_set=900)

# Sort generators by MC
sorted_gen = network.generators.sort_values(by="marginal_cost")

# Calculate cumulative capacity
cumulative_capacity = sorted_gen['p_nom'].cumsum()

# Plot
plt.figure(figsize=(10, 6))
plt.step(cumulative_capacity, sorted_gen['marginal_cost'], where='post', label="Supply Curve")
plt.xlabel('Cumulative Capacity (MW)')
plt.ylabel('Marginal Cost ($/MWh)')
plt.title('Supply Stack')
plt.grid(True, which='both', linestyle='--', linewidth=1)
plt.legend()
plt.show()

