import os

def create_path(date, max_num_nodes):
    output_directory = os.path.join("output_files", date.strftime("%Y-%m-%d") + '_MAX_' + str(max_num_nodes))
    
    # Crear el directorio si no existe
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    return output_directory

def add_path(path, method):
    output_directory = os.path.join(path, method)
    
    # Crear el directorio si no existe
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    return output_directory

def write_to_result_file(result_file_path, data, first_information = False):
    if first_information:
        with open(result_file_path, 'w') as file:
            file.write(data + "\n")
    else:
        with open(result_file_path, 'a') as file:
            file.write(data + "\n")