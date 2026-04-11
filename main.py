import streamlit as st
import math
from plot_presjek import nacrtaj_presjek

st.set_page_config(layout="wide")
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}
</style>
""", unsafe_allow_html=True)

col_space, col_title = st.columns([1.2, 1.8])

with col_title:
    st.title("Kontrola uzgona okna")

col1, col2 = st.columns([1, 1])

#with col1:

st.sidebar.header("Ulazni podaci")

# KOTE
teren = st.sidebar.number_input("Kota terena (m)", value=115.0)
niveleta = st.sidebar.number_input("Kota nivelete (m)", value=113.0)
nivo_vode = st.sidebar.number_input("Kota podzemne vode (m)", value=114.0)

# GEOMETRIJA
D = st.sidebar.number_input("Promjer okna D (m)", value=1.0)
a = st.sidebar.number_input("Stranica temelja a (m)", value=1.5)
t = st.sidebar.number_input("Debljina temeljne ploče (m)", value=0.3)
b = st.sidebar.number_input("Debljina betonskog prstena (m)", value=0.2)

# MATERIJALI
gamma_beton = st.sidebar.number_input("Spec. težina betona (kN/m3)", value=25.0)
gamma_tla = st.sidebar.number_input("Spec. težina tla (kN/m3)", value=18.0)
gamma_vode = st.sidebar.number_input("Spec. težina vode (kN/m3)", value=10.0)

# ------------------------
# FAKTOR SIGURNOSTI
# ------------------------
FS_min = st.sidebar.number_input("Traženi faktor sigurnosti", value=1.10)

# ------------------------
# KONTROLA KOTA
# ------------------------
if abs(teren - niveleta) > 10:
    st.warning("Razlika kote terena i nivelete je veća od 10 m – provjeri unos!")

# ------------------------
# OSNOVNE VISINE
# ------------------------
H_ukupno = teren - niveleta
H_voda = teren - nivo_vode

H_uronjeno = max(0,H_ukupno - H_voda)
#H_uronjeno = max(0, min(nivo_vode - niveleta, H_ukupno))
H_suho = H_ukupno - H_uronjeno

# ------------------------
# POVRŠINE
# ------------------------

R = D/2 + b
r = D/2

A_prsten = math.pi * (R**2 - r**2)
A_okno = math.pi * r**2
A_temelj = a * a

A_tlo = A_temelj - A_okno
A_prosirenje = A_temelj - math.pi * R**2

# ------------------------
# UZGON
# ------------------------
#U = gamma_vode * A_temelj * (H_uronjeno + t)
H_uzgon = max(0, nivo_vode - (niveleta - t))
U = gamma_vode * A_temelj * H_uzgon

# ------------------------
# ITERACIJA VISINE PRSTENA
# ------------------------

h_prsten = 0.0
korak = 0.05  # 5 cm

max_h = H_ukupno  # ne može biti viši od okna

FS = 0
h_ok = 0
FS_ok = 0
G_ok = 0
while FS <= FS_min:

    # TEŽINE

    # G1 – temelj
    G1 = A_temelj * t * gamma_beton

    # G2 – prsten
    G2 = A_prsten * h_prsten * gamma_beton

    # VISINE ZA TLO
    H_iznad_prstena = H_ukupno - h_prsten

    #H_uronjeno_iznad = max(0, min(H_iznad_prstena, H_uronjeno))
    H_uronjeno_iznad = max(0,H_ukupno-h_prsten-H_suho)
    H_suho_iznad = max (0, H_iznad_prstena - H_uronjeno_iznad)

    # G3 – uronjeno tlo iznad prstena
    G3 = A_prsten * H_uronjeno_iznad * gamma_tla

    # G3A – proširenje (uronjeno)
    G3A = A_prosirenje * H_uronjeno * gamma_tla

    # G4 – suho tlo iznad prstena
    G4 = A_prsten * H_suho_iznad * gamma_tla

    # G4A – proširenje (suho)
    G4A = A_prosirenje * H_suho * gamma_tla

    # UKUPNO
    G_total = G1 + G2 + G3 + G3A + G4 + G4A

    # UZGON
    #U = gamma_vode * A_temelj * H_uronjeno

    FS = G_total / U if U > 0 else 0

    if h_prsten >= H_ukupno - 0.05:
        break

    h_ok = h_prsten
    FS_ok = FS
    G_ok = G_total

    h_prsten += korak

h_prsten = h_ok
FS = FS_ok
G_total = G_ok

# KOREKCIJS MINIMSLNOG PRSTENA NAKON +korak
#if h_prsten == 0.05:
#    h_prsten = 0

# ------------------------
# SUMA
# ------------------------
G_total = G1 + G2 + G3 + G3A + G4 + G4A

with col1:
    # ------------------------
    # REZULTATI
    # ------------------------
    st.markdown("<h3 style='margin-top:0;'>Rezultati</h3>", unsafe_allow_html=True)

    st.write(f"Dubina okna = {H_ukupno:.2f} m")
    st.write(f"Visina podzemne vode = {H_uronjeno:.2f} m")

    st.write(f"Uzgon U = {U:.2f} kN")
    st.write(f"Ukupna težina ΣG = {G_total:.2f} kN")

    if U <= 0:
        FS = float("inf")
        h_prsten = 0

        st.write("Sigurnost protiv uzgona = ∞")
        st.success("Nema uzgona – prsten nije potreban")
    else:
        FS = G_total / U
        st.write(f"Sigurnost protiv uzgona = {FS:.2f}")

    st.write(f"Potrebna visina prstena = {h_prsten:.2f} m")

    if FS >= FS_min:
        st.success("OK – zadovoljava")
    else:
        st.error("NE zadovoljava")

    # ------------------------
    # KONTROLNI ISPIS
    # ------------------------
    st.subheader("Kontrola proračuna")

    st.write(f"G1 - Temeljna ploča = {G1:.2f} kN")
    st.write(f"G2 - Betonski prsten = {G2:.2f} kN")
    st.write(f"G3 - Uronjeno tlo (unutar prstena) = {G3:.2f} kN")
    st.write(f"G3A - Uronjeno tlo (proširenje) = {G3A:.2f} kN")
    st.write(f"G4 - Suho tlo (unutar prstena) = {G4:.2f} kN")
    st.write(f"G4A - Suho tlo (proširenje) = {G4A:.2f} kN")

    # ------------------------
    # DEBUG
    # ------------------------
    st.subheader("Debug")

    st.write(f"A_temelj = {A_temelj:.3f} m2")
    st.write(f"A_prstena = {A_prsten:.3f} m2")
    st.write(f"A_okna = {A_okno:.3f} m2")
    st.write(f"A_prosirenje = {A_prosirenje:.3f} m2")
    st.write(f"H_uronjeno = {H_uronjeno:.3f} m")
    st.write(f"H_suho = {H_suho:.3f} m")
    st.write(f"H_ukupno = {H_ukupno:.3f} m")
    st.write(f"H_uronjeno iznad = {H_uronjeno_iznad:.3f} m")
    st.write(f"H_prstena = {h_prsten:.3f} m")
    st.write(f"H_prstena = {h_ok:.3f} m")

with col2:
    #st.header("Grafički prikaz")
    st.markdown("<h3 style='margin-top:0;'>Grafički prikaz</h3>", unsafe_allow_html=True)

    fig = nacrtaj_presjek(
        teren,
        niveleta,
        nivo_vode,
        D,
        a,
        t,
        b,
        h_prsten,
        H_uzgon,
        H_uronjeno,
        H_suho
    )
    st.pyplot(fig, use_container_width=True)