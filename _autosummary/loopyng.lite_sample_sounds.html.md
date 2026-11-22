# loopyng.lite_sample_sounds

Generate simple waveforms for audio synthesis and testing.

Provides functions to create random samples, pure tones, triangular tones,
square tones, and annotated waveforms with different characteristics.

### Functions

| [`chk_from_pattern`](#loopyng.lite_sample_sounds.chk_from_pattern)([chk_size, pattern])            | Returns a chk with length chk_size that repeats pattern if given, or creates a random pattern of length 100   |
|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| `mk_audio_store`([chk_size])                                                                      |                                                                                                               |
| [`pure_tone`](#loopyng.lite_sample_sounds.pure_tone)([chk_size, freq, sr, max_amplitude])   | Generates a pure tone using given arguments                                                                   |
| [`random_samples`](#loopyng.lite_sample_sounds.random_samples)([chk_size, max_amplitude])        | Returns a random sample of integers of length chk_size in the range [-max_amplitude, max_amplitude]           |
| [`square_tone`](#loopyng.lite_sample_sounds.square_tone)([chk_size, freq, sr, max_amplitude]) | Generates a square tone using given arguments                                                                 |
| [`tag_wf_gen`](#loopyng.lite_sample_sounds.tag_wf_gen)([tag_wfgen_map, tag_sequence])        | Generate tagged waveforms -- i.e. `(tag, wf)` pairs.                                                          |
| [`triangular_tone`](#loopyng.lite_sample_sounds.triangular_tone)([chk_size, freq, sr, ...])       | Generates a triangular tone using given arguments                                                             |

### Classes

| [`AnnotatedWaveform`](#loopyng.lite_sample_sounds.AnnotatedWaveform)([chk_size, freq, sr, ...])   | Creates a waveform with chunks corresponding to the tags in tag_to_wf_gen_func.   |
|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|

### *class* loopyng.lite_sample_sounds.AnnotatedWaveform(chk_size=43008, freq=440, sr=44100, max_amplitude=30000)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Creates a waveform with chunks corresponding to the tags in tag_to_wf_gen_func.

```pycon
>>> np.random.seed(1)
>>> annotated_wf = AnnotatedWaveform(chk_size = 4)
>>> chk_tag_gen = annotated_wf.chk_and_tag_gen()
>>> wf, annots = annotated_wf.get_wf_and_annots()
>>> assert list(wf) == [
...     3003, -17828, -24808, 2511, 0, 1902, 3797, 5677, -30000,
...     -29900, -29800, -29700, 30000, 30000, 30000, 30000
... ]
>>> assert list(next(chk_tag_gen)[0]) == [20057, 13723, -22187, 22047]
```

#### chk_and_tag_gen(chk_tags=('random', 'pure_tone', 'triangular_tone', 'square_tone'))

Yields (chk, tag) pairs for each tag given in chk_tags

#### get_wf_and_annots(chk_tags=('random', 'pure_tone', 'triangular_tone', 'square_tone'))

Yields (wf, annots) tuple where annots is a dictionary mapping tag to chunk indices

### loopyng.lite_sample_sounds.chk_from_pattern(chk_size=43008, pattern=None)

Returns a chk with length chk_size that repeats pattern if given, or creates a random pattern of length 100

```pycon
>>> np.random.seed(1)
>>> assert all(chk_from_pattern(5) == [3003, -17828, -24808, 2511, 20057])
>>> chk = chk_from_pattern(6, [1,2,3])
>>> assert all(chk == [1, 2, 3, 1, 2, 3])
```

### loopyng.lite_sample_sounds.pure_tone(chk_size=43008, freq=440, sr=44100, max_amplitude=30000)

Generates a pure tone using given arguments

```pycon
>>> np.random.seed(1)
>>> assert all(pure_tone(5) == [0, 1902, 3797, 5677, 7534])
```

### loopyng.lite_sample_sounds.random_samples(chk_size=43008, max_amplitude=30000, \*\*kwargs)

Returns a random sample of integers of length chk_size in the range [-max_amplitude, max_amplitude]

```pycon
>>> np.random.seed(1)
>>> assert all(random_samples(5) == [3003, -17828, -24808, 2511, 20057])
```

### loopyng.lite_sample_sounds.square_tone(chk_size=43008, freq=440, sr=44100, max_amplitude=30000)

Generates a square tone using given arguments

```pycon
>>> np.random.seed(1)
>>> assert all(square_tone(5) == [30000, 30000, 30000, 30000, 30000])
```

### loopyng.lite_sample_sounds.tag_wf_gen(tag_wfgen_map=(('random', <function random_samples>), ('pure_tone', <function pure_tone>), ('triangular_tone', <function triangular_tone>), ('square_tone', <function square_tone>)), tag_sequence=None)

Generate tagged waveforms – i.e. `(tag, wf)` pairs.

* **Parameters:**
  * **tag_wfgen_map** ([`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)[`Tag`, [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[`...`](https://docs.python.org/3/builtins/constants.html#Ellipsis), [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)]]) – A `{tag: wfgen, ...}` map where wfgen is a callable taking
    no arguments and returning a sequence
  * **tag_sequence** ([`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[`Tag`] | [`None`](https://docs.python.org/3/builtins/constants.html#None)) – A sequence of tags (that should all be keys of tag_wfgen_map)
* **Returns:**

Make a generator (here with default specs):

```pycon
>>> gen = tag_wf_gen()
```

From it, source `(tag, wf)` pairs (by default, indefinitely).

```pycon
>>> tag, wf = next(gen)
```

Since by default, we’re given random `tag` and `wf`, the only thing we can
verify here is that tag is a string and `wf` has the default size of 43008.

```pycon
>>> type(tag)
<class 'str'>
>>> len(wf)
43008
```

By default the tags are randomly chosen from the `tag_wfgen_map`, but you can
also specify a iterable of tags explicitly. Obviously, the elements of this
sequence must actually be keys of `tag_wfgen_map` – this will be asserted if
the iterable is a Sequence.

You can specify a sequence of tags:

```pycon
>>> gen = tag_wf_gen(
...     tag_sequence=['random', 'pure_tone', 'triangular_tone', 'square_tone']
... )
>>> tag_and_wf_seq = list(gen)  # consume the whole gen
>>> [x[0] for x in tag_and_wf_seq]
['random', 'pure_tone', 'triangular_tone', 'square_tone']
```

The first 5 numbers of the triangular tone

```pycon
>>> assert list(tag_and_wf_seq[2][1][:5]) == [-30000, -29900, -29800, -29700, -29600]
```

### loopyng.lite_sample_sounds.triangular_tone(chk_size=43008, freq=440, sr=44100, max_amplitude=30000)

Generates a triangular tone using given arguments

```pycon
>>> np.random.seed(1)
>>> assert all(triangular_tone(5) == [-30000, -29900, -29800, -29700, -29600])
```
