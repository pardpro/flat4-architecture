#!/usr/bin/env python3
"""Educational wake-up batching model for the F4A Hardware/Realtime Profile.

The model estimates timer wake-up counts and batching delay. It does not model
an operating-system scheduler, power state, watchdog, device I/O, or end-to-end
latency, and must not be used as product acceptance evidence.
"""

from __future__ import annotations

import argparse
import math


def estimate(duration_seconds: float, source_hz: float, batch_window_ms: float) -> dict[str, float]:
    if duration_seconds <= 0 or source_hz <= 0 or batch_window_ms <= 0:
        raise ValueError("duration, source frequency, and batch window must be positive")

    source_events = math.ceil(duration_seconds * source_hz)
    direct_wakeups = source_events
    batch_window_seconds = batch_window_ms / 1000.0
    batched_wakeups = math.ceil(duration_seconds / batch_window_seconds)
    change = (batched_wakeups - direct_wakeups) / direct_wakeups * 100.0

    return {
        "source_events": source_events,
        "direct_wakeups": direct_wakeups,
        "batched_wakeups": batched_wakeups,
        "estimated_wakeup_change_percent": change,
        "maximum_batch_wait_ms": batch_window_ms,
        "average_batch_wait_ms": batch_window_ms / 2.0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=float, default=3.0, help="Modeled duration in seconds")
    parser.add_argument("--source-hz", type=float, default=100.0, help="Modeled event frequency")
    parser.add_argument("--window-ms", type=float, default=10.0, help="Batch window in milliseconds")
    args = parser.parse_args()

    try:
        result = estimate(args.duration, args.source_hz, args.window_ms)
    except ValueError as exc:
        parser.error(str(exc))

    print("F4A Hardware/Realtime educational batching model")
    print(f"Duration: {args.duration:g}s")
    print(f"Source frequency: {args.source_hz:g}Hz")
    print(f"Batch window: {args.window_ms:g}ms")
    print(f"Source events / direct wake-ups: {result['source_events']:.0f}")
    print(f"Modeled batched wake-ups: {result['batched_wakeups']:.0f}")
    change = result["estimated_wakeup_change_percent"]
    direction = "increase" if change > 0 else "reduction"
    print(f"Modeled wake-up {direction}: {abs(change):.1f}%")
    print(f"Added batching wait: average {result['average_batch_wait_ms']:.1f}ms, maximum {result['maximum_batch_wait_ms']:.1f}ms")
    print("LIMITATION: this is arithmetic, not OS, device, power, thermal, watchdog, or latency evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
