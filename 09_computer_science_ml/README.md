# Module 09 — Computer Science & Machine Learning

Euler's number **e** is woven into the mathematical fabric of modern machine
learning.  Every sigmoid gate, every softmax layer, every attention head, and
every learning-rate scheduler uses exponentials under the hood.  This module
visualises those connections.

---

## Scripts

| File | Formula | Output |
|------|---------|--------|
| `sigmoid_function.py` | σ(x) = 1/(1+e⁻ᵏˣ) | `sigmoid_softmax_ce.png/svg` |
| `softmax_function.py` | softmax(xᵢ) = eˣⁱ/Σeˣʲ | `softmax_function.png/svg` |
| `cross_entropy_loss.py` | L = −Σ y·ln(ŷ) | `cross_entropy_loss.png/svg` |
| `learning_rate_decay.py` | lr(t) = lr₀·e⁻λᵗ | `learning_rate_decay.png/svg` |
| `normal_distribution_ml.py` | He: σ=√(2/n), Xavier: σ=√(1/n) | `normal_distribution_ml.png/svg` |
| `batch_norm.py` | μ_EMA = β·μ_EMA + (1−β)·μ_batch | `batch_norm.png/svg` |
| `attention_mechanism.py` | softmax(QKᵀ/√d)·V | `attention_mechanism.png/svg` |
| `gradient_descent_viz.py` | Exponential loss surface | `gradient_descent_viz.png/svg` |
| `information_entropy.py` | H = −Σ pᵢ·ln pᵢ | `information_entropy.png/svg` |
| `algorithm_complexity.py` | O(eⁿ) complexity | `algorithm_complexity.png/svg` |
| `neural_network_init.py` | He/Xavier weight init | `neural_network_init.png/svg` |

---

## Key Concepts

### Sigmoid & Softmax
The logistic sigmoid σ(x) = 1/(1+e⁻ˣ) squashes any real number into (0,1),
making it suitable as a probability.  Softmax generalises this to multiple
classes: each class gets probability proportional to eˣⁱ, so the distribution
sums to 1.  Temperature T controls sharpness — low T makes the distribution
peaked, high T flattens it toward uniform.

### Cross-Entropy Loss
Binary CE loss L = −[y·log p̂ + (1−y)·log(1−p̂)] penalises wrong predictions
logarithmically — a prediction of 0.01 when the true label is 1 incurs a loss
of −log(0.01) ≈ 4.6 nats, while a prediction of 0.99 incurs only −log(0.99) ≈
0.01 nats.  The steep gradient near wrong predictions drives fast learning.

### Learning Rate Decay
Exponential decay lr(t) = lr₀·e⁻λᵗ is the natural continuous analogue of
step decay.  It guarantees the learning rate is always positive and decreases
smoothly, preventing oscillation late in training.

### Weight Initialisation
Random weights drawn from N(0, σ²) must be scaled with the network width:
- **He init** σ = √(2/nᵢₙ) — designed for ReLU activations; maintains variance
  across layers.
- **Xavier init** σ = √(1/nᵢₙ) — designed for symmetric activations (tanh,
  sigmoid).
Without proper initialisation, activations either explode (σ too large) or
vanish (σ too small) after a handful of layers.

### Batch Normalisation & EMA
Batch norm standardises layer inputs each mini-batch, then re-scales with
learnable γ and β.  At inference, running statistics are tracked via
exponential moving averages: μ_EMA = β·μ_EMA + (1−β)·μ_batch.  Higher β
means more momentum (slower adaptation to distribution shifts).

### Attention Mechanism
Scaled dot-product attention weights are computed as softmax(QKᵀ/√d).  The
√d scaling prevents the dot products from growing large (high variance when d
is large), which would push the softmax into saturation and kill gradients.

### Information Entropy
Shannon entropy H = −Σ pᵢ·ln pᵢ (in nats, using natural log) measures the
average surprise.  It is maximised for the uniform distribution (H = ln n) and
equals zero for a deterministic distribution.  Cross-entropy loss is the
expected log-loss under the true distribution.

### Algorithm Complexity
O(eⁿ) and O(2ⁿ) algorithms become intractable even for moderate n.  For n=30,
O(eⁿ) ≈ 10¹³ operations — 10 seconds at 1 GHz, while O(n!) ≈ 2.6×10³²
operations — over 10²² years.

---

## Running the Scripts

```bash
cd 09_computer_science_ml
python sigmoid_function.py
python softmax_function.py
python cross_entropy_loss.py
python learning_rate_decay.py
python normal_distribution_ml.py
python batch_norm.py
python attention_mechanism.py
python gradient_descent_viz.py
python information_entropy.py
python algorithm_complexity.py
python neural_network_init.py
```

Outputs are saved to `outputs/` as both `.png` and `.svg`.
