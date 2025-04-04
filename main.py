from src.processamento_imagem import ProcessadorImagem
from src.tradutor_texto import TradutoTexto
from src.exportador import Exportador

if __name__ == "__main__":
 
    # for i in range(1, 12):
    #     processador = ProcessadorImagem(f'{i}.jpg')

    #     processador.mostrar_resultados()

    trautor_texto = TradutoTexto('teste.docx')
    exportador = Exportador()

    exportador.exportar(trautor_texto.traducao_braille, 'teste.pdf', 'pdf')
