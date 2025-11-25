nome = "anônimo"
recordes = [0, 300]
usuNovo = True
arq = "recordes.txt"

def salvar():
    if usuNovo:
        with open(arq, "a") as recs:
            recs.write("\n")
            recs.write(f"Nome: {nome}\n")
            recs.write(f"Recordes: {recordes[0]}|{recordes[1]}\n")
            recs.write("\n")
    else:
        jogs = []
        with open(arq) as recs:
            for linha in recs:
                n = linha.replace("Nome: ", "").replace("\n", "")
                r = [int(v) for v in recs.readline().replace("Recordes: ", "").replace("\n", "").split("|")]
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
        for prim in recs:
            n = prim.replace("Nome: ", "").replace("\n", "")
            r = recs.readline().replace("Recordes: ", "").replace("\n", "").split("|")
            print(n)
            if n == nick:
                nome = n
                recordes = r
                if recordes[0].isdigit(): recordes[0] = int(recordes[0])
                if recordes[1].isdigit(): recordes[1] = int(recordes[1])
                usuNovo = False
                break
        else:
            nome = nick

def pegaRecordes():
    rec1 = []
    rec2 = []

    with open(arq) as recs:
        for pessoa in recs.read().split("\n\n"):
            n = pessoa.split("\n")[0].replace("Nome: ", "")
            r = [int(v) for v in pessoa.split("\n")[1].replace("Recordes: ", "").split("|")]

            #Coloca o recorde na primeira lista
            for i, j in enumerate(rec1):
                if j["reco"] < r[0]:
                    rec1.insert(i, {"nome": n, "reco": r[0]})
                    break
            else:
                rec1.append({"nome": n, "reco": r[0]})

            #Coloca o recorde na segunda lista
            for i, j in enumerate(rec2):
                if j["reco"] > r[1]:
                    rec2.insert(i, {"nome": n, "reco": r[1]})
                    break
            else:
                rec2.append({"nome": n, "reco": r[1]})

    return rec1, rec2