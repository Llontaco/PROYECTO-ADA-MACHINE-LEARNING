import math

import math

def estimar_complejidad_heuristica(for_niveles, while_niveles):
    if for_niveles == 0 and while_niveles == 0:
        return "O(1)"
    elif for_niveles == 0 and while_niveles > 0:
        return f"O((log(n))^{while_niveles})" if while_niveles > 1 else "O(log(n))"
    elif while_niveles == 0 and for_niveles == 1:
        return "O(n)"
    elif while_niveles == 0:
        return f"O(n^{for_niveles})"
    else:
        while_part = f"(log(n))^{while_niveles}" if while_niveles > 1 else "log(n)"
        return f"O(n^{for_niveles} * {while_part})"

def calcular_tn(n, for_niveles, while_niveles):
    if n <= 0:
        return 0
    result = math.pow(n, for_niveles) * math.pow(math.log(n, 2), while_niveles)
    return min(result, 4000)
