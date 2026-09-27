# Run your first experiment

[README](README.md) · [中文](README.zh-CN.md) · [Version 1.0.0](https://github.com/YucongDuan/NEPHROGENESIS-Lab/releases/tag/v1.0.0)

1. Download the source ZIP from the release page, or clone `https://github.com/YucongDuan/NEPHROGENESIS-Lab.git`.
2. Extract it and open a terminal in the folder containing `pyproject.toml`.
3. Use Python 3.10 or newer. The runtime uses the standard library only.

```sh
python -m nephrogenesis verify
python -m nephrogenesis run transport --out runs/first-experiment
python -m nephrogenesis replay runs/first-experiment
python -m nephrogenesis serve --port 8765
```

Open `http://127.0.0.1:8765` for calculations with editable inputs. Use a new output directory for each experiment. Stop the local server with Ctrl+C.

## Read a result immediately

[Open the project page](https://yucongduan.github.io/NEPHROGENESIS-Lab/) and choose **Read the example report**. This is a precomputed result viewer; run Python locally to recompute or change inputs. You can also download the repository and open `SHOWCASE.html` offline.

## Inspect and extend

- [Full instructions](README.md) and the guides in `docs/` explain assumptions and model scope.
- [Local publication check](validation/PUBLICATION_CHECK_2026-09-27.json): 198 tests passed on the recorded environment.
- [GitHub Actions](https://github.com/YucongDuan/NEPHROGENESIS-Lab/actions) supplies hosted execution results and source revisions.
- [Contributing](CONTRIBUTING.md) describes how to add experiments.

The book by Yucong Duan and Zhongdao Wu remains separately copyrighted. The companion source uses Apache-2.0; experiments use synthetic or conditional models.
