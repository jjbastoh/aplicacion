import streamlit as st
import cv2
import numpy as np
import pytesseract

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="OCR Inteligente",
    page_icon="📷",
    layout="centered"
)

# ==========================================
# TÍTULO
# ==========================================

st.title("📷 OCR Inteligente")
st.subheader("Reconocimiento de texto en imágenes")

st.write(
    "Carga una imagen desde tu computador o toma una fotografía "
    "para reconocer automáticamente el texto."
)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("⚙️ Configuración")

    st.subheader("🎨 Procesamiento")

    filtro = st.radio(
        "Selecciona el tipo de imagen:",
        ["Sin filtro", "Escala de grises", "Blanco y negro"]
    )

    st.subheader("🌎 Idioma")

    idioma = st.selectbox(
        "Idioma del texto:",
        ["Español", "Inglés"]
    )

# ==========================================
# SELECCIÓN DE IMAGEN
# ==========================================

st.header("📁 Seleccionar imagen")

opcion = st.radio(
    "¿Cómo quieres ingresar la imagen?",
    ["📂 Cargar desde el PC", "📷 Tomar una foto"],
    horizontal=True
)

img_file_buffer = None

if opcion == "📂 Cargar desde el PC":

    img_file_buffer = st.file_uploader(
        "Selecciona una imagen",
        type=["jpg", "jpeg", "png"]
    )

else:

    img_file_buffer = st.camera_input(
        "Toma una fotografía"
    )

# ==========================================
# PROCESAMIENTO
# ==========================================

if img_file_buffer is not None:

    # Leer archivo
    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8),
        cv2.IMREAD_COLOR
    )

    # ==========================================
    # MOSTRAR IMAGEN ORIGINAL
    # ==========================================

    st.header("🖼️ Imagen original")

    imagen_original = cv2.cvtColor(
        cv2_img,
        cv2.COLOR_BGR2RGB
    )

    st.image(
        imagen_original,
        caption="Imagen cargada",
        use_container_width=True
    )

    # ==========================================
    # BOTÓN PROCESAR
    # ==========================================

    st.header("🔍 Reconocimiento")

    if st.button(
        "🚀 Procesar imagen",
        use_container_width=True
    ):

        # --------------------------------------
        # APLICAR FILTRO
        # --------------------------------------

        if filtro == "Sin filtro":

            imagen_procesada = cv2.cvtColor(
                cv2_img,
                cv2.COLOR_BGR2RGB
            )

        elif filtro == "Escala de grises":

            imagen_procesada = cv2.cvtColor(
                cv2_img,
                cv2.COLOR_BGR2GRAY
            )

        else:

            gris = cv2.cvtColor(
                cv2_img,
                cv2.COLOR_BGR2GRAY
            )

            imagen_procesada = cv2.threshold(
                gris,
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]

        # --------------------------------------
        # MOSTRAR IMAGEN PROCESADA
        # --------------------------------------

        st.subheader("🎨 Imagen procesada")

        st.image(
            imagen_procesada,
            caption=f"Filtro aplicado: {filtro}",
            use_container_width=True
        )

        # --------------------------------------
        # IDIOMA
        # --------------------------------------

        if idioma == "Español":
            idioma_tesseract = "spa"
        else:
            idioma_tesseract = "eng"

        # --------------------------------------
        # OCR
        # --------------------------------------

        with st.spinner("🔎 Reconociendo texto..."):

            try:

                texto = pytesseract.image_to_string(
                    imagen_procesada,
                    lang=idioma_tesseract
                )

            except Exception as error:

                st.error(
                    "No se pudo ejecutar Tesseract."
                )

                st.code(str(error))

                texto = ""

        # ==========================================
        # RESULTADO
        # ==========================================

        st.header("📝 Resultado del OCR")

        if texto.strip():

            st.text_area(
                "Texto reconocido:",
                texto,
                height=250
            )

            # ==========================================
            # ESTADÍSTICAS
            # ==========================================

            st.subheader("📊 Estadísticas")

            palabras = texto.split()
            caracteres = len(texto)
            lineas = len(texto.splitlines())

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

            # ==========================================
            # BOTONES
            # ==========================================

            st.header("🛠️ Funciones adicionales")

            col1, col2 = st.columns(2)

            # ------------------------------------------
            # DESCARGAR
            # ------------------------------------------

            with col1:

                st.download_button(
                    "📥 Descargar texto",
                    data=texto,
                    file_name="texto_reconocido.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            # ------------------------------------------
            # MOSTRAR INFORMACIÓN
            # ------------------------------------------

            with col2:

                mostrar_info = st.button(
                    "ℹ️ Información",
                    use_container_width=True
                )

            if mostrar_info:

                st.info(
                    f"""
                    **Información del reconocimiento**

                    - Idioma: {idioma}
                    - Filtro: {filtro}
                    - Palabras encontradas: {len(palabras)}
                    - Caracteres: {caracteres}
                    """
                )

            # ==========================================
            # LECTURA EN VOZ ALTA
            # ==========================================

            st.subheader("🔊 Lectura en voz alta")

            texto_voz = texto.replace(
                "\\",
                "\\\\"
            ).replace(
                "'",
                "\\'"
            ).replace(
                "\n",
                " "
            )

            codigo_voz = f"""
            <script>
            function leerTexto() {{

                var texto = '{texto_voz}';

                var mensaje =
                    new SpeechSynthesisUtterance(texto);

                mensaje.lang = 'es-ES';

                window.speechSynthesis.cancel();

                window.speechSynthesis.speak(mensaje);
            }}
            </script>

            <button
                onclick="leerTexto()"
                style="
                    background-color:#4CAF50;
                    color:white;
                    border:none;
                    padding:12px 25px;
                    border-radius:8px;
                    font-size:16px;
                    cursor:pointer;
                ">
                🔊 Leer texto
            </button>
            """

            st.components.v1.html(
                codigo_voz,
                height=60
            )

        else:

            st.warning(
                "⚠️ No se encontró texto en la imagen."
            )

            st.write(
                "Intenta utilizar una imagen con buena iluminación "
                "y texto claramente visible."
            )

else:

    st.info(
        "👆 Selecciona una imagen o toma una fotografía para comenzar."
    )



