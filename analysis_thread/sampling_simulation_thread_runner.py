# -*- coding: utf-8 -*-
"""

Author:   Cheng Maohua
Email:    cmh@seu.edu.cn

License: this code is in the public domain
"""
import os

try:
    from analysis_thread.sampling_simulation_thread import PeriodSampling
except:
    from sampling_simulation_thread import PeriodSampling

try:   
    from analysis_task.demo_turbine.task_turbine_sampling_simulation import UnitHPSimulation
except:
    import sys
    sys.path.append("..")
    from analysis_task.demo_turbine.task_turbine_sampling_simulation import UnitHPSimulation

try:   
    from analysis_task.m300exair.task_exair_sampling_simulation import UnitExaircoffSimulation
except:
    import sys
    sys.path.append("..")
    from  analysis_task.m300exair.task_exair_sampling_simulation import  UnitExaircoffSimulation

# add your module 
 
if __name__ == "__main__":

    TaskList = []
    
    pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    analysis_taskpath = os.path.join(pardir, "analysis_task")
    
    taginfile = os.path.join(analysis_taskpath, "demo_turbine", "task_turbine_tag_in.txt")
    
    SimulationUnitHP = UnitHPSimulation(taginfile)
    TaskList.append(SimulationUnitHP)
    
    # add you tesk
    taginfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_in.txt")
    
    Simulation = UnitExaircoffSimulation(taginfile)
    TaskList.append(Simulation)
    
    
    OnlineTasks = PeriodSampling(2, TaskList)
    OnlineTasks.settag()
    OnlineTasks.worker()
 
   
