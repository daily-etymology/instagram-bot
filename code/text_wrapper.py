#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text wrapper solver

I copied this code from here:
https://www.geeksforgeeks.org/word-wrap-problem-dp-19/

This code is contributed by sahil shelangia
"""

# A Dynamic programming solution
# for Word Wrap Problem
 
# A utility function to print
# the solution
# l[] represents lengths of different
# words in input sequence. For example,
# l[] = {3, 2, 2, 5} is for a sentence
# like "aaa bb cc ddddd". n is size of
# l[] and M is line width (maximum no.
# of characters that can fit in a line)
INF = 2147483647
def printSolution(p, n, output = []):
    p = list(p)
    n = int(n)
    k = 0
    if p[n] == 1:
        k = 1
        output = []
    else:
        k, output = printSolution(p, p[n] - 1, output)
        k += 1
    # print('Line number ', k, ': From word no. ',
    #                               p[n], 'to ', n)
    
    tmp = {"line_number": k - 1,
                    "start_word": p[n] - 1,
                    "end_word" : n - 1}
    
    if not tmp in output:
        output.append(tmp)
    return k, output
 
def solveWordWrap(l, n, M):
     
    # For simplicity, 1 extra space is
    # used in all below arrays
 
    # extras[i][j] will have number
    # of extra spaces if words from i
    # to j are put in a single line
    extras = [[0 for i in range(n + 1)]
                 for i in range(n + 1)]
                  
    # lc[i][j] will have cost of a line
    # which has words from i to j
    lc = [[0 for i in range(n + 1)]
             for i in range(n + 1)]
              
    # c[i] will have total cost of
    # optimal arrangement of words
    # from 1 to i
    c = [0 for i in range(n + 1)]
     
    # p[] is used to print the solution.
    p = [0 for i in range(n + 1)]
     
    # calculate extra spaces in a single
    # line. The value extra[i][j] indicates
    # extra spaces if words from word number
    # i to j are placed in a single line
    for i in range(n + 1):
        extras[i][i] = M - l[i - 1]
        for j in range(i + 1, n + 1):
            extras[i][j] = (extras[i][j - 1] -
                                    l[j - 1] - 1)
                                     
    # Calculate line cost corresponding
    # to the above calculated extra
    # spaces. The value lc[i][j] indicates
    # cost of putting words from word number
    # i to j in a single line
    for i in range(n + 1):
        for j in range(i, n + 1):
            if extras[i][j] < 0:
                lc[i][j] = INF;
            elif j == n and extras[i][j] >= 0:
                lc[i][j] = 0
            else:
                lc[i][j] = (extras[i][j] *
                            extras[i][j])
 
    # Calculate minimum cost and find
    # minimum cost arrangement. The value
    # c[j] indicates optimized cost to
    # arrange words from word number 1 to j.
    c[0] = 0
    for j in range(1, n + 1):
        c[j] = INF
        for i in range(1, j + 1):
            if (c[i - 1] != INF and
                lc[i][j] != INF and
                ((c[i - 1] + lc[i][j]) < c[j])):
                c[j] = c[i-1] + lc[i][j]
                p[j] = i
    printSolution(p, n)
    return p, n


def solution_to_rownumber(sol):
    output = []
    for l in sol:
        tmp = [l["line_number"] for i in range(l["end_word"] - l["start_word"] + 1)]
        output += tmp
    return output
     
if __name__ == "__main__":
    # Driver Code
    l = [3,5,5,1,1]
    l = [5, 5, 5, 3, 5, 11, 10, 5, 7, 9, 3, 3, 6, 7, 3, 8, 6, 12, 5, 8, 3, 1, 4, 8, 8]
    n = len(l)
    M = 40
    sol = solveWordWrap(l, n, M)
    line_solutions = printSolution(sol[0], sol[1])
    a = solution_to_rownumber(line_solutions[1])
    # print(l)
    # print(solution_to_rownumber(sol[0]))
    
    
    
