import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# --- Tabla periódica completa (Z: (símbolo, nombre)) ---
# Fuente: IUPAC actualizada (hasta Og 118)
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
    82: ("Pb", "Plomo"), 83: ("Bi", "Bismuto"), 84: ("Po", "Polonio"), 85: ("At", "Ástato"), 86: ("Rn", "Radón"), 87: ("Fr", "Francio"), 88: ("Ra", "Radio"), 89: ("Ac", "Actinio"),
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


# --- Interfaz GTK ---
class ConfiguracionElectronicaApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Configuración Electrónica - Tabla Completa")
        self.set_border_width(10)
        self.set_default_size(500, 300)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)

        # Entrada de símbolo
        hbox_entry = Gtk.Box(spacing=8)
        vbox.pack_start(hbox_entry, False, False, 0)

        label = Gtk.Label(label="Símbolo del elemento:")
        hbox_entry.pack_start(label, False, False, 0)

        self.entry_simbolo = Gtk.Entry()
        hbox_entry.pack_start(self.entry_simbolo, True, True, 0)

        # Checkbox Semiconductores
        self.check_semic = Gtk.CheckButton(label="Destacar elementos semiconductores (industria)")
        self.check_semic.connect("toggled", self.actualizar_combo)
        vbox.pack_start(self.check_semic, False, False, 0)

        # justificación breve
        self.justif = Gtk.Label(
            label="Incluye: Si, Ge, B, P y elementos III-V (Ga, As, In, Sb) usados en materiales compuestos (GaAs, GaN, InSb, etc)."
        )
        self.justif.set_line_wrap(True)
        vbox.pack_start(self.justif, False, False, 0)

        # Lista desplegable
        hbox_combo = Gtk.Box(spacing=8)
        vbox.pack_start(hbox_combo, False, False, 0)

        label_combo = Gtk.Label(label="O selecciona un elemento:")
        hbox_combo.pack_start(label_combo, False, False, 0)

        self.combo = Gtk.ComboBoxText()
        self.actualizar_combo()

        hbox_combo.pack_start(self.combo, True, True, 0)

        # Botón Calcular
        self.button = Gtk.Button(label="Calcular")
        self.button.connect("clicked", self.on_calcular_clicked)
        vbox.pack_start(self.button, False, False, 0)

        # Resultado
        self.result_label = Gtk.Label()
        self.result_label.set_line_wrap(True)
        self.result_label.set_selectable(True)
        vbox.pack_start(self.result_label, True, True, 0)

        # Nota de excepciones
        self.excepcion_label = Gtk.Label()
        self.excepcion_label.set_line_wrap(True)
        self.excepcion_label.set_use_markup(True)
        vbox.pack_start(self.excepcion_label, False, False, 0)

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

            self.result_label.set_markup(
                f"<b>{simbolo_real} ({nombre})</b>\nNúmero atómico: {z}\nConfiguración:\n{config}"
            )

            if es_excepcion:
                self.excepcion_label.set_markup(
                    "<span foreground='blue'><i>⚠ Configuración electrónica especial debido a estabilidad de subniveles (excepción conocida).</i></span>"
                )
            else:
                self.excepcion_label.set_markup("")
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
