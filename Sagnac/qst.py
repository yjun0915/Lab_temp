import sys, os, time

import numpy as np
import pandas as pd

from itertools import product
from actions import Function
from rich.console import Console
from rich.table import Table


class QST:
    def __init__(self, stages, detector, offset):
        self.stages = stages
        self.detector = detector
        self.order = ['H1', 'Q1', 'H2', 'Q2']
        parameters = ['H', 'V', 'D', 'A', 'R', 'L']
        self.basis = np.array(list(product(parameters, parameters)))
        self.a_angle = {
            'H': [offset[0], offset[1]],
            'V': [offset[0]+45, offset[1]],
            'D': [offset[0]+22.5, offset[1]],
            'A': [offset[0]-22.5, offset[1]],
            'R': [offset[0], offset[1]+45],
            'L': [offset[0], offset[1]-45]
        }
        self.b_angle = {
            'H': [offset[2], offset[3]],
            'V': [offset[2]+45, offset[3]],
            'D': [offset[2]+22.5, offset[3]],
            'A': [offset[2]-22.5, offset[3]],
            'R': [offset[2], offset[3]+45],
            'L': [offset[2], offset[3]-45]
        }
        self.P = pd.DataFrame(columns=['H', 'V', 'D', 'A', 'R', 'L'], index=['H', 'V', 'D', 'A', 'R', 'L'])
        self.func = Function(stages)
        self.console = Console()
        self.table = Table(show_lines=True)
        self.table.add_column("", justify="center", style="cyan")

    def measure(self):
        for base in self.basis:
            for idx in range(4):
                if idx <= 1:
                    self.stages[self.order[idx]][0].move_to(self.a_angle[base[0]][idx])
                if idx >= 2:
                    self.stages[self.order[idx]][0].move_to(self.b_angle[base[1]][idx-2])
            while not all(self.func.is_stable()):
                time.sleep(0.1)

            params = self.detector.getConfiguration()['params']
            time.sleep(params['binwidth'] * params['n values'] * 1e-12)
            count_data = self.detector.getData()
            A_channel_counts = np.sum(a=count_data, axis=1)[0]
            B_channel_counts = np.sum(a=count_data, axis=1)[1]
            coincidence_data = np.sum(a=count_data, axis=1)[2]
            self.P.loc[base[0], base[1]] = coincidence_data
            sys.stdout.write('\x1b[1A\x1b[2K'*7)
            self.console.clear()
            self.console.rule(f'[bold yellow]Coincidence counts for|{base[0]}{base[1]}>: {coincidence_data}')
            self.table = Table(show_lines=True)
            self.table.add_column("", justify="center", style="cyan")
            for c in self.P.columns:
                self.table.add_column(c, justify="center")

            for idx in self.P.index:
                row = [idx] + [
                    str(int(self.P.loc[idx, col])) if not pd.isna(self.P.loc[idx, col]) else "    "
                    for col in self.P.columns
                ]
                self.table.add_row(*row)

            self.console.print(self.table)
        return self.P
