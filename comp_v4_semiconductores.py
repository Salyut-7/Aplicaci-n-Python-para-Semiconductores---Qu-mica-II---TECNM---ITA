import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from densidades import DENSIDAD
from radios_atomicos import RADIO
import matplotlib
matplotlib.use('GTK3Agg')
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# --- Base de datos de estructuras cristalinas ---
# Estructura cristalina a temperatura ambiente para cada elemento
ESTRUCTURA_CRISTALINA = {
    # ========== ESTRUCTURAS PARA SEMICONDUCTORES (PRIORIDAD) ==========
    
    # DIAMANTE (Diamond) - Estructura cúbica con base compleja
    6: "DIAMANTE",   # C (Carbono - diamante)
    14: "DIAMANTE",  # Si (Silicio - base de semiconductores)
    32: "DIAMANTE",  # Ge (Germanio)
    
    # HEXAGONAL SIMPLE
    34: "HEXAGONAL", # Se (Selenio)
    52: "HEXAGONAL", # Te (Telurio)
    
    # ORTORRÓMBICA (Orthorhombic)
    15: "ORTORROMBICA", # P (Fósforo blanco)
    16: "ORTORROMBICA", # S (Azufre)
    31: "ORTORROMBICA", # Ga (Galio)
    
    # ROMBOÉDRICA (Rhombohedral) - Similar a hexagonal pero con simetría diferente
    5: "ROMBOEDRICA",  # B (Boro)
    33: "ROMBOEDRICA", # As (Arsénico)
    51: "ROMBOEDRICA", # Sb (Antimonio)
    
    # TETRAGONAL
    49: "TETRAGONAL",  # In (Indio)
    50: "TETRAGONAL",  # Sn (Estaño blanco)
    
    # Nota: N (7) es gas a temp. ambiente, no tiene estructura cristalina simple
    
    # ========== ESTRUCTURAS METÁLICAS CLÁSICAS ==========
    
    # SC (Simple Cubic) - muy raro
    84: "SC",  # Po (Polonio)
    
    # BCC (Body-Centered Cubic)
    3: "BCC",   # Li
    11: "BCC",  # Na
    19: "BCC",  # K
    23: "BCC",  # V
    24: "BCC",  # Cr
    26: "BCC",  # Fe
    37: "BCC",  # Rb
    41: "BCC",  # Nb
    42: "BCC",  # Mo
    55: "BCC",  # Cs
    56: "BCC",  # Ba
    73: "BCC",  # Ta
    74: "BCC",  # W
    87: "BCC",  # Fr
    88: "BCC",  # Ra
    
    # FCC (Face-Centered Cubic)
    10: "FCC",  # Ne
    13: "FCC",  # Al
    18: "FCC",  # Ar
    20: "FCC",  # Ca
    28: "FCC",  # Ni
    29: "FCC",  # Cu
    36: "FCC",  # Kr
    38: "FCC",  # Sr
    45: "FCC",  # Rh
    46: "FCC",  # Pd
    47: "FCC",  # Ag
    54: "FCC",  # Xe
    77: "FCC",  # Ir
    78: "FCC",  # Pt
    79: "FCC",  # Au
    82: "FCC",  # Pb
    89: "FCC",  # Ac
    90: "FCC",  # Th
    
    # HCP (Hexagonal Close-Packed)
    4: "HCP",   # Be
    12: "HCP",  # Mg
    21: "HCP",  # Sc
    22: "HCP",  # Ti
    27: "HCP",  # Co
    30: "HCP",  # Zn
    39: "HCP",  # Y
    40: "HCP",  # Zr
    43: "HCP",  # Tc
    44: "HCP",  # Ru
    48: "HCP",  # Cd
    57: "HCP",  # La
    58: "HCP",  # Ce
    59: "HCP",  # Pr
    60: "HCP",  # Nd
    62: "HCP",  # Sm
    63: "HCP",  # Eu
    64: "HCP",  # Gd
    65: "HCP",  # Tb
    66: "HCP",  # Dy
    67: "HCP",  # Ho
    68: "HCP",  # Er
    69: "HCP",  # Tm
    70: "HCP",  # Yb
    71: "HCP",  # Lu
    72: "HCP",  # Hf
    75: "HCP",  # Re
    76: "HCP",  # Os
    81: "HCP",  # Tl
}


# --- Tabla periódica completa (Z: (símbolo, nombre)) ---
ELEMENTOS = {
    1: ("H", "Hidrógeno"), 2: ("He", "Helio"),
    3: ("Li", "Litio"), 4: ("Be", "Berilio"), 5: ("B", "Boro"), 6: ("C", "Carbono"), 7: ("N", "Nitrógeno"), 8: ("O", "Oxígeno"), 9: ("F", "Flúor"), 10: ("Ne", "Neón"),
    11: ("Na", "Sodio"), 12: ("Mg", "Magnesio"), 13: ("Al", "Aluminio"), 14: ("Si", "Silicio"), 15: ("P", "Fósforo"), 16: ("S", "Azufre"), 17: ("Cl", "Cloro"), 18: ("Ar", "Argón"),
    19: ("K", "Potasio"), 20: ("Ca", "Calcio"), 21: ("Sc", "Escandio"), 22: ("Ti", "Titanio"), 23: ("V", "Vanadio"), 24: ("Cr", "Cromo"), 25: ("Mn", "Manganeso"), 26: ("Fe", "Hierro"),
    27: ("Co", "Cobalto"), 28: ("Ni", "Níquel"), 29: ("Cu", "Cobre"), 30: ("Zn", "Zinc"), 31: ("Ga", "Galio"), 32: ("Ge", "Germanio"), 33: ("As", "Arsénico"), 34: ("Se", "Selenio"),
    35: ("Br", "Bromo"), 36: ("Kr", "Kriptón"), 37: ("Rb", "Rubidio"), 38: ("Sr", "Estroncio"), 39: ("Y", "Itrio"), 40: ("Zr", "Circonio"), 41: ("Nb", "Niobio"), 42: ("Mo", "Molibdeno"),
    43: ("Tc", "Tecnecio"), 44: ("Ru", "Rutenio"), 45: ("Rh", "Rodio"), 46: ("Pd", "Paladio"), 47: ("Ag", "Plata"), 48: ("Cd", "Cadmio"), 49: ("In", "Indio"), 50: ("Sn", "Estaño"),
    51: ("Sb", "Antimonio"), 52: ("Te", "Telurio"), 53: ("I", "Yodo"), 54: ("Xe", "Xenón"), 55: ("Cs", "Cesio"), 56: ("Ba", "Bario"), 57: ("La", "Lantano"), 58: ("Ce", "Cerio"),
    59: ("Pr", "Praseodimio"), 60: ("Nd", "Neodimio"), 61: ("Pm", "Prometio"), 62: ("Sm", "Samario"), 63: ("Eu", "Europio"), 64: ("Gd", "Gadolinio"), 65: ("Tb", "Terbio"),
    66: ("Dy", "Disprosio"), 67: ("Ho", "Holmio"), 68: ("Er", "Erbio"), 69: ("Tm", "Tulio"), 70: ("Yb", "Iterbio"), 71: ("Lu", "Lutecio"), 72: ("Hf", "Hafnio"), 73: ("Ta", "Tantalio"),
    74: ("W", "Wolframio"), 75: ("Re", "Renio"), 76: ("Os", "Osmio"), 77: ("Ir", "Iridio"), 78: ("Pt", "Platino"), 79: ("Au", "Oro"), 80: ("Hg", "Mercurio"), 81: ("Tl", "Talio"),
    82: ("Pb", "Plomo"), 83: ("Bi", "Bismuto"), 84: ("Po", "Polonio"), 85: ("At", "Astato"), 86: ("Rn", "Radón"), 87: ("Fr", "Francio"), 88: ("Ra", "Radio"), 89: ("Ac", "Actinio"),
    90: ("Th", "Torio"), 91: ("Pa", "Protactinio"), 92: ("U", "Uranio"), 93: ("Np", "Neptunio"), 94: ("Pu", "Plutonio"), 95: ("Am", "Americio"), 96: ("Cm", "Curio"), 97: ("Bk", "Berkelio"),
    98: ("Cf", "Californio"), 99: ("Es", "Einsteinio"), 100: ("Fm", "Fermio"), 101: ("Md", "Mendelevio"), 102: ("No", "Nobelio"), 103: ("Lr", "Lawrencio"), 104: ("Rf", "Rutherfordio"),
    105: ("Db", "Dubnio"), 106: ("Sg", "Seaborgio"), 107: ("Bh", "Bohrio"), 108: ("Hs", "Hassio"), 109: ("Mt", "Meitnerio"), 110: ("Ds", "Darmstadtio"), 111: ("Rg", "Roentgenio"),
    112: ("Cn", "Copernicio"), 113: ("Nh", "Nihonio"), 114: ("Fl", "Flerovio"), 115: ("Mc", "Moscovio"), 116: ("Lv", "Livermorio"), 117: ("Ts", "Tenesino"), 118: ("Og", "Oganesón")
}

# Índice inverso símbolo → Z
SIMBOLO_A_Z = {sym: z for z, (sym, _) in ELEMENTOS.items()}

# --- Secuencia de subniveles (Aufbau) ---
SUBNIVELES = [
    ("1s", 2),
    ("2s", 2), ("2p", 6),
    ("3s", 2), ("3p", 6),
    ("4s", 2),
    ("3d", 10), ("4p", 6),
    ("5s", 2),
    ("4d", 10), ("5p", 6),
    ("6s", 2),
    ("4f", 14), ("5d", 10), ("6p", 6),
    ("7s", 2),
    ("5f", 14), ("6d", 10), ("7p", 6),
]

# --- Excepciones conocidas ---
EXCEPCIONES = {
    24: "1s² 2s² 2p⁶ 3s² 3p⁶ 4s¹ 3d⁵",   # Cr
    29: "1s² 2s² 2p⁶ 3s² 3p⁶ 4s¹ 3d¹⁰",  # Cu
    42: "1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d¹⁰ 4p⁶ 5s¹ 4d⁵",  # Mo
    47: "1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d¹⁰ 4p⁶ 5s¹ 4d¹⁰", # Ag
    79: "1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d¹⁰ 4p⁶ 5s² 4d¹⁰ 5p⁶ 6s¹ 4f¹⁴ 5d¹⁰" # Au
}

# --- Conjunto industria semiconductor (B)
SEMICONDUCTORES_INDUSTRIA = {
    5,  # B (dopaje en Si)
    6,  # C (diamante, SiC)
    7,  # N (III-V como GaN)
    14, # Si (base industria)
    15, # P (dopaje)
    31, # Ga (III-V)
    32, # Ge (SiGe)
    33, # As (III-V GaAs, InAs)
    49, # In (III-V InSb)
    51, # Sb (III-V)
    34, # Se (fotovoltaicos)
    52  # Te (CdTe solar)
}

def calcular_configuracion_electronica(z):
    """Devuelve la configuración electrónica completa para un elemento."""
    if z in EXCEPCIONES:
        return EXCEPCIONES[z], True

    electrones_restantes = z
    configuracion = []

    for subnivel, capacidad in SUBNIVELES:
        if electrones_restantes <= 0:
            break
        e = min(capacidad, electrones_restantes)
        configuracion.append(f"{subnivel}^{e}")
        electrones_restantes -= e

    return " ".join(configuracion), False


# ======================================================================
# FUNCIONES PARA GENERAR GEOMETRÍAS DE CELDILLAS UNITARIAS
# ======================================================================

def generar_celdilla_sc():
    """Genera posiciones atómicas para estructura SC (Simple Cubic)"""
    # Solo en las esquinas del cubo
    posiciones = [
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
        [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]
    ]
    return np.array(posiciones)


def generar_celdilla_bcc():
    """Genera posiciones atómicas para estructura BCC (Body-Centered Cubic)"""
    # Esquinas + centro del cubo
    posiciones = [
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
        [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1],
        [0.5, 0.5, 0.5]  # Centro
    ]
    return np.array(posiciones)


def generar_celdilla_fcc():
    """Genera posiciones atómicas para estructura FCC (Face-Centered Cubic)"""
    # Esquinas + centros de caras
    posiciones = [
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
        [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1],
        [0.5, 0.5, 0],  # Centro cara xy (z=0)
        [0.5, 0, 0.5],  # Centro cara xz (y=0)
        [0, 0.5, 0.5],  # Centro cara yz (x=0)
        [0.5, 0.5, 1],  # Centro cara xy (z=1)
        [0.5, 1, 0.5],  # Centro cara xz (y=1)
        [1, 0.5, 0.5],  # Centro cara yz (x=1)
    ]
    return np.array(posiciones)


def generar_celdilla_hcp():
    """Genera posiciones atómicas para estructura HCP (Hexagonal Close-Packed)"""
    # Celdilla hexagonal simplificada
    a = 1.0
    c = 1.633 * a  # Relación c/a típica para HCP ideal
    
    posiciones = [
        # Capa inferior (z=0)
        [0, 0, 0],
        [0.5, 0.866, 0],
        [1.5, 0.866, 0],
        [2, 0, 0],
        [1.5, -0.866, 0],
        [0.5, -0.866, 0],
        
        # Capa intermedia (z=c/2)
        [1, 0.577, c/2],
        [1, -0.577, c/2],
        [0, -0.577, c/2],
        
        # Capa superior (z=c)
        [0, 0, c],
        [0.5, 0.866, c],
        [1.5, 0.866, c],
        [2, 0, c],
        [1.5, -0.866, c],
        [0.5, -0.866, c],
    ]
    return np.array(posiciones)


def generar_celdilla_diamante():
    """
    Genera posiciones atómicas para estructura DIAMANTE (Diamond)
    Usada por Si, Ge, C (diamante)
    Es una FCC con átomos adicionales en posiciones tetraédricas
    """
    # FCC base
    posiciones_fcc = [
        [0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5],
    ]
    
    # Átomos en posiciones tetraédricas (1/4, 1/4, 1/4) de cada cubo FCC
    posiciones_tetra = [
        [0.25, 0.25, 0.25],
        [0.75, 0.75, 0.25],
        [0.75, 0.25, 0.75],
        [0.25, 0.75, 0.75],
    ]
    
    posiciones = posiciones_fcc + posiciones_tetra
    return np.array(posiciones)


def generar_celdilla_tetragonal():
    """
    Genera posiciones atómicas para estructura TETRAGONAL
    Usada por In, Sn (β)
    Similar a SC pero con un eje alargado (c ≠ a)
    """
    c = 1.5  # Relación c/a > 1
    
    posiciones = [
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, c],
        [1, 1, 0], [1, 0, c], [0, 1, c], [1, 1, c],
        [0.5, 0.5, c/2]  # Centro
    ]
    return np.array(posiciones)


def generar_celdilla_ortorrombica():
    """
    Genera posiciones atómicas para estructura ORTORRÓMBICA
    Usada por Ga, P, S
    Tres ejes de diferente longitud (a ≠ b ≠ c)
    """
    a, b, c = 1.0, 0.8, 1.2
    
    posiciones = [
        [0, 0, 0], [a, 0, 0], [0, b, 0], [0, 0, c],
        [a, b, 0], [a, 0, c], [0, b, c], [a, b, c],
    ]
    return np.array(posiciones)


def generar_celdilla_hexagonal():
    """
    Genera posiciones atómicas para estructura HEXAGONAL SIMPLE
    Usada por Se, Te
    Base hexagonal con un solo átomo por celda
    """
    a = 1.0
    c = 1.4 * a
    
    # Hexágono en base
    angulos = np.linspace(0, 2*np.pi, 7)
    posiciones = []
    
    # Capa inferior
    for ang in angulos[:-1]:
        posiciones.append([a * np.cos(ang), a * np.sin(ang), 0])
    
    # Centro inferior
    posiciones.append([0, 0, 0])
    
    # Capa superior
    for ang in angulos[:-1]:
        posiciones.append([a * np.cos(ang), a * np.sin(ang), c])
    
    # Centro superior
    posiciones.append([0, 0, c])
    
    return np.array(posiciones)


def generar_celdilla_romboedrica():
    """
    Genera posiciones atómicas para estructura ROMBOÉDRICA
    Usada por As, Sb, B
    Similar a hexagonal pero con diferente simetría
    """
    a = 1.0
    alpha = 60  # Ángulo romboédrico en grados
    alpha_rad = np.radians(alpha)
    
    # Vectores base romboédricos
    posiciones = [
        [0, 0, 0],
        [a, 0, 0],
        [a * np.cos(alpha_rad), a * np.sin(alpha_rad), 0],
        [a * np.cos(alpha_rad), a * np.cos(alpha_rad), a * np.sin(alpha_rad)],
        [0.5, 0.5, 0.5],  # Posición interna
    ]
    
    return np.array(posiciones)


def dibujar_cubo(ax, origen=[0, 0, 0], tamano=1, color='blue', alpha=0.1):
    """Dibuja las aristas de un cubo"""
    x0, y0, z0 = origen
    
    # Aristas inferiores
    ax.plot([x0, x0+tamano], [y0, y0], [z0, z0], color, alpha=0.6, linewidth=1.5)
    ax.plot([x0+tamano, x0+tamano], [y0, y0+tamano], [z0, z0], color, alpha=0.6, linewidth=1.5)
    ax.plot([x0+tamano, x0], [y0+tamano, y0+tamano], [z0, z0], color, alpha=0.6, linewidth=1.5)
    ax.plot([x0, x0], [y0+tamano, y0], [z0, z0], color, alpha=0.6, linewidth=1.5)
    
    # Aristas superiores
    ax.plot([x0, x0+tamano], [y0, y0], [z0+tamano, z0+tamano], color, alpha=0.6, linewidth=1.5)
    ax.plot([x0+tamano, x0+tamano], [y0, y0+tamano], [z0+tamano, z0+tamano], color, alpha=0.6, linewidth=1.5)
    ax.plot([x0+tamano, x0], [y0+tamano, y0+tamano], [z0+tamano, z0+tamano], color, alpha=0.6, linewidth=1.5)
    ax.plot([x0, x0], [y0+tamano, y0], [z0+tamano, z0+tamano], color, alpha=0.6, linewidth=1.5)
    
    # Aristas verticales
    ax.plot([x0, x0], [y0, y0], [z0, z0+tamano], color, alpha=0.6, linewidth=1.5)
    ax.plot([x0+tamano, x0+tamano], [y0, y0], [z0, z0+tamano], color, alpha=0.6, linewidth=1.5)
    ax.plot([x0+tamano, x0+tamano], [y0+tamano, y0+tamano], [z0, z0+tamano], color, alpha=0.6, linewidth=1.5)
    ax.plot([x0, x0], [y0+tamano, y0+tamano], [z0, z0+tamano], color, alpha=0.6, linewidth=1.5)


def dibujar_caja_ortorrombica(ax, a=1.0, b=0.8, c=1.2, color='blue'):
    """Dibuja las aristas de una caja ortorrómbica"""
    # Aristas inferiores
    ax.plot([0, a], [0, 0], [0, 0], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, a], [0, b], [0, 0], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, 0], [b, b], [0, 0], color, alpha=0.6, linewidth=1.5)
    ax.plot([0, 0], [b, 0], [0, 0], color, alpha=0.6, linewidth=1.5)
    
    # Aristas superiores
    ax.plot([0, a], [0, 0], [c, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, a], [0, b], [c, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, 0], [b, b], [c, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([0, 0], [b, 0], [c, c], color, alpha=0.6, linewidth=1.5)
    
    # Aristas verticales
    ax.plot([0, 0], [0, 0], [0, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, a], [0, 0], [0, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, a], [b, b], [0, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([0, 0], [b, b], [0, c], color, alpha=0.6, linewidth=1.5)


def dibujar_prisma_hexagonal(ax, altura=1.633, color='blue'):
    """Dibuja las aristas de un prisma hexagonal para HCP y Hexagonal"""
    a = 1.0
    c = altura
    
    # Hexágono inferior
    angulos = np.linspace(0, 2*np.pi, 7)
    x_hex = a * np.cos(angulos)
    y_hex = a * np.sin(angulos)
    z_hex = np.zeros_like(angulos)
    ax.plot(x_hex, y_hex, z_hex, color, alpha=0.6, linewidth=1.5)
    
    # Hexágono superior
    ax.plot(x_hex, y_hex, z_hex + c, color, alpha=0.6, linewidth=1.5)
    
    # Aristas verticales
    for i in range(6):
        ax.plot([x_hex[i], x_hex[i]], [y_hex[i], y_hex[i]], [0, c], color, alpha=0.6, linewidth=1.5)


def dibujar_caja_tetragonal(ax, a=1.0, c=1.5, color='blue'):
    """Dibuja las aristas de una caja tetragonal (a=b≠c)"""
    # Aristas inferiores
    ax.plot([0, a], [0, 0], [0, 0], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, a], [0, a], [0, 0], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, 0], [a, a], [0, 0], color, alpha=0.6, linewidth=1.5)
    ax.plot([0, 0], [a, 0], [0, 0], color, alpha=0.6, linewidth=1.5)
    
    # Aristas superiores
    ax.plot([0, a], [0, 0], [c, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, a], [0, a], [c, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, 0], [a, a], [c, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([0, 0], [a, 0], [c, c], color, alpha=0.6, linewidth=1.5)
    
    # Aristas verticales
    ax.plot([0, 0], [0, 0], [0, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, a], [0, 0], [0, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([a, a], [a, a], [0, c], color, alpha=0.6, linewidth=1.5)
    ax.plot([0, 0], [a, a], [0, c], color, alpha=0.6, linewidth=1.5)


# ======================================================================
# WIDGET DE VISUALIZACIÓN 3D
# ======================================================================

class VisorCeldillaUnitaria(Gtk.Box):
    """Widget GTK3 que contiene el visor 3D de celdilla unitaria"""
    
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
        # Figura de Matplotlib
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Canvas GTK3
        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(600, 500)
        self.pack_start(self.canvas, True, True, 0)
        
        # Controles
        controles_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.pack_start(controles_box, False, False, 0)
        
        label_estructura = Gtk.Label(label="Tipo de estructura:")
        controles_box.pack_start(label_estructura, False, False, 0)
        
        self.combo_estructura = Gtk.ComboBoxText()
        self.combo_estructura.append_text("SC - Cúbica Simple")
        self.combo_estructura.append_text("BCC - Cúbica Centrada en el Cuerpo")
        self.combo_estructura.append_text("FCC - Cúbica Centrada en las Caras")
        self.combo_estructura.append_text("HCP - Hexagonal Compacta")
        self.combo_estructura.append_text("DIAMANTE - Estructura Diamante (Si, Ge)")
        self.combo_estructura.append_text("TETRAGONAL - Tetragonal")
        self.combo_estructura.append_text("ORTORROMBICA - Ortorrómbica")
        self.combo_estructura.append_text("HEXAGONAL - Hexagonal Simple")
        self.combo_estructura.append_text("ROMBOEDRICA - Romboédrica")
        self.combo_estructura.set_active(0)
        self.combo_estructura.connect("changed", self.on_estructura_changed)
        controles_box.pack_start(self.combo_estructura, True, True, 0)
        
        # Inicializar estructura
        self.estructura_actual = "SC"
        self.elemento_actual = None
        self.dibujar_estructura()
    
    def on_estructura_changed(self, combo):
        """Callback cuando cambia el tipo de estructura"""
        texto = combo.get_active_text()
        if texto:
            self.estructura_actual = texto.split(" - ")[0]
            self.dibujar_estructura()
    
    def actualizar_elemento(self, z):
        """Actualiza el visor para un elemento específico"""
        self.elemento_actual = z
        
        # Obtener estructura del elemento
        if z in ESTRUCTURA_CRISTALINA:
            estructura = ESTRUCTURA_CRISTALINA[z]
            
            # Seleccionar en el combo
            indices = {
                "SC": 0, "BCC": 1, "FCC": 2, "HCP": 3,
                "DIAMANTE": 4, "TETRAGONAL": 5, "ORTORROMBICA": 6,
                "HEXAGONAL": 7, "ROMBOEDRICA": 8
            }
            if estructura in indices:
                self.combo_estructura.set_active(indices[estructura])
                self.estructura_actual = estructura
        
        self.dibujar_estructura()
    
    def dibujar_estructura(self):
        """Dibuja la estructura cristalina actual"""
        self.ax.clear()
        
        # Generar posiciones según el tipo
        if self.estructura_actual == "SC":
            posiciones = generar_celdilla_sc()
            dibujar_cubo(self.ax)
            lim = (-0.2, 1.2)
            
        elif self.estructura_actual == "BCC":
            posiciones = generar_celdilla_bcc()
            dibujar_cubo(self.ax)
            lim = (-0.2, 1.2)
            
        elif self.estructura_actual == "FCC":
            posiciones = generar_celdilla_fcc()
            dibujar_cubo(self.ax)
            lim = (-0.2, 1.2)
            
        elif self.estructura_actual == "HCP":
            posiciones = generar_celdilla_hcp()
            dibujar_prisma_hexagonal(self.ax)
            self.ax.set_xlim(-0.5, 2.5)
            self.ax.set_ylim(-1.5, 1.5)
            self.ax.set_zlim(-0.2, 2)
            lim = None
            
        elif self.estructura_actual == "DIAMANTE":
            posiciones = generar_celdilla_diamante()
            dibujar_cubo(self.ax, tamano=1)
            lim = (-0.2, 1.2)
            
        elif self.estructura_actual == "TETRAGONAL":
            posiciones = generar_celdilla_tetragonal()
            dibujar_caja_tetragonal(self.ax)
            self.ax.set_xlim(-0.2, 1.2)
            self.ax.set_ylim(-0.2, 1.2)
            self.ax.set_zlim(-0.2, 1.7)
            lim = None
            
        elif self.estructura_actual == "ORTORROMBICA":
            posiciones = generar_celdilla_ortorrombica()
            dibujar_caja_ortorrombica(self.ax)
            self.ax.set_xlim(-0.2, 1.2)
            self.ax.set_ylim(-0.2, 1.0)
            self.ax.set_zlim(-0.2, 1.4)
            lim = None
            
        elif self.estructura_actual == "HEXAGONAL":
            posiciones = generar_celdilla_hexagonal()
            dibujar_prisma_hexagonal(self.ax, altura=1.4)
            self.ax.set_xlim(-1.5, 1.5)
            self.ax.set_ylim(-1.5, 1.5)
            self.ax.set_zlim(-0.2, 1.6)
            lim = None
            
        elif self.estructura_actual == "ROMBOEDRICA":
            posiciones = generar_celdilla_romboedrica()
            # Estructura romboédrica tiene geometría más compleja
            lim = (-0.2, 1.5)
        
        else:
            posiciones = generar_celdilla_sc()
            dibujar_cubo(self.ax)
            lim = (-0.2, 1.2)
        
        # Dibujar átomos
        self.ax.scatter(posiciones[:, 0], posiciones[:, 1], posiciones[:, 2],
                       c='red', s=150, alpha=0.8, edgecolors='darkred', linewidth=1.5)
        
        # Configurar ejes
        if lim:
            self.ax.set_xlim(lim)
            self.ax.set_ylim(lim)
            self.ax.set_zlim(lim)
        
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        # Título con información del elemento
        if self.elemento_actual and self.elemento_actual in ELEMENTOS:
            simbolo, nombre = ELEMENTOS[self.elemento_actual]
            estructura_real = ESTRUCTURA_CRISTALINA.get(self.elemento_actual, "No definida")
            titulo = f"{simbolo} - {nombre}\nEstructura: {self.estructura_actual}"
            if estructura_real != self.estructura_actual:
                titulo += f"\n(Estructura real: {estructura_real})"
        else:
            titulo = f"Celdilla Unitaria: {self.estructura_actual}"
        
        self.ax.set_title(titulo, fontsize=10, weight='bold')
        
        # Actualizar canvas
        self.canvas.draw()


# ======================================================================
# INTERFAZ GTK PRINCIPAL
# ======================================================================

class ConfiguracionElectronicaApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Configuración Electrónica y Estructura Cristalina")
        self.set_border_width(10)
        self.set_default_size(1000, 700)

        # Contenedor principal horizontal
        hbox_principal = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(hbox_principal)

        # ===== PANEL IZQUIERDO: Configuración Electrónica =====
        vbox_izq = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        hbox_principal.pack_start(vbox_izq, False, False, 0)

        # Entrada de símbolo
        hbox_entry = Gtk.Box(spacing=8)
        vbox_izq.pack_start(hbox_entry, False, False, 0)

        label = Gtk.Label(label="Símbolo del elemento:")
        hbox_entry.pack_start(label, False, False, 0)

        self.entry_simbolo = Gtk.Entry()
        hbox_entry.pack_start(self.entry_simbolo, True, True, 0)

        # Checkbox Semiconductores
        self.check_semic = Gtk.CheckButton(label="Destacar elementos semiconductores")
        self.check_semic.connect("toggled", self.actualizar_combo)
        vbox_izq.pack_start(self.check_semic, False, False, 0)

        # Justificación breve
        self.justif = Gtk.Label(
            label="Incluye: Si, Ge, B, P y elementos III-V\n(Ga, As, In, Sb) usados en semiconductores."
        )
        self.justif.set_line_wrap(True)
        vbox_izq.pack_start(self.justif, False, False, 0)

        # Lista desplegable
        hbox_combo = Gtk.Box(spacing=8)
        vbox_izq.pack_start(hbox_combo, False, False, 0)

        label_combo = Gtk.Label(label="Selecciona un elemento:")
        hbox_combo.pack_start(label_combo, False, False, 0)

        self.combo = Gtk.ComboBoxText()
        self.actualizar_combo()
        hbox_combo.pack_start(self.combo, True, True, 0)

        # Botón Calcular
        self.button = Gtk.Button(label="Calcular y Mostrar Estructura")
        self.button.connect("clicked", self.on_calcular_clicked)
        vbox_izq.pack_start(self.button, False, False, 0)

        # Resultado
        self.result_label = Gtk.Label()
        self.result_label.set_line_wrap(True)
        self.result_label.set_selectable(True)
        self.result_label.set_max_width_chars(40)
        vbox_izq.pack_start(self.result_label, True, True, 0)

        # Nota de excepciones
        self.excepcion_label = Gtk.Label()
        self.excepcion_label.set_line_wrap(True)
        self.excepcion_label.set_use_markup(True)
        self.excepcion_label.set_max_width_chars(40)
        vbox_izq.pack_start(self.excepcion_label, False, False, 0)

        # ===== PANEL DERECHO: Visor 3D =====
        vbox_der = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        hbox_principal.pack_start(vbox_der, True, True, 0)

        # Título del visor
        label_visor = Gtk.Label()
        label_visor.set_markup("<b>Visor de Celdilla Unitaria</b>")
        vbox_der.pack_start(label_visor, False, False, 0)

        # Widget del visor 3D
        self.visor = VisorCeldillaUnitaria()
        vbox_der.pack_start(self.visor, True, True, 0)
        
        # Instrucciones
        instrucciones = Gtk.Label()
        instrucciones.set_markup(
            "<i>Usa el ratón para rotar la estructura:\n"
            "• Botón izquierdo: rotar\n"
            "• Botón derecho: zoom\n"
            "• Botón central: mover</i>"
        )
        instrucciones.set_line_wrap(True)
        vbox_der.pack_start(instrucciones, False, False, 0)

    def on_calcular_clicked(self, widget):
        simbolo = self.entry_simbolo.get_text().strip()

        # Si no se escribió nada, usar selección
        if not simbolo:
            combo_text = self.combo.get_active_text()
            if combo_text and combo_text != "":
                simbolo = combo_text.split(" - ")[0]

        if simbolo in SIMBOLO_A_Z:
            z = SIMBOLO_A_Z[simbolo]
            simbolo_real, nombre = ELEMENTOS[z]
            config, es_excepcion = calcular_configuracion_electronica(z)

            texto = f"<b>{simbolo_real} ({nombre})</b>\nNúmero atómico: {z}\nConfiguración:\n{config}\n"

            # Agregar información de estructura cristalina
            if z in ESTRUCTURA_CRISTALINA:
                estructura = ESTRUCTURA_CRISTALINA[z]
                nombres_estructura = {
                    "SC": "Cúbica Simple",
                    "BCC": "Cúbica Centrada en el Cuerpo",
                    "FCC": "Cúbica Centrada en las Caras",
                    "HCP": "Hexagonal Compacta",
                    "DIAMANTE": "Diamante (Si, Ge, C)",
                    "TETRAGONAL": "Tetragonal",
                    "ORTORROMBICA": "Ortorrómbica",
                    "HEXAGONAL": "Hexagonal Simple",
                    "ROMBOEDRICA": "Romboédrica"
                }
                texto += f"\n<b>Estructura cristalina:</b> {nombres_estructura.get(estructura, estructura)}\n"
            else:
                texto += f"\n<span foreground='orange'>Estructura cristalina no definida</span>\n"

            dens = DENSIDAD.get(z, "Densidad no disponible")
            if dens == "Densidad no disponible":
                texto += f"<span foreground='red'>Densidad no disponible</span>\n"
            else:
                texto += f"Densidad: {dens}\n"

            radio = RADIO.get(z, "Radio atómico no disponible")
            if radio == "Radio atómico no disponible":
                texto += f"<span foreground='red'>Radio atómico no disponible</span>"
            else:
                texto += f"Radio atómico (vdW): {radio}"

            self.result_label.set_markup(texto)

            if es_excepcion:
                self.excepcion_label.set_markup(
                    "<span foreground='blue'><i>⚠ Configuración electrónica especial debido a estabilidad de subniveles.</i></span>"
                )
            else:
                self.excepcion_label.set_markup("")
            
            # Actualizar el visor 3D
            self.visor.actualizar_elemento(z)
            
        else:
            self.result_label.set_markup(
                f"<span foreground='red'>El elemento '{simbolo}' no existe en la tabla.</span>"
            )
            self.excepcion_label.set_markup("")

    def actualizar_combo(self, *args):
        self.combo.remove_all()
        self.combo.append_text("")

        if self.check_semic.get_active():
            zs = sorted(list(SEMICONDUCTORES_INDUSTRIA))
        else:
            zs = range(1, 119)

        for z in zs:
            simbolo, nombre = ELEMENTOS[z]
            self.combo.append_text(f"{simbolo} - {nombre}")

        self.combo.set_active(0)


if __name__ == "__main__":
    app = ConfiguracionElectronicaApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
