# heuristica.py
import math

# Mapeo Unicode para subíndices (opcional si se desea usar también visual en consola)
subindice_unicode = {
    '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
    '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
    'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ', 'i': 'ᵢ', 'j': 'ⱼ',
    'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ',
    'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ',
    'v': 'ᵥ', 'x': 'ₓ'
}

def to_subscript(text):
    return ''.join(subindice_unicode.get(c, c) for c in text)

def estimar_complejidad_heuristica(for_niveles, while_niveles, base_log=2):
    base_str = f"<sub>{base_log}</sub>"
    if for_niveles == 0 and while_niveles == 0:
        return "O(1)"
    elif for_niveles == 0 and while_niveles > 0:
        return f"O((log{base_str}(n))<sup>{while_niveles}</sup>)" if while_niveles > 1 else f"O(log{base_str}(n))"
    elif while_niveles == 0 and for_niveles == 1:
        return "O(n)"
    elif while_niveles == 0:
        return f"O(n<sup>{for_niveles}</sup>)"
    else:
        while_part = f"(log{base_str}(n))<sup>{while_niveles}</sup>" if while_niveles > 1 else f"log{base_str}(n)"
        return f"O(n<sup>{for_niveles}</sup> × {while_part})"

def calcular_tn(n, for_niveles, while_niveles, base_log=2):
    if n <= 0:
        return 0
    result = math.pow(n, for_niveles) * math.pow(math.log(n, base_log), while_niveles)
    return min(result, 4000)
