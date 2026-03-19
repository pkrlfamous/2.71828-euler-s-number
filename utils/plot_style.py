"""
Shared plot styling for all e-related visualizations.
Dark theme with accent colors. All plots saved as PNG + SVG.
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# Color palette
COLORS = {
    'e_gold': '#FFD700',
    'e_blue': '#4A90D9',
    'e_red': '#E74C3C',
    'e_green': '#2ECC71',
    'e_purple': '#9B59B6',
    'e_orange': '#F39C12',
    'e_cyan': '#00D2FF',
    'e_pink': '#FF6B9D',
    'bg_dark': '#1A1A2E',
    'bg_card': '#16213E',
    'text': '#EAEAEA',
    'grid': '#2A2A4A',
}


def apply_euler_style():
    """Apply consistent dark theme to all matplotlib plots."""
    plt.style.use('dark_background')
    mpl.rcParams.update({
        'figure.facecolor': COLORS['bg_dark'],
        'axes.facecolor': COLORS['bg_card'],
        'axes.edgecolor': COLORS['grid'],
        'axes.labelcolor': COLORS['text'],
        'text.color': COLORS['text'],
        'xtick.color': COLORS['text'],
        'ytick.color': COLORS['text'],
        'grid.color': COLORS['grid'],
        'grid.alpha': 0.3,
        'font.size': 12,
        'axes.titlesize': 16,
        'figure.figsize': (12, 8),
        'savefig.dpi': 150,
        'savefig.bbox': 'tight',
    })


def save_plot(fig, name, output_dir='outputs'):
    """Save figure as both PNG and SVG."""
    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(f'{output_dir}/{name}.png')
    fig.savefig(f'{output_dir}/{name}.svg')
    print(f'Saved: {output_dir}/{name}.png and .svg')
