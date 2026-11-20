# THE DAILY GLOBE — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Yetu89/daily-globe-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Yetu89/daily-globe-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up the world news of Friday, 20 November 2026: Cyclone
Akvan's landfall on India's east coast, the world court's genocide verdict
against Myanmar, Somalia's expulsion of the UAE ambassador, Russian strikes
in Kyiv, the S and P's sixth straight loss on Wall Street, Ant's market
debut, and the day's market numbers.

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
