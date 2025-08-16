import numpy as np

def build_weights(data_length, first_weight=0.1):
    
    if data_length < 2:
        return np.array([1.0], dtype=float)


    last_weight = 1.0

    step = (last_weight-first_weight)/(data_length-1)

    weights = (step * np.arange(data_length, dtype=float)) + first_weight

    return weights

def silverman(data: np.array, weights=None, factor=1.0):
    data = data.astype(float, copy=False)

    if weights is None:
        n = len(data)
        s = data.std(ddof=0)

    else:
        n = (np.sum(weights)**2) / np.sum(weights**2)
        mu = np.dot(weights, data)/ np.sum(weights)  # Operacion DOT vectores 1D = sum(a * b), sumatorio de mult elemento a elemento
        s =np.sqrt((np.dot(weights,(data-mu)**2))/ np.sum(weights))

    
    h = 1.06 * s * n**(-0.2)

    return h * factor

def K(u):
    return (np.exp(-((u**2)/2)) / np.sqrt(np.pi * 2))  


def gaussian_kde(data, x_grid_len=200, use_weights=False, fw=0.2, bw_factor=1.0):

    n = len(data)

    if use_weights is False:
        weights = np.ones(n, dtype=float)
        h = silverman(data, None, bw_factor)

    else:
        weights = build_weights(n, fw)
        h = silverman(data, weights, bw_factor)
        

    x_min = data.min()
    x_max = data.max()

    x_grid = np.linspace(x_min, x_max, x_grid_len)
        
    # Generar matriz de distancias (200 x n)
    U = (x_grid[:, None] - data[None, :]) / h   # Broadcasting

    # Aplicar kernel a toda la matriz
    K_matrix = K(U)

    # Aplicar los pesos a cada columna de la matriz, ya que en cada columna estan las distancias al dato i
    sum_matrix = K_matrix * weights

    # Sumar por filas → una densidad por cada x de x_grid
    density_vec = np.sum(sum_matrix, axis=1) / (np.sum(weights) * h)
    

    return x_grid, density_vec
