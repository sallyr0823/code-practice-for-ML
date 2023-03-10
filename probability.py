

import numpy as np
def joint_distribution_of_word_counts(texts, word0, word1):
    '''
    Parameters:
    texts (list of lists) - a list of texts; each text is a list of words
    word0 (str) - the first word to count
    word1 (str) - the second word to count

    Output:
    Pjoint (numpy array) - Pjoint[m,n] = P(X1=m,X2=n), where
      X0 is the number of times that word1 occurs in a given text,
      X1 is the number of times that word2 occurs in the same text.
    '''

    n_0 = 0
    n_1 = 0
    # find the max of occurence to form the matrix
    for words in texts:
      n_0 = max(n_0, words.count(word0))
      n_1 = max(n_1, words.count(word1))
    # from P(m=0,n=0) to max
    Pjoint = np.zeros((n_0 + 1,n_1 +1))
    
    for words in texts:
      Pjoint[words.count(word0),words.count(word1)] += 1

    Pjoint = Pjoint / Pjoint.sum()  

    return Pjoint

def marginal_distribution_of_word_counts(Pjoint, index):
    '''
    Parameters:
    Pjoint (numpy array) - Pjoint[m,n] = P(X0=m,X1=n), where
      X0 is the number of times that word1 occurs in a given text,
      X1 is the number of times that word2 occurs in the same text.
    index (0 or 1) - which variable to retain (marginalize the other) 

    Output:
    Pmarginal (numpy array) - Pmarginal[x] = P(X=x), where
      if index==0, then X is X0
      if index==1, then X is X1
    '''
    if index == 0:
      Pmarginal = np.zeros(Pjoint.shape[0])
    else:
      Pmarginal = np.zeros(Pjoint.shape[1])

    if index == 0:
      # sum each row here
      Pmarginal = Pjoint.sum(axis = 1)
    else:
      # sum each column here
      Pmarginal = Pjoint.sum(axis = 0)  

    return Pmarginal
    
def conditional_distribution_of_word_counts(Pjoint, Pmarginal):
    '''
    Parameters:
    Pjoint (numpy array) - Pjoint[m,n] = P(X0=m,X1=n), where
      X0 is the number of times that word0 occurs in a given text,
      X1 is the number of times that word1 occurs in the same text.
    Pmarginal (numpy array) - Pmarginal[m] = P(X0=m)

    Outputs: 
    Pcond (numpy array) - Pcond[m,n] = P(X1=n|X0=m)
    '''
    # initialize pcond
    Pcond = Pjoint / Pmarginal[:,None]

    return Pcond

def mean_from_distribution(P):
    '''
    Parameters:
    P (numpy array) - P[n] = P(X=n)
    
    Outputs:
    mu (float) - the mean of X
    '''
    mu = 0
    P = P / P.sum()
    for i in range(P.shape[0]):
      mu += i * P[i]
    return mu

def variance_from_distribution(P):
    '''
    Parameters:
    P (numpy array) - P[n] = P(X=n)
    
    Outputs:
    var (float) - the variance of X
    '''
    mu = mean_from_distribution(P)
    var = 0
    P = P / P.sum()
    for i in range(P.shape[0]):
      var += (i-mu)**2 * P[i]
    return var

def covariance_from_distribution(P):
    '''
    Parameters:
    P (numpy array) - P[m,n] = P(X0=m,X1=n)
    
    Outputs:
    covar (float) - the covariance of X0 and X1
    '''
    # sum each row for X_0
    mu_0 = mean_from_distribution(P.sum(axis = 1))
    # sum each row for X_1
    mu_1 = mean_from_distribution(P.sum(axis = 0))
    covar = 0
    for i in range(P.shape[0]):
      for j in range(P.shape[1]):
        covar += P[i][j] * (i - mu_0) * (j - mu_1)


    return covar

def expectation_of_a_function(P, f):
    '''
    Parameters:
    P (numpy array) - joint distribution, P[m,n] = P(X0=m,X1=n)
    f (function) - f should be a function that takes two
       real-valued inputs, x0 and x1.  The output, z=f(x0,x1),
       must be a real number for all values of (x0,x1)
       such that P(X0=x0,X1=x1) is nonzero.

    Output:
    expected (float) - the expected value, E[f(X0,X1)]
    '''
    P_0 = np.arange(P.shape[0])
    P_1 = np.arange(P.shape[1])
    expected = np.multiply(f(P_0[:,None], P_1[None,:]),P).sum()
    return expected
    
