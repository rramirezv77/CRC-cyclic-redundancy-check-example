import os

data_folders = ['dataset1', 'dataset2']
output_file = 'output.txt'

def xor(a, b):
    return 0 if a == b else 1

with open(output_file, 'w') as outfile:
    for data_folder in data_folders:
        outfile.write(f'=== Resultados para {data_folder} ===\n')
        archivos_encontrados = False
        for filename in os.listdir(data_folder):
            if filename.endswith('.txt') and (filename.startswith('data_') or filename.startswith('trama_')):
                archivos_encontrados = True
                input_path = os.path.join(data_folder, filename)
                with open(input_path, 'r') as infile:
                    trama_bits = infile.read().strip()

                registro_temporal = [0] * 16
                resultado_final = [0] * 16

                for bit in trama_bits:
                    bit = int(bit)
                    xor_1 = xor(bit, registro_temporal[15])
                    xor_2 = xor(xor_1, registro_temporal[4])
                    xor_3 = xor(xor_1, registro_temporal[11])

                    for a in range(16):
                        i = 15 - a
                        registro_temporal[i] = registro_temporal[i - 1]

                    registro_temporal[0] = xor_1
                    registro_temporal[5] = xor_2
                    registro_temporal[12] = xor_3

                for i in range(16):
                    resultado_final[i] = registro_temporal[15 - i]

                secuencia_generada = ''.join(map(str, resultado_final))
                # Solo para dataset2, marca si contiene errores
                if data_folder == 'dataset2' and '1' in secuencia_generada:
                    outfile.write(f'{filename}: {secuencia_generada} (contiene errores)\n')
                else:
                    outfile.write(f'{filename}: {secuencia_generada} (sin errores)\n')
        if not archivos_encontrados:
            outfile.write('No se encontraron archivos data_*.txt en esta carpeta.\n')
        outfile.write('\n')