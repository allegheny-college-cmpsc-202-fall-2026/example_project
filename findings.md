# Migrating Servers Problem

This document outlines the problem formulation, baseline solution, and proposed algorithmic strategy for the Migrating Servers problem. The goal is to efficiently allocate a collection of data files to a new set of servers while minimizing the total number of servers required.

## Problem Formulation

The objective of the Migrating Servers problem is to efficiently allocate a collection of data files to a new set of servers, minimizing the total number of servers required. We are provided with a list of $n$ file sizes, denoted as $F = [f_1, f_2, \dots, f_n]$, and a strict maximum storage capacity $L$ for each new server. The physical constraints of the new infrastructure dictate that a single server can hold at most two files concurrently, and the combined size of those files must not exceed $L$. Our goal is to design an algorithm that determines the absolute minimum number of servers necessary to migrate all files safely, scaling efficiently even when the number of files $n$ is very large.

## Baseline Solution

To establish a functional baseline, repeatedly select the largest remaining file, then linearly scan the other remaining files to find the largest file that can share a server with it without exceeding capacity $L$. If a compatible partner exists, assign the pair to one server; otherwise, put the largest file on a server by itself. Each iteration takes $O(n)$ time for the selection and scan, and there can be up to $n$ iterations, so the baseline runs in $O(n^2)$ time.

```text
Algorithm migrateServersBaseline(files, L):
    input: List of file sizes F of length n, server capacity L
    output: Minimum number of servers required
    
    servers_used = 0
    remaining = all files in F
    
    while remaining is not empty:
        i = largest file in remaining
        Remove i from remaining
        partner = NONE
        
        for each file j in remaining:
            if i + j <= L and (partner is NONE or j > partner):
                partner = j

        if partner is not NONE:
            Remove partner from remaining

        servers_used = servers_used + 1
        
    return servers_used
```

## Proposed Algorithmic Strategy

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

### Step-by-Step Walkthrough

To understand how the two-pointer approach works, let's trace it with an example array of files $F = [15, 20, 35, 60, 85, 90]$ and a server capacity $L = 100$.

*   **Initialization:** Array is sorted. `left` points to 15, `right` points to 90. `servers = 0`.
*   **Step 1:** Compare $15 + 90 = 105$. This is $> 100$. The 90 file goes on a server alone. `right` moves left. `servers = 1`.
*   **Step 2:** Compare $15 + 85 = 100$. This is $\le 100$. The 15 and 85 files pair up. `left` moves right, `right` moves left. `servers = 2`.
*   **Step 3:** Compare $20 + 60 = 80$. This is $\le 100$. The 20 and 60 files pair up. `left` moves right, `right` moves left. `servers = 3`.
*   **Step 4:** Only the 35 file remains (`left == right`). It goes on a server alone. `servers = 4`.

Total servers needed: 4.

## Correctness Analysis

Both algorithms successfully assign every file to a server without exceeding the capacity $L$. Because each server can hold at most two files, the only way to minimize the total number of servers is to maximize the number of pairs.

**Baseline.** The baseline algorithm's rule is: *Always pair the largest remaining file with the largest file that fits with it.* 
Why does this work? Imagine you have a massive file and you decide *not* to pair it with the largest file that fits, but instead pair it with a tiny file. You just used up a tiny file (which is very easy to pair with almost anything later) and left behind a medium file (which is much harder to pair later). By always pairing the largest file with the largest possible partner, you ensure you aren't "wasting" the highly flexible small files. 

**Proposed algorithm.** The greedy algorithm's rule is: *Look at the absolute largest file and the absolute smallest file.* 
Why is this optimal? The largest file is the hardest file to find a partner for. 
1. **If the largest and smallest files together exceed $L$:** The largest file is so big that it can't even share a server with the smallest file in the entire system. If it can't pair with the absolute smallest, it can't pair with *anything*. It must go on a server by itself.
2. **If the largest and smallest files fit together:** We pair them up. By using the smallest file to "rescue" the largest file and get it to share a server, we successfully secure a pair. This leaves the medium-sized files remaining in the middle of the list. Medium files are much better at pairing with other medium files. If we paired the smallest file with another small file instead, we'd strand the large files later with no small partners left to share their space.

## Complexity Analysis

**Baseline.** When there are $m$ files remaining, finding the largest file and scanning for its largest compatible partner each take $\mathcal{O}(m)$ time. Since each iteration assigns at least one file, there are at most $n$ iterations. In the worst case, the total work is proportional to $n+(n-1)+\cdots+1$, giving $\mathcal{O}(n^2)$ time.

**Proposed algorithm.** Sorting the $n$ file sizes takes $\mathcal{O}(n\log n)$ time with a comparison-based sort such as MergeSort. After sorting, each two-pointer iteration assigns at least one file and moves one or both pointers inward, so the traversal takes $\mathcal{O}(n)$ time. The total is $\mathcal{O}(n\log n)+\mathcal{O}(n)=\mathcal{O}(n\log n)$; sorting dominates the running time.

## Empirical Evaluation

### Implementation

We implemented our two algorithms (`methods.py`) that solve the Server Migration problem. Unit testing (`test_migration.py`) confirms that both algorithms return the correct minimum server count across multiple typical and edge cases (empty arrays, perfectly matched pairs, and unpairable elements).

### Results
We compare the performance of our two algorithms on randomly generated arrays with $L=100$ (`benchmark.py`), varying input size ($n$) from 10 to 50,000 files. We present the results in the plots below. The left plot shows the execution time on a linear scale, while the right plot uses a logarithmic scale for both axes.

| ![Benchmark Plot (Linear Scale)](benchmark_plot.png) | ![Benchmark Plot (Log Scale)](benchmark_plot_log.png) |
|---|---|

The empirical data aligns with our theoretical complexity analysis:

*   **Baseline Quadratic Scaling:** The baseline algorithm theoretically scales at $\mathcal{O}(n^2)$ due to repeatedly scanning the remaining list for the largest element.
*   **Proposed Algorithm Efficiency:** The proposed algorithm scales at $\mathcal{O}(n \log n)$, constrained almost entirely by Python's built-in sorting algorithm. Sorting the 50,000 elements and performing the $\mathcal{O}(n)$ two-pointer traversal takes just 0.0135 seconds. At $n = 50,000$, the proposed algorithm is several orders of magnitude faster than the baseline. In particular, the proposed algorithm is approximately **2,900 times faster**, illustrating that optimizing data organization (sorting) before processing drastically outperforms naive continuous searching.

**The Real-World Impact:** This performance difference has massive practical implications. If a cloud provider charges by the millisecond of compute time, running the $\mathcal{O}(n^2)$ baseline would cost thousands of times more money to execute at scale. Optimizing the underlying algorithm before writing the code is often much cheaper than buying faster hardware!