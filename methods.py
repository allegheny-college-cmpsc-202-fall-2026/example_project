# methods.py
# Implements baseline and proposed solutions for the Server Migration problem.


def migrateServersBaseline(files, L):
    """
    Baseline Algorithm: O(n^2) time complexity.
    Finds the largest remaining file, then linearly scans the rest of the 
    list to find the largest possible file that can fit on the same server.
    """
    if not files:
        return 0
        
    files_copy = files.copy()
    server_count = 0
    
    while files_copy:
        # Greedily pick the largest file available
        largest = max(files_copy)
        files_copy.remove(largest)
        
        best_match_size = -1
        best_match_idx = -1
        
        # Scan remaining files for the best valid partner
        for i, f in enumerate(files_copy):
            if f + largest <= L:
                if f > best_match_size:
                    best_match_size = f
                    best_match_idx = i
                    
        # If a partner is found, remove it as well
        if best_match_idx != -1:
            files_copy.pop(best_match_idx)
            
        server_count += 1
        
    return server_count


def migrateServersProposed(files, L):
    """
    Proposed Algorithm: O(n log n) time complexity.
    Sorts the list and utilizes a two-pointer approach to pair the 
    largest available file with the smallest available file.
    """
    if not files:
        return 0
        
    # Sorting dominates the time complexity: O(n log n)
    sorted_files = sorted(files)
    
    left = 0
    right = len(sorted_files) - 1
    server_count = 0
    
    # Two-pointer traversal: O(n)
    while left <= right:
        if left == right:
            # Only one file left; it requires its own server
            server_count += 1
            break
            
        if sorted_files[left] + sorted_files[right] <= L:
            # Files fit together: move both pointers inward
            left += 1
            right -= 1
            server_count += 1
        else:
            # Files don't fit: largest file gets its own server
            right -= 1
            server_count += 1
            
    return server_count