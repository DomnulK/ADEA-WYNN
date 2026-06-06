# ADEA - Proiect empiric: Wynn Resorts (WYNN)

Proiect empiric pentru cursul *Analiza datelor si econometrie aplicata* (ADEA),
Academia de Studii Economice Bucuresti, 2026.

**Autor:** Serban Dumitrescu
**Coordonator:** Conf. dr. Virgil Damian
**Activ analizat:** Wynn Resorts, Limited (NASDAQ: WYNN)

## Prezentare

Proiectul aplica analiza distributionala si modelare statistica asupra
rentabilitatilor Wynn Resorts, structurat in doua parti.

### Partea 1 - Distributia rentabilitatilor zilnice
Date zilnice 2005-2026 (~21 ani, 5363 observatii). Statistici descriptive,
KDE, teste de normalitate, estimare MLE pentru Student-*t* si NIG, comparatie
prin criterii informationale, si analiza cozilor cu modele GPD.

**Rezultate principale:**
- Normalitatea este respinsa categoric (cozi grele, excess kurtosis = 8,2).
- NIG este distributia globala selectata (AIC/BIC), urmata de Student-*t*
  (ν ≈ 2,9, kurtosis teoretic infinit).
- Analiza GPD arata asimetrie in regimul extrem: coada pierderilor
  (ξ = 0,23) este mai grea decat coada castigurilor (ξ = 0,10).

### Partea 2 - Numarul de modificari de pret intra-day
Date la 1 minut pe ultimele 7 zile de tranzactionare, agregate in contoare
orare. Modelare Poisson si testarea adecvarii ei.

**Rezultate principale:**
- Seria este puternic supradispersata (var/medie = 2,34); Poisson este respins
  (test de dispersie si chi-patrat).
- Binomiala negativa ofera o potrivire net superioara (AIC/BIC).
- Supradispersia este in mare parte structurala: ora de deschidere a pietei
  contine doar ~30 min de tranzactionare. Excluzand-o, indicele de dispersie
  scade la ~1,1.

## Structura

    .
    ├── data/                              # Date pre-descarcate (CSV)
    ├── scripts/
    │   ├── 01_data_pull.py                # Date zilnice (yfinance)
    │   └── 02_data_pull.py                # Date intra-day + contoare orare
    ├── notebooks/
    │   ├── 01_part1_distributii_globale.ipynb
    │   └── 02_part2_intraday_poisson.ipynb
    └── README.md

## Reproducere

```bash
conda create -n adea python=3.11 -y
conda activate adea
conda install -y numpy pandas scipy matplotlib seaborn statsmodels jupyter ipykernel
pip install yfinance arch

python scripts/01_data_pull.py
python scripts/02_data_pull.py
jupyter notebook
```

## Sursa datelor

Yahoo Finance via `yfinance`. Rentabilitati zilnice ca log-randamente:
*r*ₜ = ln(*P*ₜ / *P*ₜ₋₁).