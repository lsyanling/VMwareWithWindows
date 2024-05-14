#!/usr/bin/env python3
"""Evaluation for the paper 'Timing Analysis of Asynchronized Distributed
Cause-Effect Chains' (2021).

It includes (1) local analysis (2) global analysis and (3) plotting of the
results.
"""

import copy
import gc  # garbage collector
import argparse
import math
import numpy as np
import utilities.chain as c
import utilities.communication as comm
import utilities.generator_WATERS as waters
import utilities.generator_UUNIFAST as uunifast
import utilities.transformer as trans
import utilities.event_simulator as es
import utilities.analyzer as a
import utilities.evaluation as eva

import time
import os
from utilities.task import Task
from utilities.mytools import get_object_field_keys
from utilities.mytools import get_object_field_values


debug_flag = True  # flag to have breakpoint() when errors occur


def main():
    """Main Function."""
    ###
    # Argument Parser
    ###
    parser = argparse.ArgumentParser()

    # which part of code should be executed:
    parser.add_argument("-j", type=int, default=0)
    # utilization in 0 to 100 [percent]:
    parser.add_argument("-u", type=float, default=50)
    # task generation (0: WATERS Benchmark, 1: UUnifast):
    parser.add_argument("-g", type=int, default=0)

    # only for args.j==1:
    # name of the run:
    parser.add_argument("-n", type=int, default=-1)
    # number of task sets to generate:
    parser.add_argument("-r", type=int, default=1)

    # only for args.j==4:
    # 处理器核数
    parser.add_argument("-c", type=int, default=1)

    args = parser.parse_args()
    del parser

    current_dir = os.path.dirname(__file__)
    os.chdir(current_dir)

    if args.j == 1:
        """Single ECU analysis.

        Required arguments:
        -j1
        -u : utilization [%]
        -g : task generation setting
        -r : number of runs
        -n : name of the run

        Create task sets and cause-effect chains, use TDA, Davare, Duerr, our
        analysis, Kloda, and save the Data
        """
        ###
        # Task set and cause-effect chain generation.
        ###
        print("=Task set and cause-effect chain generation.=")

        try:
            if args.g == 0:
                # WATERS benchmark
                print("WATERS benchmark.")

                # Statistical distribution for task set generation from table 3
                # of WATERS free benchmark paper.
                profile = [0.03 / 0.85, 0.02 / 0.85, 0.02 / 0.85, 0.25 / 0.85,
                           0.25 / 0.85, 0.03 / 0.85, 0.2 / 0.85, 0.01 / 0.85,
                           0.04 / 0.85]
                # Required utilization:
                req_uti = args.u/100.0
                # Maximal difference between required utilization and actual
                # utilization is set to 1 percent:
                threshold = 1.0

                # Create task sets from the generator.
                # Each task is a dictionary.
                print("\tCreate task sets.")
                task_sets_waters = []
                while len(task_sets_waters) < args.r:
                    task_sets_gen = waters.gen_tasksets(
                            1, req_uti, profile, True, threshold/100.0, 4)
                    task_sets_waters.append(task_sets_gen[0])

                # Transform tasks to fit framework structure.
                # Each task is an object of utilities.task.Task.
                trans1 = trans.Transformer("1", task_sets_waters, 10000000)
                task_sets = trans1.transform_tasks(False)

            elif args.g == 1:
                # UUniFast benchmark.
                print("UUniFast benchmark.")

                # Create task sets from the generator.
                print("\tCreate task sets.")

                # The following can be used for task generation with the
                # UUniFast benchmark without predefined periods.

                # # Generate log-uniformly distributed task sets:
                # task_sets_generator = uunifast.gen_tasksets(
                #         5, args.r, 1, 100, args.u, rounded=True)

                # Generate log-uniformly distributed task sets with predefined
                # periods:
                periods = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
                # Interval from where the generator pulls log-uniformly.
                min_pull = 1
                max_pull = 2000

                task_sets_uunifast = uunifast.gen_tasksets_pred(
                        50, args.r, min_pull, max_pull, args.u/100.0, periods)

                # Transform tasks to fit framework structure.
                trans2 = trans.Transformer("2", task_sets_uunifast, 10000000)
                task_sets = trans2.transform_tasks(False)

            else:
                print("Choose a benchmark")
                return

            # Create cause effect chains.
            print("\tCreate cause-effect chains")
            ce_chains = waters.gen_ce_chains(task_sets)
            # ce_chains contains one set of cause effect chains for each
            # task set in task_sets.

        except Exception as e:
            print(e)
            print("ERROR: task + ce creation")
            if debug_flag:
                breakpoint()
            else:
                task_sets = []
                ce_chains = []

        ###
        # First analyses (TDA, Davare, Duerr).
        ###
        print("=First analyses (TDA, Davare, Duerr).=")
        analyzer = a.Analyzer("0")

        try:
            # TDA for each task set.
            print("TDA.")
            for idxx in range(len(task_sets)):
                try:
                    # TDA.
                    i = 1
                    for task in task_sets[idxx]:
                        # Prevent WCET = 0 since the scheduler can
                        # not handle this yet. This case can occur due to
                        # rounding with the transformer.
                        if task.wcet == 0:
                            raise ValueError("WCET == 0")
                        task.rt = analyzer.tda(task, task_sets[idxx][:(i - 1)])
                        if task.rt > task.deadline:
                            raise ValueError(
                                    "TDA Result: WCRT bigger than deadline!")
                        i += 1
                except ValueError:
                    # If TDA fails, remove task and chain set and continue.
                    task_sets.remove(task_sets[idxx])
                    ce_chains.remove(ce_chains[idxx])
                    continue

            # End-to-End Analyses.
            print("Test: Davare.")

            analyzer.davare(ce_chains)

            print("Test: Duerr Reaction Time.")
            analyzer.reaction_duerr(ce_chains)

            print("Test: Duerr Data Age.")
            analyzer.age_duerr(ce_chains)

            print("Test: DBAge.")
            analyzer.DBAge(ce_chains)

            print("Test: deltaBound.")
            analyzer.deltaBound(ce_chains)

            ###
            # Second analyses (Simulation, Our, Kloda).
            ###
            print("=Second analyses (Simulation, Our, Kloda).=")
            i = 0  # task set counter
            schedules = []
            for task_set in task_sets:
                print("=Task set ", i+1)

                # Skip if there is no corresponding cause-effect chain.
                if len(ce_chains[i]) == 0:
                    continue

                # Event-based simulation.
                print("Simulation.")

                simulator = es.eventSimulator(task_set)

                # Determination of the variables used to compute the stop
                # condition of the simulation
                max_e2e_latency = max(ce_chains[i], key=lambda chain:
                                      chain.davare).davare
                max_phase = max(task_set, key=lambda task: task.phase).phase
                max_period = max(task_set, key=lambda task: task.period).period
                hyper_period = analyzer.determine_hyper_period(task_set)

                sched_interval = (
                        2 * hyper_period + max_phase  # interval from paper
                        + max_e2e_latency  # upper bound job chain length
                        + max_period)  # for convenience

                # Information for end user.
                print("\tNumber of tasks: ", len(task_set))
                print("\tHyperperiod: ", hyper_period)
                number_of_jobs = 0
                for task in task_set:
                    number_of_jobs += sched_interval/task.period
                print("\tNumber of jobs to schedule: ",
                      "%.2f" % number_of_jobs)

                # Stop condition: Number of jobs of lowest priority task.
                simulator.dispatcher(
                        int(math.ceil(sched_interval/task_set[-1].period)))

                # Simulation without early completion.
                schedule = simulator.e2e_result()
                schedules.append(schedule)

                # Analyses.
                for chain in ce_chains[i]:
                    print("Test: Our Data Age.")
                    analyzer.max_age_our(schedule, task_set, chain, max_phase,
                                         hyper_period, reduced=False)
                    analyzer.max_age_our(schedule, task_set, chain, max_phase,
                                         hyper_period, reduced=True)

                    print("Test: Our Reaction Time.")
                    analyzer.reaction_our(schedule, task_set, chain, max_phase,
                                          hyper_period)

                    # Kloda analysis, assuming synchronous releases.
                    print("Test: Kloda.")
                    analyzer.kloda(chain, hyper_period)

                    # Test.
                    if chain.kloda < chain.our_react:
                        if debug_flag:
                            breakpoint()
                        else:
                            raise ValueError(
                                    ".kloda is shorter than .our_react")
                i += 1
        except Exception as e:
            print(e)
            print("ERROR: analysis")
            if debug_flag:
                breakpoint()
            else:
                task_sets = []
                ce_chains = []

        ###
        # Save data.
        ###
        print("=Save data.=")

        print("task_sets shape:", [np.array(t).shape for t in task_sets])
        print("ce_chains shape:", [np.array(c).shape for c in ce_chains])

        try:
            # np.savez("output/1single/task_set_u="+str(args.u)
            #          + "_n=" + str(args.n)
            #          + "_g=" + str(args.g) + ".npz", task_sets=task_sets,
            #          chains=ce_chains)

            data_to_save = {}
            for i, task_set in enumerate(task_sets):
                data_to_save[f'task_set_{i}'] = task_set
            for i, ce_chain in enumerate(ce_chains):
                data_to_save[f'ce_chain_{i}'] = ce_chain
            
            np.savez("output/1single/task_set_u=" + str(args.u) +
                        "_n=" + str(args.n) + 
                        "_g=" + str(args.g) + ".npz", **data_to_save)

        except Exception as e:
            print(e)
            print("ERROR: save")
            if debug_flag:
                breakpoint()
            else:
                return

    elif args.j == 2:
        """Interconnected ECU analysis.

        Required arguments:
        -j2
        -u : utilization (for loading)
        -g : task generation setting (for loading)

        Load data, create interconnected chains and then do the analysis by
        Davare, Duerr and Our.
        """

        if args.n == -1:
            print("ERROR: The number of runs -n is not specified.")
            return

        # Variables.
        utilization = args.u
        gen_setting = args.g
        num_runs = args.n
        number_interconn_ce_chains = 10000

        try:
            ###
            # Load data.
            ###
            print("=Load data.=")
            chains_single_ECU = []
            for i in range(num_runs):
                name_of_the_run = str(i)
                # data = np.load(
                #         "output/1single/task_set_u=" + str(utilization)
                #         + "_n=" + name_of_the_run
                #         + "_g=" + str(gen_setting)
                #         + ".npz", allow_pickle=True)

                # 加载之前保存的.npz文件
                data = np.load("output/1single/task_set_u=" + str(args.u) +
                            "_n=" + name_of_the_run + 
                            "_g=" + str(args.g) + ".npz", allow_pickle=True)

                # 初始化列表来恢复 task_sets 和 ce_chains
                restored_task_sets = []
                restored_ce_chains = []

                # 遍历文件中的每个键
                for key in data.keys():
                    if key.startswith('task_set_'):
                        # 将恢复的数组添加到 task_sets 列表
                        restored_task_sets.append(data[key])
                    elif key.startswith('ce_chain_'):
                        # 将恢复的数组添加到 ce_chains 列表
                        restored_ce_chains.append(data[key])

                for chain_set in restored_ce_chains:
                    for chain in chain_set:
                        chains_single_ECU.append(chain)

                # for chain_set in data.f.chains:
                #     for chain in chain_set:
                #         chains_single_ECU.append(chain)

                # Close data file and run the garbage collector.
                data.close()
                del data
                gc.collect()
        except Exception as e:
            print(e)
            print("ERROR: inputs from single are missing")
            if debug_flag:
                breakpoint()
            else:
                return

        ###
        # Interconnected cause-effect chain generation.
        ###
        print("=Interconnected cause-effect chain generation.=")
        chains_inter = []
        for j in range(0, number_interconn_ce_chains):
            chain_all = []  # sequence of all tasks (from chains + comm tasks)
            i_chain_all = []  # sequence of chains and comm_tasks

            # Generate communication tasks.
            com_tasks = comm.generate_communication_taskset(20, 10, 1000, True)

            # Fill chain_all and i_chain_all.
            k = 0
            for chain in list(np.random.choice(
                    chains_single_ECU, 5, replace=False)):  # randomly choose 5
                i_chain_all.append(chain)
                for task in chain.chain:
                    chain_all.append(task)
                if k < 4:  # communication tasks are only added in between
                    chain_all.append(com_tasks[k])
                    i_chain_all.append(com_tasks[k])
                k += 1

            chains_inter.append(c.CauseEffectChain(0, chain_all, i_chain_all))

            # End user notification
            if j % 100 == 0:
                print("\t", j)

        ###
        # Analyses (Davare, Duerr, Our).
        # Kloda is not included, since it is only for synchronized clocks.
        ###
        print("=Analyses (Davare, Duerr, Our).=")
        analyzer = a.Analyzer("0")

        print("Test: Davare.")
        analyzer.davare([chains_inter])

        print("Test: Duerr.")
        analyzer.reaction_duerr([chains_inter])
        analyzer.age_duerr([chains_inter])

        print("Test: Our.")
        # Our test can only be used when the single processor tests are already
        # done.
        analyzer.max_age_inter_our(chains_inter, reduced=True)
        analyzer.reaction_inter_our(chains_inter)

        print("Test: DBAge.")
        # analyzer.DBAge([chains_inter])

        print("Test: deltaBound.")
        # analyzer.deltaBound_inter([chains_inter])

        ###
        # Save data.
        ###
        print("=Save data.=")
        np.savez(
                "./output/2interconn/chains_" + "u=" + str(utilization)
                + "_g=" + str(gen_setting) + ".npz",
                chains_inter=chains_inter, chains_single_ECU=chains_single_ECU)

    elif args.j == 3:
        """Evaluation.

        Required arguments:
        -j3
        -g : task generation setting (for loading)
        """
        # Variables.
        gen_setting = args.g
        # utilizations = [50.0, 60.0, 70.0, 80.0, 90.0] # TODO
        utilizations = [50.0]

        try:
            ###
            # Load data.
            ###
            print("=Load data.=")
            chains_single_ECU = []
            chains_inter = []
            for ut in utilizations:
                data = np.load(
                        "output/2interconn/chains_" + "u=" + str(ut)
                        + "_g=" + str(args.g) + ".npz", allow_pickle=True)

                # Single ECU.
                for chain in data.f.chains_single_ECU:
                    chains_single_ECU.append(chain)

                # Interconnected.
                for chain in data.f.chains_inter:
                    chains_inter.append(chain)

                # Close data file and run the garbage collector.
                data.close()
                del data
                gc.collect()
        except Exception as e:
            print(e)
            print("ERROR: inputs for plotter are missing")
            if debug_flag:
                breakpoint()
            else:
                return

        ###
        # Draw plots.
        ###
        print("=Print time.=")
        with open("./output/time.txt", "w+", encoding="utf-8") as f:
            f.write('chainlength,' + get_object_field_keys(chains_single_ECU[0]) + '\n')
            for chain in chains_single_ECU:
                f.write(str(chain.length()) + ',' + get_object_field_values(chain) + '\n')

            # f.write("chainlength\t" +
            #         "davareTime\t"  +
            #         "duerrReact\t" +
            #         "duerrReactionTime\t"   +
            #         "duerrAgeTime\t"    +
            #         "klodaTime\t"   +
            #         "gunzelReactionTime\t"  +
            #         "gunzelAgeTime\t"   +
            #         "deltaBoundTime\t"  +
            #         "DBAgeTime\n"
            #     )
            # for chain in chains_single_ECU:
            #     f.write(f"{chain.length()}\t"   + 
            #             f"{chain.davareTime}\t" +
            #             f"{chain.duerr_react}\t"+
            #             f"{chain.duerrReactionTime}\t"  +
            #             f"{chain.duerrTime}\t"   +   # 因为analyzer代码原因，保存在chain.duerrTime中
            #             f"{chain.klodaTime}\t"  +
            #             f"{chain.gunzelReactionTime}\t" +
            #             f"{chain.gunzelAgeTime}\t"  +
            #             f"{chain.deltaBoundTime}\t" +
            #             f"{chain.DBAgeTime}\n"
            #     )

        print("=Draw plots.=")

        myeva = eva.Evaluation()

        # Single ECU Plot.
        myeva.davare_boxplot_age(
                chains_single_ECU,
                "output/3plots/davare_single_ecu_age"
                + "_g=" + str(args.g) + ".pdf",
                xaxis_label="", ylabel="Latency reduction [%]")
        myeva.davare_boxplot_reaction(
                chains_single_ECU,
                "output/3plots/davare_single_ecu_reaction"
                + "_g=" + str(args.g) + ".pdf",
                xaxis_label="", ylabel="Latency reduction [%]")

        # # Interconnected ECU Plot.
        # myeva.davare_boxplot_age_interconnected(
        #         chains_inter,
        #         "output/3plots/davare_interconnected_age"
        #         + "_g=" + str(args.g) + ".pdf",
        #         xaxis_label="", ylabel="Latency reduction [%]")
        # myeva.davare_boxplot_reaction_interconnected(
        #         chains_inter,
        #         "output/3plots/davare_interconnected_reaction"
        #         + "_g=" + str(args.g) + ".pdf",
        #         xaxis_label="", ylabel="Latency reduction [%]")

        # # Heatmap.
        # myeva.heatmap_improvement_disorder_age(
        #         chains_single_ECU,
        #         "output/3plots/heatmap" + "_our_age"
        #         + "_g=" + str(args.g) + ".pdf",
        #         yaxis_label="")
        # myeva.heatmap_improvement_disorder_react(
        #         chains_single_ECU,
        #         "output/3plots/heatmap" + "_our_react"
        #         + "_g=" + str(args.g) + ".pdf",
        #         yaxis_label="")

    elif args.j == 4:
        """Single ECU analysis.
        异步

        Required arguments:
        -j4
        -u : utilization [%]
        -g : task generation setting
        -r : number of runs
        -n : name of the run

        Create task sets and cause-effect chains, use TDA, Davare, Duerr, our
        analysis, Kloda, and save the Data
        """
        ###
        # Task set and cause-effect chain generation.
        ###
        print("=Task set and cause-effect chain generation.=")

        try:
            if args.g == 0:
                # WATERS benchmark
                print("WATERS benchmark.")

                # Statistical distribution for task set generation from table 3
                # of WATERS free benchmark paper.
                profile = [0.03 / 0.85, 0.02 / 0.85, 0.02 / 0.85, 0.25 / 0.85,
                           0.25 / 0.85, 0.03 / 0.85, 0.2 / 0.85, 0.01 / 0.85,
                           0.04 / 0.85]
                # Required utilization:
                req_uti = args.u/100.0
                # Maximal difference between required utilization and actual
                # utilization is set to 1 percent:
                threshold = 1.0

                # Create task sets from the generator.
                # Each task is a dictionary.
                print("\tCreate task sets.")
                task_sets_waters = []
                while len(task_sets_waters) < args.r:
                    task_sets_gen = waters.gen_tasksets(
                            1, req_uti, profile, True, threshold/100.0, 4)
                    task_sets_waters.append(task_sets_gen[0])

                # Transform tasks to fit framework structure.
                # Each task is an object of utilities.task.Task.
                trans1 = trans.Transformer("1", task_sets_waters, 10000000)
                task_sets = trans1.transform_tasks(True)

            elif args.g == 1:
                # UUniFast benchmark.
                print("UUniFast benchmark.")

                # Create task sets from the generator.
                print("\tCreate task sets.")

                # The following can be used for task generation with the
                # UUniFast benchmark without predefined periods.

                # # Generate log-uniformly distributed task sets:
                # task_sets_generator = uunifast.gen_tasksets(
                #         5, args.r, 1, 100, args.u, rounded=True)

                # Generate log-uniformly distributed task sets with predefined
                # periods:
                periods = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
                # Interval from where the generator pulls log-uniformly.
                min_pull = 1
                max_pull = 2000

                task_sets_uunifast = uunifast.gen_tasksets_pred(
                        50, args.r, min_pull, max_pull, args.u/100.0, periods)

                # Transform tasks to fit framework structure.
                trans2 = trans.Transformer("2", task_sets_uunifast, 10000000)
                task_sets = trans2.transform_tasks(True)

            else:
                print("Choose a benchmark")
                return

            # Create cause effect chains.
            print("\tCreate cause-effect chains")
            ce_chains = waters.gen_ce_chains(task_sets)
            # ce_chains contains one set of cause effect chains for each
            # task set in task_sets.

        except Exception as e:
            print(e)
            print("ERROR: task + ce creation")
            if debug_flag:
                breakpoint()
            else:
                task_sets = []
                ce_chains = []

        ###
        # First analyses (TDA, Davare, Duerr).
        ###
        print("=First analyses (TDA, Davare, Duerr).=")
        analyzer = a.Analyzer("0")

        try:
            # TDA for each task set.
            print("TDA.")
            for idxx in range(len(task_sets)):
                try:
                    # TDA.
                    i = 1
                    for task in task_sets[idxx]:
                        # Prevent WCET = 0 since the scheduler can
                        # not handle this yet. This case can occur due to
                        # rounding with the transformer.
                        if task.wcet == 0:
                            raise ValueError("WCET == 0")
                        task.rt = analyzer.tda(task, task_sets[idxx][:(i - 1)])
                        if task.rt > task.deadline:
                            raise ValueError(
                                    "TDA Result: WCRT bigger than deadline!")
                        i += 1
                except ValueError:
                    # If TDA fails, remove task and chain set and continue.
                    task_sets.remove(task_sets[idxx])
                    ce_chains.remove(ce_chains[idxx])
                    continue

            # End-to-End Analyses.
            print("Test: Davare.")
            analyzer.davare(ce_chains)

            print("Test: Duerr Reaction Time.")
            analyzer.reaction_duerr(ce_chains)

            print("Test: Duerr Data Age.")
            analyzer.age_duerr(ce_chains)

            # print("Test: DBAge.")
            # analyzer.DBAge(ce_chains)

            print("Test: deltaBound.")
            analyzer.deltaBound(ce_chains)

            ###
            # Second analyses (Simulation, Our, Kloda).
            ###
            print("=Second analyses (Simulation, Our, Kloda).=")
            i = 0  # task set counter
            schedules = []
            for task_set in task_sets:
                print("=Task set ", i+1)

                # Skip if there is no corresponding cause-effect chain.
                if len(ce_chains[i]) == 0:
                    continue

                # Event-based simulation.
                print("Simulation.")

                simulator = es.eventSimulator(task_set)

                # Determination of the variables used to compute the stop
                # condition of the simulation
                max_e2e_latency = max(ce_chains[i], key=lambda chain:
                                      chain.davare).davare
                max_phase = max(task_set, key=lambda task: task.phase).phase
                max_period = max(task_set, key=lambda task: task.period).period
                hyper_period = analyzer.determine_hyper_period(task_set)

                sched_interval = (
                        2 * hyper_period + max_phase  # interval from paper
                        + max_e2e_latency  # upper bound job chain length
                        + max_period)  # for convenience

                # Information for end user.
                print("\tNumber of tasks: ", len(task_set))
                print("\tHyperperiod: ", hyper_period)
                number_of_jobs = 0
                for task in task_set:
                    number_of_jobs += sched_interval/task.period
                print("\tNumber of jobs to schedule: ",
                      "%.2f" % number_of_jobs)

                # Stop condition: Number of jobs of lowest priority task.
                simulator.dispatcher(
                        int(math.ceil(sched_interval/task_set[-1].period)))

                # Simulation without early completion.
                schedule = simulator.e2e_result()
                schedules.append(schedule)

                # Analyses.
                for chain in ce_chains[i]:
                    print("Test: Our Data Age.")
                    analyzer.max_age_our(schedule, task_set, chain, max_phase,
                                         hyper_period, reduced=False)
                    analyzer.max_age_our(schedule, task_set, chain, max_phase,
                                         hyper_period, reduced=True)

                    print("Test: Our Reaction Time.")
                    analyzer.reaction_our(schedule, task_set, chain, max_phase,
                                          hyper_period)

                    # # Kloda analysis, assuming synchronous releases.
                    # print("Test: Kloda.")
                    # analyzer.kloda(chain, hyper_period)

                    # # Test.
                    # if chain.kloda < chain.our_react:
                    #     if debug_flag:
                    #         breakpoint()
                    #     else:
                    #         raise ValueError(
                    #                 ".kloda is shorter than .our_react")
                i += 1
        except Exception as e:
            print(e)
            print("ERROR: analysis")
            if debug_flag:
                breakpoint()
            else:
                task_sets = []
                ce_chains = []

        ###
        # Save data.
        ###
        print("=Save data.=")

        print("task_sets shape:", [np.array(t).shape for t in task_sets])
        print("ce_chains shape:", [np.array(c).shape for c in ce_chains])

        try:
            # np.savez("output/1single/task_set_u="+str(args.u)
            #          + "_n=" + str(args.n)
            #          + "_g=" + str(args.g) + "_offset.npz", task_sets=task_sets,
            #          chains=ce_chains)

            data_to_save = {}
            for i, task_set in enumerate(task_sets):
                data_to_save[f'task_set_{i}'] = task_set
            for i, ce_chain in enumerate(ce_chains):
                data_to_save[f'ce_chain_{i}'] = ce_chain
            
            np.savez("output/1single/task_set_u=" + str(args.u) +
                        "_n=" + str(args.n) + 
                        "_g=" + str(args.g) + "_offset.npz", **data_to_save)
            
        except Exception as e:
            print(e)
            print("ERROR: save")
            if debug_flag:
                breakpoint()
            else:
                return
        
    elif args.j == 5:
        """Interconnected ECU analysis.

        Required arguments:
        -j5
        -u : utilization (for loading)
        -g : task generation setting (for loading)

        Load data, create interconnected chains and then do the analysis by
        Davare, Duerr and Our.
        """

        if args.n == -1:
            print("ERROR: The number of runs -n is not specified.")
            return

        # Variables.
        utilization = args.u
        gen_setting = args.g
        num_runs = args.n
        number_interconn_ce_chains = 10000

        try:
            ###
            # Load data.
            ###
            print("=Load data.=")
            chains_single_ECU = []
            for i in range(num_runs):
                name_of_the_run = str(i)
                # data = np.load(
                #         "output/1single/task_set_u=" + str(utilization)
                #         + "_n=" + name_of_the_run
                #         + "_g=" + str(gen_setting)
                #         + "_offset.npz", allow_pickle=True)

                # 加载之前保存的.npz文件
                data = np.load("output/1single/task_set_u=" + str(args.u) +
                            "_n=" + name_of_the_run + 
                            "_g=" + str(args.g) + "_offset.npz", allow_pickle=True)

                # 初始化列表来恢复 task_sets 和 ce_chains
                restored_task_sets = []
                restored_ce_chains = []

                # 遍历文件中的每个键
                for key in data.keys():
                    if key.startswith('task_set_'):
                        # 将恢复的数组添加到 task_sets 列表
                        restored_task_sets.append(data[key])
                    elif key.startswith('ce_chain_'):
                        # 将恢复的数组添加到 ce_chains 列表
                        restored_ce_chains.append(data[key])

                for chain_set in restored_ce_chains:
                    for chain in chain_set:
                        chains_single_ECU.append(chain)

                # Close data file and run the garbage collector.
                data.close()
                del data
                gc.collect()
        except Exception as e:
            print(e)
            print("ERROR: inputs from single are missing")
            if debug_flag:
                breakpoint()
            else:
                return

        ###
        # Interconnected cause-effect chain generation.
        ###
        print("=Interconnected cause-effect chain generation.=")
        chains_inter = []
        for j in range(0, number_interconn_ce_chains):
            chain_all = []  # sequence of all tasks (from chains + comm tasks)
            i_chain_all = []  # sequence of chains and comm_tasks

            # Generate communication tasks.
            com_tasks = comm.generate_communication_taskset(20, 10, 1000, True)

            # Fill chain_all and i_chain_all.
            k = 0
            for chain in list(np.random.choice(
                    chains_single_ECU, 5, replace=False)):  # randomly choose 5
                i_chain_all.append(chain)
                for task in chain.chain:
                    chain_all.append(task)
                if k < 4:  # communication tasks are only added in between
                    chain_all.append(com_tasks[k])
                    i_chain_all.append(com_tasks[k])
                k += 1

            chains_inter.append(c.CauseEffectChain(0, chain_all, i_chain_all))

            # End user notification
            if j % 100 == 0:
                print("\t", j)

        ###
        # Analyses (Davare, Duerr, Our).
        # Kloda is not included, since it is only for synchronized clocks.
        ###
        print("=Analyses (Davare, Duerr, Our).=")
        analyzer = a.Analyzer("0")

        print("Test: Davare.")
        analyzer.davare([chains_inter])

        print("Test: Duerr.")
        analyzer.reaction_duerr([chains_inter])
        analyzer.age_duerr([chains_inter])

        print("Test: Our.")
        # Our test can only be used when the single processor tests are already
        # done.
        analyzer.max_age_inter_our(chains_inter, reduced=True)
        analyzer.reaction_inter_our(chains_inter)

        print("Test: DBAge.")
        # analyzer.DBAge([chains_inter])

        print("Test: deltaBound.")
        # analyzer.deltaBound_inter([chains_inter])

        ###
        # Save data.
        ###
        print("=Save data.=")
        np.savez(
                "./output/2interconn/chains_" + "u=" + str(utilization)
                + "_g=" + str(gen_setting) + "_offset.npz",
                chains_inter=chains_inter, chains_single_ECU=chains_single_ECU)
    
    elif args.j == 6:
        """Evaluation.

        Required arguments:
        -j6
        -g : task generation setting (for loading)
        """
        # Variables.
        gen_setting = args.g
        # utilizations = [50.0, 60.0, 70.0, 80.0, 90.0] # TODO
        utilizations = [50.0]

        try:
            ###
            # Load data.
            ###
            print("=Load data.=")
            chains_single_ECU = []
            chains_inter = []
            for ut in utilizations:
                data = np.load(
                        "output/2interconn/chains_" + "u=" + str(ut)
                        + "_g=" + str(args.g) + "_offset.npz", allow_pickle=True)

                # Single ECU.
                for chain in data.f.chains_single_ECU:
                    chains_single_ECU.append(chain)

                # Interconnected.
                for chain in data.f.chains_inter:
                    chains_inter.append(chain)

                # Close data file and run the garbage collector.
                data.close()
                del data
                gc.collect()
        except Exception as e:
            print(e)
            print("ERROR: inputs for plotter are missing")
            if debug_flag:
                breakpoint()
            else:
                return

        ###
        # Draw plots.
        ###
        print("=Print time.=")
        with open("./output/time_offset.txt", "w+", encoding="utf-8") as f:
            f.write('chainlength,' + get_object_field_keys(chains_single_ECU[0]) + '\n')
            for chain in chains_single_ECU:
                f.write(str(chain.length()) + ',' + get_object_field_values(chain) + '\n')

        print("=Draw plots.=")

        myeva = eva.Evaluation()

        # Single ECU Plot.
        myeva.davare_boxplot_age(
                chains_single_ECU,
                "output/3plots/davare_single_ecu_age"
                + "_g=" + str(args.g) + "_offset.pdf",
                xaxis_label="", ylabel="Latency reduction [%]")
        myeva.davare_boxplot_reaction(
                chains_single_ECU,
                "output/3plots/davare_single_ecu_reaction"
                + "_g=" + str(args.g) + "_offset.pdf",
                xaxis_label="", ylabel="Latency reduction [%]")

        # # Interconnected ECU Plot.
        # myeva.davare_boxplot_age_interconnected(
        #         chains_inter,
        #         "output/3plots/davare_interconnected_age"
        #         + "_g=" + str(args.g) + "_offset.pdf",
        #         xaxis_label="", ylabel="Latency reduction [%]")
        # myeva.davare_boxplot_reaction_interconnected(
        #         chains_inter,
        #         "output/3plots/davare_interconnected_reaction"
        #         + "_g=" + str(args.g) + "_offset.pdf",
        #         xaxis_label="", ylabel="Latency reduction [%]")

        # # Heatmap.
        # myeva.heatmap_improvement_disorder_age(
        #         chains_single_ECU,
        #         "output/3plots/heatmap" + "_our_age"
        #         + "_g=" + str(args.g) + ".pdf",
        #         yaxis_label="")
        # myeva.heatmap_improvement_disorder_react(
        #         chains_single_ECU,
        #         "output/3plots/heatmap" + "_our_react"
        #         + "_g=" + str(args.g) + ".pdf",
        #         yaxis_label="")

    elif args.j == 7:
        """多核 analysis.

        Required arguments:
        -j7
        -u : utilization (for loading)
        -g : task generation setting (for loading)

        Load data, create interconnected chains and then do the analysis by
        Davare, Duerr and Our.
        """
        # 处理器核数
        n = args.c

        # Variables.
        utilization = args.u
        gen_setting = args.g
        num_runs = args.n
        number_interconn_ce_chains = 30000

        try:
            ###
            # Load data.
            ###
            print("=Load data.=")
            chains_single_ECU = []
            com_tasks = []
            for i in range(num_runs):
                name_of_the_run = str(i)

                # 加载之前保存的.npz文件
                data = np.load("output/1single/task_set_u=" + str(args.u) +
                            "_n=" + name_of_the_run + 
                            "_g=" + str(args.g) + "_offset.npz")

                # 初始化列表来恢复 task_sets 和 ce_chains
                restored_task_sets = []
                restored_ce_chains = []

                # 遍历文件中的每个键
                for key in data.keys():
                    if key.startswith('task_set_'):
                        # 将恢复的数组添加到 task_sets 列表
                        restored_task_sets.append(data[key])
                    elif key.startswith('ce_chain_'):
                        # 将恢复的数组添加到 ce_chains 列表
                        restored_ce_chains.append(data[key])

                for chain_set in restored_ce_chains:
                    for chain in chain_set:
                        chains_single_ECU.append(chain)

                for task_set in restored_task_sets:
                    for task in task_set:
                        copyTask = Task(task.id, task.phase, task.bcet, task.wcet, task.period,
                 task.deadline, task.priority, message=True)
                        copyTask.rt = task.rt
                        com_tasks.append(copyTask)

                # data = np.load(
                #         "output/1single/task_set_u=" + str(utilization)
                #         + "_n=" + name_of_the_run
                #         + "_g=" + str(gen_setting)
                #         + "_offset.npz", allow_pickle=True)
                # for chain_set in data.f.chains:
                #     for chain in chain_set:
                #         chains_single_ECU.append(chain)

                # for task_set in data.f.task_sets:
                #     for task in task_set:
                #         copyTask = Task(task.id, task.phase, task.bcet, task.wcet, task.period,
                #  task.deadline, task.priority, message=True)
                #         copyTask.rt = task.rt
                #         com_tasks.append(copyTask)

                # Close data file and run the garbage collector.
                data.close()
                del data
                gc.collect()
        except Exception as e:
            print(e)
            print("ERROR: inputs from single are missing")
            if debug_flag:
                breakpoint()
            else:
                return
            
        ###
        # multiprocessor cause-effect chain generation.
        ###
        print("=multiprocessor cause-effect chain generation.=")
        chains_inter = []
        for j in range(0, number_interconn_ce_chains):
            chain_all = []  # sequence of all tasks (from chains + comm tasks)
            i_chain_all = []  # sequence of chains and comm_tasks

            # 由于原来任务集的任务已经在上面copy了，通过切割定理，无需用通信任务表示处理器切换，这里的代码保留但不使用
            # Generate communication tasks.
            # com_tasks = comm.generate_communication_taskset(20, 10, 1000, True)

            # Fill chain_all and i_chain_all.

            k = 0
            multi_GunzelAgeTime = 0
            multi_GunzelReactionTime = 0

            for chain in list(np.random.choice(chains_single_ECU, n, replace=False)):  # randomly choose 处理器数量个链

                # 只取长度小于等于4的链
                if chain.length() > 4:
                    continue

                i_chain_all.append(chain)
                for task in chain.chain:
                    chain_all.append(task)
                multi_GunzelAgeTime += chain.gunzelAgeTime
                multi_GunzelReactionTime += chain.gunzelReactionTime

            inter_chain = c.CauseEffectChain(0, chain_all, i_chain_all)
            inter_chain.multi_GunzelAgeTime = multi_GunzelAgeTime
            inter_chain.multi_GunzelReactionTime = multi_GunzelReactionTime

            chains_inter.append(inter_chain)

            # End user notification
            if j % 100 == 0:
                print("\t", j)

        ###
        # Analyses (Davare, Duerr, Our).
        # Kloda is not included, since it is only for synchronized clocks.
        ###
        print("=Analyses (Davare, Duerr, Our).=")
        analyzer = a.Analyzer("0")

        print("Test: Davare.")
        analyzer.davare([chains_inter])

        # print("Test: Duerr.")
        # analyzer.reaction_duerr([chains_inter])
        # analyzer.age_duerr([chains_inter])

        print("Test: Our.")
        # Our test can only be used when the single processor tests are already
        # done.
        analyzer.max_age_inter_our(chains_inter, reduced=True)
        analyzer.reaction_inter_our(chains_inter)

        # print("Test: DBAge.")
        # analyzer.DBAge([chains_inter])

        print("Test: deltaBound.")
        analyzer.deltaBound_inter(chains_inter)

        ###
        # Save data.
        ###
        print("=Save data.=")

        try:
            np.savez(
                "./output/4multi/chains_" + "u=" + str(utilization)
                + "_g=" + str(gen_setting) + "_multi.npz",
                chains_inter=chains_inter, chains_single_ECU=chains_single_ECU)

        except Exception as e:
            print(e)
            print("ERROR: save")
            if debug_flag:
                breakpoint()
            else:
                return
            

        print("=Print time.=")
        with open("./output/time_multi.txt", "w+", encoding="utf-8") as f:
            f.write('chainlength,' + get_object_field_keys(chains_inter[0]) + '\n')
            for chain in chains_inter:
                f.write(str(chain.length()) + ',' + get_object_field_values(chain) + '\n')

            # f.write("chainlength\t" +
            #         "davareTime\t" 
            #         "duerrReactionTime\t"   +
            #         "duerrAgeTime\t"    +
            #         "klodaTime\t"   +
            #         "gunzelReactionTime\t"  +
            #         "gunzelAgeTime\t"   +
            #         "deltaBoundTime\t"  +
            #         "DBAgeTime\t"  +
            #         "multi_gunzelReactionTime\t"  +
            #         "deltaBound\t"  +
            #         "inter_gunzelReaction\n"
            #     )
            # for chain in chains_inter:
            #     f.write(f"{chain.length()}\t"   + 
            #             f"{chain.davareTime}\t" + 
            #             f"{chain.duerrReactionTime}\t"  +
            #             f"{chain.duerrAgeTime}\t"   +
            #             f"{chain.klodaTime}\t"  +
            #             f"{chain.gunzelReactionTime}\t" +
            #             f"{chain.gunzelAgeTime}\t"  +
            #             f"{chain.deltaBoundTime}\t" +
            #             f"{chain.DBAgeTime}\t"  +
            #             f"{chain.multi_GunzelReactionTime}\t" +
            #             f"{chain.deltaBound}\t" +
            #             f"{chain.inter_our_react}\n"
            #     )

if __name__ == '__main__':
    main()
