import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Análisis de Spotify", layout="wide")

st.title("🎵 Análisis de Canciones de Spotify")

# Configurar matplotlib para modo oscuro
plt.style.use('dark_background')


# Cargar datos
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("spotify_songs.csv")
        return df
    except FileNotFoundError:
        st.error("El archivo 'spotify_songs.csv' no se encontró. Por favor, asegúrate de que esté en el mismo directorio.")
        return None

df = load_data()

if df is not None:
    # Mostrar datos crudos
    if st.checkbox("Mostrar datos crudos"):
        st.write(df.head(100))

    st.markdown("---")

    # Layout de columnas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribución de Popularidad")
        fig_hist, ax_hist = plt.subplots()
        ax_hist.hist(df['track_popularity'], bins=20, color='skyblue', edgecolor='black')
        ax_hist.set_xlabel('Popularidad')
        ax_hist.set_ylabel('Frecuencia')
        st.pyplot(fig_hist)

    with col2:
        st.subheader("Top 10 Géneros Musicales")
        if 'playlist_genre' in df.columns:
            genre_counts = df['playlist_genre'].value_counts().head(10)
            fig_bar, ax_bar = plt.subplots()
            genre_counts.plot(kind='bar', color='lightgreen', ax=ax_bar)
            ax_bar.set_xlabel('Género')
            ax_bar.set_ylabel('Cantidad de Canciones')
            st.pyplot(fig_bar)
        else:
            st.warning("No se encontró la columna 'playlist_genre'.")

    st.markdown("---")

    st.subheader("Relación entre Bailabilidad y Energía")
    if 'danceability' in df.columns and 'energy' in df.columns:
        fig_scatter, ax_scatter = plt.subplots()
        ax_scatter.scatter(df['danceability'], df['energy'], alpha=0.5, c='purple')
        ax_scatter.set_xlabel('Bailabilidad')
        ax_scatter.set_ylabel('Energía')
        st.pyplot(fig_scatter)
    else:
        st.warning("Faltan columnas 'danceability' o 'energy'.")

    # Filtros interactivos
    st.sidebar.header("Filtros")
    if 'playlist_genre' in df.columns:
        selected_genre = st.sidebar.selectbox("Selecciona un Género", ["Todos"] + list(df['playlist_genre'].unique()))
        
        if selected_genre != "Todos":
            filtered_df = df[df['playlist_genre'] == selected_genre]
            st.subheader(f"Top 10 Canciones más escuchadas: {selected_genre}")
        else:
            filtered_df = df
            st.subheader("Top 10 Canciones más escuchadas (Global)")


        # Ordenar por popularidad y tomar el top 10
        if 'track_popularity' in df.columns:
            # Top 10 más escuchadas
            top_10 = filtered_df.sort_values(by='track_popularity', ascending=False).head(10)
            
            # Crear gráfico de barras horizontales para las más escuchadas
            fig_top, ax_top = plt.subplots(figsize=(10, 6))
            track_labels = [f"{row['track_name'][:30]}..." if len(row['track_name']) > 30 else row['track_name'] 
                           for _, row in top_10.iterrows()]
            ax_top.barh(range(len(top_10)), top_10['track_popularity'], color='lightcoral')
            ax_top.set_yticks(range(len(top_10)))
            ax_top.set_yticklabels(track_labels)
            ax_top.set_xlabel('Popularidad')
            ax_top.set_title('Top 10 Canciones Más Escuchadas')
            ax_top.invert_yaxis()  # Para que la más popular esté arriba
            plt.tight_layout()
            st.pyplot(fig_top)
            
            st.dataframe(top_10[['track_name', 'track_artist', 'track_popularity']].reset_index(drop=True))
            
            st.markdown("---")
            
            # Top 10 menos escuchadas
            if selected_genre != "Todos":
                st.subheader(f"Top 10 Canciones menos escuchadas: {selected_genre}")
            else:
                st.subheader("Top 10 Canciones menos escuchadas (Global)")
            
            bottom_10 = filtered_df.sort_values(by='track_popularity', ascending=True).head(10)
            
            # Crear gráfico de barras horizontales para las menos escuchadas
            fig_bottom, ax_bottom = plt.subplots(figsize=(10, 6))
            track_labels_bottom = [f"{row['track_name'][:30]}..." if len(row['track_name']) > 30 else row['track_name'] 
                                  for _, row in bottom_10.iterrows()]
            ax_bottom.barh(range(len(bottom_10)), bottom_10['track_popularity'], color='lightblue')
            ax_bottom.set_yticks(range(len(bottom_10)))
            ax_bottom.set_yticklabels(track_labels_bottom)
            ax_bottom.set_xlabel('Popularidad')
            ax_bottom.set_title('Top 10 Canciones Menos Escuchadas')
            ax_bottom.invert_yaxis()  # Para que la menos popular esté arriba
            plt.tight_layout()
            st.pyplot(fig_bottom)
            
            st.dataframe(bottom_10[['track_name', 'track_artist', 'track_popularity']].reset_index(drop=True))
            
            # Mostrar grilla completa de canciones del género seleccionado
            st.markdown("---")
            if selected_genre != "Todos":
                st.subheader(f"📋 Todas las canciones del género: {selected_genre}")
                st.write(f"Total de canciones: **{len(filtered_df)}**")
            else:
                st.subheader("📋 Todas las canciones")
                st.write(f"Total de canciones: **{len(filtered_df)}**")
            
            # Seleccionar columnas relevantes para mostrar
            columns_to_show = ['track_name', 'track_artist', 'track_album_name', 'track_popularity']
            
            # Agregar columnas adicionales si existen
            optional_columns = ['danceability', 'energy', 'valence', 'tempo']
            for col in optional_columns:
                if col in filtered_df.columns:
                    columns_to_show.append(col)
            
            # Mostrar la grilla con todas las canciones
            st.dataframe(
                filtered_df[columns_to_show].sort_values(by='track_popularity', ascending=False),
                use_container_width=True,
                height=400
            )
        else:
            st.warning("No se encontró la columna 'track_popularity'.")
