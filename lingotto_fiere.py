from csv import reader

class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = superficie
        self.padiglione = padiglione
        self.prezzo_base = prezzo_base
        self.tipo = "Standard"
        self.disponibile = True
        self.espositore = None

    def calcola_prezzo(self):
        return self.prezzo_base

    def __str__(self):
        if self.disponibile:
            stato = "Disponibile"
        else:
            stato = f"Assegnato a {self.espositore.codice} - {self.espositore.nome} {self.espositore.cognome}"

        return (
            f"{self.codice}: {self.tipo} | {self.superficie} mq - Padiglione {self.padiglione} - "
            f"Prezzo {self.calcola_prezzo():.2f} euro - {stato}"
        )

class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, numero_prese):
        # Uso super() per inizializzare gli attributi comuni a tutti gli stand
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.tipo = "Prese Extra"
        self.numero_prese = numero_prese

    def calcola_prezzo(self):
        return self.prezzo_base * (1 + 0.07 * self.numero_prese)

    def __str__(self):
        return super().__str__() + f" - Prese aggiuntive: {self.numero_prese}"

class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __str__(self):
        if self.stand is None:
            return f"{self.codice} - {self.nome} {self.cognome} - Nessuno stand assegnato"

        return f"{self.codice} - {self.nome} {self.cognome} - Stand {self.stand.codice}"

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        # TODO

    """Aggiungere setter e getter se necessari"""
    # TODO

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        # TODO

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        # TODO

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        # TODO

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        # TODO
