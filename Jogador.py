nome = "anônimo"
recordes = ["-", "-"]
usuNovo = True
arq = "recordes.txt"

def mudarNome(novNome):
    global nome
    if novNome != "anônimo":
        nome = novNome
    else:
        return False

def salvar():
    if usuNovo:
        with open(arq, "a") as recs:
            recs.write(f"Nome: {nome}\n")
            recs.write(f"Recordes: {recordes[0]}|{recordes[1]}\n")
            recs.write("\n")
    else:
        jogs = []
        with open(arq) as recs:
            for linha in recs:
                n = linha.replace("Nome: ", "").replace("\n", "")
                r = recs.readline().replace("Recordes: ", "").replace("\n", "").split("|")
                if r[0].isdigit(): r[0] = int(r[0])
                if r[1].isdigit(): r[1] = int(r[1])
                jogs.append({"Nome": n, "Recordes": r})
                recs.readline()

        for j in jogs:
            if j["Nome"] == nome:
                j["Recordes"] = recordes
                break

        with open(arq, "w") as recs:
            for j in jogs:
                recs.write(f"Nome: {j['Nome']}\n")
                recs.write(f"Recordes: {j['Recordes'][0]}|{j['Recordes'][1]}\n")
                recs.write("\n")


def achaJog(nick):
    global nome, recordes, usuNovo

    with open(arq) as recs:
        for _ in recs:
            n = recs.readline().replace("Nome: ", "").replace("\n", "")
            r = recs.readline().replace("Recordes: ", "").replace("\n", "").split("|")
            if n == nick:
                nome = n
                recordes = r
                if recordes[0].isdigit(): recordes[0] = int(recordes[0])
                if recordes[1].isdigit(): recordes[1] = int(recordes[1])
                usuNovo = False
                break
        else:
            nome = nick