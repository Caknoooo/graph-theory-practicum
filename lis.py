from sortedcontainers import SortedList

def find_lis_subarray(arr):
  lis = SortedList()
  prev_indices = [-1] * len(arr)

  for i, num in enumerate(arr):
    index = lis.bisect_left(num)
    if index == len(lis):
      lis.add(num)
    else:
      del lis[index]
      lis.add(num)

    if index > 0:
      prev_indices[i] = arr.index(lis[index - 1])

  max_length = len(lis)
  lis_subarray = []
  index = arr.index(lis[-1])

  while index >= 0:
    lis_subarray.append(arr[index])
    index = prev_indices[index]

  lis_subarray.reverse()

  return lis_subarray

# Input array
arr = [10, 22, 9, 33, 21, 50, 41, 60, 17, 62]

# Find LIS subarray
lis_subarray = find_lis_subarray(arr)

# Print the LIS subarray and its length
print("LIS :", ", ".join(map(str, lis_subarray)))
print("Length :", len(lis_subarray))
