import streamlit as st
import base64
import json
from groq import Groq

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA Y ESTILO KAWAII/GL
# ==========================================
st.set_page_config(page_title="Nuestro Test de Amor GL 💖", page_icon="🐱", layout="centered")

st.markdown("""
    <style>
    /* Fuente redondeada y tierna */
    @import url('https://fonts.googleapis.com/css2?family=Mali:ital,wght@0,400;0,600;1,400&display=swap');
    
    /* Fondo degradado de ensueño */
    .stApp {
        background: linear-gradient(135deg, #ffe6f0 0%, #e6f0ff 50%, #f0e6ff 100%);
        font-family: 'Mali', cursive;
    }
    
    /* Títulos con brillo pastel */
    h1, h2, h3 {
        color: #ff6699 !important;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.9);
        font-weight: 600;
    }
    
    /* Cajas de texto (Text Areas) */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border: 2px dashed #ffb3cc !important;
        border-radius: 15px !important;
        color: #5a5a5a !important;
        font-family: 'Mali', cursive;
        padding: 12px;
        box-shadow: 0 2px 5px rgba(255, 179, 204, 0.2);
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border: 2px solid #ff6699 !important;
        box-shadow: 0 0 10px rgba(255, 102, 153, 0.4);
    }
    
    /* Botones súper lindos */
    .stButton button {
        background: linear-gradient(90deg, #ff99cc, #ffcc99) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        box-shadow: 0 4px 8px rgba(255, 153, 204, 0.4) !important;
        transition: transform 0.2s, box-shadow 0.2s;
        width: 100%;
        margin-top: 10px;
    }
    .stButton button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 12px rgba(255, 153, 204, 0.6) !important;
        background: linear-gradient(90deg, #ffcc99, #ff99cc) !important;
    }
    
    /* Cajas de alerta e info */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        border-left: 5px solid #ff6699 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Selector múltiple (Lenguajes del amor) */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border: 2px dashed #ffb3cc !important;
        border-radius: 15px !important;
        font-family: 'Mali', cursive;
        color: #5a5a5a !important;
    }
    div[data-baseweb="select"] span {
        color: #ff6699 !important;
        font-weight: bold;
    }
    /* ¡Arreglo mágico para que los textos se lean! */
p, label, div[data-testid="stWidgetLabel"] p, .stMarkdown p {
    color: #4a4a4a !important; /* Gris oscuro suave */
}

/* Asegurar que el texto dentro de las cajas de respuesta sea oscuro */
.stTextArea textarea {
    color: #333333 !important;
}

/* Color de las opciones en el menú desplegable de los lenguajes del amor */
div[data-baseweb="select"] span {
    color: #4a4a4a !important;
}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CONFIGURACIÓN DE GROQ (¡Pon tu NUEVA API Key aquí!)
# ==========================================

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ==========================================
# LAS 15 PREGUNTAS DEFINITIVAS
# ==========================================
PREGUNTAS = [
    "1. Últimamente, ¿cómo has estado emocionalmente? ¿Hay algo que te tenga ansiosa, estresada o con la mente muy ocupada y que casi no has contado? 🥺",
    "2. Si no existieran límites de dinero ni miedo, ¿a qué te gustaría dedicar tu vida? ✨",
    "3. ¿Cómo recargas tu energía emocional cuando sientes que te has quedado sin batería? 🔋",
    "4. Cuando tienes un mal día, ¿prefieres espacio, consejos o solo una oreja que te escuche? 🫂",
    "5. ¿Cómo te gusta que te demuestren amor? (Selecciona tus lenguajes del amor principales) 💌",
    "6. ¿Cuál es tu mayor miedo cuando se trata de abrirte emocionalmente con alguien? 👻",
    "7. ¿Qué evento de tu infancia crees que marcó la persona que eres hoy? 🌟",
    "8. ¿Cómo manejas los desacuerdos y qué necesitas para sentirte segura durante una discusión? 🕊️",
    "9. ¿Cómo te imaginas tu vida ideal en 5 años? Describe cómo se sentiría tu hogar. 🏡",
    "10. ¿Qué significa para ti la confianza y cómo se construye día a día? 🤝",
    "11. ¿Qué límites personales consideras innegociables en una relación? 🚧",
    "12. ¿Qué es eso que amas profundamente de ti misma y que a veces te cuesta reconocer? 🌸",
    "13. ¿Qué pequeños rituales o tradiciones te gustaría que creáramos o mantuviéramos juntas? 🕯️",
    "14. ¿Qué es algo que siempre has querido intentar pero no te has atrevido, y que podríamos hacer juntas? 🎢",
    "15. ¿Qué es lo que más te ha gustado de conocerme hasta ahora y qué te gustaría que construyéramos nosotras? 💖"
]

OPCIONES_AMOR = [
    "Palabras de afirmación (halagos, mensajes lindos) 🗣️",
    "Tiempo de calidad (atención plena, planes juntas) ⏳",
    "Regalos (detalles materiales, sorpresas) 🎁",
    "Actos de servicio (ayuda práctica, favores) 🛠️",
    "Contacto físico (abrazos, caricias, cercanía) 🤗"
]

# ==========================================
# LÓGICA DE LA APP (MODO A DISTANCIA)
# ==========================================
if 'paso' not in st.session_state:
    st.session_state.paso = 0
if 'respuestas_p1' not in st.session_state:
    st.session_state.respuestas_p1 = {}

st.markdown("<h1>🐱 Test de Compatibilidad GL 🐱</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 18px;'>Para sentirse vistas, entendidas y muy amadas 💖</p>", unsafe_allow_html=True)

# --- PANTALLA DE INICIO ---
if st.session_state.paso == 0:
    st.subheader("🌸 ¿Quién está usando la app?")
    st.write("Elijan sabiamente. La primera en responder tendrá que enviarle un código a la otra.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Soy la primera en responder 💖"):
            st.session_state.paso = 1
            st.rerun()
    with col2:
        if st.button("Ya tengo el código 🔐"):
            st.session_state.paso = 3
            st.rerun()

# --- PASO 1: JUGADORA 1 RESPONDE ---
elif st.session_state.paso == 1:
    st.subheader("🌸 Turno de la Jugadora 1")
    st.write("Responde con calma y mucha sinceridad. Al terminar, la app te dará un código para que se lo envíes a tu novia.")
    
    with st.form("form_p1"):
        respuestas = {}
        for i, pregunta in enumerate(PREGUNTAS):
            if i == 4: # Pregunta 5 (Lenguajes del amor)
                st.markdown(f"**{pregunta}**")
                seleccion = st.multiselect("Elige tus principales:", OPCIONES_AMOR, key=f"p1_{i}")
                explicacion = st.text_area("¿Cómo se ve esto en la práctica? (Opcional)", key=f"p1_extra_{i}")
                respuestas[str(i)] = f"Lenguajes elegidos: {', '.join(seleccion)}. Explicación: {explicacion}"
            else:
                respuestas[str(i)] = st.text_area(pregunta, key=f"p1_{i}")
        
        submit = st.form_submit_button("Generar Código de Amor 💖")
        if submit:
            if any(r.strip() == "" for r in respuestas.values() if "Lenguajes elegidos: ." in r or r.strip() == ""):
                st.error("Por favor, responde todas las preguntas para que el test sea mágico ✨")
            else:
                st.session_state.respuestas_p1 = respuestas
                st.session_state.paso = 2
                st.rerun()

# --- PASO 2: JUGADORA 1 GENERA CÓDIGO ---
elif st.session_state.paso == 2:
    st.subheader("✨ ¡Respuestas guardadas! ✨")
    st.write("Copia este **Código de Amor** y envíaselo a tu novia por WhatsApp. Ella deberá abrir la app, elegir la opción 'Ya tengo el código' y pegarlo.")
    
    codigo = base64.b64encode(json.dumps(st.session_state.respuestas_p1).encode()).decode()
    st.code(codigo, language="text")
    
    st.info("💡 Una vez que se lo hayas enviado, ella podrá responder sus preguntas y verán el resultado juntas.")
    if st.button("Volver al inicio 🔄"):
        st.session_state.clear()
        st.rerun()

# --- PASO 3: JUGADORA 2 INGRESA CÓDIGO ---
elif st.session_state.paso == 3:
    st.subheader("🐰 Pega el Código de Amor")
    st.write("Pega aquí el código que te envió tu novia por WhatsApp para desbloquear tus preguntas.")
    
    codigo_input = st.text_area("Pega el código aquí:")
    if st.button("Desbloquear preguntas 🔓"):
        try:
            decoded = base64.b64decode(codigo_input.strip()).decode()
            st.session_state.respuestas_p1 = json.loads(decoded)
            st.session_state.paso = 4
            st.rerun()
        except Exception as e:
            st.error("El código no es válido. Asegúrate de copiar todo el texto, sin espacios extra. 🥺")

# --- PASO 4: JUGADORA 2 RESPONDE ---
elif st.session_state.paso == 4:
    st.subheader("🐰 Turno de la Jugadora 2")
    st.write("¡Código aceptado! Ahora te toca a ti, mi amor. Responde con sinceridad.")
    
    with st.form("form_p2"):
        respuestas_p2 = {}
        for i, pregunta in enumerate(PREGUNTAS):
            if i == 4: # Pregunta 5 (Lenguajes del amor)
                st.markdown(f"**{pregunta}**")
                seleccion = st.multiselect("Elige tus principales:", OPCIONES_AMOR, key=f"p2_{i}")
                explicacion = st.text_area("¿Cómo se ve esto en la práctica? (Opcional)", key=f"p2_extra_{i}")
                respuestas_p2[str(i)] = f"Lenguajes elegidos: {', '.join(seleccion)}. Explicación: {explicacion}"
            else:
                respuestas_p2[str(i)] = st.text_area(pregunta, key=f"p2_{i}")
        
        submit = st.form_submit_button("Calcular nuestra compatibilidad 💞")
        if submit:
            if any(r.strip() == "" for r in respuestas_p2.values() if "Lenguajes elegidos: ." in r or r.strip() == ""):
                st.error("¡Faltan respuestas! Responde todo para ver el resultado 🥺")
            else:
                st.session_state.respuestas_p2 = respuestas_p2
                st.session_state.paso = 5
                st.rerun()

# --- PASO 5: RESULTADOS MÁGICOS ---
elif st.session_state.paso == 5:
    st.subheader("🔮 Analizando su conexión...")
    
    with st.spinner("Invocando a la IA del amor... 🐱✨"):
        try:
            client = Groq(api_key=GROQ_API_KEY)
            
            # Formatear las respuestas para el prompt
            texto_p1 = "\n".join([f"{PREGUNTAS[i]}: {st.session_state.respuestas_p1[str(i)]}" for i in range(len(PREGUNTAS))])
            texto_p2 = "\n".join([f"{PREGUNTAS[i]}: {st.session_state.respuestas_p2[str(i)]}" for i in range(len(PREGUNTAS))])
            
            prompt = f"""
            Actúa como un consejero de parejas y experto en psicología del amor, con un tono súper dulce, empático y poético. 
            Somos dos chicas (relación GL) que estamos iniciando nuestra relación y pronto dejaremos la distancia para estar juntas en persona. 
            Hemos respondido un test profundo de 15 preguntas basado en la teoría de la autorrevelación.
            
            Respuestas de la Jugadora 1 (La que respondió primero):
            {texto_p1}
            
            Respuestas de la Jugadora 2 (La que respondió después):
            {texto_p2}
            
            Tu tarea es realizar un análisis psicológico profundo pero muy cariñoso y visualmente hermoso:
            1. Calcular un 'Nivel de Compatibilidad' del 1 al 100% basándote en sus valores, sueños, estilos de apego y lenguajes del amor. Explica brevemente por qué ese número.
            2. Analizar sus puntos de conexión profunda (puntos verdes 🌸). Destaca dónde brillan juntas.
            3. Identificar áreas de crecimiento o diferencias que deben conversar con calma, sin juzgar (puntos amarillos 🍋). 
            4. Darles un consejo psicológico práctico y muy romántico para fortalecer su vínculo ahora que están a punto de estar juntas en persona, fomentando la seguridad emocional. Presta especial atención a sus lenguajes del amor y a los rituales que quieren crear.
            
            Usa un tono muy dulce, en español y háblanos en femenino. Incluye muchos emojis de gatitos, corazones, flores y destellos. 
            Estructura la respuesta con títulos bonitos y viñetas para que sea fácil de leer. ¡El objetivo es que se sientan vistas, entendidas y muy amadas! 
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192", # Modelo rápido y gratuito de Groq
            )
            
            resultado = chat_completion.choices[0].message.content
            st.success("¡Análisis completado! 💖")
            st.markdown(resultado)
            
        except Exception as e:
            st.error(f"Ups, hubo un error con la IA: {e}. Revisa que tu API Key de Groq esté bien puesta en el código.")
            
    if st.button("Volver a empezar 🔄"):
        st.session_state.clear()
        st.rerun()
