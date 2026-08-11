# SafeguardShift V2 raw evidence

The final verified V2 evidence bundle was produced by GitHub Actions run `31477490866` on 2026-08-11.

Final Actions artifact:

- name: `safeguardshift-v2-primary3-COMPLETE`
- artifact ID: `9095878773`
- artifact ZIP SHA-256: `8a7443c331e6875f004ed2134946d62e962d1e6487ce376f0897547b71bb534c`
- artifact size: 5,032,508 bytes
- Actions retention expiry: 2026-11-09

Raw-file checksums inside the bundle:

| File | Bytes | SHA-256 |
|---|---:|---|
| `canonical-primary3.jsonl` | 62,792,768 | `d973aeedf05d9cae38cc859fc9249c3f6859eb8947b586e8d256dad6912f0597` |
| `canonical-frontier.jsonl` | 1,329,252 | `698962393621163cba9eaff7f1790a4f0ead74d14a081a676da98a2702278d4c` |
| `deepseek-provider-diagnostic.jsonl` | 11,801,930 | `e42f901067904abeba8100c2e2aa94551e7dbf1b72f223be0d0cf0b0f3f21d97` |
| `primary3-missing-final.json` | 3 | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |

The primary matrix is complete at 3,240/3,240 cells. The frontier diagnostic is complete at 60/60 cells. DeepSeek is intentionally retained as an incomplete provider/interface diagnostic with 586/1,080 accepted cells and is not pooled into the primary behavioral estimand.

The Actions artifact is a temporary transport location, not a permanent research archive. Before its retention deadline, mirror the exact bundle to a durable release/archive without modifying its bytes, and preserve the hashes above. The summary and provenance files committed in `results/v2/` are sufficient to verify the mirrored raw bundle.
