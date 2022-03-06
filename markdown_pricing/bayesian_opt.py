
#!/usr/bin/env python

"""bayesian_opt.py: Optimization"""

__author__ = "Jidhu Mohan"
__copyright__ = "Copyright (C) 2022 Factory-AI project"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jidhu Mohan"
__email__ = "Jidhu.Mohan@gmail.com"
__status__ = "PoV" 


from bayes_opt import BayesianOptimization
from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs

class OPT:
    """ optimizer class """
    def __init__(self, objective_fun, bounds,verbose=2):
        self.optimizer = BayesianOptimization(f=objective_fun, 
                                                pbounds=bounds,
                                                verbose=verbose, random_state=1)

    def run(self, init_points=2, n_iter=5):
        self.optimizer.maximize(init_points=init_points, n_iter=n_iter)
        print(self.optimizer.max)

    def change_bounds(self, new_bounds):
        self.optimizer.set_bounds(new_bounds=new_bounds)

    def guide(self, params):
        self.optimizer.probe(params=params, lazy=True)

    def get_history(self):
        for i,res in enumerate(self.optimizer.res):
            print(f"Iteration {i}: \t {res}")

    def save(self, filename='factory_opt/log.json'):
        logger = JSONLogger(path=filename)
        self.optimizer.subscribe(event=Events.OPTIMIZATION_STEP, subscriber=logger)

    def load(self, filename='factory_opt/log.json'):
        load_logs(self.optimizer, logs=filename)
        print(f"{len(self.optimizer.space)} points loaded successfully..")


