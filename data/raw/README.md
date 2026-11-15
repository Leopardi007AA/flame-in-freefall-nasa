# data/raw — original NASA PSI tables

Each `PSI-xx/` folder contains `PSI-xx_psi_page_preview.csv`: the **first rows of the experimental table shown on the PSI page** of the investigation (text copied from the psi.nasa.gov site on 14 November 2026, without any change to the values).

- They are **partial previews**, not the full datasets. The full dataset can be downloaded from the PSI page (DOI in the file `data/investigations.csv`).
- No value was added, corrected or estimated: they were only transcribed from the page.
- To replace a preview with the full download, put the original file in the same folder and delete the preview.
- File names must not contain “sample” or “example”: the “Real data” tab skips them.
