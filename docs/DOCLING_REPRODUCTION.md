# Reproduce the Docling measurement

The recorded run uses Docling 2.142.1, its standard PDF pipeline, CPU, OCR disabled
and table structure disabled. Heron layout processing still needs model weights.
Model source: https://huggingface.co/docling-project/docling-layout-heron .
The model card lists Apache-2.0. Model weights are not redistributed by this kit.

## Pinned artifact used in the measured run

| Property | Value |
| --- | --- |
| Model repository | docling-project/docling-layout-heron |
| Revision | 8f39ad3c0b4c58e9c2d2c84a38465abf757272d8 |
| Filename | model.safetensors |
| Bytes | 171658996 |
| SHA-256 | 00333a43451945aaf89db8ca9c0a17e75d1537c17db60fdb91aa95f4c7929e0c |

Normal setup is `python -m pip install ".[docling]"`, followed by the documented
engine command. This host's initial Hugging Face library downloads stalled. A
direct HTTPS download of the same pinned public file succeeded. We verified its
full SHA-256 before copying it into the existing snapshot cache. Other snapshot
files had already downloaded. No engine output, model weights, or ground truth
was changed to improve results.

To repeat the fallback in PowerShell after the normal attempt created that cache:

```powershell
$revision = '8f39ad3c0b4c58e9c2d2c84a38465abf757272d8'
$expectedHash = '00333a43451945aaf89db8ca9c0a17e75d1537c17db60fdb91aa95f4c7929e0c'
New-Item -ItemType Directory -Force tmp | Out-Null
curl.exe -L --fail --connect-timeout 15 --max-time 180 "https://huggingface.co/docling-project/docling-layout-heron/resolve/$revision/model.safetensors" -o tmp/heron-model.safetensors
if ($LASTEXITCODE -ne 0) { throw 'Model download failed' }
if ((Get-FileHash tmp/heron-model.safetensors -Algorithm SHA256).Hash -ne $expectedHash) { throw 'Model checksum mismatch' }
$snapshot = Join-Path $env:USERPROFILE ".cache/huggingface/hub/models--docling-project--docling-layout-heron/snapshots/$revision"
if (-not (Test-Path -LiteralPath $snapshot)) { throw 'Run the normal setup first, or use your configured HF cache path' }
Copy-Item -LiteralPath tmp/heron-model.safetensors -Destination (Join-Path $snapshot 'model.safetensors')
$env:HF_HUB_OFFLINE = '1'
arabic-pdf-kit run --engine docling --output tmp/docling.json --html tmp/docling.html
```

Expected measured summary: 0 PASS, 8 FAIL, 0 ERROR, 0 SKIPPED, exit 1. Offline mode
now uses a complete cache; it does not mean the engine was skipped. No API key is
required. Configure your actual Hugging Face cache path if it differs from the
default Windows path above. On another platform, use the same revision and verify
the same hash before placing the file in its snapshot cache.

The earlier incomplete-cache ERROR is preserved separately in docling-smoke.json
as historical infrastructure evidence. Do not use it as the current result.
