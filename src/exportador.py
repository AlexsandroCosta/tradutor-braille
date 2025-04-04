import os
import fitz
from typing import Literal
from docx import Document

class Exportador:
    def __init__(self, codificacao: str = 'utf-8', tamanho_fonte_pdf: int = 12):
        self.codificacao = codificacao
        self.tamanho_fonte_pdf = tamanho_fonte_pdf

    def _verificar_caminho(self, caminho: str):
        """Valida se o caminho de saída é válido."""
        pasta = os.path.dirname(caminho)
        
        if pasta and not os.path.exists(pasta):
            raise ValueError(f'A pasta não existe: {pasta}')
        
    def exportar_txt(self, texto: str, caminho_saida: str):
        try:
            with open(caminho_saida, 'w', encoding=self.codificacao) as arquivo:
                arquivo.write(texto)
        except Exception as e:
            raise IOError(f'Erro ao exportar txt: {str(e)}')
        
    def exportar_pdf(self, texto: str, caminho_saida: str):
        try:
            pdf = fitz.open()
            pagina = pdf.new_page()

            pagina.insert_text(
                (50, 70),
                texto,
                fontsize = self.tamanho_fonte_pdf,
                fontname = 'helv',
                color = (0,0,0) # Cor preta (RGB)
            )

            pdf.save(caminho_saida)
            pdf.close()
        except Exception as e:
            raise IOError(f'Erro ao exportar PDF: {str(e)}')
        
    def exportar_docx(self, texto: str, caminho_saida: str):
        try:
            docx = Document()
            docx.add_paragraph(texto)
            docx.save(caminho_saida)
        except Exception as e:
            raise IOError(f'Erro ao exportar docx: {str(e)}')
        
    def exportar(self, texto: str, caminho_saida: str, formato: Literal['txt', 'docx', 'pdf']):
        """
        Exporta texto para um arquivo no formato especificado.
        
        Args:
            texto: Texto a ser exportado.
            caminho_saida: Caminho do arquivo de saída.
            formato: Formato de exportação (txt, docx, pdf).
        """

        self._verificar_caminho(caminho_saida)

        if formato == 'txt':
            self.exportar_txt(texto, caminho_saida)
        elif formato == 'pdf':
            self.exportar_pdf(texto, caminho_saida)
        elif formato == 'docx':
            self.exportar_docx(texto, caminho_saida)
        else:
            raise ValueError(f'Formato não suportado: {formato}')