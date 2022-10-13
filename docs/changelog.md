
# Changelog

## 0.1.9

- Corrected the type signature of the `enabled_when_frozen` decorator. The new
  signature is `(method: Callable) -> Any`. The signature was previously
  `(method: _F) -> _F` where `_F` is a type variable bounded by `Callable`.
  This was incorrect because if a callable object that was not a user function
  was given, then the return type would be a user function, which is
  inconsistent with the signature.
