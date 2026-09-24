class jogo:
    def __init__(self, nome, estilo, plataforma):
        self.nome = nome
        self.estilo = estilo
        self.plataforma = plataforma
        self.horasjogadas = 0.0
        self.status = "NÃO INICIADO"

    def jogar(self, horas):
        self.horasjogadas += horas
        self.status = "JOGANDO"
        print(f"O jogo {self.nome} foi jogado por {horas}.\nTotal de horas jogadas: {self.horasjogadas} h")

# testando a classe jogo:

primeiroteste = jogo("Pacman","2d","pc")

print(primeiroteste.nome)
print(primeiroteste.estilo)
print(primeiroteste.plataforma)
        
primeiroteste.jogar(2)
primeiroteste.jogar(4)
        