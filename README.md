# Real Estate Hedonic Price Model (Korea)

> Hedonic pricing models for Korean apartment transactions with spatial autocorrelation correction

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

## Problem

Korean real estate analysis commonly uses naive OLS hedonic models that violate spatial independence assumptions. Apartments in Seoul's Gangnam district exhibit strong spatial clustering — a model that ignores this produces biased implicit price estimates for structural, neighborhood, and locational attributes.

## Solution

A rigorous hedonic pricing framework with:

1. **Classical Hedonic** (Rosen, 1974) as OLS baseline
2. **Spatial Hedonic** with SAR/SEM correction (PySAL/spreg)
3. **Hierarchical Linear Model** for dong(동)-level nesting
4. **MOLIT API integration** for real-time transaction data pipeline

## Data Pipeline

```
MOLIT 실거래가 API → Cleaning → Geocoding (Kakao) → Spatial Join (행정동)
→ Feature Engineering → Model Estimation → Implicit Price Report
```

## Key Variables

| Category | Variables |
|----------|----------|
| **Structural** | Floor area, floor level, age, total units, parking ratio |
| **Neighborhood** | School quality (학군), park proximity, commercial density |
| **Transportation** | Subway distance, bus stops count, road accessibility |
| **Environmental** | Noise level, view quality, slope, flood risk zone |

## Repository Structure

```
real-estate-hedonic/
├── src/
│   ├── molit_api.py            # MOLIT 실거래가 API wrapper
│   ├── geocoder.py             # Kakao/V-World geocoding
│   ├── feature_builder.py      # Structural + neighborhood features
│   ├── hedonic_models.py       # OLS, SAR, SEM, GWR
│   └── implicit_prices.py      # Marginal willingness-to-pay calculator
├── notebooks/
│   ├── 01_data_collection_molit.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_spatial_hedonic_estimation.ipynb
│   └── 04_implicit_price_analysis.ipynb
├── data/
│   └── README.md
├── docs/
│   └── variable_codebook.md
├── tests/
├── requirements.txt
└── LICENSE
```

## Quick Start

```bash
git clone https://github.com/DongsooJung/real-estate-hedonic.git
cd real-estate-hedonic
pip install -r requirements.txt

# MOLIT API 키 설정
export MOLIT_API_KEY="your_key_here"

jupyter notebook notebooks/01_data_collection_molit.ipynb
```

## Sample Output

| Attribute | OLS Implicit Price | Spatial Hedonic | Δ |
|-----------|-------------------|-----------------|---|
| 1㎡ floor area | — | — | — |
| 1 floor higher | — | — | — |
| 1min closer to subway | — | — | — |
| Top school district | — | — | — |

*Results populated with Seoul Gangnam-gu 2024 transaction data.*

## References

- Rosen, S. (1974). Hedonic Prices and Implicit Markets. *JPE*.
- Can, A. (1992). Specification and Estimation of Hedonic Housing Price Models. *Regional Science and Urban Economics*.
- 국토교통부. 실거래가 공개시스템 API 문서.

## License

MIT License

## Author

**Dongsoo Jung** — SNU Ph.D. Candidate · Smart City Engineering  
Research Focus: Spatial Econometrics × Real Estate × Urban Policy
