#! /usr/bin/python

import sys

def getFactors(num):
  factors = list()
  for i in range(1, num+1):
    if num % i == 0:
      factors.append(i)
  return factors


def main(argv=None):
  if argv is None:
    argv = sys.argv

  # Writing data.1
  f = open('data.1', 'w')

  for i in range(1, 101):
    factors = getFactors(i)
    for factor in factors:
      f.write(str(factor))
      f.write(" ")
    f.write("\n")
  f.close()

  # Writing data.2
  f = open('data.2', 'w')
  for i in range(1, 101):
    for j in range(1, 101):
      if j % i == 0:
        f.write(str(j))
        f.write(" ")
    f.write("\n")
  f.close()

if __name__ == '__main__':
  main()