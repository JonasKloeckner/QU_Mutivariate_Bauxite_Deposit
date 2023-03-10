
import numpy as np
import itertools
from scipy.stats import mvn


def calculate_D90(cdf_1, cdf_2):
    diff_cdf = np.absolute(cdf_1 - cdf_2)
    d90 = np.percentile(a = diff_cdf, q = 90)

    return d90


def calculate_mv_cdf_array_np(sim_values_array, data_values_array):
    mv_cdf_array = np.zeros(shape=data_values_array.shape[0])

    for i in range(data_values_array.shape[0]):
        thresholds = data_values_array[i, :]
        indicator_mv_cdf = np.less_equal(sim_values_array, thresholds)
        indicator_mv_cdf_2 = np.min(indicator_mv_cdf, axis=1)
        mv_cdf_array[i] = np.mean(indicator_mv_cdf_2)

    return mv_cdf_array



def Calculate_Mean_Multivariate_D90(sim_values, ref_values, data_values_array, n_dim_d90):

    n_var = sim_values.shape[1]
    combinations = np.array(list(itertools.combinations(iterable=np.arange(n_var), r=n_dim_d90) ))

    sum_d90 = 0.000
    count_d90 = 0.00

    for i in range(len(combinations)):
        # Get the combination

        list_of_cols = list(combinations[i])




        # Calculate the cdfs of the reference and of the sim_values
        mv_cdf_1 = calculate_mv_cdf_array_np(sim_values_array = sim_values[:, list_of_cols], data_values_array = data_values_array[:, list_of_cols])


        mv_cdf_2 = calculate_mv_cdf_array_np(sim_values_array = ref_values[:, list_of_cols], data_values_array = data_values_array[:, list_of_cols])

        d90 = calculate_D90(cdf_1 = mv_cdf_1, cdf_2 = mv_cdf_2)

        sum_d90 = sum_d90 + d90
        count_d90 = count_d90 + 1.00

    mean_d90 = sum_d90/count_d90

    return mean_d90



def Calculate_Mean_Multivariate_D90_Multigaussian(sim_values, mean_vector, cov_matrix, data_values_array, n_dim_d90):

    n_var = sim_values.shape[1]
    combinations = np.array(list(itertools.combinations(iterable=np.arange(n_var), r=n_dim_d90) ))

    sum_d90 = 0.000
    count_d90 = 0.00

    for i in range(len(combinations)):
        # Get the combination

        list_of_cols = list(combinations[i])




        # Calculate the cdfs of the reference and of the sim_values
        mv_cdf_1 = calculate_mv_cdf_array_np(sim_values_array = sim_values[:, list_of_cols], data_values_array = data_values_array[:, list_of_cols])


        mv_cdf_true = calculate_true_mv_cdf_array(data_values_array=data_values_array, mean_vector=mean_vector, rho_matrix=cov_matrix)

        d90 = calculate_D90(cdf_1 = mv_cdf_1, cdf_2 = mv_cdf_true)

        sum_d90 = sum_d90 + d90
        count_d90 = count_d90 + 1.00

    mean_d90 = sum_d90/count_d90

    return mean_d90


def calculate_true_mv_cdf_array(data_values_array, mean_vector, rho_matrix):
    true_mv_cdf = np.zeros(data_values_array.shape[0])
    n_var = data_values_array.shape[1]
    lower = np.full(shape=n_var, fill_value=-1.0e21)
    for i in range(len(true_mv_cdf)):
        upper = data_values_array[i, :]
        true_mv_cdf[i], i = mvn.mvnun(lower, upper, mean_vector, rho_matrix)

    return true_mv_cdf
