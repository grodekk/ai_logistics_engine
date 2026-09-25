## CLI benchmark – `/analytics/monthly-expenses`

Benchmark executed with `oha` against the same endpoint and the same server configuration.

Each run used:

- 5000 requests
- concurrency levels: 1, 5, 10, 20
- `oha --no-tui`
- same machine and database
- same Uvicorn launcher
- `SelectorEventLoop`
- one server process

### Sync

| Concurrency | Requests/sec | Avg latency | p95 latency | p99 latency |
|---:|---:|---:|---:|---:|
| 1  | 2787.24 | 0.357 ms | 0.452 ms | 0.512 ms |
| 5  | 3415.83 | 1.461 ms | 1.980 ms | 2.200 ms |
| 10 | 3381.67 | 2.950 ms | 3.250 ms | 3.449 ms |
| 20 | 3404.60 | 5.846 ms | 6.340 ms | 6.570 ms |

### Async

| Concurrency | Requests/sec | Avg latency | p95 latency | p99 latency |
|---:|---:|---:|---:|---:|
| 1  | 2399.01 | 0.415 ms | 0.522 ms | 0.610 ms |
| 5  | 4383.21 | 1.138 ms | 1.511 ms | 2.284 ms |
| 10 | 4378.33 | 2.278 ms | 3.051 ms | 5.942 ms |
| 20 | 4629.74 | 4.289 ms | 4.979 ms | 5.454 ms |

### Sync vs async

| Concurrency | Sync RPS | Async RPS | RPS change | Sync avg | Async avg | Avg latency change | Sync p95 | Async p95 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1  | 2787.24 | 2399.01 | -13.9% | 0.357 ms | 0.415 ms | +16.3% | 0.452 ms | 0.522 ms |
| 5  | 3415.83 | 4383.21 | +28.3% | 1.461 ms | 1.138 ms | -22.1% | 1.980 ms | 1.511 ms |
| 10 | 3381.67 | 4378.33 | +29.5% | 2.950 ms | 2.278 ms | -22.8% | 3.250 ms | 3.051 ms |
| 20 | 3404.60 | 4629.74 | +36.0% | 5.846 ms | 4.289 ms | -26.6% | 6.340 ms | 4.979 ms |

At concurrency 1, the synchronous implementation is faster, which is expected because the async version introduces additional scheduling and connection-pool overhead without benefiting from overlapping I/O.

Under concurrent load, the async implementation scales better. At concurrency 5–20, throughput increases by approximately 28–36%, while average latency decreases by approximately 22–27%.

The synchronous implementation reaches a throughput plateau at roughly 3.4k requests/sec, while the asynchronous implementation reaches approximately 4.6k requests/sec at concurrency 20.