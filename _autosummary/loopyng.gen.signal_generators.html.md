# loopyng.gen.signal_generators

Generating Signals

### Functions

| [`alphabet_to_bins`](#loopyng.gen.signal_generators.alphabet_to_bins)([alphabet])                     | Returns a dictionary matching each word in alphabet to bins of size 10.0 ranging from 0 to 10 \* len(alphabet)                                                                               |
|---------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`bernoulli`](#loopyng.gen.signal_generators.bernoulli)([p_out])                               | Returns a random sample of a bernoulli distribution with probability p_out                                                                                                                   |
| [`bernoulli_gen`](#loopyng.gen.signal_generators.bernoulli_gen)([p_out])                           | Returns a generator that returns random samples of a bernoulli distribution with probability p_out                                                                                           |
| [`call_repeatedly`](#loopyng.gen.signal_generators.call_repeatedly)(func, \*args, \*\*kwargs)        | Returns a generator that calls func repeatedly with the given args and kwargs                                                                                                                |
| `categorical_gen`(gen_it)                                                                         |                                                                                                                                                                                              |
| `create_session`(symbol_gen, outlier_gen, alphabet)                                               |                                                                                                                                                                                              |
| [`gen_words`](#loopyng.gen.signal_generators.gen_words)([N, alphabet, spread_pct, proba_dist]) | Returns a generator of lists, with each consisting of n repetitions of a random word for alphabet, with n being determined by a normal distribution with mean N and variance N \* spread_pct |
| [`inlier_outlier`](#loopyng.gen.signal_generators.inlier_outlier)(segment, interval_size, ...)      |                                                                                                                                                                                              |
| [`normal_dist`](#loopyng.gen.signal_generators.normal_dist)(mu, sigma)                           | Returns a random sample from a normal distribution with mean mu and variance sigma                                                                                                           |
| `session_to_df`(session)                                                                          |                                                                                                                                                                                              |
| `signal`(symbol_gen, outlier_gen, alphabet)                                                       |                                                                                                                                                                                              |
| [`string_to_num`](#loopyng.gen.signal_generators.string_to_num)(word)                              | Converts a string to a list of numbers corresponding to the alphabetical order of the characters in the string                                                                               |

### loopyng.gen.signal_generators.alphabet_to_bins(alphabet='abcde')

Returns a dictionary matching each word in alphabet to bins of size 10.0 ranging from 0 to 10 \* len(alphabet)

```pycon
>>> assert alphabet_to_bins() == {
...     'a': (0.0, 10.0), 'b': (10.0, 20.0), 'c': (20.0, 30.0),
...     'd': (30.0, 40.0), 'e': (40.0, 50.0)
... }
```

### loopyng.gen.signal_generators.bernoulli(p_out=0.1)

Returns a random sample of a bernoulli distribution with probability p_out

```pycon
>>> assert bernoulli(0) == 0
>>> assert bernoulli(1) == 1
```

### loopyng.gen.signal_generators.bernoulli_gen(p_out=0.5)

Returns a generator that returns random samples of a bernoulli distribution with probability p_out

### loopyng.gen.signal_generators.call_repeatedly(func, \*args, \*\*kwargs)

Returns a generator that calls func repeatedly with the given args and kwargs

```pycon
>>> gen = call_repeatedly(alphabet_to_bins)
>>> assert next(gen) == {'a': (0.0, 10.0), 'b': (10.0, 20.0), 'c': (20.0, 30.0), 'd': (30.0, 40.0), 'e': (40.0, 50.0)}
>>> assert next(gen) == {
...     'a': (0.0, 10.0), 'b': (10.0, 20.0), 'c': (20.0, 30.0),
...     'd': (30.0, 40.0), 'e': (40.0, 50.0)
... }
```

### loopyng.gen.signal_generators.gen_words(N=30, alphabet='abcde', spread_pct=0.01, proba_dist='normal')

Returns a generator of lists, with each consisting of n repetitions of a random word for alphabet, with n being
determined by a normal distribution with mean N and variance N \* spread_pct

```pycon
>>> gen = gen_words(N=3, alphabet=('foo',), spread_pct=0)
>>> assert next(gen) == ['foo', 'foo', 'foo']
```

### loopyng.gen.signal_generators.inlier_outlier(segment, interval_size, outlier_status)

```pycon
>>> assert inlier_outlier([0,1], 10, 0) < 1
>>> low = np.random.randint(5, 10)
>>> high = np.random.randint(low, 20)
>>> assert inlier_outlier([low, high], low*high, 1) < low + low*high
```

### loopyng.gen.signal_generators.normal_dist(mu, sigma)

Returns a random sample from a normal distribution with mean mu and variance sigma

### loopyng.gen.signal_generators.string_to_num(word)

Converts a string to a list of numbers corresponding to the alphabetical order of the characters in the string

```pycon
>>> assert string_to_num('abc') == [0, 1, 2]
>>> assert string_to_num('generator') == [2, 1, 3, 1, 5, 0, 6, 4, 5]
```
