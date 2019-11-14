
import random
import numpy
import array
import collections
import matplotlib.pyplot as plt

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


class Experiment:

    # Problem parameter
    NB_QUEENS = 8

    def __init__(self, _is_premutation, _cxpb, _mutpb):
        self.is_premutation = _is_premutation
        self.cxpb =_cxpb
        self.mutpb = _mutpb

    def evaluateFunc(self,individual):
        size = len(individual)
        # Count the number of conflicts with other queens.
        # The conflicts can only be diagonal, count on each diagonal line
        left_diagonal = [0] * (2 * size - 1)
        right_diagonal = [0] * (2 * size - 1)

        # Sum the number of queens on each diagonal:
        for i in range(size):
            left_diagonal[i + individual[i]] += 1
            right_diagonal[size - 1 - i + individual[i]] += 1

        # Count the number of conflicts on each diagonal
        sum_ = 0
        for i in range(2 * size - 1):
            if left_diagonal[i] > 1:
                sum_ += left_diagonal[i] - 1
            if right_diagonal[i] > 1:
                sum_ += right_diagonal[i] - 1

        if not self.is_premutation:
            #Count the number of conflicts on each row
            row_freq =  collections.Counter(individual)
            d = dict((k, v) for k, v in row_freq.items() if v > 1)
            sum_ += len(d)

        row_freq = collections.Counter(individual)
        d = dict((k, v) for k, v in row_freq.items() if v > 1)
        if len(d) > 1:
            x=1

        score = 1/(sum_+1)
        return score,


    def createMutate(self,individual):
        if self.is_premutation:
            indx1,indx2 = random.sample(range(0, self.NB_QUEENS - 1), 2)
            num1 = individual[indx1]
            num2 = individual[indx2]
            individual[indx1] = num2
            individual[indx2] = num1
        else:
            index = random.randint(0, self.NB_QUEENS - 1)
            value = random.randint(0, self.NB_QUEENS - 1)
            individual[index] = value
        return individual,

    def setExperiment(self):
        if self.is_premutation:
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", list, fitness=creator.FitnessMax)
            toolbox = base.Toolbox()
            toolbox.register("permutation", random.sample, range(self.NB_QUEENS), self.NB_QUEENS)
            toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.permutation)

        if not self.is_premutation:
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", array.array, typecode="b", fitness=creator.FitnessMax, strategy=None)
            toolbox = base.Toolbox()
            toolbox.register("array", random.sample, range(self.NB_QUEENS), self.NB_QUEENS)
            toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.array)

            # Structure initializers
            # An individual is a list that represents the position of each queen.
            # Only the line is stored, the column is the index of the number in the list.
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", self.evaluateFunc)
        # crossover method - single point
        if self.is_premutation:
            toolbox.register("mate", tools.cxPartialyMatched)
        if not self.is_premutation:
            toolbox.register("mate", tools.cxOnePoint)
        # mutate method - one point (we create it)
        toolbox.register("mutate", self.createMutate)
        # toolbox.register("mutate", tools.mutShuffleIndexes, indpb = 2.0/NB_QUEENS)
        toolbox.register("select", tools.selRoulette)
        # toolbox.register("select", tools.selTournament, tournsize=3)
        # deap.tools.selRoulette(individuals, k, fit_attr='fitness')

        random.seed(0)
        pop = toolbox.population(n=100)
        hof = tools.HallOfFame(1)
        # logbook = tools.Logbook()
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("Avg", numpy.mean)
        stats.register("median", numpy.median)
        stats.register("Min", numpy.min)
        stats.register("Max", numpy.max)

        pop, log1 = algorithms.eaSimple(pop, toolbox, cxpb=self.cxpb, mutpb=self.mutpb, ngen=100, stats=stats, halloffame=hof,verbose=True)
        #pop, log2 = algorithms.eaSimple(pop, toolbox, cxpb=_cxpb, mutpb=_mutpb, ngen=100, stats=stats, halloffame=hof,verbose=True)
        #pop, log3 = algorithms.eaSimple(pop, toolbox, cxpb=_cxpb, mutpb=_mutpb, ngen=100, stats=stats, halloffame=hof,verbose=True)
        #self.getPlot(log1, log2, log3)
        return log1

    def getPlot(self,log1, log2,log3):

        gen = log1.select("gen")
        median1, median2, median3 = log1.select("median"), log2.select("median"), log3.select("median")
        Avg1, Avg2, Avg3 = log1.select("Avg"), log2.select("Avg"), log3.select("Avg")
        # min = log.select("Min")
        # max = log.select("Max")

        # fig, ax1 = plt.subplots()
        # line1 = ax1.plot(gen, min, "b-", label="Best Fitness")
        # ax1.set_xlabel("Generation")
        # line2 = ax1.plot(gen, max, "r-", label="Worst Fitness")
        # line3 = ax1.plot(gen, Avg, "g-", label="Average Fitness")
        # line4 = ax1.plot(gen, median, "y-", label="Median Fitness")
        # lns = line1 + line2 + line3 + line4
        # labs = [l.get_label() for l in lns]
        # ax1.legend(lns, labs, loc="center right")
        #
        # plt.show()