import os
import datetime




#numComp = "1"
#os.environ["comp"+numComp] = "False"
#os.system("export COMP = False")

data = os.getenv("COMP1")#["COMP1"]

print(data)

#os.environ["COMP1"]="True"
os.environ["COMP1"]="True"
#os.system("export COMP1=True")

data = os.getenv("COMP1")

print(data)

