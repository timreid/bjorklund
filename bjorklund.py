"""
implements a variation of the rhythmic sequencing algorithm as described in:
E. Bjorklund. A metric for measuring the evenness of timing system rep-rate patterns.
SNS ASD Technical Note SNS-NOTE-CNTRL-100, Los Alamos National Laboratory,
Los Alamos, U.S.A., 2003.
and the application to rhythm as described in:
G. T. Toussaint, The Euclidean algorithm generates traditional musical rhythms,
Proceedings of BRIDGES: Mathematical Connections in Art, Music, and Science,
Banff, Alberta, Canada, July 31 to August 3, 2005
"""
from collections import deque
from copy import deepcopy

def bjorklund(onsets, steps, rotation, evenness):
    """
    Args:
        onsets: the number of onsets aka ones to distribute onto the steps
        steps: the number of steps in the sequence, empty steps are known as zeros
        rotation: the amount of right cyclic rotation
        evenness: the 'evenness' of the distribution of onsets onto steps
        with 1.0 corresponding to maximally even and 0.0 corresponding to minimally even
    """
    def flatten(nested_list):
        """
        completely flattens an arbitrarily deeply nested list
        """
        nested_list = deepcopy(nested_list)
        while nested_list:
            sublist = nested_list.pop(0)
            if isinstance(sublist, list):
                nested_list = sublist + nested_list
            else:
                yield sublist
    assert isinstance(steps, int)
    assert steps > 0
    assert isinstance(onsets, int)
    assert onsets <= steps
    assert isinstance(rotation, int)
    assert isinstance(evenness, float)
    assert evenness >= 0
    assert evenness <= 1
    #convert the float paramater e into an int giving the temporary reduction of steps
    #this faciliates variable evenness
    reduction = int((1 - evenness) * (steps - onsets))
    #prepare the input lists
    ones = onsets * [1]
    zeroes = (steps - onsets - reduction) * [0]
    if len(ones) > len(zeroes):
        larger = ones
        smaller = zeroes
    else:
        larger = zeroes
        smaller = ones
    #the algorithm works by repeatedly pairing all elements from the smaller list with the
    #larger list until one of the lists is empty
    while True:
        #holds the paired elements
        paired_elements = []
        #pair the elements
        for i, _ in enumerate(smaller):
            paired_elements.append([larger[i], smaller[i]])
        #holds the unpaired elements from the larger list
        unpaired_elements = larger[len(smaller):]
        #if either list is empty the algorithm is done
        if unpaired_elements == []:
            sequence = list(flatten(paired_elements))
            break
        if paired_elements == []:
            sequence = list(flatten(unpaired_elements))
            break
        #otherwise continue
        if len(unpaired_elements) > len(paired_elements):
            larger = unpaired_elements
            smaller = paired_elements
        else:
            larger = paired_elements
            smaller = unpaired_elements
    #add back the zeros which were removed to facilitate variable evenness
    sequence += (reduction * [0])
    #convert to a deque for easy rotation
    sequence = deque(sequence)
    #perform cyclic right rotation
    sequence.rotate(rotation)
    #convert to a list to obtain the final result
    return list(sequence)
