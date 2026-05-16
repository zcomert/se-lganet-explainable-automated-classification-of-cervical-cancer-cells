# SE-LGANet

**Explainable automated classification of cervical cancer cells using
squeeze-and-excitation blocks and local & global attention mechanisms.**

SE-LGANet is a convolutional neural network that combines Squeeze-and-Excitation (SE)
blocks with a dual local/global attention mechanism for multi-class classification of
cervical Pap smear cells. The model is trained on the SIPaKMeD dataset and validated
on Mendeley LBC and Herlev. Grad-CAM is used as the explainability layer.

> Companion code for the manuscript: see [`docs/manuscript.md`](docs/manuscript.md).

## Highlights

- Synergizes SE blocks with dual-scale (local + global) attention to enhance feature
  extraction and cervical-cell classification accuracy.
- Integrates Grad-CAM for visual explanations, improving transparency in AI-driven
  diagnostics.
- Demonstrates high sensitivity and specificity, confirming robustness across cell
  categories.
- Reproducible across three public datasets: **SIPaKMeD**, **Mendeley LBC**, **Herlev**.

## Architecture

Three progressively stronger models are built (see manuscript §2.5):

1. **CNN** — baseline (Figure 1).
2. **CNN-SE** — CNN augmented with SE blocks (Figure 2).
3. **SE-LGANet** — adds batch normalisation, local attention per conv block, and a final
   global attention layer (Figure 3).

![SE-LGANet architecture](figures/image3.png)

## Results

Reported test-set performance (hold-out 80:20 split, batch 16, 128 epochs with early
stopping, Adam, lr = 1e-3):

| Model | Dataset | Accuracy | Sensitivity | Specificity | F1 | #Params |
|---|---|---|---|---|---|---|
| CNN | SIPaKMeD | 0.8728 | 0.8731 | 0.9682 | 0.8725 | 4,879,173 |
| CNN-SE | SIPaKMeD | 0.8975 | 0.8978 | 0.9744 | 0.8983 | 4,922,821 |
| **SE-LGANet** | **SIPaKMeD** | **0.9148** | **0.9157** | **0.9787** | **0.9151** | **2,916,197** |
| SE-LGANet | Mendeley LBC | 0.9688 | 0.9170 | 0.9912 | 0.9174 | — |
| SE-LGANet | Herlev (binary) | 0.8962 | 0.9343 | — | — | — |

See manuscript Tables 3–5 for full hyper-parameters and comparative literature.

## Repository structure

```
.
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── .gitignore
├── src/
│   ├── helper.py            # data loading & preprocessing utilities
│   └── confusion.py         # confusion matrix + performance metrics
├── notebooks/
│   ├── 01_cnn_baseline.ipynb            # CNN  — Figure 1
│   ├── 02_cnn_se.ipynb                  # CNN-SE — Figure 2
│   ├── 03_se_lganet_sipakmed.ipynb      # SE-LGANet on SIPaKMeD — Figure 3 (main)
│   ├── 04_se_lganet_mendeley_lbc.ipynb  # Mendeley LBC transfer — Figure 9
│   ├── 05_se_lganet_herlev.ipynb        # Herlev transfer — Figure 10
│   ├── 06_gradcam_cnn.ipynb             # Grad-CAM (CNN) — Figure 8a
│   ├── 07_gradcam_cnn_se.ipynb          # Grad-CAM (CNN-SE) — Figure 8b
│   ├── 08_gradcam_se_lganet.ipynb       # Grad-CAM (SE-LGANet) — Figures 8c, 9b, 10b
│   └── 09_intermediate_features.ipynb   # Intermediate-layer visualisation — Figure 7
├── data/
│   ├── README.md            # how to obtain the full datasets
│   └── samples/             # 1–2 example images per class (for quick inspection)
├── figures/                 # all manuscript figures (image1.png … image22.png)
└── docs/
    └── manuscript.md        # full paper text
```

## Installation

Python ≥ 3.10 and TensorFlow 2.x are required.

```bash
git clone <this-repo-url>
cd SE-LGANet
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

## Datasets

Only a handful of sample images are tracked (`data/samples/`). To reproduce the
full experiments, download the original datasets and follow the layout described in
[`data/README.md`](data/README.md):

- **SIPaKMeD** — <https://www.cs.uoi.gr/~marina/sipakmed.html>
- **Mendeley LBC** — <https://data.mendeley.com/datasets/zddtpgzv63/4>
- **Herlev** — <https://mde-lab.aegean.gr/index.php/downloads/>

## Reproducing the results

After installing dependencies and downloading the datasets, run the notebooks in
order:

1. `notebooks/01_cnn_baseline.ipynb` — baseline CNN on SIPaKMeD.
2. `notebooks/02_cnn_se.ipynb` — CNN-SE on SIPaKMeD.
3. `notebooks/03_se_lganet_sipakmed.ipynb` — **proposed SE-LGANet** on SIPaKMeD.
4. `notebooks/04_se_lganet_mendeley_lbc.ipynb` — transfer to Mendeley LBC.
5. `notebooks/05_se_lganet_herlev.ipynb` — transfer to Herlev (binary).
6. `notebooks/06_gradcam_cnn.ipynb` to `08_gradcam_se_lganet.ipynb` — Grad-CAM visualisations.
7. `notebooks/09_intermediate_features.ipynb` — intermediate-layer feature maps.

Each notebook saves model weights and history to the working directory; these are
git-ignored (see below).

## Pretrained weights

Trained `.h5` weights and `.pkl` training histories are **not** committed to the
repository (size and licensing). Re-training the three models on SIPaKMeD takes
roughly 1–2 hours per model on a single NVIDIA P6000-class GPU; see the manuscript
for the exact training environment and hyper-parameters.

## Citation

If you use this code or the SE-LGANet architecture, please cite:

```bibtex
@article{alcin2026selganet,
  title   = {SE-LGANet: Explainable automated classification of cervical cancer cells
             using squeeze-and-excitation blocks and local and global attention mechanisms},
  author  = {Al{\c{c}}in, {\"O}mer Faruk and Aslan, Muzaffer and C{\"o}mert, Zafer},
  year    = {2026},
  note    = {Manuscript}
}
```

A machine-readable citation record is provided in [`CITATION.cff`](CITATION.cff).

## License

Source code is released under the [MIT License](LICENSE). The included sample
images remain subject to the licenses of their original datasets (SIPaKMeD,
Mendeley LBC, Herlev) and are redistributed here only for illustrative purposes.

## Authors

- **Ömer Faruk Alçin** — Department of Software Engineering, Inonu University,
  Malatya, Turkiye · <omer.alcin@inonu.edu.tr>
- **Muzaffer Aslan** — Department of Electrical and Electronics Engineering,
  Bingol University, Bingol, Turkiye · <muzafferaslan@bingol.edu.tr>
- **Zafer Cömert** — Department of Software Engineering, Samsun University,
  Samsun, Turkiye · <zcomert@samsun.edu.tr>
