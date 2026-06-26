import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Sivun asetukset ja CSS-tyylit
# -----------------------------

st.set_page_config(
    page_title="Finnish Government Debt Dashboard",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #faf8f5;
    }

    .block-container {
        padding-top: 4rem;
        padding-bottom: 4rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1400px;
    }

    hr {
        border: none;
        border-top: 2px solid #e5e7eb;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    div[data-testid="stDataFrame"] {
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 6px;
        background-color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Yläosan otsikko ja KPI-kortit
# -----------------------------

st.title("🇫🇮 Finnish Government Debt Analytics Dashboard")
st.subheader("Suomen valtion velan kehitys 2000–2025")

df = pd.read_csv("data/transformed_debt_data.csv")

start_debt = df.iloc[0]["debt_billion_eur"]
latest_debt = df.iloc[-1]["debt_billion_eur"]
increase = latest_debt - start_debt
increase_percent = (increase / start_debt) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="border:2px solid #e5e7eb;border-radius:10px;padding:20px;box-shadow:0 4px 12px rgba(0,0,0,0.06);">
        <h4 style="margin:0;color:#555;">Velka vuonna 2000</h4>
        <h1 style="color:#16a34a;margin-bottom:0;">{start_debt:.1f}</h1>
        <h3 style="margin-top:0;">mrd €</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="border:2px solid #e5e7eb;border-radius:10px;padding:20px;box-shadow:0 4px 12px rgba(0,0,0,0.06);">
        <h4 style="margin:0;color:#555;">Velka vuonna 2025</h4>
        <h1 style="color:#ca8a04;margin-bottom:0;">{latest_debt:.1f}</h1>
        <h3 style="margin-top:0;">mrd €</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="border:2px solid #e5e7eb;border-radius:10px;padding:20px;box-shadow:0 4px 12px rgba(0,0,0,0.06);">
        <h4 style="margin:0;color:#555;">Kasvu 2000–2025</h4>
        <h1 style="color:#dc2626;margin-bottom:0;">{increase:.1f}</h1>
        <h3 style="margin-top:0;">mrd €</h3>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="border:2px solid #e5e7eb;border-radius:10px;padding:20px;box-shadow:0 4px 12px rgba(0,0,0,0.06);">
        <h4 style="margin:0;color:#555;">Kasvu yhteensä</h4>
        <h1 style="color:#2563eb;">{increase_percent:.1f} %</h1>
        <h3 style="margin-top:0;">mrd €</h3>
    </div>
    """, unsafe_allow_html=True)
    
st.divider()

# -----------------------------
# Velan kehityksen ja vuosittaisen kasvun visualisoinnit
# -----------------------------

st.subheader("Velan kehitys ja vuosittainen kasvu")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_line = px.line(
        df,
        x="year",
        y="debt_billion_eur",
        markers=True,
        labels={
            "year": "Vuosi",
            "debt_billion_eur": "Velka (mrd €)"
        }
    )

    fig_line.update_traces(
        line=dict(color="#16a34a", width=4),
        marker=dict(color="#16a34a", size=8)
    )

    fig_line.update_layout(
        title="Velan kokonaiskehitys",
        hovermode="x unified",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

with chart_col2:
    # Muutetaan vuosittainen kasvu miljardeiksi euroiksi
    growth_df = df.dropna(subset=["annual_growth_eur"]).copy()
    growth_df["annual_growth_billion_eur"] = (
        growth_df["annual_growth_eur"] / 1000
    )

    fig_bar = px.bar(
        growth_df,
        x="year",
        y="annual_growth_billion_eur",
        labels={
            "year": "Vuosi",
            "annual_growth_billion_eur": "Kasvu (mrd €)"
        }
    )

    fig_bar.update_traces(
        marker_color="#dc2626"
    )

    fig_bar.update_layout(
        title="Vuosittainen velan kasvu",
        template="plotly_white",
        hovermode="x unified",
        height=450
    )

    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

# Lasketaan vertailujaksojen keskimääräinen vuosikasvu
debt_2000 = df.loc[df["year"] == 2000, "debt_billion_eur"].iloc[0]
debt_2019 = df.loc[df["year"] == 2019, "debt_billion_eur"].iloc[0]
debt_2020 = df.loc[df["year"] == 2020, "debt_billion_eur"].iloc[0]
debt_2025 = df.loc[df["year"] == 2025, "debt_billion_eur"].iloc[0]

growth_2000_2019 = debt_2019 - debt_2000
avg_2000_2019 = growth_2000_2019 / 19

growth_2020_2025 = debt_2025 - debt_2020
avg_2020_2025 = growth_2020_2025 / 5

forecast_2030 = debt_2025 + (avg_2020_2025 * 5)
growth_2025_2030 = forecast_2030 - debt_2025

summary_df = pd.DataFrame({
    "Aikajakso": ["2000–2019", "2020–2025", "2025–2030 (*)"],
    "Vuosia": [19, 5, 5],
    "Kasvu": [
        round(growth_2000_2019, 1),
        round(growth_2020_2025, 1),
        round(growth_2025_2030, 1)
    ],
    "Kasvu/vuosi": [
        round(avg_2000_2019, 2),
        round(avg_2020_2025, 2),
        round(avg_2020_2025, 2)
    ]
})

st.divider()

# -----------------------------
# Kasvujaksojen vertailu ja ennuste vuoteen 2030
# -----------------------------

forecast_col1, forecast_col2 = st.columns(2)

with forecast_col1:
    st.markdown("### Velan kasvujaksojen vertailu")

    st.markdown(f"""
    <div style="background-color:white;border:2px solid #e5e7eb;border-radius:12px;padding:22px;box-shadow:0 4px 12px rgba(0,0,0,0.06);">
        <h4 style="color:#16a34a;">2000–2019</h4>
        <p><b>Kasvu yhteensä:</b> {growth_2000_2019:.1f} mrd €</p>
        <p><b>Keskimäärin:</b> {avg_2000_2019:.2f} mrd € / vuosi</p>
        <hr>
        <h4 style="color:#ca8a04;">2020–2025</h4>
        <p><b>Kasvu yhteensä:</b> {growth_2020_2025:.1f} mrd €</p>
        <p><b>Keskimäärin:</b> {avg_2020_2025:.2f} mrd € / vuosi</p>
        <hr>
        <h4 style="color:#dc2626;">2025–2030 (*)</h4>
        <p><b>Konservatiivinen ennuste:</b> {growth_2025_2030:.1f} mrd €</p>
        <p><b>Keskimäärin:</b> {avg_2020_2025:.2f} mrd € / vuosi</p>
    </div>
    """, unsafe_allow_html=True)

with forecast_col2:
    st.markdown("### Velan kehitys 2000 - 2025 ja ennuste 2025 - 2030")
    forecast_years = list(range(2026, 2031))
    forecast_values = [
        debt_2025 + avg_2020_2025 * i
        for i in range(1, 6)
    ]

    historical_df = df[["year", "debt_billion_eur"]].copy()
    historical_df["type"] = "Toteutunut"

    forecast_df = pd.DataFrame({
        "year": forecast_years,
        "debt_billion_eur": forecast_values,
        "type": "Konservatiivinen ennuste"
    })

    projection_df = pd.concat([historical_df, forecast_df], ignore_index=True)

    fig_projection = px.line(
        projection_df,
        x="year",
        y="debt_billion_eur",
        color="type",
        markers=True,
        labels={
            "year": "Vuosi",
            "debt_billion_eur": "Velka (mrd €)",
            "type": ""
        }
    )

    fig_projection.update_layout(
    title="",
    template="plotly_white",
    hovermode="x unified",
    height=420,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

    fig_projection.add_vline(
        x=2025,
        line_width=2,
        line_dash="dash",
        line_color="gray"
    )

    st.plotly_chart(fig_projection, use_container_width=True, config={"displayModeBar": False})
    
    st.info(
        f"Konservatiivinen ennuste 2030: {forecast_2030:.1f} mrd €. "
        f"Laskelma perustuu vuosien 2020–2025 keskimääräiseen "
        f"vuosikasvuun ({avg_2020_2025:.2f} mrd € / vuosi)."
    )
    
    st.caption(
        "*Vuodet 2025–2030 ovat konservatiivinen lineaarinen ennuste, "
        "ei varsinainen talousennuste."
    )


st.divider()

# -----------------------------
# Puhdistetun Tilastokeskuksen aineiston näyttäminen taulukkona
# -----------------------------

st.subheader("Tilastokeskuksen Suomen valtionvelka aineisto")

st.write(
    "Puhdistettu aineisto sisältää alkuperäiset velkatiedot ja analyysia varten lasketut lisäsarakkeet."
)
    
st.dataframe(df, use_container_width=True)