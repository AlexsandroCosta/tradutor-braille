from pathlib import Path
from docx import Document
from typing import Literal
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DejaVuSans', 'fontes/DejaVuSans.ttf'))

class Exportador:
    def __init__(self, codificacao: str = 'utf-8', tamanho_fonte_pdf: int = 12):
        self.codificacao = codificacao
        self.tamanho_fonte_pdf = tamanho_fonte_pdf

    def _verificar_caminho(self, caminho: str):
        """Valida se o caminho de saída é válido."""
        caminho_arquivo = Path(caminho)
        
        if caminho_arquivo.exists():
            raise ValueError(f'Já existe um arquivo com esse mesmo nome e extensão: {caminho_arquivo}')
        
    def exportar_txt(self, texto: str, caminho_saida: str):
        try:
            with open(caminho_saida, 'w', encoding=self.codificacao) as arquivo:
                arquivo.write(texto)
        except Exception as e:
            raise IOError(f'Erro ao exportar txt: {str(e)}')
        
    def exportar_pdf(self, texto: str, caminho_saida: str):
        try:
            c = canvas.Canvas(str(caminho_saida), pagesize=A4)
            c.setFont('DejaVuSans', 12)
            
            _, altura = A4

            x = 50
            y = altura - 50
            for linha in texto.split('\n'):
                c.drawString(x, y, linha)
                y -= 15

                if y < 50:
                    c.showPage()
                    y = altura - 50

            c.save()
        except Exception as e:
            raise IOError(f'Erro ao exportar PDF: {str(e)}')
        
    def exportar_docx(self, texto: str, caminho_saida: str):
        try:
            docx = Document()
            docx.add_paragraph(texto)
            docx.save(caminho_saida)
        except Exception as e:
            raise IOError(f'Erro ao exportar docx: {str(e)}')
        
    def exportar(self, texto: str, nome_arquivo: str, formato: Literal['txt', 'docx', 'pdf']):
        """
        Exporta texto para um arquivo no formato especificado.
        """
        if not (formato in ['txt', 'docx', 'pdf']):
            raise ValueError(f'Formato não suportado: {formato}')
        
        caminho_saida = Path('media/exportacoes')
        caminho_saida.mkdir(parents=True, exist_ok=True)

        caminho_saida = f'{caminho_saida}/{nome_arquivo}.{formato}'

        self._verificar_caminho(caminho_saida)

        if formato == 'txt':
            self.exportar_txt(texto, caminho_saida)
        elif formato == 'pdf':
            self.exportar_pdf(texto, caminho_saida)
        else:
            self.exportar_docx(texto, caminho_saida)