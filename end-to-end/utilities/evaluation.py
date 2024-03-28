"""Drawing Plots."""
import matplotlib.pyplot as plt
import numpy as np


class Evaluation:
    """Collection of functions to draw plots."""
    ymin = -5  # y-axis beginning
    ymax = 105  # y-axis ending
    hlines = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]  # horizontal lines
    ylabel = ""  # global label for y-axis

    def davare_boxplot_age(self, chains, filename, xaxis_label="",
                           ylabel=None):
        """Boxplot: Single ECU, maximum data age.

        Shows the latency reduction [%] of several analyses compared to Davare.
        """
        if ylabel is None:
            ylabel = self.ylabel

        # Analysis results.
        kloda = []
        duerr = []
        our = []  # reduced data age (for comparison)
        DBAge = []

        for chain in chains:
            duerr.append((1 - (chain.duerr_age / chain.davare)) * 100)
            kloda.append((1 - (chain.kloda / chain.davare)) * 100)
            our.append((1 - (chain.our_red_age / chain.davare)) * 100)
            DBAge.append((1 - (chain.DBAge / chain.davare)) * 100)

        # Plotting.
        # Blue box configuration:
        boxprops = dict(linewidth=4, color='blue')
        # Median line configuration:
        medianprops = dict(linewidth=4, color='red')
        whiskerprops = dict(linewidth=4, color='black')
        capprops = dict(linewidth=4)
        # Size parameters:
        plt.rcParams.update({'font.size': 18})
        plt.rcParams.update({'figure.subplot.top': 0.99})
        plt.rcParams.update({'figure.subplot.bottom': 0.25})
        plt.rcParams.update({'figure.subplot.left': 0.06})
        plt.rcParams.update({'figure.subplot.right': 0.90})
        plt.rcParams.update({'figure.figsize': [10, 4.8]})
        # Draw plots:
        fig1, ax1 = plt.subplots()
        ax1.set_ylim([self.ymin, self.ymax])
        ax1.set_ylabel(ylabel, fontsize=25)
        ax1.hlines(self.hlines, 0, 5, linestyles=(0, (5, 5)),
                   colors="lightgrey")
        my_plot = ax1.boxplot(
                [duerr, kloda, our, DBAge],
                labels=["Dürr", "Kloda", "Günzel", "DBAge"],
                showfliers=False,
                boxprops=boxprops,
                medianprops=medianprops,
                whiskerprops=whiskerprops,
                capprops=capprops,
                widths=0.6)
        ax1.set_yticks([0, 20, 40, 60, 80, 100])
        ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax1.tick_params(axis='x', rotation=0, labelsize=20)
        ax1.tick_params(axis='y', rotation=0, labelsize=20)
        ax1.set_xlabel(xaxis_label, fontsize=20)
        plt.tight_layout()

        # Save.
        plt.savefig(filename)

    def davare_boxplot_reaction(self, chains, filename, xaxis_label="",
                                ylabel=None):
        """Boxplot: Single ECU, maximum reaction time.

        Shows the latency reduction [%] of several analyses compared to Davare.
        """
        if ylabel is None:
            ylabel = self.ylabel

        # Analysis results.
        kloda = []
        duerr = []
        our = []
        deltaBound = []

        for chain in chains:
            duerr.append((1 - (chain.duerr_react / chain.davare)) * 100)
            kloda.append((1 - (chain.kloda / chain.davare)) * 100)
            our.append((1 - (chain.our_react / chain.davare)) * 100)
            deltaBound.append((1 - (chain.deltaBound / chain.davare)) * 100)

        # Plotting.
        # Blue box configuration:
        boxprops = dict(linewidth=4, color='blue')
        # Median line configuration:
        medianprops = dict(linewidth=4, color='red')
        whiskerprops = dict(linewidth=4, color='black')
        capprops = dict(linewidth=4)
        # Size parameters:
        plt.rcParams.update({'font.size': 18})
        plt.rcParams.update({'figure.subplot.top': 0.99})
        plt.rcParams.update({'figure.subplot.bottom': 0.25})
        # plt.rcParams.update({'figure.subplot.left': 0.18})
        # plt.rcParams.update({'figure.subplot.right': 0.99})
        # plt.rcParams.update({'figure.figsize': [10, 4.8]})
        plt.rcParams.update({'figure.subplot.left': 0.06})
        plt.rcParams.update({'figure.subplot.right': 0.90})
        plt.rcParams.update({'figure.figsize': [10, 4.8]})
        # Draw plots:
        fig1, ax1 = plt.subplots()
        ax1.set_ylim([self.ymin, self.ymax])
        ax1.set_ylabel(ylabel, fontsize=25)
        # ax1.hlines(self.hlines, 0, 4, linestyles=(0, (5, 5)),
        #            colors="lightgrey")
        ax1.hlines(self.hlines, 0, 5, linestyles=(0, (5, 5)),
                   colors="lightgrey")
        my_plot = ax1.boxplot(
                [duerr, kloda, our, deltaBound],
                labels=["Dürr", "Kloda", "Günzel", "delta-Bound"],
                showfliers=False,
                boxprops=boxprops,
                medianprops=medianprops,
                whiskerprops=whiskerprops,
                capprops=capprops,
                widths=0.6)
        ax1.set_yticks([0, 20, 40, 60, 80, 100])
        ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        # ax1.tick_params(axis='x', rotation=0, labelsize=35)
        # ax1.tick_params(axis='y', rotation=0, labelsize=35)
        # ax1.set_xlabel(xaxis_label, fontsize=40)
        ax1.tick_params(axis='x', rotation=0, labelsize=20)
        ax1.tick_params(axis='y', rotation=0, labelsize=20)
        ax1.set_xlabel(xaxis_label, fontsize=20)
        plt.tight_layout()

        # Save.
        plt.savefig(filename)

    def davare_boxplot_age_interconnected(self, chains, filename,
                                          xaxis_label="", ylabel=None):
        """Boxplot: Interconnected ECU, maximum data age.

        Shows the latency reduction [%] of several analyses compared to Davare.
        """
        if ylabel is None:
            ylabel = self.ylabel

        # Analysis results.
        duerr = []
        our = []  # reduced interconnected data age (for comparison)
        DBAge = []

        for chain in chains:
            duerr.append((1-(chain.duerr_age/chain.davare))*100)
            our.append((1-(chain.inter_our_red_age/chain.davare))*100)
            DBAge.append((1-(chain.DBAge/chain.davare))*100)

        # Plotting.
        # Blue box configuration:
        boxprops = dict(linewidth=4, color='blue')
        # Median line configuration:
        medianprops = dict(linewidth=4, color='red')
        whiskerprops = dict(linewidth=4, color='black')
        capprops = dict(linewidth=4)
        # Size parameters:
        plt.rcParams.update({'font.size': 18})
        plt.rcParams.update({'figure.subplot.top': 0.99})
        plt.rcParams.update({'figure.subplot.bottom': 0.25})
        plt.rcParams.update({'figure.subplot.left': 0.18})
        plt.rcParams.update({'figure.subplot.right': 0.99})
        plt.rcParams.update({'figure.figsize': [10, 4.8]})
        # Draw plots:
        fig1, ax1 = plt.subplots()
        ax1.set_ylim([self.ymin, self.ymax])
        ax1.set_ylabel(ylabel, fontsize=20)
        ax1.hlines(self.hlines, 0, 4, linestyles=(0, (5, 5)),
                   colors="lightgrey")
        my_plot = ax1.boxplot(
                [duerr, our, DBAge],
                labels=["Dürr", "Günzel", "DBAge"],
                showfliers=False,
                boxprops=boxprops,
                medianprops=medianprops,
                whiskerprops=whiskerprops,
                capprops=capprops,
                widths=0.6)
        ax1.set_yticks([0, 20, 40, 60, 80, 100])
        ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax1.tick_params(axis='x', rotation=0, labelsize=20)
        ax1.tick_params(axis='y', rotation=0, labelsize=20)
        ax1.set_xlabel(xaxis_label, fontsize=20)
        plt.tight_layout()

        # Save.
        plt.savefig(filename)

    def davare_boxplot_reaction_interconnected(self, chains, filename,
                                               xaxis_label="", ylabel=None):
        """Boxplot: Interconnected ECU, maximum reaction time.

        Shows the latency reduction [%] of several analyses compared to Davare.
        """
        if ylabel is None:
            ylabel = self.ylabel

        # Analysis results.
        duerr = []
        our = []
        deltaBound = []

        for chain in chains:
            duerr.append((1-(chain.duerr_react/chain.davare))*100)
            our.append((1-(chain.inter_our_react/chain.davare))*100)
            deltaBound.append((1-(chain.inter_deltaBound/chain.davare))*100)

        # Plotting.
        # Blue box configuration:
        boxprops = dict(linewidth=4, color='blue')
        # Median line configuration:
        medianprops = dict(linewidth=4, color='red')
        whiskerprops = dict(linewidth=4, color='black')
        capprops = dict(linewidth=4)
        # Size parameters:
        plt.rcParams.update({'font.size': 18})
        plt.rcParams.update({'figure.subplot.top': 0.99})
        plt.rcParams.update({'figure.subplot.bottom': 0.25})
        plt.rcParams.update({'figure.subplot.left': 0.18})
        plt.rcParams.update({'figure.subplot.right': 0.99})
        plt.rcParams.update({'figure.figsize': [10, 4.8]})
        # Draw plots:
        fig1, ax1 = plt.subplots()
        ax1.set_ylim([self.ymin, self.ymax])
        ax1.set_ylabel(ylabel, fontsize=25)
        ax1.hlines(self.hlines, 0, 3, linestyles=(0, (5, 5)),
                   colors="lightgrey")
        my_plot = ax1.boxplot(
                [duerr, our, deltaBound],
                labels=["Dürr", "Günzel", "delta-Bound"],
                showfliers=False,
                boxprops=boxprops,
                medianprops=medianprops,
                whiskerprops=whiskerprops,
                capprops=capprops,
                widths=0.6)
        ax1.set_yticks([0, 20, 40, 60, 80, 100])
        ax1.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax1.tick_params(axis='x', rotation=0, labelsize=35)
        ax1.tick_params(axis='y', rotation=0, labelsize=35)
        ax1.set_xlabel(xaxis_label, fontsize=40)
        plt.tight_layout()

        # Save.
        plt.savefig(filename)

    def heatmap_improvement_disorder_age(self, chains, filename,
                                         yaxis_label="", xaxis_label=""):
        """Heatmap: Reduction of maximum data age w.r.t. normalized chain
        disorder.

        Shows the latency reduction [%] of our analyses compared to Davare.
        """
        import seaborn as sns  # only necessary for heatmaps

        # Analysis results.
        disorder_ratio = []
        improvement = []
        for chain in chains:
            improvement.append((1-(chain.our_age/chain.davare))*100)
            if len(chain.chain) == 1:
                disorder_ratio.append(0)
            else:
                disorder_ratio.append(float(chain.chain_disorder)
                                      / float(len(chain.chain)-1))

        # Prepare plot.
        xedges = []
        yedges = []
        for x in range(20+1):
            xedges.append(x*0.05)
        for y in range(20+1):
            yedges.append(y*5)
        heatmap, xedges, yedges = np.histogram2d(disorder_ratio, improvement,
                                                 bins=(xedges, yedges))
        heatmap = np.log(heatmap+1)  # logarithmic color-scaling

        # Draw plot.
        plt.clf()
        fig1, ax1 = plt.subplots()
        ax = sns.heatmap(heatmap, linewidth=0.5)

        # Configurations.
        cbar = ax.collections[0].colorbar
        cbar.set_ticks([0, 4, 8])
        cbar.set_ticklabels(['$10^0$-1', '$10^4$-1', '$10^8$-1'])
        cbar.ax.tick_params(labelsize=33)
        xticks = [0, 4, 8, 12, 16, 20]
        yticks = [0, 4, 8, 12, 16, 20]
        ax1.invert_yaxis()
        ax.set_xticks(xticks)
        ax.set_xticklabels(("0", "0.2", "0.4", "0.6", "0.8", "1"))
        # ax.set_yticks(yticks)
        ax.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax.tick_params(axis='x', rotation=0, labelsize=28)
        ax.tick_params(axis='y', rotation=0, labelsize=38)
        ax1.set_xlabel(xaxis_label, fontsize=38)
        ax1.set_ylabel(yaxis_label, fontsize=38)
        plt.tight_layout()

        # Save.
        plt.savefig(filename)

    def heatmap_improvement_disorder_react(self, chains, filename,
                                           yaxis_label="", xaxis_label=""):
        """Heatmap: Reduction of maximum reaction time w.r.t. normalized chain
        disorder.

        Shows the latency reduction [%] of our analyses compared to Davare.
        """
        import seaborn as sns  # only necessary for heatmaps

        # Analysis results.
        disorder_ratio = []
        improvement = []
        for chain in chains:
            improvement.append((1-(chain.our_react/chain.davare))*100)
            if len(chain.chain) == 1:
                disorder_ratio.append(0)
            else:
                disorder_ratio.append(float(chain.chain_disorder)
                                      / float(len(chain.chain)-1))

        # Prepare plot.
        xedges = []
        yedges = []
        for x in range(20+1):
            xedges.append(x*0.05)
        for y in range(20+1):
            yedges.append(y*5)
        heatmap, xedges, yedges = np.histogram2d(disorder_ratio, improvement,
                                                 bins=(xedges, yedges))
        heatmap = np.log(heatmap+1)  # logarithmic color-scaling

        # Draw plot.
        plt.clf()
        fig1, ax1 = plt.subplots()
        ax = sns.heatmap(heatmap, linewidth=0.5)

        # Configurations.
        cbar = ax.collections[0].colorbar
        cbar.set_ticks([0, 4, 8])
        cbar.set_ticklabels(['$10^0$-1', '$10^4$-1', '$10^8$-1'])
        cbar.ax.tick_params(labelsize=33, rotation=0)
        xticks = [0, 4, 8, 12, 16, 20]
        yticks = [0, 4, 8, 12, 16, 20]
        ax1.invert_yaxis()
        ax.set_xticks(xticks)
        ax.set_xticklabels(("0", "0.2", "0.4", "0.6", "0.8", "1"))
        ax.set_yticks(yticks)
        ax.set_yticklabels(("0", "20", "40", "60", "80", "100"))
        ax.tick_params(axis='x', rotation=0, labelsize=28)
        ax.tick_params(axis='y', rotation=0, labelsize=38)
        ax1.set_xlabel(xaxis_label, fontsize=38)
        ax1.set_ylabel(yaxis_label, fontsize=38)
        plt.tight_layout()

        # Save.
        plt.savefig(filename)