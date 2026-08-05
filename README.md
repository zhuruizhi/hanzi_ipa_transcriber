# hanzi-ipa-transcriber

This repository provides a Python script for converting Chinese characters into Mandarin or Cantonese IPA transcriptions with Chao tone numerals and exporting the results in TIPA-compatible LaTeX format.

The script supports two pronunciation systems:

- Mandarin (`dialect="mandarin"`)
- Cantonese (`dialect="cantonese"`)

## Usage

Run the function `transcribe()` by entering Chinese characters and specifying the target dialect:

```python
print(transcribe("睿", dialect="mandarin"))

print(transcribe("喺", dialect="cantonese"))
```

The script returns the IPA transcription with Chao tone numerals in TIPA-compatible LaTeX format.

Before using the output in LaTeX documents, load the `tipa` package:

```latex
\usepackage{tipa}
```

## Phonetic references

The Mandarin transcriptions are based on the following references:

- Duanmu, San. 2007. *The Phonology of Standard Chinese*. 2nd ed. Oxford: Oxford University Press.
- Lee, Wai-Sum, and Eric Zee. 2003. "Standard Chinese (Beijing)." *Journal of the International Phonetic Association* 33(1): 109–112. https://doi.org/10.1017/S0025100303001208.
- Lin, Yen-Hwei. 2007. *The Sounds of Chinese*. Cambridge: Cambridge University Press.

The Cantonese transcriptions are based on the following references:

- Matthews, Stephen, and Virginia Yip. 2011. *Cantonese: A Comprehensive Grammar*. 2nd ed. London: Routledge.
- 張勵妍、倪列懷、潘禮美. 2018. *香港粵語大詞典*. Hong Kong: 天地圖書有限公司.

## BibTeX

```bibtex
@book{Duanmu2007,
  author    = {Duanmu, San},
  title     = {The Phonology of Standard Chinese},
  edition   = {2},
  year      = {2007},
  publisher = {Oxford University Press},
  address   = {Oxford}
}

@article{LeeZee2003,
  author  = {Lee, Wai-Sum and Zee, Eric},
  title   = {Standard Chinese ({Beijing})},
  journal = {Journal of the International Phonetic Association},
  volume  = {33},
  number  = {1},
  pages   = {109--112},
  year    = {2003},
  doi     = {10.1017/S0025100303001208}
}

@book{Lin2007,
  author    = {Lin, Yen-Hwei},
  title     = {The Sounds of Chinese},
  year      = {2007},
  publisher = {Cambridge University Press},
  address   = {Cambridge}
}

@book{MatthewsYip2011,
  author    = {Matthews, Stephen and Yip, Virginia},
  title     = {Cantonese: A Comprehensive Grammar},
  edition   = {2},
  year      = {2011},
  publisher = {Routledge},
  address   = {London}
}

@book{ZhangNiPan2018,
  author    = {張勵妍 and 倪列懷 and 潘禮美},
  title     = {香港粵語大詞典},
  year      = {2018},
  publisher = {天地圖書有限公司},
  address   = {Hong Kong}
}
```
