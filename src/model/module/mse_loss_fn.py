import torch
from torch.nn import MSELoss
import logging


class MSELossFn(torch.nn.Module):
    """
        torch Mean Square Error wrapper module. It adapts shape and data types
        to calculate mse into both training and validation phases. 

    :param float_result: Select when module return a tensor of float number.
            - When is false(default) it return a tensor. Used in training
              phase because it support automatic differentiation.
            - When is true return a float number. Used in evaluation phase.
    """
    def __init__(self, reduction='mean', float_result: bool=False): 
        super().__init__()
        self.__fn = MSELoss()
        self.__float_result = float_result


    def __flatten(self, values, label):
        if(len(values.shape) > 1):
            logging.debug(f'flatten {label} of shape {values.shape}')
            return values.squeeze(1)
        return values


    def forward(self, y_pred, y_true):
        y_pred, y_true = self.__flatten(y_pred, 'y_pred'), self.__flatten(y_true, 'y_true')

        loss = self.__fn(y_pred.float(), y_true.float())

        return loss.item() if self.__float_result else loss