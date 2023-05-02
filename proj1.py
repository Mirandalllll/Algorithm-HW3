# test for the change commit
# to see if it is still work or not
# change history and commit content
import time
import random
import argparse
import matplotlib.pyplot as plt

# change some content and test it.
def read_input(filePath):
    """
    Read data from input file
    :param filePath: input file path
    :return: data in the file
    """
    data = []
    with open(filePath, "r+") as file:
        for line in file.readlines():
            line = line.strip().split(" ")
            line = [int(i) for i in line]
            data.extend(line)
    return data

def output_data(filePath):
    """
    Generate random data and write to input file
    :param filePath: input file path
    """
    with open(filePath, "w") as file:
        data = [random.randint(1, 1000) for i in range(1000000)]
        for i in data:
            file.write(str(i) + " ")

def median_of_medians(arr, sub):
    """
    Find the median of the medians of sublists
    :param arr: the input list
    :param sub: divide input arr into sublists with size subsize
    :return: pivot element
    """
    if len(arr) <= sub:
        return sorted(arr)[len(arr) // 2]
    
    sublists = [arr[i:i + sub] for i in range(0, len(arr), sub)]
    sortedSublists = [sorted(sublist) for sublist in sublists]
    medians = [sublist[len(sublist) // 2] for sublist in sortedSublists]
    
    if len(medians) <= sub:
        return sorted(medians)[len(medians) // 2]
    
    return median_of_medians(medians, sub)



def insertionSort(arr):
    """
    Sort an array using the insertion sort algorithm
    :param arr: unsorted array
    :return: sorted array
    """
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and current < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr

def partition(arr, pivot):
    """
    Partition an array into three parts: values lower than the pivot, values equal to the pivot, and values greater
    than the pivot.
    :param arr: the input array
    :param pivot: the pivot value
    :return: a tuple of three arrays (left, middle, right)
    """
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return left, middle, right

def hybridSort(arr, subsize, threshold):    
    """
    Sort an array using the hybrid sort algorithm
    :param arr: unsorted array
    :param subsize: divide input arr into sublists with size subsize
    :param threshold: threshold value to switch to insertion sort
    :return: sorted array
    """
    if len(arr) <= threshold:
        return insertionSort(arr)
    else:
        pivot_value = median_of_medians(arr, subsize)
        left, middle, right = partition(arr, pivot_value)
        return hybridSort(left, subsize, threshold) + middle + hybridSort(right, subsize, threshold)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-input", help="Input file path", default="inputFile")
    parser.add_argument("-output", help="Output file path", default="outputFile")
    parser.add_argument("-r", type=int, help="parameter r", default=5)
    parser.add_argument("-n", type=int, help="threshold", default=10)
    parser.add_argument("-test", choices=['normal', 'parameter'], help="Test different parameter or run normally", default='normal')

    args = parser.parse_args()

    try:
        if args.test == 'normal':
            if not args.input or not args.output:
                print("Please provide input and output file paths.")
                exit()
            with open(args.output, "w") as f:
                data = read_input(args.input)
                s_time = time.time()
                sorted_data = hybridSort(data, args.r, args.n)
                e_time = time.time()
                print("Use time (s): ", e_time - s_time)
                for item in sorted_data:
                    f.write(str(item) + " ")

        elif args.test == 'parameter': # test different paramaters
            if not args.input:
                print("Please provide input file path.")
                exit()
            output_data(args.input)
            data = read_input(args.input)
            r_list = [5, 7, 9, 11]
            n_list = [i for i in range(10, 200, 10)]
            plt_time = []
            for r in r_list:
                plt_subtime = []
                print("Begin: ", r)
                for n in n_list:
                    args.r = r
                    args.n = n
                    s_time = time.time()
                    sorted_data = hybridSort(data, args.r, args.n)
                    e_time = time.time()
                    plt_subtime.append(e_time - s_time)
                plt_time.append(plt_subtime)
            # plot data
            for i in range(len(plt_time)):
                plt.plot(n_list, plt_time[i])
            plt.legend(['r = 5', 'r = 7', 'r = 9', 'r = 11'], loc='upper right')
            plt.xlabel("n")
            plt.ylabel("time")
            plt.xticks(n_list)
            # plt.savefig("/Users/lliu58/Library/Mobile Documents/com~apple~CloudDocs/Desktop/PhD申请/田纳西/SP2023/Algorithm/HW3/Code/res.png")
            plt.show()
            

    except Exception as e:
        print("An error occurred:", e)





