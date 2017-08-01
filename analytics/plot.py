import numpy as np
import matplotlib.pyplot as plt

def draw_hist(slots, sinks, intents):
    f1 = plt.figure(1)
    plt.hist(slots, bins=4)
    plt.title("Histogram to show no. of slots for Alexa Repos (" + str(len(slots)) + ")")
    
    f2 = plt.figure(2)
    plt.hist(sinks, bins='auto')
    plt.title("Histogram to show no. of sink calls for Alexa Repos (" + str(len(sinks)) + ")")
   
    f3 = plt.figure(3)
    plt.hist(intents, bins='auto')
    plt.title("Histogram to show no. of intent functions for Alexa Repos (" + str(len(intents)) + ")")
   
    plt.show()
