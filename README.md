# Metagenomic Analysis Pipeline for Rhizospheric Microbiome of Coffea canephora L.

## Overview
Instructions for replicating the metagenomic analysis of the rhizospheric microbiome of Coffea canephora L. in the Central Highlands region, Vietnam [1]. The pipeline includes data preprocessing, taxonomic and functional analyses using QIIME2 and PICRUSt2, and visualization with Krona.

### About Project:
All files are stored on Google Cloud in the 'AS41073481-dmach1' project within the 'metagenomics' instance.

NOTE: My username on the on the Google Cloud instance is 'ethanmach1998'

### Prerequisites
- Docker
- Conda
- QIIME2 (version 2020.8)
- PICRUSt2 (version 2.3.0-b)
- KronaTools

## Workflow Steps

### 1. Data Preprocessing
Quality control is performed using bcl2fastq, Trimmomatic, and Cutadapt.
- Minimum average score: ≥20
- Minimum read length: ≥100
- Download the SRA data using:
  - ```
    cd /home/ethanmach1998/final/samples
    ``` 
  - ```$ fasterq-dump SRR17644439 --fasta```

### 2. QIIME2 Installation and Setup
Install QIIME2 (2020.8) using Docker:

```
$ docker pull qiime2/core:2020.8
$ docker run -it -v ~/final/samples/:/data qiime2/core:2020.8
```

### 3. Taxonomic Analysis
Import data into QIIME2:
```
$ cd /data/

$ qiime tools import
--type 'SampleData[PairedEndSequencesWithQuality]'
--input-path manifest.csv
--input-format PairedEndFastqManifestPhred33
--output-path demux.qza
```

Run QIIME2 DADA2 for sequence denoising:
```
$ qiime dada2 denoise-paired
--i-demultiplexed-seqs demux.qza
--p-trunc-len-f 0
--p-trunc-len-r 0
--o-representative-sequences asv-sequences.qza
--o-table feature-table.qza
--o-denoising-stats dada2-stats.qza
```

Align reads with SILVA database for taxonomic classification:
```
$ qiime feature-classifier classify-consensus-blast
--i-query asv-sequences.qza
--i-reference-reads silva-138-99-seqs.qza
--i-reference-taxonomy silva-138-99-tax.qza
--o-classification taxonomy.qza
```

### 4. Functional Analysis with PICRUSt2
Install and activate PICRUSt2:
```
$ wget https://github.com/picrust/picrust2/archive/refs/tags/v2.3.0-b.tar.gz
$ tar xvzf v2.3.0-b.tar.gz
$ cd ~/picrust2-2.3.0-b
$ conda env create -f picrust2-env.yaml
$ conda activate picrust2
$ pip install --editable .
```

Export files from QIIME2 for PICRUSt2 processing:
```
$ qiime tools export \
--input-path feature-table.qza \
--output-path exported-feature-table

$ biom convert \
-i exported-feature-table/feature-table.biom \
-o feature-table.biom \
--to-hdf5

$ qiime tools export \
--input-path asv-sequences.qza \
--output-path exported-asv-sequences
```

Run PICRUSt2 pipeline:
```
$ source activate ~/anaconda3/bin/activate
$ conda activate picrust2
$ picrust2_pipeline.py -s ~/final/samples/exported-asv-sequences/dna-sequences.fasta -i ~/final/samples/exported-feature-table/feature-table.biom -o picrust2_outputs -p 1
```

### 5. Visualization with Krona
Install and set up Krona on Docker.
Generate taxonomy Krona plot:
- Modify taxonomy.qza and re-import to QIIME2.
- Run the following commands:
  - ```
    $ qiime krona collapse-and-plot \
    --i-table feature-table.qza \
    --i-taxonomy modified_taxonomy.qza \
    --o-krona-plot krona_tax.qzv
    ```
Finish PiCRust2 pipeline and classify pathways:
- Use custom Python scripts (`custom_map_gen.py` and `tsv_converter.py`) for pathway categorization.
- Add descriptions to pathway abundances file.
- Convert the output for Krona visualization:
  - `$ ktImportText -o krona_func.html krona_path_abun.tsv`


### Works cited:
[1] Tran, D. M. (2022). Rhizosphere microbiome dataset of Robusta coffee (Coffea canephora L.) grown in the Central Highlands, Vietnam, based on 16S rRNA metagenomics analysis. Data in Brief, 42, 108106. https://doi.org/10.1016/j.dib.2022.108106