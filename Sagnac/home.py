from scipy.optimize import minimize
from actions import Function

import numpy as np
import pandas as pd

import time, sys

class FastAxis:
    def __init__(self, stages, detector):
        self.stages = stages
        self.detector = detector
        self.order = ['H1', 'Q1', 'H2', 'Q2']
        self.func = Function(stages)
        self.iteration = [0]
        self.debuger = [0]

    def obj_function(self, x):
        try:
            for idx in range(len(x)):
                self.stages[self.order[idx]][0].move_to(x[idx])
            while not all(self.func.is_stable()):
                # print("[Status]: ", self.func.status()[0], " >< [Is Stable]: ", self.func.is_stable())
                time.sleep(0.1)

            params = self.detector.getConfiguration()['params']
            time.sleep(params['binwidth']*params['n values']*1e-12)
            count_data = self.detector.getData()
            A_channel_counts = np.sum(a=count_data, axis=1)[0]
            B_channel_counts = np.sum(a=count_data, axis=1)[1]
            coincidence_data = np.sum(a=count_data, axis=1)[2]
            #print("A: ", A_channel_counts, ", B: ", B_channel_counts, ", CC: ", coincidence_data)
            self.debuger.append(coincidence_data)
            return -1 * (A_channel_counts * B_channel_counts)
        except Exception as e:
            print("[ERROR in obj_function]:", e)
            return np.inf

    def callback(self, xk):
        self.iteration[0] += 1
        print(f"Iteration {self.iteration[0]}: x = {xk}")
        sys.stdout.flush()

    def excute(self, x0):
        MLE_model = minimize(
            fun=self.obj_function,
            x0=x0,
            callback=self.callback,
            method='Powell',
            bounds=[
                (0, 360),
                (0, 360),
                (0, 360),
                (0, 360)
            ],
            options={
                'disp': True,
                'maxiter': 100,
            },
            tol=1e-6
        )
        pd.DataFrame(self.debuger).to_csv(path_or_buf='log.csv', sep=',')
        return MLE_model
