"""
Complex Exponential Map: w = e^z
Domain coloring: hue encodes arg(w), brightness encodes |w|.
Shows how vertical strips in the z-plane map to annuli in the w-plane.
"""
import matplotlib
matplotlib.use('Agg')

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from utils.plot_style import apply_euler_style, save_plot, COLORS

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')


def domain_color(w):
    """
    Convert complex array w to RGB image using domain coloring.
    Hue  = arg(w) mapped to [0, 1]
    Value= tanh(|w|) so brightness saturates gracefully
    Saturation = 0.85 (vivid)
    """
    angle = np.angle(w)                        # -π to π
    hue = (angle + np.pi) / (2 * np.pi)       # 0 to 1
    mag = np.abs(w)
    value = np.tanh(mag / 3)                   # compress magnitude
    sat = np.ones_like(hue) * 0.85

    hsv = np.stack([hue, sat, value], axis=-1)
    rgb = mcolors.hsv_to_rgb(hsv)
    return rgb


def main():
    apply_euler_style()

    # ── Input grid ────────────────────────────────────────────────────────
    res = 600
    x_range = np.linspace(-2.5, 2.5, res)
    y_range = np.linspace(-np.pi, np.pi, res)
    X, Y = np.meshgrid(x_range, y_range)
    Z = X + 1j * Y          # z = x + iy
    W = np.exp(Z)            # w = e^z

    # Domain-coloring of the output
    rgb_out = domain_color(W)

    # For the input panel: color by real part stripes (to visualize strips)
    stripe_hue = (np.mod(X, 1.0))              # periodic stripes in real part
    stripe_sat = np.ones_like(stripe_hue) * 0.7
    stripe_val = 0.5 + 0.5 * np.tanh(Y / np.pi)
    rgb_in = mcolors.hsv_to_rgb(
        np.stack([stripe_hue, stripe_sat, stripe_val], axis=-1)
    )

    fig, (ax_in, ax_out) = plt.subplots(1, 2, figsize=(18, 9))
    fig.patch.set_facecolor(COLORS['bg_dark'])
    fig.suptitle(
        r'Complex Exponential Map: $w = e^z$',
        fontsize=22, color=COLORS['e_gold'], fontweight='bold'
    )

    # ── Left: input domain ─────────────────────────────────────────────
    ax_in.set_facecolor(COLORS['bg_card'])
    ax_in.imshow(rgb_in, origin='lower',
                 extent=[x_range[0], x_range[-1], y_range[0], y_range[-1]],
                 aspect='auto')

    # Overlay grid lines for vertical strips
    for xv in np.arange(-2, 3, 0.5):
        ax_in.axvline(xv, color='white', lw=0.5, alpha=0.4)
    for yv in np.arange(-np.pi, np.pi + 0.1, np.pi / 4):
        ax_in.axhline(yv, color='white', lw=0.5, alpha=0.4)

    # Highlight one strip: 0 ≤ Re(z) ≤ 1
    from matplotlib.patches import Rectangle
    strip = Rectangle((0, -np.pi), 1, 2 * np.pi,
                       linewidth=2.5, edgecolor=COLORS['e_gold'],
                       facecolor=COLORS['e_gold'], alpha=0.12)
    ax_in.add_patch(strip)
    ax_in.text(0.5, 0, 'Vertical\nStrip\n$0 \\leq \\mathrm{Re}(z) \\leq 1$',
               ha='center', va='center', color=COLORS['e_gold'], fontsize=10,
               fontweight='bold',
               bbox=dict(facecolor=COLORS['bg_dark'], alpha=0.6, pad=3))

    ax_in.set_xlabel('Re(z)', color=COLORS['text'])
    ax_in.set_ylabel('Im(z)', color=COLORS['text'])
    ax_in.set_title('Input: z-plane  (strips color-coded)', color=COLORS['text'])
    ax_in.set_yticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    ax_in.set_yticklabels(['-π', '-π/2', '0', 'π/2', 'π'])

    # ── Right: output domain coloring ────────────────────────────────────
    ax_out.set_facecolor(COLORS['bg_card'])
    im = ax_out.imshow(rgb_out, origin='lower',
                       extent=[x_range[0], x_range[-1], y_range[0], y_range[-1]],
                       aspect='auto')

    # Draw unit circle in the output (|w|=1 ↔ Re(z)=0)
    circ_t = np.linspace(-np.pi, np.pi, 300)
    # In the mapped output, the unit circle corresponds to x=0
    # Overlay: for each y we know |e^(iy)| = 1, so draw the vertical line x=0
    ax_out.axvline(0, color='white', lw=1.5, alpha=0.7, linestyle='--',
                   label='|w|=1  (Re(z)=0)')
    ax_out.axvline(1, color=COLORS['e_gold'], lw=1.5, alpha=0.7, linestyle='--',
                   label='|w|=e  (Re(z)=1)')
    ax_out.legend(fontsize=9, facecolor=COLORS['bg_dark'],
                  edgecolor=COLORS['grid'], labelcolor=COLORS['text'],
                  loc='upper right')

    ax_out.set_xlabel('Re(z)', color=COLORS['text'])
    ax_out.set_ylabel('Im(z)', color=COLORS['text'])
    ax_out.set_title(
        r'Output: domain coloring of $e^z$' + '\n'
        r'Hue = $\arg(e^z)$, Brightness = $\tanh(|e^z|)$',
        color=COLORS['text']
    )
    ax_out.set_yticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    ax_out.set_yticklabels(['-π', '-π/2', '0', 'π/2', 'π'])

    # Colorwheel legend
    legend_ax = fig.add_axes([0.91, 0.1, 0.04, 0.35])
    th_leg = np.linspace(0, 2 * np.pi, 256)
    hue_leg = th_leg / (2 * np.pi)
    sat_leg = np.ones(256) * 0.85
    val_leg = np.ones(256) * 0.85
    hsv_leg = np.stack([hue_leg, sat_leg, val_leg], axis=-1)[np.newaxis, :, :]
    rgb_leg = mcolors.hsv_to_rgb(hsv_leg)
    legend_ax.imshow(np.rot90(rgb_leg, 1), aspect='auto', origin='lower')
    legend_ax.set_xticks([])
    legend_ax.set_yticks([0, 64, 128, 192, 255])
    legend_ax.set_yticklabels(['-π', '-π/2', '0', 'π/2', 'π'],
                               color=COLORS['text'], fontsize=8)
    legend_ax.set_title('arg(w)', color=COLORS['text'], fontsize=8)

    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    save_plot(fig, 'complex_exp_map', OUTPUT_DIR)
    plt.close(fig)
    print("complex_exp_map.py done.")


if __name__ == '__main__':
    main()
