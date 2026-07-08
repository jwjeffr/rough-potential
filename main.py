from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from config import CONFIG


def main():

    fig = plt.figure(figsize=(20, 5))
    ax = fig.add_subplot(111)
    ax_inset = ax.inset_axes(
        [1.15, 0.5, 0.8, 0.65],
        xlim=(-0.05, 0.65),
        ylim=(0.655, 1.045)
    )
    ax.indicate_inset_zoom(ax_inset, edgecolor="black")
    ax_inset.grid()

    for num_dims in range(1, 5 + 1):

        path = Path("diffusionRoughPotentialKMC") / \
               f"diffusionCoefficientRoughPot-T{CONFIG.temperature}-EsEl-{num_dims}D.txt"
        sigmas_kmc, _, diffusivities, error_bars = np.loadtxt(path).T
        ratios = diffusivities / diffusivities[0]
        ratio_error_bars = ratios * np.sqrt(
            (error_bars / diffusivities) ** 2 + (error_bars[0] / diffusivities[0] ** 2)
        )
        ratio_error_bars[0] = 0.0
        for a in (ax, ax_inset):
            a.errorbar(
                CONFIG.beta * sigmas_kmc,
                ratios,
                yerr=ratio_error_bars,
                fmt="o",
                alpha=0.6,
                zorder=6,
                color=CONFIG.colors[str(num_dims)],
                label=rf"KMC {num_dims}d",
                capsize=4
            )

    for num_dims in range(1, 5 + 1):
        βσ_vals = np.linspace(0.0, 2.0, 1_000)
        ratios = np.exp(βσ_vals ** 2 / num_dims)

        for a in (ax, ax_inset):
            a.plot(
                βσ_vals,
                1.0 / ratios,
                label=rf"$\exp(-\beta^2\sigma^2/{num_dims:0d})$",
                color=CONFIG.colors[str(num_dims)],
                linewidth=2.5
            )

    ax.legend(ncol=2, bbox_to_anchor=(1.425, -0.1, 0.5, 0.5))
    ax.set_xlabel(r"$\beta\sigma$")
    ax.set_ylabel(r"$D/D^*$")
    ax.grid()

    top_ax = ax.secondary_xaxis(
        "top",
        functions=(lambda βσ: βσ / CONFIG.beta, lambda σ: CONFIG.beta * σ)
    )
    top_ax.set_xlabel(rf"$\sigma$ (eV) at T = {CONFIG.temperature:.0f} K")

    ax.text(0.125, 0.1, "(a)", ha="center", va="center", fontdict={"size": 25})
    ax_inset.text(0.1, 0.725, "(b)", ha="center", va="center", fontdict={"size": 25})

    fig.tight_layout()
    plt.show()
    fig.savefig("ratio.pdf", dpi=800, bbox_inches="tight")


if __name__ == "__main__":

    plt.rcParams["font.size"] = 12
    mpl.use("TkAgg")
    main()
