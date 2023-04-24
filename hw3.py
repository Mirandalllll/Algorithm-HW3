import time
import random
import argparse
import matplotlib.pyplot as plt

# Read data from input file. filePath: input file path. return: array in the file
def read_input(filePath): 
    array = []
    with open(filePath, "r+") as inputfile:
        for row in inputfile.readlines():
            row = row.strip().split(" ")
            row = [int(i) for i in row]
            array.extend(row)
    return array

# Generate random data and write to input file
def output_data(filePath):
    with open(filePath, "w") as resfile:
        res_array = [random.randint(1, 1000) for i in range(1000000)]
        for i in res_array:
            resfile.write(str(i) + " ")

# Find the median of the medians of sublists
def median_of_medians(arr, sub):
    if len(arr) <= sub:
        return sorted(arr)[len(arr) // 2]
    
    sublis = [arr[i:i + sub] for i in range(0, len(arr), sub)]
    sortedSublis = [sorted(sublist) for sublist in sublis]
    medians = [sublist[len(sublist) // 2] for sublist in sortedSublis]
    
    if len(medians) <= sub:
        return sorted(medians)[len(medians) // 2]
    
    return median_of_medians(medians, sub)

# Sort an array using the insertion sort algorithm
def insertionSort(arr):
    for i in range(1, len(arr)):
        k = arr[i]
        j = i - 1
        while j >= 0 and k < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = k
    return arr

# Partition an array into three parts: values lower than the pivot, values equal to the pivot, and values greater than the pivot.
def partition(arr, pivot):
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return left, middle, right

# Sort an array using the hybrid sort
def hybridSort(arr, subsize, threshold):    
    if len(arr) <= threshold:
        return insertionSort(arr)
    else:
        pivot_value = median_of_medians(arr, subsize)
        left, middle, right = partition(arr, pivot_value)
        return hybridSort(left, subsize, threshold) + middle + hybridSort(right, subsize, threshold)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-input", help = "Input file path", default = "input-test")
    parser.add_argument("-output", help = "Output file path", default = "output-res")
    parser.add_argument("-r", type = int, help = "parameter r", default = 11) # according to pic to choose the best one
    parser.add_argument("-n", type = int, help = "threshold", default = 90) # according to pic to choose the best one
    parser.add_argument("-test", choices = ['normal', 'parameter'], help = "Test different parameter or run normally", 
                        default = 'parameter') # default = 'normal' to generate the output-res. default = 'parameter' to test different paramaters

    args = parser.parse_args()

    try:
        if args.test == 'normal':
            if not args.input or not args.output:
                print("Please provide input and output file paths.")
                exit()
            with open(args.output, "w") as f:
                testcase = read_input(args.input)
                s_time = time.time()
                sorted_testcase = hybridSort(testcase, args.r, args.n)
                e_time = time.time()
                print("Use time (s): ", e_time - s_time)
                for item in sorted_testcase:
                    f.write(str(item) + " ")
        # test different parameters and generate the pictures to support the determinations
        elif args.test == 'parameter': 
            if not args.input:
                print("Please provide input file path.")
                exit()
            output_data(args.input)
            testcase = read_input(args.input)
            r_list = [5, 7, 9, 11]
            n_list = [i for i in range(10, 200, 10)]
            plt_time = []
            for r in r_list:
                plt_subtime = []
                print("Begin: ", r)
                for n in n_list:
                    args.r = r
                    args.n = n
                    start_time = time.time()
                    sorted_data = hybridSort(testcase, args.r, args.n)
                    est_time = time.time()
                    plt_subtime.append(est_time - start_time)
                plt_time.append(plt_subtime)
            # plot data
            for i in range(len(plt_time)):
                plt.plot(n_list, plt_time[i])
            plt.legend(['r = 5', 'r = 7', 'r = 9', 'r = 11'], loc='upper right')
            plt.xlabel("n")
            plt.ylabel("Time")
            plt.xticks(n_list)
            plt.savefig("res.jpg") # picture saved in local
            plt.show()
            

    except Exception as e:
        print("An error occurred:", e)





