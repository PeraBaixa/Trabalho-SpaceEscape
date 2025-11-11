nome = "anônimo"
recordes = ["-", "-"]
usuNovo = True

def mudarNome(novNome):
    global nome
    if novNome != "anônimo":
        nome = novNome
    else:
        return False

def salvar():
    pass

def achaJog(nick):
    global nome, recordes, usuNovo

    with open("recordes.txt") as arquivo:
        while True:
            n = arquivo.readline().replace("Nome: ", "").replace.("\n", "")
            r = arquivo.readline().replace("Nome: ", "").replace.("\n", "").split("|")
            if n == nick:
                nome = n
                recordes = r
                if recordes[0].isdigit(): recordes[0] = int(recordes[0])
                if recordes[1].isdigit(): recordes[1] = int(recordes[1])
                usuNovo = False
                break