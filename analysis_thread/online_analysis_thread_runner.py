# -*- coding: utf-8 -*-
"""
    Author:   Cheng Maohua
    Email:    cmh@seu.edu.cn
    License: MIT
"""
import os

import sys
sys.path.append("./")
sys.path.append("..")

from analysis_thread.online_analysis_thread import PeriodAnalysis

from analysis_task.demo_turbine.task_turbine_online_analysis import UnitHP

# TODO: add your module
from analysis_task.m300exair.task_exair_online_analysis import UnitExaircoff

if __name__ == "__main__":

    TaskList = []

    pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    analysis_taskpath = os.path.join(pardir, "analysis_task")

    taginfile = os.path.join(analysis_taskpath, "demo_turbine", "task_turbine_tag_in.txt")
    tagoutfile = os.path.join(analysis_taskpath, "demo_turbine", "task_turbine_tag_out.txt")

    DemoUnitHP = UnitHP(taginfile, tagoutfile)
    TaskList.append(DemoUnitHP)

    # TODO: add your task
    taginfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_in.txt")
    tagoutfile = os.path.join(analysis_taskpath, "m300exair", "task_exair_tag_out.txt")

    TaskExaircoff = UnitExaircoff(taginfile, tagoutfile)
    TaskList.append(TaskExaircoff)

    OnlineTasks = PeriodAnalysis(2, TaskList)
    OnlineTasks.setouttag()
    OnlineTasks.worker()
