"""Lector y simulador minimo de archivos .jff de JFLAP (solo biblioteca estandar)."""

import itertools
import xml.etree.ElementTree as ET


class Automata:
    def __init__(self, ruta):
        raiz = ET.parse(ruta).getroot()
        self.tipo = raiz.findtext("type")
        self.expresion = raiz.findtext("expression")
        self.nombres, self.finales, self.inicial, self.delta = {}, set(), None, {}
        if self.tipo != "fa":
            return
        nodo = raiz.find("automaton")
        nodo = raiz if nodo is None else nodo
        for e in nodo.findall("state"):
            self.nombres[e.get("id")] = e.get("name")
            if e.find("initial") is not None:
                self.inicial = e.get("id")
            if e.find("final") is not None:
                self.finales.add(e.get("id"))
        for t in nodo.findall("transition"):
            clave = (t.findtext("from"), t.findtext("read") or "")
            self.delta.setdefault(clave, set()).add(t.findtext("to"))
        self.alfabeto = sorted({a for _, a in self.delta if a})

    def _cerradura(self, estados):
        vistos, pila = set(estados), list(estados)
        while pila:
            for n in self.delta.get((pila.pop(), ""), ()):
                if n not in vistos:
                    vistos.add(n)
                    pila.append(n)
        return vistos

    def acepta(self, w):
        actuales = self._cerradura({self.inicial})
        for c in w:
            actuales = self._cerradura(
                {n for q in actuales for n in self.delta.get((q, c), ())}
            )
        return bool(actuales & self.finales)

    def es_afd_total(self):
        return all(
            len(self.delta.get((q, a), ())) == 1
            for q in self.nombres
            for a in self.alfabeto
        ) and not any(a == "" for _, a in self.delta)

    def tabla(self):
        """Renglones (estado, marca, {simbolo: destinos}) en orden de id numerico."""
        filas = []
        for q in sorted(self.nombres, key=int):
            marca = ("→" if q == self.inicial else "") + ("∗" if q in self.finales else "")
            destinos = {
                a: sorted(self.nombres[d] for d in self.delta.get((q, a), ()))
                for a in self.alfabeto
            }
            filas.append((self.nombres[q], marca, destinos))
        return filas

    def prefijo_minimo(self):
        """Para cada estado, la cadena mas corta que lo alcanza (BFS sobre AFD)."""
        minimos, cola = {self.inicial: ""}, [self.inicial]
        while cola:
            q = cola.pop(0)
            for a in self.alfabeto:
                for n in sorted(self.delta.get((q, a), ())):
                    if n not in minimos:
                        minimos[n] = minimos[q] + a
                        cola.append(n)
        return {self.nombres[q]: w for q, w in minimos.items()}


def cadenas(alfabeto, longitud_max):
    for k in range(longitud_max + 1):
        for t in itertools.product(alfabeto, repeat=k):
            yield "".join(t)
