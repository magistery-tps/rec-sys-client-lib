import torch

class BatchDot(torch.nn.Module):
    def forward(self, a, b, transpose: bool=True):
        if transpose:
            b = torch.transpose(b, 1, 2)

        return torch.bmm(a, b).squeeze(2).squeeze(1)