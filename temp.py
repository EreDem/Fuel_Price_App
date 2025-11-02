from mlp import MLP
import numpy as np
from mlp import Trainer
import pandas as pd

from preprocessing import data_to_features

ki_e5 = MLP(27, 1, 64, 2)
ki_e10 = MLP(27, 1, 64, 2)
ki_diesel = MLP(27, 1, 64, 2)

trainer = Trainer(ki_e5)
trainer.train(10, "e5", 512, 3)

trainer = Trainer(ki_e10)
trainer.train(10, "e10", 512, 3)

trainer = Trainer(ki_diesel)
trainer.train(10, "diesel", 512, 3)
