import numpy as np
import matplotlib.pyplot as plt

def draw_hist(slots, sinks, intents):
    f1 = plt.figure(1)
    plt.hist(slots, bins=[0, 1, 2, 3, 4, 5, 6, 10, 20])
    plt.title("Histogram to show no. of slots for Alexa Repos (" + str(len(slots)) + ")")
    plt.xlabel("No. of Slots")
    plt.ylabel("Frequency Density")
    plt.minorticks_on()
    plt.grid(True, which='both')

    f2 = plt.figure(2)
    plt.hist(sinks, bins='auto')
    plt.title("Histogram to show no. of sink calls for Alexa Repos (" + str(len(sinks)) + ")")
    plt.xlabel("No. of sink module calls (request/request-promise)")
    plt.ylabel("Frequency Density")
    plt.minorticks_on()
    plt.grid(True, which='both')
   
    f3 = plt.figure(3)
    plt.hist(intents, bins='auto')
    plt.title("Histogram to show no. of intent functions for Alexa Repos (" + str(len(intents)) + ")")
    plt.xlabel("No. of intent functions")
    plt.ylabel("Frequency Density")
    plt.minorticks_on()
    plt.grid(True, which='both')

    plt.show()
