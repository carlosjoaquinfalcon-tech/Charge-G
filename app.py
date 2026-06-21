import streamlit as st
from dataclasses import dataclass, asdict
import pandas as pd

st.set_page_config(page_title="Fantasy Shop", page_icon="🎮", layout="wide")

st.markdown("""
<style>
.main {
    background-color: #0f0f17;
}
h1,h2,h3 {
    color:#c77dff;
}
.stButton>button {
    background-color:#7b2cbf;
    color:white;
}
</style>
""", unsafe_allow_html=True)

@dataclass
class Producto:
    ID_Producto:int
    Nombre:str
    Categoria:str
    Precio_USD:float
    Stock_Disponible:int
    Compatible_VR:bool
    Requiere_Calibracion:bool

def cargar_iniciales():
    return [
        Producto(1001,"Charge G Haptic Suit X1","Traje Háptico",1499.99,12,True,True),
        Producto(1002,"Charge G Vision VR Pro","Gafas VR",899.99,25,True,False),
        Producto(1003,"Charge G Phantom Gloves","Guantes Hápticos",499.99,18,True,True),
        Producto(1004,"Charge G Motion Tracker","Sensores",299.99,40,True,False),
        Producto(1005,"Charge G Speed Glide Pro","Mouse Glides",39.99,100,False,False)
    ]

if "productos" not in st.session_state:
    st.session_state.productos = cargar_iniciales()

st.sidebar.title("Fantasy Shop")
pagina = st.sidebar.radio(
    "Menú",
    ["Inicio","Catálogo","Alta","Modificar","Eliminar","Estadísticas"]
)

if pagina == "Inicio":
    st.title("🧙 Fantasy Shop")
    st.subheader("Gaming inmersivo y realidad virtual")
    st.write("Tienda especializada en trajes hápticos, gafas VR, sensores y accesorios premium.")
    
    c1,c2,c3 = st.columns(3)
    c1.metric("Productos", len(st.session_state.productos))
    c2.metric("Categorías", len(set(p.Categoria for p in st.session_state.productos)))
    valor = sum(p.Precio_USD*p.Stock_Disponible for p in st.session_state.productos)
    c3.metric("Inventario USD", f"{valor:,.2f}")
    
    st.markdown("---")
    st.write("### Productos destacados")
    for p in st.session_state.productos[:3]:
        st.info(f"{p.Nombre} - USD {p.Precio_USD}")

elif pagina == "Catálogo":
    st.title("📦 Catálogo")
    
    buscar = st.text_input("Buscar producto")
    categorias = ["Todas"] + sorted(list(set(p.Categoria for p in st.session_state.productos)))
    filtro = st.selectbox("Categoría", categorias)

    datos = []
    for p in st.session_state.productos:
        if buscar.lower() not in p.Nombre.lower():
            continue
        if filtro != "Todas" and p.Categoria != filtro:
            continue
        datos.append(asdict(p))

    st.dataframe(pd.DataFrame(datos), use_container_width=True)

elif pagina == "Alta":
    st.title("➕ Alta de Producto")

    with st.form("alta"):
        idp = st.number_input("ID Producto", min_value=1, step=1)
        nombre = st.text_input("Nombre")
        categoria = st.selectbox("Categoría",
        ["Traje Háptico","Gafas VR","Guantes Hápticos","Sensores","Mouse Glides"])
        precio = st.number_input("Precio USD", min_value=0.0)
        stock = st.number_input("Stock", min_value=0, step=1)
        vr = st.checkbox("Compatible VR")
        calib = st.checkbox("Requiere calibración")

        if st.form_submit_button("Guardar"):
            existe = any(p.ID_Producto == int(idp) for p in st.session_state.productos)

            if existe:
                st.error("El ID ya existe. Debe ser único.")
            else:
                st.session_state.productos.append(
                    Producto(int(idp), nombre, categoria, precio, int(stock), vr, calib)
                )
                st.success("Producto agregado correctamente")

elif pagina == "Modificar":
    st.title("✏️ Modificación de Producto")

    if st.session_state.productos:
        ids = [p.ID_Producto for p in st.session_state.productos]
        seleccionado = st.selectbox("Seleccione ID", ids)

        prod = next(p for p in st.session_state.productos if p.ID_Producto == seleccionado)

        nombre = st.text_input("Nombre", prod.Nombre)
        precio = st.number_input("Precio", value=float(prod.Precio_USD))
        stock = st.number_input("Stock", value=int(prod.Stock_Disponible))
        vr = st.checkbox("Compatible VR", value=prod.Compatible_VR)
        calib = st.checkbox("Requiere calibración", value=prod.Requiere_Calibracion)

        if st.button("Actualizar"):
            prod.Nombre = nombre
            prod.Precio_USD = precio
            prod.Stock_Disponible = int(stock)
            prod.Compatible_VR = vr
            prod.Requiere_Calibracion = calib
            st.success("Producto actualizado")

elif pagina == "Eliminar":
    st.title("🗑️ Eliminar Producto")

    ids = [p.ID_Producto for p in st.session_state.productos]

    if ids:
        seleccionado = st.selectbox("Seleccione ID", ids)

        if st.button("Eliminar Producto"):
            st.session_state.productos = [
                p for p in st.session_state.productos
                if p.ID_Producto != seleccionado
            ]
            st.success("Producto eliminado correctamente")

elif pagina == "Estadísticas":
    st.title("📊 Estadísticas")

    total = len(st.session_state.productos)
    valor = sum(p.Precio_USD * p.Stock_Disponible for p in st.session_state.productos)
    stock = sum(p.Stock_Disponible for p in st.session_state.productos)

    st.metric("Cantidad de productos", total)
    st.metric("Stock total", stock)
    st.metric("Valor total inventario USD", f"{valor:,.2f}")

    tabla = pd.DataFrame([asdict(p) for p in st.session_state.productos])
    st.dataframe(tabla, use_container_width=True)
