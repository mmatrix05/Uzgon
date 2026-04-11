import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['hatch.linewidth'] = 0.1

def nacrtaj_presjek(
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
):
    fig, ax = plt.subplots(figsize=(6, 8))

    # KOTE
    y_teren = teren
    y_niveleta = niveleta
    y_dno = niveleta - t
    y_voda = nivo_vode

    # GEOMETRIJA
    half_a = a / 2
    r_okno = D / 2
    r_vanjski = D / 2 + b

    H_ukupno = teren - niveleta

    # ------------------------
    # TEMELJ
    # ------------------------
    ax.add_patch(plt.Rectangle(
        (-half_a, y_dno),
        a,
        t,
        facecolor='lightgrey',
        #hatch='///',
        linewidth=0.5,
        edgecolor='black'
    ))

    # OKNO (prazno - maska)
    ax.add_patch(plt.Rectangle(
        (-r_okno, y_niveleta),
        2 * r_okno,
        H_ukupno,
        facecolor='white',
        edgecolor='black',
        zorder=5
    ))

    # ------------------------
    # PRSTEN
    # ------------------------
    ax.add_patch(plt.Rectangle(
        (-r_vanjski, y_niveleta),
        2 * r_vanjski,
        h_prsten,
        facecolor='lightgrey',
        edgecolor='black'
    ))

    # ------------------------
    # TLO – PROŠIRENJE
    # ------------------------
    ax.add_patch(plt.Rectangle(
        (-half_a, y_niveleta),
        half_a - r_vanjski,
        H_ukupno,
        facecolor='#c2a280',
        hatch='..',
        edgecolor='black'
    ))

    ax.add_patch(plt.Rectangle(
        (r_vanjski, y_niveleta),
        half_a - r_vanjski,
        H_ukupno,
        facecolor='#c2a280',
        hatch='..',
        edgecolor='black'
    ))

    # ------------------------
    # TLO IZNAD PRSTENA
    # ------------------------
    ax.add_patch(plt.Rectangle(
        (-r_vanjski, y_niveleta + h_prsten),
        2 * r_vanjski,
        H_ukupno - h_prsten,
        facecolor='#c2a280',
        hatch='..',
        edgecolor='black'
    ))

    # ------------------------
    # VODA
    # ------------------------
    ax.axhline(y=y_voda, linestyle="--", color='blue', zorder=10)

    # VISINE
    H_ukupno = teren - niveleta
    y_dno = niveleta - t
    H_uzgon = max(0, nivo_vode - (niveleta - t))

    # VODA (poluprozirno)
    if H_uzgon > 0:
        ax.add_patch(plt.Rectangle(
            (-half_a, y_dno),
            a,
            H_uzgon,
            facecolor='blue',
            alpha=0.1,
            zorder=5
        ))

    # OZNAKE
    ax.text(0, y_teren, "Teren", ha='center', va='bottom')
    ax.text(0, y_niveleta, "Niveleta", ha='center', va='top')
    ax.text(0, y_voda, "Voda", ha='center', va='bottom', zorder=10)

    # POSTAVKE
    ax.set_xlim(-half_a - 0.5, half_a + 0.5)
    ax.set_ylim(y_dno - 1, y_teren + 1)

    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Presjek okna")

    return fig