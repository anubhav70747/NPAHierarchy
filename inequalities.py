
# NON LOCAL GAMES

# takes the probability table returns the chsh game for Alice and Bob
def chsh_AB(P):
  chsh=0
  for x in range(2):
    for y in range(2):
      for u in range(2):
        for v in range(2):
            if  x * y == u ^ v:
              chsh=chsh+P([u,v],[x,y],['A','B'])
  return chsh/4

# takes the probability table returns the chsh game for Bob and Charlie
def chsh_BC(P):
  chsh=0
  for x in range(2):
    for y in range(2):
      for u in range(2):
        for v in range(2):
            if  x * y == u ^ v:
              chsh=chsh+P([u,v],[x,y],['B','C'])
  return chsh/4

# takes the probability table and the parameters p and q to return the biased chsh game for Alice and Bob
def biased_chsh(P,p,q):
  sum = p * q * ( P([0,0],[0,0]) + P([1,1],[0,0]) )
  sum = sum + p * (1-q) * ( P([0,0],[0,1]) + P([1,1],[0,1]) )
  sum = sum + (1-p) * q * ( P([0,0],[1,0]) + P([1,1],[1,0]) )
  sum = sum + (1-p) * (1-q) * ( P([0,1],[1,1]) + P([1,0],[1,1]) )
  return sum

# takes the probability table and the parameters p and q to return the biased chsh marginal for Alice
def biased_chshA(P,p,q):
  sum = p * q * ( P([0],[0],['A']) )
  sum = sum + p * (1-q) * ( P([0],[0],['A']) )
  sum = sum + (1-p) * q * ( P([0],[1],['A']) )
  sum = sum + (1-p) * (1-q) * ( P([1],[1],['A']) )
  return sum

# takes the probability table and the parameters p and q to return the biased chsh marginal for Bob
def biased_chshB(P,p,q):
  sum = p * q * ( P([0],[0],['B']) )
  sum = sum + p * (1-q) * ( P([0],[1],['B']) )
  sum = sum + (1-p) * q * ( P([0],[0],['B']) )
  sum = sum + (1-p) * (1-q) * ( P([1],[1],['B']) )
  return sum

# takes the probability table returns the svetlichny game
def svetlichny_game(P):
  svet=0
  for x in range(2):
    for y in range(2):
      for z in range(2):
        for u in range(2):
          for v in range(2):
            for w in range(2):
              if  (x * y)^(y * z)^(z * x) == u ^ v ^ w:
                svet=svet+P([u,v,w],[x,y,z])
  return svet/8

# takes the probability table returns the mermin game 1
def mermin_game_1(P):
  svet=0
  for x in range(2):
    for y in range(2):
      for z in range(2):
        for u in range(2):
          for v in range(2):
            for w in range(2):
              if  (x * y * z) == u ^ v ^ w:
                svet=svet+P([u,v,w],[x,y,z])
  return svet/8

# takes the probability table returns the mermin game 2
def mermin_game_2(P):
  svet=0
  for x in range(2):
    for y in range(2):
      for z in range(2):
        for u in range(2):
          for v in range(2):
            for w in range(2):
              if  (x * y)^(y * z) == u ^ v ^ w:
                svet=svet+P([u,v,w],[x,y,z])
  return svet/8

# takes the probability table returns the Guess Your Neighbour's Input game
def gyni(P):
  return 0.25 * (P([0,0,0],[0,0,0]) + P([1,0,1],[1,1,0]) + P([1,1,0],[0,1,1]) + P([0,1,1],[1,0,1]))

# FACET INEQUALITIES

# takes the probability table and input setting
# returns expectation terms for three parties with output -1,+1
def expectation_value_tri(P, input_):
    vals = [-1, 1]
    return sum(a*b*c*P([a, b, c], input_) for a in vals for b in vals for c in vals)

# takes the probability table, input settings and party labels
# returns expectation terms for two parties with output -1,+1
def expectation_value_bi(P, input_ , parties):
    vals = [-1, 1]
    return sum(a*b*P([a, b], input_ ,parties) for a in vals for b in vals )

# takes the probability table returns the chsh inequality as sum of expectation terms
# from -2*(2**0.5) to +2*(2**0.5)
def chsh(P):
   return expectation_value_bi(P, [0,0] ,['A','B']) + expectation_value_bi(P, [0, 1],['A','B']) + \
      expectation_value_bi(P, [1,0],['A','B']) - expectation_value_bi(P, [1, 1],['A','B'])

# takes the probability table returns the mermin inequality as sum of expectation terms
# from -4 to +4
def mermin(P):
   return expectation_value_tri(P, [1, 0, 0]) + expectation_value_tri(P, [0, 1, 0]) + \
      expectation_value_tri(P, [0, 0, 1]) - expectation_value_tri(P, [1, 1, 1])

# takes the probability table returns the svetlichny inequality as sum of expectation terms
# from -4*(2**0.5) to +4*(2**0.5)
def svetlichny(P):
  Stev = 0
  for x in range(2):
    for y in range(2):
      for z in range(2):
	Stev = Stev + (-1)**( x*y + y*z + z*x )* expectation_value_tri(P,[x,y,z])
  return Stev

# takes the probability table returns the I(P) inequality
def IP(P):
  return - 2 * P([0,0],[1,1],['A','B']) - 2 * P([0,0],[1,1],['B','C']) - 2 * P([0,0],[1,1],['A','C']) - P([0,0,0],[0,0,1]) - P([0,0,0],[0,1,0]) - P([0,0,0],[1,0,0]) + 2 * P([0,0,0],[1,1,0]) + 2 * P([0,0,0],[1,0,1]) + 2 * P([0,0,0],[0,1,1]) + 2 * P([0,0,0],[1,1,1])

# takes the probability table returns I3322 inequality
def I3322(P):
  sum = 0
  sum = sum - P([0],[0],'A') - 2*P([0],[0],'B') - P([0],[1],'B') + P([0,0],[0,0],['A','B']) + P([0,0],[1,0],['A','B']) + P([0,0],[2,0],['A','B']) + P([0,0],[0,1],['A','B']) + P([0,0],[1,1],['A','B']) - P([0,0],[2,1],['A','B']) + P([0,0],[0,2],['A','B']) - P([0,0],[1,2],['A','B'])
  return sum

# takes the probability table returns the CH game for Alice and Bob
def ch_AB(P):
  return - P([1,0],[0,0]) - P([0,0],[0,1]) - P([0,1],[1,1]) + P([0,0],[1,0])

