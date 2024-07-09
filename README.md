# mimic-cxr-jpg-loader

mimic-cxr-jpg-loader is a Python package that provides utilities to easily load the MIMIC-CXR-JPG Dataset [\[1\]](#1), [\[2\]](#2) which is available on Physionet [\[3\]](#3). This dataset contains chest X-ray images in JPG format from the MIMIC-CXR dataset, which is a large publicly available dataset of chest radiographs in DICOM format.

## Installation

You can install mimic-cxr-jpg-loader via pip:

```bash
pip install mimic-cxr-jpg-loader
```

## Usage

To use this package, simply create a new Dataset by providing the required filepaths and, optionally, a list of modifiers.

```python3
from mimic_cxr_jpg_loader.dataset import MIMICDataset
from mimic_cxr_jpg_loader.modifiers import *

dataset = MIMICDataset(
    root="/example/datasets/MIMIC-CXR-JPG",
    split_path="/example/datasets/MIMIC-CXR-JPG/mimic-cxr-2.0.0-split.csv",
    modifiers=[
        FilterByViewPosition(ViewPosition.PA),
        FilterBySplit(Split.TRAIN),
        UIgnore(Pathology.CARDIOMEGALY),
    ],
)
```

Afterwards, access the dataset like a regular Pytorch Dataset, e.g. `dataset[idx]`, which will return a tuple in the format `(img, labels)` where img is a Pillow Image object and labels a Pandas Series object containing all data about it.

This labels variable will include a row containing all columns existing in the [CheXpert](https://stanfordmlgroup.github.io/competitions/chexpert/)[\[4\]](#4) format, for instance `labels[Pathology.CARDIOMEGALY]` will return the labels for the Cardiomegaly condition. If you want only the labels of a specific condition, pass the option `target_pathology = Pathology.YOUR_DESIRED_CONDITION` to the `MIMICDataset`, in which case `labels` will correspond to a vector with numeric labels for said pathology.

### Modifiers

**Filters:**

| Filter | Description | Values |
| ------ | ----------- | ------ |
| FilterByViewPosition | Obtain images from the specified View Position | `ViewPosition.AP`, `ViewPosition.PA`, `ViewPosition.LATERAL` |
| FilterBySplit | Obtain images from the specified Split | `Split.TRAIN`, `Split.TEST`, `Split.VAL` |

**Uncertain labels:**

The CheXpert labelling system allows 3 possible values for different pathologies: 1 if positive, 0 if negative and -1 if uncertain. To deal with this uncertainty the authors of the tool propose different methods. We provide implementations to obtain labels as described for each of the methods.

| Modifier | Description |
| ------- | ------------ |
| UIgnore | Ignore (remove) all images with uncertain labels (-1) |
| UZeroes | Map all instances of the uncertain label to 0
| UOnes | Map all instances of the uncertain label to 1
| UMultiClass | Treat the uncertainty label as its own class with label 2 |

## Requirements

- Python >= 3.8
- Pandas
- Pillow

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contribution

Contributions are welcome! Please feel free to open a pull request.

## Issues

If you encounter any issues or have suggestions, please feel free to [open an issue](https://github.com/filipepcampos/mimic-cxr-jpg-loader/issues).

## Acknowledgments

- The MIMIC-CXR-JPG dataset was made available by the MIT Laboratory for Computational Physiology.
- This package is inspired by the need for simplified access to the MIMIC-CXR-JPG dataset.

## References

<a id="1">\[1\]</a>
Johnson, A., Lungren, M., Peng, Y., Lu, Z., Mark, R., Berkowitz, S., & Horng, S. (2024). MIMIC-CXR-JPG - chest radiographs with structured labels (version 2.1.0). PhysioNet. https://doi.org/10.13026/jsn5-t979.

<a id="2">\[2\]</a>
Johnson AE, Pollard TJ, Berkowitz S, Greenbaum NR, Lungren MP, Deng CY, Mark RG, Horng S. MIMIC-CXR: A large publicly available database of labeled chest radiographs. arXiv preprint arXiv:1901.07042. 2019 Jan 21.

<a id="3">\[3\]</a>
Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation \[Online\]. 101 (23), pp. e215–e220

<a id="4">\[4\]</a>
Jeremy Irvin, Pranav Rajpurkar, Michael Ko, Yifan Yu, Silviana Ciurea-Ilcus, Christopher Chute, Henrik Marklund, Behzad Haghgoo, Robyn L. Ball, Katie S. Shpanskaya, Jayne Seekins, David A. Mong, Safwan S. Halabi, Jesse K. Sandberg, Ricky Jones, David B. Larson, Curtis P. Langlotz, Bhavik N. Patel, Matthew P. Lungren, & Andrew Y. Ng (2019). CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison. CoRR, abs/1901.07031.
