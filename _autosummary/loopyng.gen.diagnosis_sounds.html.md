# loopyng.gen.diagnosis_sounds

Tools for generating diagnostic audio signals.

Provides classes and functions to create special sound patterns useful for
testing and diagnosing audio processing pipelines and equipment.

### Functions

| [`mk_some_buzz_wf`](#loopyng.gen.diagnosis_sounds.mk_some_buzz_wf)([freq, n_samples, sr])            | Produce a sawtooth waveform with given frequency and n_samples.                                                                                          |
|----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `mk_sounds_with_timed_bleeps`([n_samples, ...])                                                    |                                                                                                                                                          |
| [`right_triangles`](#loopyng.gen.diagnosis_sounds.right_triangles)([samples_per_period, n_samples])  | Simplified sawtooth waveform.                                                                                                                            |
| `slow_mask`(arr, msk)                                                                              |                                                                                                                                                          |
| [`ums_to_01_array`](#loopyng.gen.diagnosis_sounds.ums_to_01_array)(ums, n_ums_bits)                  | Converts ums to an array with length n_ums_bits equivalent to a binary representation of ums assert all(ums_to_01_array(100,1) == [1, 1, 0, 0, 1, 0, 0]) |
| [`utcnow_ms`](#loopyng.gen.diagnosis_sounds.utcnow_ms)()                                       | Returns the current time in UTC in milliseconds                                                                                                          |
| [`wf_with_timed_bleeps`](#loopyng.gen.diagnosis_sounds.wf_with_timed_bleeps)([n_samples, bleep_loc, ...]) | Not sure this works as expected.                                                                                                                         |
| [`window`](#loopyng.gen.diagnosis_sounds.window)(seq[, n])                                  | Returns a sliding window (of width n) over data from the iterable s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                                            |
| `zero_crossing_gaps`(wf)                                                                           |                                                                                                                                                          |

### Classes

| `BinarySound`(redundancy, repetition[, nbits, ...])                                            |    |
|------------------------------------------------------------------------------------------------|----|
| [`TimeSound`](#loopyng.gen.diagnosis_sounds.TimeSound)([sr, buf_size_frm, amplitude, ...]) |    |
| [`WfGen`](#loopyng.gen.diagnosis_sounds.WfGen)([sr, buf_size_frm, amplitude])          |    |

### *class* loopyng.gen.diagnosis_sounds.TimeSound(sr=44100, buf_size_frm=2048, amplitude=0.5, n_ums_bits=30)

Bases: [`WfGen`](#loopyng.gen.diagnosis_sounds.WfGen)

### *class* loopyng.gen.diagnosis_sounds.WfGen(sr=44100, buf_size_frm=2048, amplitude=0.5)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

```pycon
>>> wfgen = WfGen(sr=44100, buf_size_frm=2048, amplitude=0.5)
>>> lookup = wfgen.mk_lookup_table(freq=4400)
>>> assert len(lookup) == 10
>>> wfgen.mk_sine_wf(n_frm=5, freq=4400)
array([0.        , 0.293316  , 0.47508605, 0.47618432, 0.29619315])
```

### loopyng.gen.diagnosis_sounds.mk_some_buzz_wf(freq=440, n_samples=43008, sr=44100)

Produce a sawtooth waveform with given frequency and n_samples.
The sample rate `sr` serves to interpret the `freq` specification in the number
of samples unit.

#### SEE ALSO
right_triangles

### loopyng.gen.diagnosis_sounds.right_triangles(samples_per_period=3, n_samples=7)

Simplified sawtooth waveform.

```pycon
>>> import numpy as np
>>> assert np.all(
... right_triangles(samples_per_period=3, n_samples=7)
... == np.array(
...     [-32767, -10922,  10922, -32767, -10922,  10922, -32767],
...     dtype=int16
... ))
```

### loopyng.gen.diagnosis_sounds.ums_to_01_array(ums, n_ums_bits)

Converts ums to an array with length n_ums_bits equivalent to a binary representation of ums
assert all(ums_to_01_array(100,1) == [1, 1, 0, 0, 1, 0, 0])

### loopyng.gen.diagnosis_sounds.utcnow_ms()

Returns the current time in UTC in milliseconds

### loopyng.gen.diagnosis_sounds.wf_with_timed_bleeps(n_samples=88200, bleep_loc=400, bleep_spec=100, sr=44100)

Not sure this works as expected. Docs needed.

### loopyng.gen.diagnosis_sounds.window(seq, n=2)

Returns a sliding window (of width n) over data from the iterable
s -> (s0,s1,…s[n-1]), (s1,s2,…,sn), …
