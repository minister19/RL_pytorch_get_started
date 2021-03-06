import torch
import numpy as np

A = np.array([1, 2, 3])
B = np.array([4, 5, 6])

print(A@B)
print(A.dot(B))

C = 3
try:
    print(A@C)
except Exception as e:
    print(e)
print(A.dot(C))

x = torch.tensor([[1], [2]])
print(x)
print(x[:, 0])

x = torch.tensor([[[1], [2]], [[1], [2]]])
print(x)
print(x[:, 0])
print(x[:, 1])
