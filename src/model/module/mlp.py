from torch.nn import Module, Linear, BatchNorm1d, ReLU, Dropout, Sequential
from pytorch_common.modules import CommonMixin


class MultiLayerPerceptron(Module, CommonMixin):
    def __init__(self, input_units: int, units_per_layer: list[int], dropout: float, n_outputs: int=1):
        super().__init__()
        layers = []

        for units in units_per_layer:
            layers.extend([
                Linear(input_units, units),
                BatchNorm1d(units),
                ReLU(),
                Dropout(p=dropout)
            ])
            input_units = units

        layers.append(Linear(input_units, n_outputs))

        self.mlp = Sequential(*layers)

    def forward(self, x):
        """
        :param x: Float tensor of size ``(batch_size, embed_dim)``
        """
        return self.mlp(x)
