from model.predictor.predictor import AbstractPredictor
import torch


class ModulePredictor(AbstractPredictor):
    def __init__(self, model): self.model = model

    def predict(self, user_idx, item_idx,  n_neighbors=10, debug=False):
        input_batch = torch.tensor([user_idx, item_idx]).to(self.model.device).unsqueeze(0)
        
        return self.predict_batch(input_batch)

    def predict_batch(self, batch, n_neighbors=10, debug=False):
        input_batch = batch.to(self.model.device)

        y_pred = self.model(input_batch)
    
        return y_pred.cpu().detach()
