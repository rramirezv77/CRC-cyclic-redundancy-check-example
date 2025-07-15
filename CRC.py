import os

# Lista de carpetas a procesar
data_folders = ['dataset1', 'dataset2']
# Nombre del archivo de salida
output_file = 'output.txt'

# Función XOR para bits
def xor(a, b):
    return 0 if a == b else 1

# Abrir el archivo de salida en modo escritura
with open(output_file, 'w') as outfile:
    # Procesar cada carpeta de datos
    for data_folder in data_folders:
        # Escribir encabezado para cada carpeta
        outfile.write(f'=== Resultados para {data_folder} ===\n')
        archivos_encontrados = False
        # Recorrer todos los archivos en la carpeta
        for filename in os.listdir(data_folder):
            # Filtrar archivos que empiezan con 'data_' o 'trama_' y terminan en '.txt'
            if filename.endswith('.txt') and (filename.startswith('data_') or filename.startswith('trama_')):
                archivos_encontrados = True
                input_path = os.path.join(data_folder, filename)
                # Leer la trama de bits del archivo
                with open(input_path, 'r') as infile:
                    trama_bits = infile.read().strip()

                # Inicializar registros temporales para el cálculo CRC
                registro_temporal = [0] * 16
                resultado_final = [0] * 16

                # Procesar cada bit de la trama
                for bit in trama_bits:
                    bit = int(bit)
                    xor_1 = xor(bit, registro_temporal[15])
                    xor_2 = xor(xor_1, registro_temporal[4])
                    xor_3 = xor(xor_1, registro_temporal[11])

                    # Desplazar los registros temporales
                    for a in range(16):
                        i = 15 - a
                        registro_temporal[i] = registro_temporal[i - 1]

                    # Actualizar posiciones específicas según el polinomio CRC
                    registro_temporal[0] = xor_1
                    registro_temporal[5] = xor_2
                    registro_temporal[12] = xor_3

                # Guardar el resultado final del CRC
                for i in range(16):
                    resultado_final[i] = registro_temporal[15 - i]

                # Convertir el resultado a cadena de texto
                secuencia_generada = ''.join(map(str, resultado_final))
                # Solo para dataset2, marca si contiene errores si hay algún '1'
                if data_folder == 'dataset2' and '1' in secuencia_generada:
                    outfile.write(f'{filename}: {secuencia_generada} (contiene errores)\n')
                else:
                    outfile.write(f'{filename}: {secuencia_generada}\n')
        # Si no se encontraron archivos válidos, escribir mensaje
        if not archivos_encontrados:
            outfile.write('No se encontraron archivos data_*.txt en esta carpeta.\n')
        # Línea en blanco para separar resultados de carpetas diferentes
        outfile.write('\n')