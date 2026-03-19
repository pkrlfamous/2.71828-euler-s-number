"""
Mandelbrot Set with smooth escape-time coloring using natural logarithm (base e).
Smooth color = iteration + 1 - log(log(|z|)) / log(2)
This formula connects the Mandelbrot fractal to Euler's number e.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

MAX_ITER = 256
ESCAPE_RADIUS = 256.0   # large radius for smooth coloring


def mandelbrot_smooth(c_grid, max_iter=MAX_ITER, escape_r=ESCAPE_RADIUS):
    """
    Compute smooth iteration count for each point in c_grid.
    Returns float array with smooth escape values; interior = NaN.
    """
    z = np.zeros_like(c_grid, dtype=complex)
    smooth = np.full(c_grid.shape, np.nan, dtype=float)
    active = np.ones(c_grid.shape, dtype=bool)

    log_log_r = math.log(math.log(escape_r))
    log2 = math.log(2)

    for i in range(1, max_iter + 1):
        z[active] = z[active] ** 2 + c_grid[active]
        escaped = active & (np.abs(z) > escape_r)
        if escaped.any():
            absz = np.abs(z[escaped])
            # smooth = iter + 1 - log(log(|z|)) / log(2)
            smooth[escaped] = i + 1.0 - (np.log(np.log(absz)) - log_log_r) / log2
        active[escaped] = False
        if not active.any():
            break

    return smooth


def main():
    apply_euler_style()

    res = 900
    x_min, x_max = -2.5, 1.0
    y_min, y_max = -1.25, 1.25

    x = np.linspace(x_min, x_max, res)
    y = np.linspace(y_min, y_max, res)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y

    print("  Computing Mandelbrot set (this may take a moment)...")
    smooth = mandelbrot_smooth(C)

    fig = plt.figure(figsize=(18, 10))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r'Mandelbrot Set — Smooth Coloring via $\ln$ (Euler\'s $e$)',
        fontsize=20, color=COLORS['e_gold'], fontweight='bold'
    )

    # ── Main Mandelbrot ───────────────────────────────────────────────────
    ax_main = fig.add_subplot(1, 2, 1)
    ax_main.set_facecolor('#000000')

    # Interior = black; exterior = smooth gradient
    display = np.where(np.isnan(smooth), -1.0, smooth)
    cmap = plt.cm.inferno  # type: ignore[attr-defined]
    cmap_copy = mcolors.ListedColormap(cmap(np.linspace(0, 1, 512)))
    norm = mcolors.PowerNorm(gamma=0.4, vmin=0, vmax=MAX_ITER)

    img_data = np.where(np.isnan(smooth), np.nan, smooth)
    ax_main.imshow(
        np.where(np.isnan(smooth), np.nan, smooth),
        origin='lower', extent=[x_min, x_max, y_min, y_max],
        cmap='inferno', norm=norm, aspect='auto'
    )
    # Black for interior (NaN → use set_bad)
    cmap_main = plt.cm.inferno.copy()  # type: ignore[attr-defined]
    cmap_main.set_bad(color='black')
    ax_main.cla()
    ax_main.set_facecolor('#000000')
    masked = np.ma.array(smooth, mask=np.isnan(smooth))
    ax_main.imshow(masked, origin='lower',
                   extent=[x_min, x_max, y_min, y_max],
                   cmap=cmap_main, norm=norm, aspect='auto')

    ax_main.set_xlabel('Re(c)', color=COLORS['text'])
    ax_main.set_ylabel('Im(c)', color=COLORS['text'])
    ax_main.set_title('Mandelbrot Set\n(black = bounded, colors = escape speed)',
                      color=COLORS['text'])

    cbar = fig.colorbar(
        plt.cm.ScalarMappable(norm=norm, cmap=cmap_main),  # type: ignore[attr-defined]
        ax=ax_main, fraction=0.04, pad=0.02
    )
    cbar.set_label('Smooth iteration count', color=COLORS['text'])
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=COLORS['text'])

    # ── Zoom panel ───────────────────────────────────────────────────────
    ax_zoom = fig.add_subplot(1, 2, 2)
    ax_zoom.set_facecolor('#000000')

    zx_min, zx_max = -0.76, -0.72
    zy_min, zy_max =  0.09,  0.13
    xz = np.linspace(zx_min, zx_max, res)
    yz = np.linspace(zy_min, zy_max, res)
    Xz, Yz = np.meshgrid(xz, yz)
    Cz = Xz + 1j * Yz
    smooth_z = mandelbrot_smooth(Cz)
    masked_z = np.ma.array(smooth_z, mask=np.isnan(smooth_z))

    ax_zoom.imshow(masked_z, origin='lower',
                   extent=[zx_min, zx_max, zy_min, zy_max],
                   cmap=cmap_main, norm=norm, aspect='auto')
    ax_zoom.set_xlabel('Re(c)', color=COLORS['text'])
    ax_zoom.set_ylabel('Im(c)', color=COLORS['text'])
    ax_zoom.set_title(
        f'Zoom: Re ∈ [{zx_min}, {zx_max}], Im ∈ [{zy_min}, {zy_max}]',
        color=COLORS['text']
    )

    # Formula annotation
    formula = (
        r"Smooth color = $n + 1 - \frac{\ln(\ln|z_n|)}{\ln 2}$" + "\n\n"
        r"where $\ln = \log_e$,  $e = 2.71828\ldots$" + "\n"
        r"This eliminates discrete banding artifacts."
    )
    ax_zoom.text(0.02, 0.02, formula, transform=ax_zoom.transAxes,
                 fontsize=9.5, color=COLORS['e_gold'],
                 bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['bg_dark'],
                           edgecolor=COLORS['e_gold'], alpha=0.9))

    # Show zoom box on main
    from matplotlib.patches import Rectangle
    rect = Rectangle((zx_min, zy_min), zx_max - zx_min, zy_max - zy_min,
                      linewidth=2, edgecolor=COLORS['e_gold'],
                      facecolor='none', linestyle='--', zorder=10)
    ax_main.add_patch(rect)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_plot(fig, 'mandelbrot_connection', OUTPUT_DIR)
    plt.close(fig)
    print("mandelbrot_connection.py done.")


if __name__ == '__main__':
    main()
