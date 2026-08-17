"""Lazy, informative handling of loopyng's optional dependencies.

loopyng is a signal-*generation* library: its core -- making waveforms out of
numbers -- needs only numpy and scipy. Plotting (matplotlib), notebook playback
(IPython) and the tabular/scaling helpers (pandas, scikit-learn) serve a minority
of the API, so they are optional extras rather than hard install requirements.

That creates a problem this module exists to solve. If a module raises at
*import* time when an extra is missing, `import loopyng` breaks on a bare
install -- the very install the extras were supposed to make possible. If the
package instead swallows the ImportError, the symbol silently vanishes and the
user gets an inscrutable AttributeError somewhere far from the cause.

So: import the optional module if it is there, and otherwise bind a placeholder
that imports fine and raises a clear, actionable ImportError the moment anyone
actually *uses* it. The error names the missing module, what wanted it, and the
exact pip command that fixes it.

    >>> plt = optional_import("no_such_plotting_lib", extra="viz")
    >>> plt.figure()                                    # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    ImportError: no_such_plotting_lib is not installed...

The placeholder is a *class*, not an instance, so it can also stand in for a
type used as a base class -- ``class TimeFormatter(Formatter)`` still defines
cleanly, and only fails when someone tries to instantiate it.

One distinction this module is careful about: *absent* and *renamed* are not the
same failure. ``optional_from`` can fail because the module is missing (an
install problem) or because the module is right there but no longer exports the
name (an API change -- ``matplotlib.cm.get_cmap`` vanished in matplotlib 3.11).
Folding the second into the first produces the worst error a library can emit:
"install matplotlib" on a machine where matplotlib is installed. The two cases
therefore carry different messages, and only the first one mentions pip.
"""

import importlib

PACKAGE_NAME = "loopyng"


def _install_message(target: str, extra: str, used_by: str | None) -> str:
    """Build the "you need to install X" message shown to the user."""
    needed_by = f", needed by {used_by}" if used_by else ""
    return (
        f"{target} is not installed{needed_by}. It is an optional dependency of "
        f"{PACKAGE_NAME}. Install it with:  "
        f'pip install "{PACKAGE_NAME}[{extra}]"'
    )


def _api_mismatch_message(module_name: str, attribute: str, used_by: str | None) -> str:
    """Build the message for a dependency that IS installed but lost the name.

    A missing *module* and a missing *attribute of a present module* are
    different failures with opposite remedies, and telling a user to install
    something they already have is worse than saying nothing: it sends them to
    pip, which reports success, and leaves them where they started. So this case
    gets its own wording -- it never says "not installed".
    """
    needed_by = f", needed by {used_by}" if used_by else ""
    installed_version = _version_of(module_name.split(".")[0])
    return (
        f"{module_name} is installed but has no attribute {attribute!r}"
        f"{needed_by}. This is an API change or a version mismatch"
        f"{installed_version}, not a missing install -- reinstalling or "
        f"installing a {PACKAGE_NAME} extra will not fix it. Please report it at "
        f"https://github.com/thorwhalen/{PACKAGE_NAME}/issues"
    )


def _version_of(distribution_name: str) -> str:
    """Return " (found <name> X.Y)" if the version can be read, else ""."""
    try:
        module = importlib.import_module(distribution_name)
        version = getattr(module, "__version__", None)
    except ImportError:  # pragma: no cover - the caller just imported it
        version = None
    return f" (found {distribution_name} {version})" if version else ""


# Dunders a caller reads for information about the module rather than as part of
# a language protocol. These deserve the informative ImportError; the protocol
# dunders (__copy__, __wrapped__, __iter__, ...) must stay AttributeError so that
# copy/pickle/inspect keep working instead of exploding with the wrong type.
INFORMATIONAL_DUNDERS = ("__version__", "__file__", "__path__", "__all__")


class MissingDependencyType(type):
    """Metaclass whose classes raise a clear ImportError on any real use.

    Attribute access and instantiation both raise; protocol dunder lookups raise
    AttributeError instead, so ordinary introspection (``repr``, ``copy``,
    ``inspect``) keeps working rather than exploding with the wrong error type.
    """

    def __getattr__(cls, name):
        is_protocol_dunder = (
            name.startswith("__")
            and name.endswith("__")
            and name not in INFORMATIONAL_DUNDERS
        )
        if is_protocol_dunder:
            raise AttributeError(name)
        raise ImportError(cls._missing_dependency_message)

    def __call__(cls, *args, **kwargs):
        raise ImportError(cls._missing_dependency_message)

    def __repr__(cls):
        return f"<missing optional dependency: {cls._missing_dependency_target}>"


def _placeholder(target: str, message: str):
    """Make the stand-in class bound in place of an import that did not work.

    :param target: What could not be bound, e.g. ``"matplotlib.cm.get_cmap"``
    :param message: The ImportError text raised when anyone uses it
    """
    return MissingDependencyType(
        "MissingOptionalDependency",
        (),
        {
            "_missing_dependency_target": target,
            "_missing_dependency_message": message,
            "__doc__": message,
        },
    )


def optional_import(module_name: str, *, extra: str, used_by: str | None = None):
    """Import ``module_name``, or return a placeholder that explains its absence.

    :param module_name: Module to import, e.g. ``"matplotlib.pylab"``
    :param extra: The loopyng extra that provides it, e.g. ``"viz"``
    :param used_by: What needs it, for the error message
    :return: The module, or a placeholder raising ImportError when used

    >>> np = optional_import("numpy", extra="viz")
    >>> np.array([1, 2]).tolist()
    [1, 2]
    """
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return _placeholder(module_name, _install_message(module_name, extra, used_by))


def optional_from(
    module_name: str, attribute: str, *, extra: str, used_by: str | None = None
):
    """Like ``from module_name import attribute``, tolerating a missing module.

    :param module_name: Module to import from, e.g. ``"IPython.display"``
    :param attribute: Name to pull out of it, e.g. ``"Audio"``
    :param extra: The loopyng extra that provides it, e.g. ``"notebook"``
    :param used_by: What needs it, for the error message
    :return: The attribute, or a placeholder raising ImportError when used

    The two ways this can fail are kept apart on purpose. A missing *module* is
    an install problem and gets the "install the extra" message. A module that
    imports fine but no longer has the attribute is an API/version problem, and
    saying "not installed" about a package the user demonstrably has installed
    sends them to pip for a fix pip cannot make:

    >>> array = optional_from("numpy", "array", extra="viz")
    >>> array([1, 2]).tolist()
    [1, 2]
    >>> gone = optional_from("numpy", "no_such_numpy_function", extra="viz")
    >>> gone()                                          # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    ImportError: numpy is installed but has no attribute 'no_such_numpy_function'...
    """
    target = f"{module_name}.{attribute}"
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return _placeholder(target, _install_message(target, extra, used_by))
    try:
        return getattr(module, attribute)
    except AttributeError:
        return _placeholder(
            target, _api_mismatch_message(module_name, attribute, used_by)
        )


def require(module_name: str, *, extra: str, used_by: str | None = None):
    """Import ``module_name`` now, raising the informative ImportError if absent.

    For call sites that need the dependency immediately -- typically to resolve
    a default argument that cannot be evaluated at import time.

    :param module_name: Module to import
    :param extra: The loopyng extra that provides it
    :param used_by: What needs it, for the error message
    :return: The module

    >>> require("numpy", extra="viz").pi  # doctest: +ELLIPSIS
    3.14159...
    """
    try:
        return importlib.import_module(module_name)
    except ImportError as error:
        raise ImportError(_install_message(module_name, extra, used_by)) from error
