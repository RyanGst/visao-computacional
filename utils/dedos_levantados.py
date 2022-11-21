def dedos_levantados(maos):
    dedos = []
    for pontadedo in [8, 12, 16, 20]:

        # se a cordenada y do ponto do dedo for menor que a do ponto anterior
        if maos['coordenadas'][pontadedo][1] < maos['coordenadas'][pontadedo - 2][1]:
            dedos.append(1)
        else:
            dedos.append(0)

    return dedos
