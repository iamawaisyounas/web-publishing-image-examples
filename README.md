# Web publishing image examples

Small, runnable examples for preparing article images and checking the exported files. This repository adds a local file inventory to the longer [Practical Image Workflows](https://github.com/iamawaisyounas/practical-image-workflows) guide.

**Affiliation:** the publisher is affiliated with [TinyImage](https://tinyimage.io/), [DR Checker](https://dr-checker.com/), [HEIC to PNG](https://heictopng.io/) and [HEIC to JPEG](https://heictojpeg.io/). These examples work independently of those products. Competing tools and native CMS pipelines are valid alternatives. Prepared with AI assistance; product references checked 11 October 2026.

## Contents

- [Inventory a directory](#inventory-a-directory)
- [Compare two exports](#compare-two-exports)
- [Publish responsive images](#publish-responsive-images)
- [Choose a preparation path](#choose-a-preparation-path)
- [Check the published page](#check-the-published-page)
- [Limitations and verification](#limitations-and-verification)
- [Contribute](#contribute)

## Inventory a directory

Requirements: Python 3.9 or later; standard library only. Download [audit_images.py](audit_images.py) into a working directory, or clone this repository. Keep originals in a separate directory from publication candidates.

```sh
python audit_images.py ./exports --budget-kib 300 > image-inventory.csv
```

The CSV contains a relative filename, exact byte count, SHA-256 fingerprint and an `ok` or `over_budget` flag for each recognized filename extension. It scans subdirectories in a stable order and skips symbolic links. It opens files locally and makes no network requests.

The default budget is **300 KiB per file**, an illustrative project budget rather than a web standard. Use a budget appropriate to your page, image role, audience and visual requirements. One KiB is 1,024 bytes. Exit codes: `0` means inventory completed, including when files exceed the budget; `2` means invalid input or an unreadable file. Consult the CSV flags rather than treating exit code zero as a visual-quality pass.

Recognized extensions: JPG/JPEG, PNG, WebP, AVIF, GIF, HEIC/HEIF and SVG. The extension controls inclusion; the script does not decode images, validate their actual format, measure dimensions or remove metadata. SHA-256 can identify byte-identical files; it does not measure visual similarity.

## Compare two exports

1. Pick a nonsensitive source image and save an untouched master.
2. Produce two candidates with the same crop and intended display size. Record tool, settings, date and dimensions yourself.
3. Put candidates in `exports/` and run the inventory command.
4. Open both at their intended rendered size. Inspect text, edges, gradients, skin tones and transparency where relevant.
5. Record the chosen file, its bytes and the reason for choosing it. Smaller bytes alone do not establish a better result.

For a conversion with input size `A` and output size `B`, the byte reduction is `100 * (A - B) / A`, provided `A > 0`. Use actual file bytes; the result may be negative if an export is larger. No example reduction or product benchmark is claimed here.

## Publish responsive images

This is illustrative markup. Generate your own `garden-800.jpg` and `garden-1600.jpg` first; they are not bundled. Replace the dimensions and alternative text with your image's actual values.

```html
<img
  src="/images/garden-800.jpg"
  srcset="/images/garden-800.jpg 800w, /images/garden-1600.jpg 1600w"
  sizes="(max-width: 840px) calc(100vw - 32px), 800px"
  width="1600"
  height="1067"
  alt="Raised garden beds beside a gravel path"
>
```

The `sizes` expression must match the actual layout. Preserve the aspect ratio in `width` and `height`. A CMS or framework may generate variants for you; inspect its output before building another pipeline. See [MDN responsive images](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images) and [Google's image guidance](https://developers.google.com/search/docs/appearance/google-images).

## Choose a preparation path

| Starting point | Possible path | Check before continuing |
|---|---|---|
| HEIC photo that your CMS rejects | [HEIC to JPEG](https://heictojpeg.io/) for a photographic export; [HEIC to PNG](https://heictopng.io/) for a decoded editing intermediate | Orientation, color, dimensions and metadata; a PNG cannot restore detail already lost in the source |
| Image that needs a smaller publication export | Your CMS image pipeline, [TinyImage](https://tinyimage.io/) or [Squoosh](https://squoosh.app/) | Actual downloaded bytes and visual appearance; check whether processing uploads your files |
| Screenshot with small text | Crop a copy, preserve a lossless intermediate and compare final exports at the article width | Labels and punctuation remain legible; remove sensitive text from the pixels |
| Domain-level backlink-strength question | [DR Checker](https://dr-checker.com/) can provide a separate Domain Rating check | DR is not an image-quality measurement, a Google score or proof that a page will rank |

These links are optional workflow choices, not integrations in the Python script. Consult current product pages for limits and [TinyImage's privacy policy](https://tinyimage.io/privacy) before uploading. For a broader comparison, use [Free Tools for Website Publishing and SEO Checks](https://github.com/iamawaisyounas/free-web-publishing-seo-tools).

## Check the published page

- Inspect the actual page on narrow and wide screens. Confirm image URLs load and alternative text describes the image's role.
- Compare the browser's requested image variant with the intended layout. Do not assume a small source file means every visitor receives it.
- Use [PageSpeed Insights](https://pagespeed.web.dev/) for a page-level diagnostic, recording date and URL; distinguish lab and field data.
- Check that private information is absent from both visible pixels and metadata. This script does not sanitize either.
- Treat link attributes, public visibility and search indexing as separate checks. A product link does not guarantee a ranking gain.

## Limitations and verification

Run the included tests:

```sh
python -m unittest -v test_audit_images.py
```

Tests use temporary byte fixtures with image-like filenames; they verify inventory behavior, not whether those bytes form decodable images. Coverage includes recursion and stable order, exact size/hash values, budget boundaries, CSV quoting, unsupported extensions and missing directories. No real images or customer files are bundled. No compression, conversion, visual-quality or ranking benchmark was collected.

## Contribute

Open an issue or PR with a concrete publishing problem, a small reproducible example and expected behavior. Keep the script local and dependency-free. Include tests for behavioral changes. Disclose affiliations when proposing tools; provide primary sources and dates for changing product facts. Do not add affiliate redirects or unsupported performance claims.
