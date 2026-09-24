import streamlit as st
import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import fitz  # Importa a biblioteca PyMuPDF

# Configuração inicial da página
st.set_page_config(
    page_title="PDF Advanced Suite",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILIZAÇÃO CSS (Cards Visuais com Efeito Hover) ---
st.markdown("""
<style>
    .card-container {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 15px;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card-container:hover {
        transform: translateY(-4px);
        box-shadow: 4px 4px 18px rgba(0,0,0,0.08);
        border-color: #ff4b4b;
    }
    .card-icon {
        font-size: 50px;
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 20px;
        font-weight: bold;
        color: #262730;
        margin-bottom: 10px;
    }
    .card-text {
        font-size: 14px;
        color: #555555;
        line-height: 1.4;
    }
    /* Estilização para o botão de popover parecer um botão de ação destacado */
    .stPopover button {
        width: 100% !important;
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px !important;
        font-weight: bold !important;
    }
    .stPopover button:hover {
        background-color: #e04141 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS FOR PDF LOGIC ---

def parse_range(range_str, max_pages):
    """Converte strings como '1-3, 5' numa lista de índices de páginas (0-indexed)"""
    pages = set()
    for part in range_str.split(','):
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                # Garante que está dentro dos limites do PDF
                start = max(1, min(start, max_pages))
                end = max(1, min(end, max_pages))
                pages.update(range(start - 1, end))
            except ValueError:
                pass
        else:
            try:
                p = int(part)
                if 1 <= p <= max_pages:
                    pages.add(p - 1)
            except ValueError:
                pass
    return sorted(list(pages))


# --- CORPO DA APLICAÇÃO ---
st.title("🧰 PDF Advanced Suite")
st.subheader("Ferramentas rápidas de manipulação e transformação de documentos")
st.write("---")

# Layout em Grelha (2x2) para as 4 ferramentas
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# --- 1. MERGE DE PDFs ---
with row1_col1:
    st.markdown("""
    <div class="card-container">
        <div class="card-icon">🔀</div>
        <div class="card-title">Merge / Juntar PDFs</div>
        <div class="card-text">Combine múltiplos ficheiros PDF numa única e ordenada sequência de documentos.</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.popover("Abrir Ferramenta: Juntar PDFs", use_container_width=True):
        st.markdown("### 🔀 Unir Ficheiros PDF")
        uploaded_files = st.file_uploader("Selecione dois ou mais PDFs", type=["pdf"], accept_multiple_files=True, key="pop_merge")
        if uploaded_files and len(uploaded_files) >= 2:
            st.write(f"📂 {len(uploaded_files)} ficheiros carregados.")
            if st.button("Processar e Unir", key="exec_merge"):
                with st.spinner("A juntar ficheiros..."):
                    
                    # CORREÇÃO AQUI: Usar PdfWriter() em vez de PdfMerger()
                    merger = PdfWriter() 
                    
                    for file in uploaded_files:
                        merger.append(file)
                    
                    output_pdf = io.BytesIO()
                    merger.write(output_pdf)
                    merger.close()
                    output_pdf.seek(0)
                    
                    st.success("PDFs combinados com sucesso!")
                    st.download_button(
                        label="📥 Descarregar PDF Unido",
                        data=output_pdf,
                        file_name="pdf_unido.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        elif uploaded_files:
            st.warning("Por favor, selecione pelo menos 2 ficheiros para efetuar a junção.")


# --- 2. RETIRAR PÁGINAS ---
with row1_col2:
    st.markdown("""
    <div class="card-container">
        <div class="card-icon">✂️</div>
        <div class="card-title">Retirar Páginas</div>
        <div class="card-text">Remova ou extraia intervalos específicos de páginas do seu documento original.</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.popover("Abrir Ferramenta: Retirar Páginas", use_container_width=True):
        st.markdown("### ✂️ Extrair / Remover Páginas")
        uploaded_file = st.file_uploader("Carregue o PDF original", type=["pdf"], key="pop_split")
        if uploaded_file:
            
            reader = PdfReader(uploaded_file)
            total_pages = len(reader.pages)
            st.info(f"O documento carregado tem {total_pages} páginas.")

            pages_to_keep = st.text_input("Indique as páginas a manter (ex: 1-3, 5, 7-9)", placeholder=f"1-{total_pages}")

            if st.button("Cortar e Extrair", key="exec_split"):
                if pages_to_keep:
                    with st.spinner("A processar páginas..."):
                        writer = PdfWriter()
                        target_pages = parse_range(pages_to_keep, total_pages)
                        
                        if target_pages:
                            for page_num in target_pages:
                                writer.add_page(reader.pages[page_num])
                            
                            output_pdf = io.BytesIO()
                            writer.write(output_pdf)
                            writer.close()
                            output_pdf.seek(0)
                            
                            st.success(f"Extração concluída! {len(target_pages)} páginas extraídas.")
                            st.download_button(
                                label="📥 Descarregar PDF Cortado",
                                data=output_pdf,
                                file_name="pdf_extraido.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        else:
                            st.error("Nenhuma página válida encontrada no intervalo introduzido.")
                else:
                    st.error("Por favor, preencha o campo com as páginas desejadas.")


# --- 3. NUMERAR PDFs ---
with row2_col1:
    st.markdown("""
    <div class="card-container">
        <div class="card-icon">🔢</div>
        <div class="card-title">Numerar Páginas</div>
        <div class="card-text">Adicione paginação automática (ex: Página 1 de X) no rodapé ou cabeçalho do PDF.</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.popover("Abrir Ferramenta: Numerar PDF", use_container_width=True):
        st.markdown("### 🔢 Adicionar Numeração")
        uploaded_file = st.file_uploader("Carregue o PDF", type=["pdf"], key="pop_number")
        if uploaded_file:
            reader = PdfReader(uploaded_file)
            total_pages = len(reader.pages)

            position = st.selectbox("Posição do Número", ["Rodapé Direito", "Rodapé Centro"])
            start_page = st.number_input("Começar a numeração a partir da página física:", min_value=1, max_value=total_pages, value=1)

            if st.button("Aplicar Numeração", key="exec_number"):
                with st.spinner("A aplicar numeração..."):
                    writer = PdfWriter()
                    
                    for idx, page in enumerate(reader.pages):
                        if idx + 1 >= start_page:
                            # Cria uma folha PDF temporária com o ReportLab para desenhar o texto do número
                            packet = io.BytesIO()
                            can = canvas.Canvas(packet, pagesize=(page.mediabox.width, page.mediabox.height))
                            can.setFont("Helvetica", 9)
                            
                            text = f"Página {idx + 1} de {total_pages}"
                            
                            # Define coordenadas com base na opção selecionada
                            if position == "Rodapé Centro":
                                x_pos = float(page.mediabox.width) / 2
                                can.drawCentredString(x_pos, 30, text)
                            else: # Rodapé Direito
                                x_pos = float(page.mediabox.width) - 50
                                can.drawRightString(x_pos, 30, text)
                                
                            can.save()
                            packet.seek(0)
                            
                            # Funde o texto gerado por cima da página atual do PDF original
                            number_pdf = PdfReader(packet)
                            page.merge_page(number_pdf.pages[0])
                        
                        writer.add_page(page)
                    
                    output_pdf = io.BytesIO()
                    writer.write(output_pdf)
                    writer.close()
                    output_pdf.seek(0)
                    
                    st.success("Numeração de páginas aplicada!")
                    st.download_button(
                        label="📥 Descarregar PDF Numerado",
                        data=output_pdf,
                        file_name="pdf_numerado.pdf",
                        mime="application/pdf",
                        use_container_width=True)

# --- 4. COMPRIMIR PDF ---
with row2_col2:
    st.markdown("""
    <div class="card-container">
        <div class="card-icon">📉</div>
        <div class="card-title">Comprimir PDF</div>
        <div class="card-text">Reduza o tamanho do ficheiro removendo metadados redundantes e otimizando streams de dados do PDF.</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.popover("Abrir Ferramenta: Comprimir", use_container_width=True):
        st.markdown("### 📉 Reduzir Tamanho do PDF")
        uploaded_file = st.file_uploader("Carregue o PDF pesado", type=["pdf"], key="pop_compress")
        if uploaded_file:
            compression_level = st.select_slider(
                "Nível de Compressão (Atenção: diminui a qualidade visual)",
                options=["Baixa (Melhor Qualidade)", "Média", "Alta (Ficheiro Mais Leve)"],
                value="Média"
            )
            
            if st.button("Executar Compressão", key="exec_compress"):
                with st.spinner("A processar imagens e a comprimir..."):
                    try:
                        # Ler os bytes do ficheiro carregado pelo Streamlit
                        pdf_bytes = uploaded_file.read()
                        
                        # Abrir o PDF a partir da memória usando PyMuPDF
                        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                        
                        # Criar um buffer em memória para guardar o resultado
                        output_buffer = io.BytesIO()
                        
                        # Mapear a seleção do slider para os parâmetros corretos de compressão
                        if compression_level == "Baixa (Melhor Qualidade)":
                            # Apenas otimização de estrutura e limpeza de objetos duplicados
                            doc.save(output_buffer, garbage=3, deflate=True)
                        
                        elif compression_level == "Média":
                            # Comprime imagens reduzindo a sua qualidade com compressão JPEG estruturada
                            doc.save(
                                output_buffer, 
                                garbage=4, 
                                deflate=True, 
                                linear=True, 
                                expand_images=True
                            )
                        
                        else:  # Alta (Ficheiro Mais Leve)
                            # Aplica compressão máxima forçando a linearização do documento
                            doc.save(
                                output_buffer, 
                                garbage=4, 
                                deflate=True, 
                                clean=True, 
                                deflate_images=True
                            )
                        
                        compressed_data = output_buffer.getvalue()
                        doc.close()
                        output_buffer.close()
                        
                        st.success(f"Compressão concluída com sucesso no nível: {compression_level}!")
                        st.download_button(
                            label="📥 Descarregar PDF Comprimido",
                            data=compressed_data,
                            file_name="pdf_comprimido.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Erro ao processar a compressão: {str(e)}")

st.write("---")
st.caption("💡 Dica: Ao clicar em qualquer um dos botões, abre-se uma janela pop-up contextual para submeter os ficheiros.")
