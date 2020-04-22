# from http://20bits.com/article/introduction-to-dynamic-programming
def max_subarray_sum(a):
    bounds, max_sum, current_sum, begin_idx = (0,0), -float('infinity'), 0, 0
    print("bounds", bounds, "max_sum", max_sum, "current_sum", current_sum, "begin_idx", begin_idx)
    
    for i in range(len(a)):
        current_sum = current_sum + a[i]
        if current_sum > max_sum: bounds, max_sum = (begin_idx, i+1), current_sum
        if current_sum < 0: current_sum, begin_idx = 0, i+1
        print("i = ", i, "bounds", bounds, "max_sum", max_sum, "current_sum", current_sum, "begin_idx", begin_idx)
    return (max_sum, bounds)


a = [-8, 9, 6, -6, 1, 8]
a = [1,2,-5,4,7,-2]
max_subarray_sum(a)
