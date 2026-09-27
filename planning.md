# Planning and Analysis

## Problem Formulation

The objective of the Migrating Servers problem is to efficiently allocate a collection of data files to a new set of servers, minimizing the total number of servers required. We are provided with a list of $n$ file sizes, denoted as $F = [f_1, f_2, \dots, f_n]$, and a strict maximum storage capacity $L$ for each new server. The physical constraints of the new infrastructure dictate that a single server can hold at most two files concurrently, and the combined size of those files must not exceed $L$. Our goal is to design an algorithm that determines the absolute minimum number of servers necessary to migrate all files safely, scaling efficiently even when the number of files $n$ is very large.

## Baseline Solution

To establish a functional baseline, we can implement a naive pairing strategy. This approach simply iterates through the list of files and attempts to pair each unassigned file with the largest available partner it finds that satisfies the capacity constraint $L$. Otherwise, the file is placed on a server by itself.

```text
Algorithm migrateServersBaseline(files, L):
    input: List of file sizes F of length n, server capacity L
    output: Minimum number of servers required
    
    servers_used = 0
    Mark all files as UNASSIGNED
    
    for each file i in F:
        if file i is already ASSIGNED:
            continue
            
        Find an UNASSIGNED file j in F such that:
            1. Fits on the same server (file i + file j <= L)
            2. Is the largest possible size that still fits
            
        if partner j is found:
            Mark file j as ASSIGNED
            
        Mark file i as ASSIGNED
        servers_used = servers_used + 1
        
    return servers_used
```

## Algorithmic Strategy

To efficiently find the minimum number of servers, we propose a greedy algorithmic strategy that pairs large and small files together. The core insight is that to minimize wasted space and maximize the number of pairs, we should always try to pair the largest remaining file with the smallest remaining file. 

We begin by sorting the list of file sizes in ascending order. We then initialize two pointers: one at the start of the sorted list (the smallest file) and one at the end (the largest file). We check if the sum of the files at these two pointers is less than or equal to $L$. If the pair of files fit on a new server, we place them on a single server and move both pointers inward. If they do not fit, the largest file must be too large to pair with even the smallest available file. Therefore, it must occupy a server on its own, and we move only the pointer for the larger file inward. We repeat this process until all files are assigned.

```text
Algorithm migrateServersGreedy(F, L):
    input: List of file sizes F of length n, server capacity L
    output: Minimum number of servers required
    
    Sort F in ascending order
    servers_used = 0
    left = 0
    right = n - 1
    
    while left <= right:
        if left == right:
            // Only one file remains
            servers_used = servers_used + 1
            break
            
        if F[left] + F[right] <= L:
            // Pair the smallest and largest files
            left = left + 1
            right = right - 1
            servers_used = servers_used + 1
        else:
            // Largest file must go alone
            right = right - 1
            servers_used = servers_used + 1
            
    return servers_used
```

## Complexity Analysis

We find that the greedy algorithm yields a significant improvement in running time. The naive baseline algorithm operates with a worst-case time complexity of $\mathcal{O}(n^2)$, because, for every file, it potentially scans the remainder of the array to find a suitable partner. Our proposed greedy strategy is more efficient. The dominant operation is the initial sorting of the array, which incurs a running time of $\mathcal{O}(n \log n)$ assuming an efficient sorting algorithm like [Merge Sort](https://en.wikipedia.org/wiki/Merge_sort). Following the sort, the two-pointer traversal evaluates the array in a single pass, which takes exactly $\mathcal{O}(n)$ time. Therefore, the overall running time is $\mathcal{O}(n \log n)$. 