import math
from scipy.stats import norm

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


with open('./dados/microdados2021_arq10.txt', 'r') as f1, open('./dados/microdados2021_arq11.txt', 'r') as f2:
    linhas1 = f1.readlines()
    linhas2 = f2.readlines()

sitaucao1 = {"contagem":0} # Pai e Mãe com ensino medio para cima (D,E,F)
sitaucao2 = {"contagem":0} # Pai com ensino medio para cima (D,E,F) e Mãe com fundamental para baixo (A,B,C)
sitaucao3 = {"contagem":0} # Mãe com ensino medio para cima (D,E,F) e Pai com fundamental para baixo (A,B,C)
sitaucao4 = {"contagem":0} # Pai e Mãe com ensino fundamental para baixo (A,B,C)

contagem1 = 0
contagem2 = 0
contagem3 = 0
contagem4 = 0
sufixos = ('A','B','C','D','E','F')
for i, linha1 in enumerate(linhas1):
    linha2 = linhas2[i]
    if (linha1[:-2].endswith(sufixos) and linha2[:-2].endswith(sufixos)):
        pai = linha1[-3]
        mae = linha2[-3]
        
        if((pai=='D' or pai=='E' or pai=='F') and (mae=='A' or mae=='B' or mae=='C')): # pai sup mae inf
            print(F"P {pai} M {mae}\n")
            contagem2+=1
        elif((pai=='D' or pai=='E' or pai=='F') and (mae=='D' or mae=='E' or mae=='F')): #  pai sup mae sup
            contagem1+=1
        elif((pai=='A' or pai=='B' or pai=='C') and (mae=='D' or mae=='E' or mae=='F')): #  pai inf mae sup)
            contagem3+=1
        elif((pai=='A' or pai=='B' or pai=='C') and (mae=='A' or mae=='B' or mae=='C')): #  pai inf mae inf)
            contagem4+=1
total = contagem1 + contagem2 + contagem3 + contagem4

sitaucao1['contagem'] = contagem1
sitaucao2['contagem'] = contagem2
sitaucao3['contagem'] = contagem3
sitaucao4['contagem'] = contagem4

print(f"Situação 1\n",wilson_confidence_interval(sitaucao1['contagem'],total,0.95), " ",contagem1/total)
print(f"Situação 2\n",wilson_confidence_interval(sitaucao2['contagem'],total,0.95) ," ",contagem2/total)
print(f"Situação 3\n",wilson_confidence_interval(sitaucao3['contagem'],total,0.95) ," ",contagem3/total)
print(f"Situação 4\n",wilson_confidence_interval(sitaucao4['contagem'],total,0.95), " ",contagem4/total)

