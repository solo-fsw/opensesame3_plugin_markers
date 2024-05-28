# %% Imports
import unittest
import os
from libopensesame.experiment import experiment
from qtpy.QtWidgets import QApplication

logfile_path = os.path.join(os.path.dirname(__file__), r'./data/tmp.csv')
experiment_path = os.path.join(os.path.dirname(__file__), r'data')

crashing_experiments = [
    
]

normal_experiments = [
    
]

class runExperiments(unittest.TestCase):
    
    def test_runTests(self):
        app = QApplication([])
                
        for experiment_file in normal_experiments:
            print(f"Testing {experiment_file}")
            e = experiment(
                logfile = logfile_path,
                experiment_path = experiment_path,
                string = os.path.join(experiment_path, experiment_file)
            )
            e.var.canvas_backend = r'legacy'
            e.run()
            self.assertEqual(True, True)
            
    def test_runTestsCrash(self):
        app = QApplication([])
        for experiment_file in crashing_experiments:
            print(f"Testing {experiment_file}")
            e = experiment(
                logfile = logfile_path,
                experiment_path = experiment_path,
                string = os.path.join(experiment_path, experiment_file)
            )
            e.var.canvas_backend = r'legacy'
            
            with self.assertRaises(Exception) as exception:  # TODO: Exception types!
                e.run()
            print(e)

if __name__ == '__main__':
    unittest.main()
