from timeme import Timer
from sort import bubbleSort, mergeSort
import random
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np


if __name__ == '__main__':
    print('also look here: ', __name__) 
    MIN = 0
    MAX = 1000
    bubble_sort_mean = []
    merge_sort_mean = []
    bubble_sort_std_dev = []
    merge_sort_std_dev = []
    arr_sizes = []
    for i in tqdm(range(5, 1000, 100)):
        sample = random.choices(range(MIN, MAX), k=i)
        thing = bubbleSort(sample, timeme=True, timeme_params={'parallelize':True})
        thing = mergeSort(sample, timeme=True, timeme_params={'parallelize': True})
        experiment = Timer.records['sorting_experiment']
        arr_sizes.append(int(i))
        bubble_sort_mean.append(
                experiment['bubbleSort'][-1].aggregate['mean'])
        bubble_sort_std_dev.append(
                experiment['bubbleSort'][-1].aggregate['std_dev'])
        merge_sort_mean.append(
                experiment['mergeSort'][-1].aggregate['mean'])
        merge_sort_std_dev.append(
                experiment['mergeSort'][-1].aggregate['std_dev'])

    bubble_sort_mean = np.array(bubble_sort_mean)
    bubble_sort_std_dev = np.array(bubble_sort_std_dev)
    merge_sort_mean = np.array(merge_sort_mean)
    merge_sort_std_dev = np.array(merge_sort_std_dev)
    plt.plot(arr_sizes,
             bubble_sort_mean,
             color='blue',
             label='bubble sort',
             marker='.')
    plt.fill_between(arr_sizes,
                     bubble_sort_mean - bubble_sort_std_dev,
                     bubble_sort_mean + bubble_sort_std_dev,
                     color='blue',
                     alpha=0.2)
    plt.plot(arr_sizes, 
             merge_sort_mean,
             color='darkorange',
             label='merge sort',
             marker='.')
    plt.fill_between(arr_sizes,
                     merge_sort_mean - merge_sort_std_dev,
                     merge_sort_mean + merge_sort_std_dev,
                     color='darkorange',
                     alpha=0.2)
    plt.title('Merge Sort vs Bubble Sort')
    plt.xlabel('Size of array')
    plt.ylabel('Time to execute function (s)')
    plt.legend()
    plt.show()

