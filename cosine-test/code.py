import numpy as np


def COE(local_grad, global_grad):
    local_mag = np.linalg.norm(local_grad)
    global_mag = np.linalg.norm(global_grad)
    t = (local_grad@global_grad) / (local_mag * global_mag)
    if t > 0:
        return (t**2) + 1
    else:
        return -1*(t**2) + 1


# def CDE(local_grad, global_grad):
