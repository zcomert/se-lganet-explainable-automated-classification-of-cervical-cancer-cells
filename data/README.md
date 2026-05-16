# Datasets

This repository ships only a **handful of sample images per class** (see `samples/`) so that
notebooks can be opened and inspected without external downloads. To reproduce the
results reported in the manuscript, please download the full public datasets from their
official sources and place them under `data/` as described below.

## 1. SIPaKMeD (primary dataset)

- Source: Plissiti et al., *SIPaKMeD: A New Dataset for Feature and Image Based Classification of Normal and Pathological Cervical Cells in Pap Smear Images*, ICIP 2018.
- DOI: <https://doi.org/10.1109/ICIP.2018.8451588>
- Download: <https://www.cs.uoi.gr/~marina/sipakmed.html>

Expected layout after extraction (used by `notebooks/01–03` and `notebooks/06–09`):

```
data/sipakmed/
├── train/
│   ├── im_Dyskeratotic/
│   ├── im_Koilocytotic/
│   ├── im_Metaplastic/
│   ├── im_Parabasal/
│   └── im_Superficial-Intermediate/
└── test/
    └── (same five subfolders)
```

Split ratio: 80% train / 20% test (Section 2.1, Table 1 of the manuscript).

## 2. Mendeley LBC

- Source: Hussain et al., *Liquid based-cytology Pap smear dataset for automated multi-class diagnosis of pre-cancerous and cervical cancer lesions*, Data in Brief 2020.
- DOI: <https://doi.org/10.1016/j.dib.2020.105589>
- Download: <https://data.mendeley.com/datasets/zddtpgzv63/4>

Expected layout (used by `notebooks/04`):

```
data/mendeley_lbc/
├── train/
│   ├── High_squamous_intra_epithelial_lesion/
│   ├── Low_squamous_intra_epithelial_lesion/
│   ├── Negative_for_intraepithelial_malignancy/
│   └── Squamous_cell_carcinoma/
└── test/
    └── (same four subfolders)
```

## 3. Herlev (binary)

- Source: Jantzen et al., *Pap-smear Benchmark Data For Pattern Classification*, NiSIS 2005.
- Download: <https://mde-lab.aegean.gr/index.php/downloads/>

Expected layout (binary, used by `notebooks/05`):

```
data/herlev/
├── train/
│   ├── normal/
│   └── abnormal/
└── test/
    ├── normal/
    └── abnormal/
```

## Notes

- These dataset folders are git-ignored (see `.gitignore`); only `data/samples/` is tracked.
- All datasets are publicly distributed for research use; please honour the original
  authors' citation requests when reusing them.
