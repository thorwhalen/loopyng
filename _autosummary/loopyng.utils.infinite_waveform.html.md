# loopyng.utils.infinite_waveform

Infinite waveform generation tools.

Provides classes and functions to create and manipulate waveforms that can be
queried for arbitrary time segments.

### Classes

| [`InfiniteWaveform`](#loopyng.utils.infinite_waveform.InfiniteWaveform)(gen_spectrum[, noise_amp])   | A tiny little class emulating an infinite waveform with a given spectrum.   |
|------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|

### *class* loopyng.utils.infinite_waveform.InfiniteWaveform(gen_spectrum, noise_amp=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A tiny little class emulating an infinite waveform with a given spectrum.
Note that if choosing to add noise to the waveform, the generator will be considerably slower

#### query(bt, tt)

Returns a generator of the infinite waveform from bt to tt
