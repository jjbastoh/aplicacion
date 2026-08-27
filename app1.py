import streamlit as st
import cv2
import numpy as np
import pytesseract
import base64

# -----------------------------------
# CONFIGURACIÓN
# -----------------------------------

st.set_page_config(
    page_title="OCR Inteligente",
    page_icon="📷",
    layout="centered"
)

st.title("📷 OCR Inteligente")
st.write("Toma una foto y convierte automáticamente la imagen en texto.")

# -----------------------------------
# BARRA LATERAL
# -----------------------------------

with st.sidebar:
    st.header("⚙️ Configuración")

    filtro = st.radio(
        "Aplicar filtro",
        ("Con Filtro", "Sin Filtro")
    )

    idioma = st.selectbox(
        "Idioma del texto",
        ("Español", "Inglés")
    )

# -----------------------------------
# CÁMARA
# -----------------------------------

img_file_buffer = st.camera_input("📸 Toma una foto")

# -----------------------------------
# PROCESAMIENTO
# -----------------------------------

if img_file_buffer is not None:

    # Leer imagen
    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8),
        cv2.IMREAD_COLOR
    )

    # -----------------------------------
    # APLICAR FILTRO
    # -----------------------------------

    if filtro == "Con Filtro":

        # Convertir a escala de grises
        gray = cv2.cvtColor(
            cv2_img,
            cv2.COLOR_BGR2GRAY
        )

        # Reducir ruido
        gray = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

        # Convertir a blanco y negro
        cv2_img = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        imagen_mostrar = cv2_img

    else:

        imagen_mostrar = cv2.cvtColor(
            cv2_img,
            cv2.COLOR_BGR2RGB
        )

    # -----------------------------------
    # MOSTRAR IMAGEN
    # -----------------------------------

    st.subheader("🖼️ Imagen procesada")

    st.image(
        imagen_mostrar,
        caption="Imagen utilizada para el OCR",
        use_container_width=True
    )

    # -----------------------------------
    # OCR
    # -----------------------------------

    if idioma == "Español":
        idioma_tesseract = "spa"
    else:
        idioma_tesseract = "eng"

    try:

        text = pytesseract.image_to_string(
            imagen_mostrar,
            lang=idioma_tesseract
        )

    except Exception as e:

        st.error("No se pudo ejecutar Tesseract.")
        st.error(e)
        text = ""

    # -----------------------------------
    # RESULTADO
    # -----------------------------------

    st.subheader("📝 Texto reconocido")

    if text.strip():

        st.text_area(
            "Resultado:",
            text,
            height=200
        )

        # -----------------------------------
        # ESTADÍSTICAS
        # -----------------------------------

        palabras = text.split()
        caracteres = len(text)
        lineas = len(text.splitlines())

        st.subheader("📊 Estadísticas")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Palabras",
                len(palabras)
            )

        with col2:
            st.metric(
                "Caracteres",
                caracteres
            )

        with col3:
            st.metric(
                "Líneas",
                lineas
            )

        # -----------------------------------
        # DESCARGAR TEXTO
        # -----------------------------------

        st.subheader("💾 Guardar resultado")

        st.download_button(
            label="📥 Descargar texto",
            data=text,
            file_name="texto_reconocido.txt",
            mime="text/plain"
        )

        # -----------------------------------
        # LEER TEXTO EN VOZ ALTA
        # -----------------------------------

        st.subheader("🔊 Escuchar texto")

        texto_voz = text.replace("\n", " ")

        texto_voz = texto_voz.replace(
            "'",
            "\\'"
        )

        html_audio = f"""
        <script>
        function hablar() {{
            var texto = '{texto_voz}';

            var mensaje = new SpeechSynthesisUtterance(texto);

            mensaje.lang = 'es-ES';

            window.speechSynthesis.speak(mensaje);
        }}
        </script>

        <button onclick="hablar()"
        style="
        background-color:#ff4b4b;
        color:white;
        border:none;
        padding:10px 20px;
        border-radius:8px;
        cursor:pointer;
        font-size:16px;
        ">
        🔊 Leer texto
        </button>
        """

        st.components.v1.html(
            html_audio,
            height=60
        )

    else:

        st.warning(
            "⚠️ No se encontró texto. "
            "Intenta tomar una foto con mejor iluminación."
        )

    


