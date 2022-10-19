from pytorch_common.modules import FitMixin
from torch.nn import Module, ReLU
from .mlp import MultiLayerPerceptron
from .multi_feature_embedding import MultiFeatureEmbedding


class NNMF(Module, FitMixin):
    def __init__(
        self,
        features_n_values: list[int], 
        embedding_size: int, 
        units_per_layer: list[int], 
        dropout: float,
        sparse: bool = False
    ):
        super().__init__()
        self.embedding = MultiFeatureEmbedding(features_n_values, embedding_size, sparse=sparse)
        self.__init_mlp(features_n_values, embedding_size, units_per_layer, dropout)
        self.act = ReLU()

    def __init_mlp(self, features_n_values, embedding_size, units_per_layer, dropout):
        # Embedding output must be flattened to pass through mlp...
        self.mlp_input_dim = len(features_n_values) * embedding_size
        self.mlp = MultiLayerPerceptron(self.mlp_input_dim, units_per_layer, dropout)

    def __flatten_emb(self, emb): return emb.view(-1, self.mlp_input_dim)

    def forward(self, x):
        x_emb = self.embedding(x)

        output = self.mlp(self.__flatten_emb(x_emb))

        return self.act(output.squeeze(1))
