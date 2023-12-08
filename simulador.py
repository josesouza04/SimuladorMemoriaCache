import sys

def simulate_cache(cache_size, line_size, num_sets, memory_access_file):
    # Inicialização da cache
    cache = [{'valid': 0, 'block_id': 0} for _ in range(cache_size // line_size * num_sets)]

    hits = 0
    misses = 0

    with open(memory_access_file, 'r') as file:
        addresses = [int(line.strip(), 16) for line in file]

    output_content = []  # Lista para armazenar o conteúdo a ser impresso no arquivo

    for address in addresses:
        set_index = (address // line_size) % num_sets
        block_id = (address // line_size) & 0xFFFFFFF0  # Mantém apenas os 32 bits superiores

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
            found_empty_line = False

            # Verifica se há uma linha vazia no conjunto
            for line in range(set_index * (cache_size // line_size), (set_index + 1) * (cache_size // line_size)):
                if not cache[line]['valid']:
                    cache[line]['valid'] = 1
                    cache[line]['block_id'] = block_id
                    found_empty_line = True
                    break

            # Se não encontrou uma linha vazia, substitui a primeira linha do conjunto
            if not found_empty_line:
                replace_index = set_index * (cache_size // line_size)
                cache[replace_index]['valid'] = 1
                cache[replace_index]['block_id'] = block_id

        # Armazena o conteúdo da cache para a impressão posterior
        output_content.extend(print_cache(cache, line_size))

    return output_content, hits, misses

def print_cache(cache, line_size):
    result = []
    result.append("================")
    result.append("IDX V * ADDR *")
    for i, line in enumerate(cache):
        addr_str = f"0x{(i*line_size + line['block_id']):08X}" if line['valid'] else ""
        result.append(f"{i:03d} {line['valid']} {addr_str}")
    result.append("================")
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

        output_file.write(f"#hits: {hits}\n#miss: {misses}\n")

if _name_ == "_main_":
    main()