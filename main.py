from interface import WinProbabilityInterface

# Create an instance of the interface
interface_instance = WinProbabilityInterface()

# Predict with +1000 gold diff
print("Gold +1000:", interface_instance.predict(gold_diff=1000) * 100)

# Predict with -1000 gold diff
print("Gold -1000:", interface_instance.predict(gold_diff=-1000) * 100)
