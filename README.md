# QU_Mutivariate_Bauxite_Deposit

Uncertainty and risk management are essential for decision-making in the sustainable extraction of mineral resources. Uncertainty in mine planning typically starts with the geostatistical simulation of the variables that influence the decision process, which produces a series of equally probable models. Then a transfer function is applied to each model. The result is a distribution of the response function, which calculates the probability (or risk) that a given area achieves the product quality standards. 

High-risk operations often fail to achieve the ore quality standards and decrease the mineral resources value. In this context, failure in managing risk may collapse mining operations, leading to unrepairable economic, environmental, and social damages. However, risk assessment is a challenge in the case of multivariate deposits such as bauxite deposits. In these deposits, the response function depends on multiple variables simultaneously. The variables that characterize bauxite deposits also exhibit complex relationships and sum and fraction constraints. The geostatistical simulations should reproduce these peculiarities. 

This work proposes a workflow to measure risk and uncertainty in complex multivariate deposits aiming at sustainable gains for the mining operations. The workflow starts with a multivariate geostatistical simulation using Projection Pursuit Multivariate Transform. Then these simulated models are combined with the initially planned dig lines and mining scheduling. The results informed the dig lines and periods with the highest risks and uncertainty for all variables, allowing the decision team to take measures focusing on sustainable goals. The methodology is illustrated in a case study of a significant bauxite deposit located in northern Brazil.


This repository cointains the python code for multivariate geostatistical simulations with sum and fraction constraints for a bauxite deposit using several modules of the Geostatistical Software Library (GSLib).

The article can be found at: [Application of risk assessment to improve sustainability in bauxite mining](https://doi.org/10.1016/j.resourpol.2021.102328)
