from Experiment import *
import pandas as pd
import statistics


def getPlot(log1, log2, log3, titel):
    Exp_data = pd.DataFrame(columns=('Generation', 'Best Fitness', 'Worst Fitness', 'Average Fitness','Median Fitness'))

    gen = log1.select("gen")
    median1, median2, median3 = log1.select("median"), log2.select("median"), log3.select("median")
    Avg1, Avg2, Avg3 = log1.select("Avg"), log2.select("Avg"), log3.select("Avg")
    min1, min2, min3 = log1.select("Min"), log2.select("Min"), log3.select("Min")
    max1, max2, max3 = log1.select("Max"), log2.select("Max"), log3.select("Max")

    median = [statistics.mean(k) for k in zip(median1,median2,median3)]
    Avg = [statistics.mean(k) for k in zip(Avg1, Avg2, Avg3)]
    min = [statistics.mean(k) for k in zip(min1, min2, min3)]
    max = [statistics.mean(k) for k in zip(max1, max2, max3)]

    Exp_data['Generation'] = gen
    Exp_data['Best Fitness'] = max
    Exp_data['Worst Fitness'] = min
    Exp_data['Average Fitness'] = Avg
    Exp_data['Median Fitness'] = median

    Exp_data.to_csv('C:/EvolutionaryAlgorithm/Assigments1/Results/'+ titel +'.csv')

    fig, ax1 = plt.subplots()
    line1 = ax1.plot(gen, max, "b-", label="Best Fitness")
    ax1.set(xlabel='Generation', ylabel='Fitness',
           title=titel + ' Avg Results')
    ax1.grid()
    line2 = ax1.plot(gen, min, "r-", label="Worst Fitness")
    line3 = ax1.plot(gen, Avg, "g-", label="Average Fitness")
    line4 = ax1.plot(gen, median, "y-", label="Median Fitness")
    lns = line1 + line2 + line3 + line4
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="lower right")
    plt.show()

def main(seed=0):
    Experiment1 = Experiment(False, 0.7, 0.001)
    log1_1 = Experiment1.setExperiment()
    log1_2 = Experiment1.setExperiment()
    log1_3 = Experiment1.setExperiment()
    getPlot(log1_1, log1_2, log1_3,'Experiment1')

    Experiment2 = Experiment(True, 0.4, 0.001)
    log2_1 = Experiment2.setExperiment()
    log2_2 = Experiment2.setExperiment()
    log2_3 = Experiment2.setExperiment()
    getPlot(log2_1, log2_2, log2_3,'Experiment2')

    Experiment3 = Experiment(True, 0.1, 0.001)
    log3_1 = Experiment3.setExperiment()
    log3_2 = Experiment3.setExperiment()
    log3_3 = Experiment3.setExperiment()
    getPlot(log3_1, log3_2, log3_3,'Experiment3')

    Experiment4 = Experiment(True, 0.7, 0.01)
    log4_1 = Experiment4.setExperiment()
    log4_2 = Experiment4.setExperiment()
    log4_3 = Experiment4.setExperiment()
    getPlot(log4_1, log4_2, log4_3,'Experiment4')

    Experiment5 = Experiment(True, 0.7, 0.1)
    log5_1 = Experiment5.setExperiment()
    log5_2 = Experiment5.setExperiment()
    log5_3 = Experiment5.setExperiment()
    getPlot(log5_1, log5_2, log5_3,'Experiment5')

    return

if __name__ == "__main__":
    main()