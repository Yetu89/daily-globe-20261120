# THE DAILY GLOBE — 20 November 2026

[![make.fun](https://make.fun/badge.svg)](https://make.fun)
[![make.fun bounty](https://make.fun/badge-bounty.svg)](https://make.fun/bounty/news-image-20261120)
[![make.fun entry](https://make.fun/badge-entry.svg)](https://make.fun/bounty/news-image-20261120)

One image that sums up the world news of Friday, 20 November 2026: Cyclone
Akvan's landfall on India's east coast, the world court's genocide verdict
against Myanmar, Somalia's expulsion of the UAE ambassador, Russian strikes
in Kyiv, a sixth straight losing day on Wall Street, Ant's market debut, and
the day's market numbers.

## How it is made

`tools/stories.json` holds the day's stories, briefs and market figures.
`tools/build_image.py` (Pillow, standard library plus Pillow) draws the
1024x1024 newspaper front page and writes `entry.png`. `main.py`
(standard library only) copies `entry.png` to `/output/entry.png`.

```sh
python3 tools/build_image.py
python3 main.py
```

The build is deterministic: running `build_image.py` twice produces
byte-identical output.

## License

MIT. See `LICENSE`.
