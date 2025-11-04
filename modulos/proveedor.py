import streamlit as st
from modulos.config.conexion import obtener_conexion

def mostrar_proveedor():
    st.header("🏢 Registro de Proveedores")

    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # Formulario para registrar proveedor
        with st.form("form_proveedor"):
            nombre = st.text_input("Nombre del proveedor")
            telefono = st.text_input("Teléfono")
            direccion = st.text_area("Dirección")
            enviar = st.form_submit_button("✅ Guardar proveedor")

            if enviar:
                if nombre.strip() == "":
                    st.warning("⚠️ Debes ingresar el nombre del proveedor.")
                else:
                    try:
                        cursor.execute(
                            """
                            INSERT INTO Proveedores (Nombre, Telefono, Direccion)
                            VALUES (%s, %s, %s)
                            """,
                            (nombre, telefono, direccion)
                        )
                        con.commit()
                        st.success(f"✅ Proveedor registrado correctamente: {nombre}")
                        st.rerun()
                    except Exception as e:
                        con.rollback()
                        st.error(f"❌ Error al registrar el proveedor: {e}")

        # Mostrar proveedores registrados
        st.subheader("📋 Lista de proveedores registrados")
        try:
            cursor.execute("SELECT ID_Proveedor, Nombre, Telefono, Direccion FROM Proveedores ORDER BY ID_Proveedor DESC")
            proveedores = cursor.fetchall()

            if proveedores:
                for prov in proveedores:
                    with st.expander(f"Proveedor #{prov[0]} - {prov[1]}"):
                        st.write(f"📞 Teléfono: {prov[2]}")
                        st.write(f"🏠 Dirección: {prov[3]}")
            else:
                st.info("No hay proveedores registrados todavía.")

        except Exception as e:
            st.error(f"❌ Error al cargar la lista de proveedores: {e}")

    except Exception as e:
        st.error(f"❌ Error general: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()
