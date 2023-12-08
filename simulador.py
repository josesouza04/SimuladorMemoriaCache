import sys

def simulate_cache(cache_size, line_size, num_sets, memory_access_file):
    # Inicialização da cache
    cache = [{'valid': 0, 'block_id': 0} for _ in range(cache_size // line_size * num_sets)]

    hits = 0
    misses = 0

    with open(memory_access_file, 'r') as file:
        addresses = [int(line.strip(), 16) for line in file]

    for address in addresses:
        set_index = (address // line_size) % num_sets
        block_id = address & ~(line_size - 1)  # Ignorando os bits de deslocamento
        block_id_hex = hex(block_id)[2:].upper()  # Convertendo para hexadecimal e maiúsculas
        block_id_hex = '0x' + block_id_hex.zfill(8)  # Preenchendo com zeros à esquerda para ter 32 bits
        block_id_hex = hex(int(block_id_hex, 16) & ~0x3FF)
        block_id_hex = hex(int(block_id_hex, 16) >> 10)
        


        # Verifica se há hit
        hit = False
        for line in range(set_index * (cache_size // line_size), (set_index + 1) * (cache_size // line_size)):
            if cache[line]['valid'] and cache[line]['block_id'] == block_id:
                hits += 1
                hit = True
                break

        # Se não houver hit, realiza miss e atualiza a cache
        if not hit:
            misses += 1
            replace_index = set_index * (cache_size // line_size)
            cache[replace_index]['valid'] = 1
            cache[replace_index]['block_id'] = block_id

    return cache, hits, misses


def print_cache(cache, num_sets, output_file=None):
    output = "================\n"
    for i in range(num_sets):
        output += "IDX V ** ADDR **\n"
        for j in range(num_sets):
            if cache[j]['valid']:
                block_id_hex = format(cache[j]['block_id'], '08X')
                output += f"{j:03d} 1 0x{block_id_hex}\n"
            else:
                output += f"{j:03d} 0\n"
        output += "================\n"

    if output_file:
        output_file.write(output)
    else:
        print(output)



def main():
    if len(sys.argv) != 5:
        print("Uso: python simulador.py <cache_size> <line_size> <num_sets> <memory_access_file>")
        sys.exit(1)

    cache_size = int(sys.argv[1])
    line_size = int(sys.argv[2])
    num_sets = int(sys.argv[3])
    memory_access_file = sys.argv[4]

    cache, hits, misses = simulate_cache(cache_size, line_size, num_sets, memory_access_file)

    with open("output.txt", 'w') as output_file:
        print_cache(cache,num_sets, output_file)
        output_file.write(f"#hits: {hits}\n#miss: {misses}\n")

if __name__ == "__main__":
    main()
