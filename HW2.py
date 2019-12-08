import sys
import os.path

def convert_to_int_list(arr):
    arr = [int(i) for i in arr] 
    return arr


def print_allocation(original_block_sizes, process_sizes, allocated_blocks):
    print("Blocks :",original_block_sizes)
    print("Processes :", process_sizes)
    print()
    print("Process No.", "Process Size","\t" + "Block No.")
    for i in range (0, len(process_sizes)):
        if allocated_blocks[i] == -1:
            print(i+1, process_sizes[i], "Not allocated" , sep="\t"*2)
        else:
            print(i+1, process_sizes[i], allocated_blocks[i], sep="\t"*2)
    

# first-fit algorithm
def first_fit_algorithm(original_block_sizes, process_sizes):
    block_sizes = original_block_sizes.copy()
    allocated_blocks = [-1] * len(process_sizes)
    
    for process_size in process_sizes:
      for block_size in block_sizes:
          
        if block_size >= process_size:
          block_size_index = block_sizes.index(block_size)
          block_sizes[block_size_index] -= process_size         
          allocated_blocks[process_sizes.index(process_size)] = (block_size_index + 1)
          break
      
    print_allocation(original_block_sizes, process_sizes, allocated_blocks)


# best-fit algorithm
def best_fit_algorithm(original_block_sizes, process_sizes):
    block_sizes = original_block_sizes.copy()
    allocated_blocks = [-1] * len(process_sizes)
    
    for process_size in process_sizes:
        # find best block 
        block_index_to_allocate = find_best_block(block_sizes, process_size)
        
        # allocate block
        if(block_index_to_allocate != -1):
            block_sizes[block_index_to_allocate] -= process_size
            allocated_blocks[process_sizes.index(process_size)] = block_index_to_allocate + 1
    
    print_allocation(original_block_sizes, process_sizes, allocated_blocks)


# best-fit helper function
def find_best_block(block_sizes, process_size):
    best_block_size = -1
    best_block_index = -1
    
    for block_size in block_sizes:
        if(block_size >= process_size):
            if(best_block_size == -1 or block_size < best_block_size):
                best_block_size = block_size
                best_block_index = block_sizes.index(block_size)
            
    return best_block_index


# main body
if(len(sys.argv) == 2):
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], 'r') as f:
           try:
                file_content = f.readlines()
           except : 
               exit("Cannot open file !")
    else:
        sys.exit("Input file not exist")
else:
    sys.exit("Inproper input number !")
        
for line in file_content:
    if(file_content.index(line) == 0):
        original_block_sizes = line.split(";")
    else:
        process_sizes = line.split(" ")
        
# convert string lists to int lists
original_block_sizes = convert_to_int_list(original_block_sizes)
process_sizes = convert_to_int_list(process_sizes)

first_fit_algorithm(original_block_sizes, process_sizes)
print()
best_fit_algorithm(original_block_sizes, process_sizes)