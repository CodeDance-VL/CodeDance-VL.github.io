# CodeDance project page

Website for **CodeDance: A Dynamic Tool-integrated MLLM for Executable Visual Reasoning**. CodeDance uses executable code and adaptive tool use for multimodal visual reasoning.

- [Project website](https://codedance-vl.github.io/)
- [Paper](https://arxiv.org/abs/2512.17312)
- [Code and release information](https://github.com/CodeDance-VL/CodeDance)
- [SFT dataset](https://huggingface.co/datasets/Peterwatwec/CodeDance-SFT) · [RL dataset](https://huggingface.co/datasets/Peterwatwec/CodeDance-RL)

The Models and Demo buttons currently lead to the code repository for release information.

## Preview and edit

This is a static website; publishing does not require a build step. With Python 3 installed, run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000>. Edit page text, links, and tables in `index.html`, styles in `static/css/index.css`, and figures in `static/images/`. Figures link to their full-resolution versions. MathJax is bundled locally for equation rendering.

## Check and publish

With Node.js 22.22 or later in the 22.x series, or Node.js 24.8 or later, and Python 3.9 or later:

```sh
npm ci
npm run check
```

Checks validate HTML, local assets, links within the page, and leftover placeholders. They run automatically for pull requests and pushes to `main`. Before publishing, preview the page on phone and desktop widths and check figures, tables, and equations.

GitHub Pages publishes the root of `main` automatically. See the repository's [Actions](https://github.com/CodeDance-VL/CodeDance-VL.github.io/actions) for check and deployment status.

## Attribution

The page is based on [Nerfies](https://nerfies.github.io/). Keep the footer attribution and the existing [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) website notice. See [third-party notices](THIRD_PARTY_NOTICES.md) for bundled dependencies. Linked code, datasets, and models retain their own licenses.
