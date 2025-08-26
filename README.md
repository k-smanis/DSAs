# Project README

&#x20;

## Overview

This project implements various algorithms and data structures in a clean, testable, and reusable way, entirely from scratch.. It also includes lightweight performance utilities to measure execution time and peak memory usage during tests.

## Features

- **Algorithms**: Implemented from first principles without high-level shortcuts.
- **Data Structures**: Stacks, queues, linked lists, trees, graphs, and more (organized under `src/`).
- **Performance Measurement** (standard library only):

  - Peak memory via `tracemalloc` (captures the entire call, including recursion).
  - Wall‑clock execution time in milliseconds.
  - CSV logging of results for later analysis (commit hash, test name, elapsed time, peak KiB).

## License

This project is licensed under the MIT License.
