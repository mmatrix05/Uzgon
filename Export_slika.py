import matplotlib.pyplot as plt

# import tvoje funkcije za crtanje
from plot_presjek import nacrtaj_presjek
from io import BytesIO

def export_slika(
    teren, niveleta, nivo_vode,
    D, a, t, b,
    FS, h_prsten,
    U, G_total,
    file_name="proracun_okno.png"
):
    # -------------------------
    # POSTAVKE
    # -------------------------
    cm_to_inch = 1 / 2.54

    fig_width = 17 * cm_to_inch
    fig_height = 20 * cm_to_inch  # max ~23 cm → uzmemo sigurnu vrijednost

    plt.rcParams['font.family'] = 'Calibri'
    plt.rcParams['font.size'] = 11

    # -------------------------
    # FIGURA
    # -------------------------
    fig, (ax_text, ax_plot) = plt.subplots(
        1, 2,
        figsize=(fig_width, fig_height),
        gridspec_kw={'width_ratios': [1, 1.5]}
    )

    # -------------------------
    # LIJEVO – TEKST
    # -------------------------
    ax_text.axis('off')

    tekst = f"""ULAZNI PODACI

Kota terena: {teren:.2f} m
Kota nivelete: {niveleta:.2f} m
Razina vode: {nivo_vode:.2f} m

Promjer okna: {D:.2f} m
Temelj: {a:.2f} x {a:.2f} m
Debljina temelja: {t:.2f} m
Debljina prstena: {b:.2f} m


REZULTATI

Uzgon U: {U:.2f} kN
Ukupna težina ΣG: {G_total:.2f} kN
"""

    ax_text.text(0, 1, tekst, va='top')

    # ISTAKNUTI REZULTATI
    ax_text.text(
        0, 0.35,
        f"FS = {FS:.2f}",
        fontsize=12,
        fontweight='bold'
    )

    ax_text.text(
        0, 0.30,
        f"Potrebna visina prstena = {h_prsten:.2f} m",
        fontsize=12,
        fontweight='bold'
    )

    # -------------------------
    # DESNO – SKICA
    # -------------------------
    nacrtaj_presjek(
        teren,
        niveleta,
        nivo_vode,
        D,
        a,
        t,
        b,
        h_prsten,
        ax=ax_plot  # KLJUČNO!
    )

    # -------------------------
    # FINAL TOUCH
    # -------------------------
    buffer = BytesIO()
    plt.savefig(buffer, dpi=300, bbox_inches='tight')
    plt.close(fig)

    buffer.seek(0)
    return buffer

    #plt.savefig("temp.png", dpi=300, bbox_inches='tight')
    #plt.close(fig)