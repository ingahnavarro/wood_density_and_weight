import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import wood_density



class WoodProperties:
    """
    Represents the properties of a wood type.

    Args:
        name: The name of the wood.
        specific_gravity: The specific gravity of the wood.
        fibre_saturation_point: The fiber saturation point of the wood (%).

    Returns:
        None

    Assumptions:
        None
    """
    def __init__(self, name: str, specific_gravity: float, fibre_saturation_point: float):
        self.name = name
        self.specific_gravity = specific_gravity
        self.fibre_saturation_point = fibre_saturation_point


class ElementProperties:
    """
    Represents the properties of a structural element.

    Args:
        name: The name of the element.
        width: The width of the element (m).
        depth: The depth of the element (m).
        length: The length of the element (m).

    Returns:
        None

    Assumptions:
        None
    """

    def __init__(self, name: str, width: float, depth: float, length: float):
        self.name = name
        self.width = width
        self.depth = depth
        self.length = length

def create_contour_plot(x, y, z, xlabel, ylabel, title, colorbar_label, scatter_x,
                        scatter_y):
    fig, ax = plt.subplots(figsize=(6, 5))
    contour = ax.contourf(x, y, z, cmap="viridis")
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.set_title(title, fontsize=10)
    cbar = fig.colorbar(contour, label=colorbar_label)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label(colorbar_label, fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.scatter(
        scatter_x,
        scatter_y,
        color="red",
        marker="o",
        s=100,
    )
    fig.set_size_inches(fig.get_size_inches() * 0.50)
    return fig


def main():
    st.set_page_config(
        page_title="Calculadora de densidad y peso de una pieza de madera",
        layout="wide",
        page_icon="🪵",
    )
    st.title("Calculadora de Densidad y Peso de una Pieza de Madera")

    st.header("Propiedades de la Madera")
    wood_name = st.text_input("Nombre de la Madera", "Pino chileno")
    wood_specific_gravity = st.number_input(
        "Gravedad Específica", min_value=0.0, value=0.50, step=0.5
    )
    wood_fibre_saturation_point = st.number_input(
        "Punto de Saturación de la Fibra (%)", value=30.0, step=0.5
    )

    st.header("Propiedades del Elemento")
    element_name = st.text_input("Nombre del Elemento", "Pieza 1")
    element_width = st.number_input(
        "Ancho (m)", min_value=0.0, value=0.05, step=0.025
    )
    element_depth = st.number_input(
        "Profundidad (m)", min_value=0.0, value=0.125, step=0.025
    )
    element_length = st.number_input(
        "Largo (m)", min_value=0.0, value=2.50, step=0.05
    )
    moisture_point = st.number_input(
        "Contenido de Humedad (%)", value=18.0, step=0.5
    )

    if "tab_selection" not in st.session_state:
        st.session_state.tab_selection = "Resumen"

    if "fig1" not in st.session_state:
        st.session_state.fig1 = None
    if "fig2" not in st.session_state:
        st.session_state.fig2 = None
    if "density_results" not in st.session_state:
        st.session_state.density_results = None
    if "weight_results" not in st.session_state:
        st.session_state.weight_results = None
    if "moisture_grid" not in st.session_state:
        st.session_state.moisture_grid = None
    if "specific_gravity_grid" not in st.session_state:
        st.session_state.specific_gravity_grid = None

    if st.button("Calcular y Mostrar"):
        try:
            wood = WoodProperties(
                wood_name, wood_specific_gravity, wood_fibre_saturation_point
            )
            element = ElementProperties(
                element_name,
                element_width,
                element_depth,
                element_length,
            )
            calculator = wood_density.WeightCalculator(wood, element)

            tab1, tab2, tab3 = st.tabs(["Resumen", "Gráfico de Densidad", "Gráfico de Peso"])

            st.session_state.tab_selection = "Resumen"
            if tab2:
                st.session_state.tab_selection = "Gráfico de Densidad"
            if tab3:
                st.session_state.tab_selection = "Gráfico de Peso"

            with tab1:
                st.subheader("Resultados:")
                wood_point = WoodProperties(
                    wood_name, wood_specific_gravity, wood_fibre_saturation_point
                )
                calculator_point = wood_density.WeightCalculator(wood_point, element)
                density_point = calculator_point.calculate_density_at_moisture_content(
                    moisture_point
                )
                weight_point = calculator_point.calculate_weight_at_moisture_content(
                    moisture_point
                )

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        f"<div style='word-wrap: break-word;'>Densidad a {moisture_point}% de humedad y {wood_specific_gravity} de gravedad específica:</div>",
                        unsafe_allow_html=True,
                    )
                    st.metric(
                        label="",
                        value=f"{density_point:.2f} kg/m³",
                    )
                with col2:
                    st.markdown(
                        f"<div style='word-wrap: break-word;'>Peso a {moisture_point}% de humedad y {wood_specific_gravity} de gravedad específica:</div>",
                        unsafe_allow_html=True,
                    )
                    st.metric(
                        label="",
                        value=f"{weight_point:.2f} kg",
                    )
            with tab2:

                moisture_range = np.linspace(0, max(40, moisture_point), 100)
                specific_gravity_range = np.linspace(0.3, max(1.0, wood_specific_gravity), 100)
                st.session_state.moisture_grid, st.session_state.specific_gravity_grid = np.meshgrid(
                    moisture_range, specific_gravity_range
                )

                st.session_state.density_results = np.array(
                    [
                        [
                            wood_density.WeightCalculator(
                                WoodProperties(
                                    wood_name, sg, wood_fibre_saturation_point
                                ),
                                element,
                            ).calculate_density_at_moisture_content(mc)
                            for mc in moisture_range
                        ]
                        for sg in specific_gravity_range
                    ]
                )
                st.session_state.fig1 = create_contour_plot(
                    st.session_state.moisture_grid,
                    st.session_state.specific_gravity_grid,
                    st.session_state.density_results,
                    "Contenido de Humedad (%)",
                    "Gravedad Específica",
                    "Densidad vs. Contenido de Humedad y Gravedad Específica",
                    "Densidad (kg/m³)",
                    moisture_point,
                    wood_specific_gravity,
                )
                st.pyplot(st.session_state.fig1)

            with tab3:
                moisture_range = np.linspace(0, max(40, moisture_point), 100)
                specific_gravity_range = np.linspace(0.3, max(1.0, wood_specific_gravity), 100)
                st.session_state.moisture_grid, st.session_state.specific_gravity_grid = np.meshgrid(
                    moisture_range, specific_gravity_range
                )

                st.session_state.weight_results = np.array(
                    [
                        [
                            wood_density.WeightCalculator(
                                WoodProperties(
                                    wood_name, sg, wood_fibre_saturation_point
                                ),
                                element,
                            ).calculate_weight_at_moisture_content(mc)
                            for mc in moisture_range
                        ]
                        for sg in specific_gravity_range
                    ]
                )
                st.session_state.fig2 = create_contour_plot(
                    st.session_state.moisture_grid,
                    st.session_state.specific_gravity_grid,
                    st.session_state.weight_results,
                    "Contenido de Humedad (%)",
                    "Gravedad Específica",
                    "Peso vs. Contenido de Humedad y Gravedad Específica",
                    "Peso (kg)",
                    moisture_point,
                    wood_specific_gravity,
                )
                st.pyplot(st.session_state.fig2)

        except ValueError as e:
            st.error(f"Error: {e}")
        except TypeError as e:
            st.error(f"Error: {e}")

    if st.session_state.tab_selection == "Gráfico de Densidad":
        st.session_state.tab_selection = "Gráfico de Densidad"
    if st.session_state.tab_selection == "Gráfico de Peso":
        st.session_state.tab_selection = "Gráfico de Peso"


if __name__ == "__main__":
    main()
