from numpy import zeros
import numpy as np

class Gaussian_distribution:

    def __init__(self, rho_matrix, sim_values):
        self.rho_matrix = rho_matrix
        self.n_var = rho_matrix.shape[0]
        self.mean_vector = zeros(rho_matrix.shape[0])
        self.sim_values = sim_values





def Get_Correlation_Matrix(n_var):
    A = np.random.randn(n_var, n_var)

    Cov = np.matmul(A, np.transpose(A))

    variances = np.diagonal(Cov)

    std_dev = np.sqrt(variances)

    rho_matrix = np.ones(shape = Cov.shape)

    for i in range(Cov.shape[0]):
        for j in range(Cov.shape[1]):
            rho_matrix[i][j] = Cov[i][j]/(std_dev[i]*std_dev[j])


    return rho_matrix



