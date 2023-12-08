import sys
from collections import deque

def simulate_cache(cache_size, line_size, num_sets, memory_access_file):
    if num_sets == 1:
        # Associatividade completa
        cache = [{'valid': 0, 'block_id': 0} for _ in range(cache_size // line_size)]
        fifo_queue = deque()
    else:
        # Associatividade por conjuntos
        lines_per_set = cache_size // (line_size * num_sets)
        cache = [{'valid': 0, 'block_id': 0} for _ in range(cache_size // line_size)]
        fifo_queue = [deque() for _ in range(num_sets)]

    hits = 0
    misses = 0

    with open(memory_access_file, 'r') as file:
        addresses = [int(line.strip(), 16) for line in file]

    output_content = []

    for address in addresses:
        block_id = address & ~(line_size - 1)

        if num_sets == 1:
            set_index = 0
        else:
            set_index = (block_id // (line_size*num_sets)) % num_sets

        hit = False
        if num_sets == 1:
            for line in range(cache_size // line_size):
                if cache[line]['valid'] and cache[line]['block_id'] == block_id:
                    hits += 1
                    hit = True
                    break
        else:
            for line in range(set_index * lines_per_set, (set_index + 1) * lines_per_set):
                if cache[line]['valid'] and cache[line]['block_id'] == block_id:
                    hits += 1
                    hit = True
                    break

        if not hit:
            misses += 1
            replace_index = -1
            if num_sets == 1:
                if len(fifo_queue) == cache_size // line_size:
                    replace_index = fifo_queue.popleft()
                else:
                    for line in range(cache_size // line_size):
                        if not cache[line]['valid']:
                            replace_index = line
                            break
            else:
                if len(fifo_queue[set_index]) == lines_per_set:
                    replace_index = fifo_queue[set_index].popleft()
                else:
                    for line in range(set_index * lines_per_set, (set_index + 1) * lines_per_set):
                        if not cache[line]['valid']:
                            replace_index = line
                            break

            cache[replace_index]['valid'] = 1
            cache[replace_index]['block_id'] = block_id
            fifo_queue.append(replace_index)

        output_content.extend(print_cache(cache, line_size))

    return output_content, hits, misses

def print_cache(cache, line_size):
    result = []
    result.append("================")
    result.append("IDX V ** ADDR **")
    for i, line in enumerate(cache):
        addr_str = f"0x{(line['block_id'] >> 10):08X}" if line['valid'] else ""
        result.append(f"{i:03d} {line['valid']} {addr_str}")
    return result

def main():
    if len(sys.argv) != 5:
        print("Uso: python simulador.py <cache_size> <line_size> <num_sets> <memory_access_file>")
        sys.exit(1)

    cache_size = int(sys.argv[1])
    line_size = int(sys.argv[2])
    num_sets = int(sys.argv[3])
    memory_access_file = sys.argv[4]

    output_content, hits, misses = simulate_cache(cache_size, line_size, num_sets, memory_access_file)

    with open("output.txt", 'w') as output_file:
        for line in output_content:
            output_file.write(line + "\n")
        output_file.write("================\n")
        output_file.write(f"#hits: {hits}\n#miss: {misses}\n")

if __name__ == "__main__":
    main()
