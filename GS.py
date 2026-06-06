import os
 
 
modulos_disponiveis = ["Painel Solar A", "Painel Solar B", "Reator Auxiliar", "Bateria Principal"]
 
faixas_por_sensor = {
    "temperatura": {"NORMAL": (15, 40), "ATENÇÃO": (40, 60), "CRÍTICO": (60, 120)},
    "energia":     {"NORMAL": (60, 100), "ATENÇÃO": (30, 60), "CRÍTICO": (0,  30)},
    "comunicacao": {"NORMAL": (70, 100), "ATENÇÃO": (40, 70), "CRÍTICO": (0,  40)},
    "bateria":     {"NORMAL": (50, 100), "ATENÇÃO": (20, 50), "CRÍTICO": (0,  20)},
}
 
acoes_automatizadas = {
    "temperatura": {
        "ATENÇÃO": "Reduzindo carga nos painéis solares para dissipar calor.",
        "CRÍTICO": "Ativando sistema de resfriamento e isolando módulo térmico.",
    },
    "energia": {
        "ATENÇÃO": "Ajustando ângulo dos painéis para maximizar captação.",
        "CRÍTICO": "Desligando sistemas não essenciais. Ativando reserva de energia.",
    },
    "comunicacao": {
        "ATENÇÃO": "Realinhando antena direcional. Verificando interferências.",
        "CRÍTICO": "Alternando para canal de backup. Aguardando reconexão.",
    },
    "bateria": {
        "ATENÇÃO": "Limitando consumo. Iniciando ciclo de recarga.",
        "CRÍTICO": "Modo de sobrevivência ativado. Apenas sistemas vitais operando.",
    },
}
 
configuracao_sensores = {
    "temperatura": ("Temperatura",   "°C", 0,   120),
    "energia":     ("Energia Solar", "%",  0,   100),
    "comunicacao": ("Comunicação",   "%",  0,   100),
    "bateria":     ("Bateria",       "%",  0,   100),
}
 
pesos_saude = {
    "energia":     0.35,
    "bateria":     0.30,
    "comunicacao": 0.20,
    "temperatura": 0.15,
}
 
medicoes = []
 
 
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")
 
 
def exibir_cabecalho():
    print("=" * 60)
    print("          MONITORAMENTO DE SISTEMAS ENERGÉTICOS")
    print("=" * 60)
 
 
def pedir_numero(descricao, unidade, minimo, maximo):
    while True:
        entrada = input(f"  {descricao} ({unidade}) [{minimo}-{maximo}]: ").strip()
        try:
            valor = float(entrada)
        except ValueError:
            print("  Entrada inválida. Digite apenas números.")
            continue
        if valor < minimo or valor > maximo:
            print(f"  Valor fora do intervalo permitido ({minimo} a {maximo}).")
            continue
        return round(valor, 1)
 
 
def classificar_leitura(sensor, valor):
    for status in ("CRÍTICO", "ATENÇÃO", "NORMAL"):
        minimo, maximo = faixas_por_sensor[sensor][status]
        if minimo <= valor <= maximo:
            return status
    return "CRÍTICO"
 
 
def icone_status(status):
    icones = {"NORMAL": "[OK]", "ATENÇÃO": "[!!]", "CRÍTICO": "[XX]"}
    return icones[status]
 
 
def calcular_saude_missao(leituras):
    pontuacao_por_sensor = {
        "energia":     min(leituras["energia"], 100),
        "bateria":     min(leituras["bateria"], 100),
        "comunicacao": min(leituras["comunicacao"], 100),
        "temperatura": max(0, 100 - ((leituras["temperatura"] - 15) / 105) * 100),
    }
 
    score = round(sum(pontuacao_por_sensor[s] * pesos_saude[s] for s in pesos_saude), 1)
 
    if score >= 75:
        estado = "ESTÁVEL"
    elif score >= 45:
        estado = "EM RISCO"
    else:
        estado = "CRÍTICA"
 
    return score, estado
 
 
def montar_barra_saude(score):
    tamanho = 30
    preenchido = int((score / 100) * tamanho)
    barra = "#" * preenchido + "-" * (tamanho - preenchido)
    return f"[{barra}] {score:.1f}%"
 
 
def analisar_tendencias():
    if len(medicoes) < 2:
        return None
 
    ultimas_medicoes = medicoes[-3:] if len(medicoes) >= 3 else medicoes
 
    def calcular_variacao_media(sensor):
        valores = [medicao["leituras"][sensor] for medicao in ultimas_medicoes]
        variacoes = [valores[i+1] - valores[i] for i in range(len(valores) - 1)]
        return sum(variacoes) / len(variacoes)
 
    variacao_energia = calcular_variacao_media("energia")
    variacao_bateria = calcular_variacao_media("bateria")
 
    alertas_preditivos = []
 
    if variacao_energia < -5:
        projecao = max(round(medicoes[-1]["leituras"]["energia"] + variacao_energia * 2, 1), 0)
        alertas_preditivos.append(
            f"Energia solar em queda ({variacao_energia:+.1f}% por medição). "
            f"Projeção para próxima leitura: {projecao}%."
        )
 
    if variacao_bateria < -5:
        projecao = max(round(medicoes[-1]["leituras"]["bateria"] + variacao_bateria * 2, 1), 0)
        alertas_preditivos.append(
            f"Bateria em queda ({variacao_bateria:+.1f}% por medição). "
            f"Projeção para próxima leitura: {projecao}%."
        )
 
    if variacao_energia > 8 and medicoes[-1]["leituras"]["bateria"] < 80:
        alertas_preditivos.append(
            "Geração solar em alta. Recomendado redirecionar excedente para recarga da bateria."
        )
 
    return alertas_preditivos if alertas_preditivos else None
 
 
def gerar_sugestoes(leituras):
    sugestoes = []
 
    if leituras["energia"] < 60:
        sugestoes.append("Reposicionar painéis solares para aumentar captação de energia renovável.")
    if leituras["bateria"] < 50:
        sugestoes.append("Priorizar recarga da bateria durante períodos de alta irradiação solar.")
    if leituras["temperatura"] > 40:
        sugestoes.append("Redistribuir carga entre módulos para reduzir geração de calor residual.")
    if leituras["energia"] >= 80 and leituras["bateria"] < 80:
        sugestoes.append("Excedente de energia solar disponível — redirecionar para recarga da bateria.")
    if leituras["energia"] < 30 and leituras["bateria"] < 30:
        sugestoes.append("Reservas críticas: suspender operações não essenciais e aguardar janela solar.")
 
    return sugestoes
 
 
def coletar_leituras():
    limpar_tela()
    exibir_cabecalho()
    print("\n  Informe os dados atuais da missão:\n")
 
    leituras = {}
    for sensor, (nome, unidade, minimo, maximo) in configuracao_sensores.items():
        leituras[sensor] = pedir_numero(nome, unidade, minimo, maximo)
 
    print("\n  Módulo ativo:")
    for numero, nome_modulo in enumerate(modulos_disponiveis, 1):
        print(f"  [{numero}] {nome_modulo}")
 
    while True:
        entrada = input("  Opção: ").strip()
        try:
            indice = int(entrada) - 1
            if 0 <= indice < len(modulos_disponiveis):
                leituras["modulo"] = modulos_disponiveis[indice]
                break
        except ValueError:
            pass
        print("  Opção inválida.")
 
    return leituras
 
 
def mostrar_analise(leituras):
    limpar_tela()
    exibir_cabecalho()
    print(f"\n  Módulo: {leituras['modulo']}\n")
    print(f"  {'SENSOR':<20} {'VALOR':>10}  STATUS")
    print("  " + "-" * 44)
 
    status_por_sensor = {}
    sensores_com_problema = []
 
    for sensor, (nome, unidade, *_) in configuracao_sensores.items():
        valor = leituras[sensor]
        status = classificar_leitura(sensor, valor)
        status_por_sensor[sensor] = (valor, status)
        print(f"  {nome:<20} {valor:>7.1f}{unidade}  {icone_status(status)} {status}")
        if status != "NORMAL":
            sensores_com_problema.append((sensor, status))
 
    print("  " + "-" * 44)
 
    score, estado = calcular_saude_missao(leituras)
    print(f"\n  SAÚDE DA MISSÃO: {estado}")
    print(f"  {montar_barra_saude(score)}\n")
 
    if sensores_com_problema:
        print("  ALERTAS E RESPOSTAS AUTOMATIZADAS:\n")
        for sensor, status in sensores_com_problema:
            acao = acoes_automatizadas[sensor].get(status, "")
            nome_sensor = configuracao_sensores[sensor][0].upper()
            print(f"  {icone_status(status)} {nome_sensor} — {status}")
            if acao:
                print(f"     → {acao}")
            print()
    else:
        print("  Todos os sistemas dentro dos parâmetros normais.\n")
 
    medicoes.append({
        "leituras": leituras,
        "status_por_sensor": status_por_sensor,
        "score": score,
        "estado": estado,
    })
 
    tendencias = analisar_tendencias()
    if tendencias:
        print("  ANÁLISE PREDITIVA:\n")
        for alerta in tendencias:
            print(f"  [>>] {alerta}")
        print()
 
    sugestoes = gerar_sugestoes(leituras)
    if sugestoes:
        print("  SUGESTÕES DE SUSTENTABILIDADE:\n")
        for sugestao in sugestoes:
            print(f"  [*] {sugestao}")
        print()
 
    input("  ENTER para voltar ao menu...")
 
 
def mostrar_relatorio():
    limpar_tela()
    exibir_cabecalho()
    print(f"\n  RELATÓRIO GERAL DA MISSÃO\n")
 
    if not medicoes:
        print("  Nenhuma medição registrada ainda.")
        input("\n  ENTER para voltar...")
        return
 
    print(f"  Total de medições: {len(medicoes)}\n")
 
    media_por_sensor = {
        sensor: round(sum(m["leituras"][sensor] for m in medicoes) / len(medicoes), 1)
        for sensor in faixas_por_sensor
    }
 
    print(f"  {'SENSOR':<22} {'MÉDIA':>8}  STATUS")
    print("  " + "-" * 44)
    for sensor, (nome, unidade, *_) in configuracao_sensores.items():
        media = media_por_sensor[sensor]
        status = classificar_leitura(sensor, media)
        print(f"  {nome:<22} {media:>6.1f}{unidade}  {icone_status(status)} {status}")
 
    score_medio = round(sum(m["score"] for m in medicoes) / len(medicoes), 1)
    print(f"\n  Saúde média da missão : {montar_barra_saude(score_medio)}")
 
    total_alertas = sum(
        1 for medicao in medicoes
        for _, status in medicao["status_por_sensor"].values()
        if status != "NORMAL"
    )
    print(f"  Total de alertas      : {total_alertas}")
 
    melhor_medicao = max(medicoes, key=lambda m: m["score"])
    pior_medicao   = min(medicoes, key=lambda m: m["score"])
    print(f"\n  Melhor medição : {melhor_medicao['score']:.1f}% ({melhor_medicao['estado']}) — {melhor_medicao['leituras']['modulo']}")
    print(f"  Pior medição   : {pior_medicao['score']:.1f}% ({pior_medicao['estado']}) — {pior_medicao['leituras']['modulo']}")
 
    print()
    input("  ENTER para voltar ao menu...")
 
 
def main():
    while True:
        limpar_tela()
        exibir_cabecalho()
        print("""
  [1] Registrar monitoramento
  [2] Relatório geral
  [0] Encerrar
""")
        opcao = input("  Opção: ").strip()
 
        if opcao == "1":
            leituras = coletar_leituras()
            mostrar_analise(leituras)
        elif opcao == "2":
            mostrar_relatorio()
        elif opcao == "0":
            limpar_tela()
            print("\n  Sistema encerrado.\n")
            break
 
 
if __name__ == "__main__":
    main()