# loopyng.gen.simple

Waveforms generated only with builtins (no numpy etc.)
Meant to be copy/pasted where needed in tests.

### Functions

| [`inverted_tiles`](#loopyng.gen.simple.inverted_tiles)([motif, cap])               | Infinite generator of chunks taken by transforming the input motif.   |
|---------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| [`inverted_tiles_wf`](#loopyng.gen.simple.inverted_tiles_wf)([motif, cap, wf_length]) | Get a (possibly infinite) waveform through inverted_tiles chunks      |

### loopyng.gen.simple.inverted_tiles(motif=(1, 2, 3, 4, 5), cap=20000)

Infinite generator of chunks taken by transforming the input motif.
The iterative transformation is constituted of a translation by the length of the
motif and an inversion of the sign.

* **Parameters:**
  * **motif** – The iterable to use as the (incremented and inverted) pattern to
    make waveforms out of.
  * **cap** – The maximum absolute value to include in a waveform.
    Also determines when we resset the chk to be the motif.

```pycon
>>> g = inverted_tiles()
>>> next(g), next(g), next(g)
([1, 2, 3, 4, 5], [-6, -7, -8, -9, -10], [11, 12, 13, 14, 15])
>>> g = inverted_tiles(motif=(1, 2, 3), cap=10)
>>> [*next(g), *next(g), *next(g), *next(g)]
[1, 2, 3, -4, -5, -6, 7, 8, 9, -10, -11, -12]
```

### loopyng.gen.simple.inverted_tiles_wf(motif=(1, 2, 3, 4, 5), cap=20000, wf_length=43008)

Get a (possibly infinite) waveform through inverted_tiles chunks

These waveforms are originally meant to be used with [1,…,n] motifs and used for
diagnosis. Indeed, the samples alternate sign (so waveform can be made audible),
but checking for the absolute value of the samples, you should see incrementing
integers.

* **Parameters:**
  * **motif** – The iterable to use as the (incremented and inverted) pattern to
    make waveforms out of.
  * **cap** – The maximum absolute value to include in a waveform.
    Also determines when we resset the chk to be the motif.
  * **wf_length** – Length of the desired waveform, or None for an infinite iterable

```pycon
>>> wf = inverted_tiles_wf()
>>> len(wf)
43008
>>> wf[:15]
[1, 2, 3, 4, 5, -6, -7, -8, -9, -10, 11, 12, 13, 14, 15]
>>> inverted_tiles_wf(motif=(1, 2, 3), cap=10, wf_length=15)
[1, 2, 3, -4, -5, -6, 7, 8, 9, -10, -11, -12, 1, 2, 3]
```
