import math 
import numpy as np
import optimizers as optim 
import torch 
from hyperopt import fmin,tpe,hp 
import matplotlib.pyplot as plt 

plt.style.use('seaborn-white')

def rosenbrock(tensor):
    # this fucntion is used for optimization graphs 
    x,y=tensor 
    return (1-x)**2 + 100*(y-x**2)**2

def rastrigin(tensor,lib=torch):
    x,y=tensor
    A=10 
    f=(
        A*2 
        +(x**2 - A * lib.cos(x*math.pi*2))
        +(x**2 - A * lib.cos(y**math.pi*2))
    )
    return f 

def execute_steps(
        func,initial_state,optimizer_class,optimizer_config,num_iter=500
):
    x=torch.Tensor(initial_state).requires_grad_(True)
    optimizer=optimizer_class([x],**optimizer_config)
    steps=[]
    steps=np.zeros((2,num_iter+1))
    steps[:, 0] = np.array(initial_state)
    for i in range(1, num_iter + 1):
        optimizer.zero_grad()
        f = func(x)
        f.backward(retain_graph=True)
        optimizer.step()
        steps[:, i] = x.detach().numpy()
    return steps


def objective_rastrigin(params):
    lr=params['lr']
    optimizer_class=params['optimizer_class']
    minimum=(1.0,1.0)
    initial_state=(-2.0,2.0)
    optimizer_config=dict(lr=lr)
    steps = execute_steps(
        rastrigin, initial_state, optimizer_class, optimizer_config, num_iter=500
    )
    return (steps[0][-1] - minimum[0]) ** 2 + (steps[1][-1] - minimum[1]) ** 2

def objective_rosenbrok(params):
    lr = params['lr']
    optimizer_class = params['optimizer_class']
    minimum = (1.0, 1.0)
    initial_state = (-2.0, 2.0)
    optimizer_config = dict(lr=lr)
    num_iter = 100
    steps = execute_steps(
        rosenbrock, initial_state, optimizer_class, optimizer_config, num_iter
    )
    return (steps[0][-1] - minimum[0]) ** 2 + (steps[1][-1] - minimum[1]) ** 2


def plot_rastrigin(grad_iter,optimizer_name,lr):
    x=np.linspace(-4.5,4.5,250)
    y=np.linspace(-4.5,4.5,250)
    minimum=(0,0)
    X,Y=np.meshgrid(x,y)
    Z=rastrigin([X,Y],lib=np)
    iter_x,iter_y=grad_iter[0,:],grad_iter[1,:]
    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_subplot(1, 1, 1)
    ax.contour(X, Y, Z, 20, cmap='jet')
    ax.plot(iter_x, iter_y, color='r', marker='x')
    ax.set_title(
        f'Rastrigin func: {optimizer_name} with '
        f'{len(iter_x)} iterations, lr={lr:.6}'
    )
    plt.plot(*minimum, 'gD')
    plt.plot(iter_x[-1], iter_y[-1], 'rD')
    plt.savefig(f'rastrigin_{optimizer_name}.png')


def plot_rosenbrok(grad_iter, optimizer_name, lr):
    x = np.linspace(-2, 2, 250)
    y = np.linspace(-1, 3, 250)
    minimum = (1.0, 1.0)

    X, Y = np.meshgrid(x, y)
    Z = rosenbrock([X, Y])

    iter_x, iter_y = grad_iter[0, :], grad_iter[1, :]

    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_subplot(1, 1, 1)
    ax.contour(X, Y, Z, 90, cmap='jet')
    ax.plot(iter_x, iter_y, color='r', marker='x')

    ax.set_title(
        f'Rosenbrock func: {optimizer_name} with {len(iter_x)} '
        f'iterations, lr={lr:.6}'
    )
    plt.plot(*minimum, 'gD')
    plt.plot(iter_x[-1], iter_y[-1], 'rD')
    plt.savefig(f'rosenbrock_{optimizer_name}.png')


def execute_experiments(
    optimizers, objective, func, plot_func, initial_state, seed=1
):
    seed = seed
    for item in optimizers:
        optimizer_class, lr_low, lr_hi = item
        space = {
            'optimizer_class': hp.choice('optimizer_class', [optimizer_class]),
            'lr': hp.loguniform('lr', lr_low, lr_hi),
        }
        best = fmin(
            fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=200,
            rstate=np.random.RandomState(seed),
        )
        print(best['lr'], optimizer_class)

        steps = execute_steps(
            func,
            initial_state,
            optimizer_class,
            {'lr': best['lr']},
            num_iter=500,
        )
        plot_func(steps, optimizer_class.__name__, best['lr'])


if __name__ == '__main__':
 
    optimizers = [
        (optim.accsgd, -8, -0.1),
        
    ]
    execute_experiments(
        optimizers, objective_rastrigin, rastrigin, plot_rastrigin, (-2.0, 3.5)
    )

    optimizers = [
        (optim.accsgd, -8, -0.1),
       
    ]
    execute_experiments(
        optimizers,
        objective_rosenbrok,
        rosenbrock,
        plot_rosenbrok,
        (-2.0, 2.0),
    )

