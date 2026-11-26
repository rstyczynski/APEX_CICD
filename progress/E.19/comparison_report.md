# Equivalent Python and JavaScript support check comparison

## Workload and conditions

Hosted run 45875517420, source 99b05eb54e01974b60e49aefe4dfe0192f9f7dd3. Two independent ubuntu-24.04 jobs, each running both runtimes on the exact same host/image and fixture bytes. Runtime order is reversed in the second job. Two paired replicas per runtime. Each sample launches five independent helper processes: tool, output, provenance, candidate metadata and trusted Review. Each replica records one first-process batch and ten repeated batches. Cold means first invocation in a fresh job, not proof of a cold physical host. Warm means repeated invocation with filesystem caches, not a persistent interpreter. Only the shared valid-input domain is timed; stricter missing-input behavior is tested separately.

## Observed timings

javascript: v24.22.1 on image 20261122.23.1. First-invocation n=2, median 167.27 ms per five-check batch. Repeated n=20, median 168.45 ms, range 119.80–228.23 ms.

python: Python 3.12.3 on image 20261122.23.1. First-invocation n=2, median 120.97 ms per five-check batch. Repeated n=20, median 138.60 ms, range 99.73–162.49 ms.

compare (2, python, javascript): runtime-availability step 0s, both measurement steps 3s total, total job 10s. API timestamps have one-second granularity. No runtime installation step occurred.

compare (1, javascript, python): runtime-availability step 0s, both measurement steps 3s total, total job 18s. API timestamps have one-second granularity. No runtime installation step occurred.

Overall comparison workflow elapsed 22s, including scheduling and both paired jobs. This is shared experiment wall time, not a per-language native pipeline result.

## Simplicity and maintenance

The five JavaScript guards require zero package dependencies, zero npm installs and zero setup-node steps. GitHub supplies Node24 for native JavaScript actions. Python was already installed in the benchmark runner; no Python installation cost or avoided installation time is claimed. The old helpers use the Python standard library and shell invocation; their explicit setup cost on this image was also zero. JavaScript improves action discoverability, declared workflow input boundaries and one shared failure implementation, but adds metadata and entrypoint files that must remain synchronized. Neither language makes receipt authenticity or trusted-source selection automatic.

Measured helper timings cover subprocess startup, reading, parsing and hashing small files. Two paired independent hosts and twenty repeated batches cannot establish production tail latency, full pipeline speedup or a causal host-cache effect. JavaScript should be chosen for the Python-free reusable-action requirement, not an assumed speed advantage. The separate actual native qualification is functional evidence, not a controlled timing comparison against E.18's full pipeline.

## Rejected exploratory comparison

Earlier five-check run 45875048579 used different runner image revisions across runtime groups during a hosted-image rollout. It is retained under tests/timings-five but excluded from the accepted comparison. Corrected run 45875517420 pairs both runtimes on each host and counterbalances order. This controls the within-pair image difference, while background load and provider physical-host warmth remain uncontrolled.
