
## Dependencies
* python 3.6.1 (no additional modules)

## Approach to the problem

#### Finding the median by Max,Min heaps
Main challenge in this problem is calculating running median of `TRANSACTION_AMT` grouped by `ZIP_CODE`, as we know in order to compute median a sorted list is required.In case streaming data if we store `TRANSACTION_AMT` in to a list for each `ZIP_CODE` then we need to perform sorting of a list repetitively to find running median and it becomes computationally very expensive as the list grows because of streaming data.

The trick here is to use Min-Max heap based algorithm to find median,which makes use of two different heaps. Max_heap is for values greater than median and Min_heap is for values less than median so whenever a new record is read `TRANSACTION_AMT` value will be pushed to one of these heaps  `if len('Max_heap') <= len('Min_heap') then push to Max_heap else push to Min_heap`.

With this approach it is guaranteed that values gretaer than median will be in Max_heap and less than median will be in Min_heap.Now median can be computed using Max_heap and Min_heap as 
` if len(Max_heap) > len(Min_heap) then median=Max_heap[0] `
`else median=(Max_heap[0]-Min_heap[0])/2`.

#### Custom dictionary data structure
Next challenge is to group incoming records by `CMTE_ID` in combination with `ZIP_CODE`,`TRANSACTION_DT` and report running median,number of transactions and Total of Donations. To handle this a dictionary data structure with lists as its values is created for both `ZIP_CODE`,`TRANSACTION_DT` cases.

For example in `Median values by ZIP_CODE` case : dictionary structure looks like `dict_={'key':{'max_heap': list, 'min_heap':list, 'count':None, 'Total':None }}` which is a dictionary of dictionary. So whenever a new record is read `key` is obtained as combination of `CMTE_ID|ZIP_CODE` , corresponding values  `max_heap,min_heap,count,Total` are updated.Similar method is followed for `Median values by TRANSACTION_DT` case with `CMTE_ID|TRANSACTION_DT` as key.

## Summary of steps
1) Data structure chosen is a dictionary of dictionaries with max_heap,min_heap lists for median calculation and count of total transactions,total of donations received.
2) Read one record at a time from input file and simulataenously update dictionaries for by `ZIP_CODE` and by `TRANSACTION_DT` cases    
3) For by `ZIP_CODE` case whenever a new record is read , dictionary gets updated and running median is calculated and results will be written to the output file
4) For by `TRANSACTION_DT` case for every record dictionary gets updated but output file is generated at the end.



