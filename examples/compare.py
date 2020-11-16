from timeme import Timer
from sort import bubbleSort, mergeSort


if __name__ == '__main__':
    sample = [1,2,5,4,3]
    thing = bubbleSort(sample, timeme=True)
    thing = mergeSort(sample, timeme=True)
    experiment = Timer.records['sorting_experiment']
    print('bubble sort stats: ', experiment['bubbleSort'][-1].aggregate)
    print('merge sort stats: ', experiment['mergeSort'][-1].aggregate)
