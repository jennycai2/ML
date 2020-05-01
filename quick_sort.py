    def partition(nums, left, right):
        n = right - left 
        print("\narray", nums[left:right], "left", nums[left], "right", nums[right-1])
        if (n <= 1):
            return 0
        original_left = left
        original_right = right     
        pivot_idx = right - 1
        right = pivot_idx - 1
        pivot = nums[pivot_idx]
        print("pivot", pivot, "length of array", n)

        while left != right:
            while left < right and nums[left] < pivot:
                print("left", left)
                left += 1
                
            while right > left and nums[right] > pivot:
                print("right", right)
                right -= 1
              
            if left != right:
                nums[left], nums[right] = nums[right], nums[left]
                print("switch, left, right", left, right, "values", nums[left], nums[right])
        if (nums[left] > nums[pivot_idx]): 
            nums[left], nums[pivot_idx] = nums[pivot_idx], nums[left]
            pivot_idx = left
            print("switch, left, pivot_idx", left, pivot_idx, "values", nums[left], nums[pivot_idx])
            
        print("after partition, ", nums[original_left:original_right], "left", left, "right", right)
              
        #divide into two subarrays
        if (pivot_idx > original_left): # pivot_idx might be 0
            print("left subarray ", nums[original_left:pivot_idx])
            partition(nums, original_left, pivot_idx) 
            
        if (pivot_idx + 1 < original_right):
            print("right subarray", nums[pivot_idx+1:original_right])
            partition(nums, pivot_idx+1, original_right)
            
        return
        
    def quick_sort(arr):
        return partition(arr, 0, len(arr)) 
