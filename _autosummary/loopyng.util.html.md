# loopyng.util

A few general utils

### Functions

| [`getmodulename`](#loopyng.util.getmodulename)(obj[, default])   | Get name of module of object                                    |
|----------------------------------------------------------------------------------|-----------------------------------------------------------------|
| [`simple_chunker`](#loopyng.util.simple_chunker)(a, chk_size)     | Generate fixed sized non-overlapping chunks of an iterable `a`. |

### Classes

| `ModuleNotFoundErrorNiceMessage`([msg])   |    |
|-------------------------------------------|----|
| `ModuleNotFoundIgnore`()                  |    |

### loopyng.util.getmodulename(obj, default='')

Get name of module of object

### loopyng.util.simple_chunker(a, chk_size)

Generate fixed sized non-overlapping chunks of an iterable `a`.

```pycon
>>> list(simple_chunker(range(7), 3))
[(0, 1, 2), (3, 4, 5)]
```
