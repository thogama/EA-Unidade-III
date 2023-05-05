import math
from scipy.stats import norm
from scipy.stats import chi2_contingency
from scipy.stats import pearsonr
import statsmodels.api as sm


import numpy as np

# Intervalo de Confiaça de Wilson
def wilson_confidence_interval(pos_events, n_total, conf_level=0.95):
    """
    Calculates the Wilson score interval for a proportion with a given confidence level.
    
    Args:
    pos_events (int): Number of events of interest.
    n_total (int): Total number of observations.
    conf_level (float, optional): Confidence level (default is 0.95).
    
    Returns:
    tuple: Lower and upper bounds of the confidence interval.
    """
    z_alpha_2 = norm.ppf(1 - (1 - conf_level) / 2)
    phat = pos_events / n_total
    a = phat + z_alpha_2**2 / (2 * n_total)
    b = z_alpha_2 * math.sqrt((phat*(1 - phat) + z_alpha_2**2 / (4 * n_total)) / n_total)
    lower = (a - b) / (1 + z_alpha_2**2 / n_total)
    upper = (a + b) / (1 + z_alpha_2**2 / n_total)
    return lower, upper

#'./dados/microdados2021_arq10.txt' # Arquivo de ecolaridade do pai
#'./dados/microdados2021_arq11.txt' # Arquivo de ecolaridade da mãe


with open('./dados/pai/dado.txt', 'r') as f1, open('./dados/mae/dado.txt', 'r') as f2,open('./dados/incentivo/dado.txt', 'r') as f3:
    linhas1 = f1.readlines()
    linhas2 = f2.readlines()
    linhas3 = f3.readlines()

sitaucao1 = {"contagem":0,"influencia_dos_pais":0} # Pai e Mãe com ensino medio para cima (D,E,F)
sitaucao2 = {"contagem":0,"influencia_dos_pais":0} # Pai com ensino medio para cima (D,E,F) e Mãe com fundamental para baixo (A,B,C)
sitaucao3 = {"contagem":0,"influencia_dos_pais":0} # Mãe com ensino medio para cima (D,E,F) e Pai com fundamental para baixo (A,B,C)
sitaucao4 = {"contagem":0,"influencia_dos_pais":0} # Pai e Mãe com ensino fundamental para baixo (A,B,C)

contagem1 = 0
contagem2 = 0
contagem3 = 0
contagem4 = 0
regressao_escolaridade = []
regressao_incentivo = []
sufixos = ('A','B','C','D','E','F')
for i, linha1 in enumerate(linhas1):
    linha2 = linhas2[i]
    linha3 = linhas3[i]
    if (linha1[:-2].endswith(sufixos) and linha2[:-2].endswith(sufixos)):
        pai = linha1[-3]
        mae = linha2[-3]
        if((pai=='D' or pai=='E' or pai=='F') and (mae=='A' or mae=='B' or mae=='C')): # pai sup mae inf
            contagem2+=1
            regressao_escolaridade.append(1)
            if(linha3[:-2]).endswith("B"):
                regressao_incentivo.append(1)
                sitaucao2['influencia_dos_pais']+=1
            else:
                regressao_incentivo.append(0)
        elif((pai=='D' or pai=='E' or pai=='F') and (mae=='D' or mae=='E' or mae=='F')): #  pai sup mae sup
            contagem1+=1
            regressao_escolaridade.append(2)

            if(linha3[:-2]).endswith("B"):
                regressao_incentivo.append(1)
                sitaucao1['influencia_dos_pais']+=1
            else:
                regressao_incentivo.append(0)
        elif((pai=='A' or pai=='B' or pai=='C') and (mae=='D' or mae=='E' or mae=='F')): #  pai inf mae sup)
            contagem3+=1
            regressao_escolaridade.append(1)
            if(linha3[:-2]).endswith("B"):
                regressao_incentivo.append(1)
                sitaucao3['influencia_dos_pais']+=1
            else:
                regressao_incentivo.append(0)
        elif((pai=='A' or pai=='B' or pai=='C') and (mae=='A' or mae=='B' or mae=='C')): #  pai inf mae inf)
            contagem4+=1
            regressao_escolaridade.append(0)
            if(linha3[:-2]).endswith("B"):
                regressao_incentivo.append(1)  
                sitaucao4['influencia_dos_pais']+=1
            else:
                regressao_incentivo.append(0)
total = contagem1 + contagem2 + contagem3 + contagem4

sitaucao1['contagem'] = contagem1
sitaucao2['contagem'] = contagem2
sitaucao3['contagem'] = contagem3
sitaucao4['contagem'] = contagem4


print(f"Situação 1\n",sitaucao1['contagem'],sitaucao1['influencia_dos_pais'])
print(f"Situação 2\n",sitaucao2['contagem'],sitaucao2['influencia_dos_pais'])
print(f"Situação 3\n",sitaucao3['contagem'],sitaucao3['influencia_dos_pais'])
print(f"Situação 4\n",sitaucao4['contagem'],sitaucao4['influencia_dos_pais'])

# Teste de Contigencia

observacao1 = sitaucao1['contagem'] - sitaucao1['influencia_dos_pais']
observacao2 = sitaucao1['influencia_dos_pais']

observacao3 = sitaucao2['contagem'] - sitaucao2['influencia_dos_pais']
observacao4 = sitaucao2['influencia_dos_pais']

observacao5 = sitaucao3['contagem'] - sitaucao3['influencia_dos_pais']
observacao6 = sitaucao3['influencia_dos_pais']

observacao7 = sitaucao4['contagem'] - sitaucao4['influencia_dos_pais']
observacao8 = sitaucao4['influencia_dos_pais']

observacoes = [[observacao2 + observacao4 + observacao6 + observacao8],
               [observacao1 + observacao3 + observacao5 + observacao7]]
chi2, p_value, dof, expected = chi2_contingency(observacoes)
print(p_value)


# Teste de Correlação de Pearson
corr, p_value2 = pearsonr([sitaucao1['contagem'],
                           sitaucao2['contagem'],
                           sitaucao3['contagem'],
                           sitaucao4['contagem']],
                         [sitaucao1['influencia_dos_pais'],
                          sitaucao2['influencia_dos_pais'],
                          sitaucao3['influencia_dos_pais'],
                          sitaucao4['influencia_dos_pais']])

print(corr,p_value2)



# 0: nenhum dos pais possui ensino superior
# 1: um dos pais possui ensino superior
# 2: ambos os pais possuem ensino superior




X = sm.add_constant(regressao_escolaridade)
Y = regressao_incentivo
model = sm.Logit(Y, X)
result = model.fit()

print(result.summary())
