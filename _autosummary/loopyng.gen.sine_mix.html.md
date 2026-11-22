# loopyng.gen.sine_mix

Utilities for creating and mixing sine wave signals.

Provides functions to generate and combine sine waves with different frequencies,
phases, and amplitudes to create complex waveforms.

### Functions

| `asis`(x)                                                                                        |                                                                                                    |
|--------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| `dflt_sprout_to_wf_params`(annot)                                                                |                                                                                                    |
| [`dflt_wf_params_to_wf`](#loopyng.gen.sine_mix.dflt_wf_params_to_wf)(weights[, freqs, ...])     | A default for wf_params_to_wf                                                                      |
| [`freq_based_stationary_wf`](#loopyng.gen.sine_mix.freq_based_stationary_wf)([freqs, weights, ...]) | Makes a stationary waveform by mixing a number of freqs together, possibly with different weights. |
| [`mk_sine_wf`](#loopyng.gen.sine_mix.mk_sine_wf)([freq, n_samples, sr, phase, gain])  | Make a sine waveform                                                                               |

### Classes

| [`MinMaxRand`](#loopyng.gen.sine_mix.MinMaxRand)([min, max, rand_func])        | Like a partial, but meant for bounded rand functions.   |
|-------------------------------------------------------------------------------------------|---------------------------------------------------------|
| [`MinMaxRandDict`](#loopyng.gen.sine_mix.MinMaxRandDict)([iid_seed_gen])           |                                                         |
| [`NumAnnotsAndWaveformChunks`](#loopyng.gen.sine_mix.NumAnnotsAndWaveformChunks)([seeds, ...]) |                                                         |

### *class* loopyng.gen.sine_mix.MinMaxRand(min=0, max=1, rand_func=<bound method Random.uniform of <random.Random object>>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Like a partial, but meant for bounded rand functions.
Could have just done:

```text
r = partial(random.uniform, min, max)
r()
```

But we need to be able to have access to r.min and r.max

#### rand_func(a, b)

Get a random number in the range [a, b) or [a, b] depending on rounding.

The mean (expected value) and variance of the random variable are:

> E[X] = (a + b) / 2
> Var[X] = (b - a) \*\* 2 / 12

### *class* loopyng.gen.sine_mix.MinMaxRandDict(iid_seed_gen=(('rpm', MinMaxRand(min=100, max=1000, rand_func=<bound method Random.uniform of <random.Random object>>)), ('temperature', MinMaxRand(min=10, max=25, rand_func=<bound method Random.uniform of <random.Random object>>)), ('pressure', MinMaxRand(min=50, max=500, rand_func=<bound method Random.uniform of <random.Random object>>))))

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

```pycon
>>> from loopyng.gen.sine_mix import MinMaxRandDict, MinMaxRand
>>>
>>> rand_gen = MinMaxRandDict((
...     ('rpm', MinMaxRand(100, 1000)),
...     ('temperature', MinMaxRand(10, 25)),
...     ('pressure', MinMaxRand(50, 500)),
... ))
>>> t = list(rand_gen.read(4))
>>> assert len(t) == 4
>>> assert list(t[0]) == ['rpm', 'temperature', 'pressure']
>>> t
[{'rpm': 577.8533852127333,
  'temperature': 18.306495707512724,
  'pressure': 357.72481026748113},
 {'rpm': 457.0605450014562,
  'temperature': 23.94969543436332,
  'pressure': 483.1119334545017},
 {'rpm': 489.8445225473431,
  'temperature': 17.176275589569695,
  'pressure': 415.8337855923849},
 {'rpm': 120.84000962564362,
  'temperature': 21.153044572476936,
  'pressure': 449.5124385844328}]
```

### *class* loopyng.gen.sine_mix.NumAnnotsAndWaveformChunks(seeds=(('rpm', MinMaxRand(min=100, max=1000, rand_func=<bound method Random.uniform of <random.Random object>>)), ('temperature', MinMaxRand(min=10, max=25, rand_func=<bound method Random.uniform of <random.Random object>>)), ('pressure', MinMaxRand(min=50, max=500, rand_func=<bound method Random.uniform of <random.Random object>>))), seed_to_sprout_gen=<class 'loopyng.gen.sine_mix.MinMaxRandDict'>, sprout_to_annot=<function asis>, sprout_to_wf_params=<function dflt_sprout_to_wf_params>, wf_params_to_wf=<function dflt_wf_params_to_wf>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

#### seed_to_sprout_gen

alias of [`MinMaxRandDict`](#loopyng.gen.sine_mix.MinMaxRandDict)

#### wf_params_to_wf(freqs=None, n_samples=43008, sr=44100)

A default for wf_params_to_wf

* **Parameters:**
  * **weights** – The weights these frequencies should have (all weights will be normalized
  * **freqs** – List(-like) of frequencies (in Hz)
  * **n_samples** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – The number of samples of waveform you want
  * **sr** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Sample rate
* **Returns:**
  Waveform. A numpy array of samples of the specified sine wave

```pycon
>>> n_samples = random.randint(2,5)
>>> wf = dflt_wf_params_to_wf(weights = [1,2,3,4], n_samples=100)
>>> len(wf)
100
>>> wf
array([ 0.        ,  0.08534908,  0.16988139,  ..., -0.22847099, -0.22552675])
```

### loopyng.gen.sine_mix.dflt_wf_params_to_wf(weights, freqs=None, n_samples=43008, sr=44100)

A default for wf_params_to_wf

* **Parameters:**
  * **weights** – The weights these frequencies should have (all weights will be normalized
  * **freqs** – List(-like) of frequencies (in Hz)
  * **n_samples** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – The number of samples of waveform you want
  * **sr** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Sample rate
* **Returns:**
  Waveform. A numpy array of samples of the specified sine wave

```pycon
>>> n_samples = random.randint(2,5)
>>> wf = dflt_wf_params_to_wf(weights = [1,2,3,4], n_samples=100)
>>> len(wf)
100
>>> wf
array([ 0.        ,  0.08534908,  0.16988139,  ..., -0.22847099, -0.22552675])
```

### loopyng.gen.sine_mix.freq_based_stationary_wf(freqs=(200, 400, 600, 800), weights=None, n_samples=43008, sr=44100)

Makes a stationary waveform by mixing a number of freqs together,
possibly with different weights.

* **Parameters:**
  * **freqs** – List(-like) of frequencies (in Hz)
  * **weights** – The weights these frequencies should have (all weights will be normalized
  * **n_samples** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – The number of samples of waveform you want
  * **sr** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Sample rate
* **Return type:**
  `ndarray`
* **Returns:**
  Waveform. A numpy array of samples of the specified sine wave

```pycon
>>> n_samples = random.randint(2,5)
>>> wf = freq_based_stationary_wf(n_samples=n_samples)
>>> assert len(wf) == n_samples
>>> wf = freq_based_stationary_wf(n_samples = 3, weights = [1,2,3,4])
>>> import numpy as np
>>> assert np.allclose(wf, [0.        , 0.08534908, 0.16988139], rtol=1e-3)
```

### loopyng.gen.sine_mix.mk_sine_wf(freq=440, n_samples=43008, sr=44100, phase=0, gain=1)

Make a sine waveform

* **Parameters:**
  * **freq** – Frequency (in Hz)
  * **n_samples** – The number of samples of waveform you want
  * **sr** – Sample rate
  * **phase** – Phase (in radians)
  * **gain** – (A number to multiply the base sine wave by)
* **Returns:**
  Waveform. A numpy array of samples of the specified sine wave

```pycon
>>> n_samples = random.randint(2,5)
>>> wf = mk_sine_wf(n_samples=n_samples)
>>> assert len(wf) == n_samples
>>> wf = mk_sine_wf(n_samples=3)
>>> import numpy as np
>>> assert np.allclose(wf, [0.        , 0.06264832, 0.12505052], rtol=1e-3)
```
