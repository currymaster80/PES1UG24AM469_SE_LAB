# Lab 5: Static Code Analysis — Issue Documentation

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Use of MD5 hash | Security — High | 49 | MD5 is a weak hashing algorithm and should not be used for security-sensitive purposes. | Replace MD5 with SHA-256 if a stronger hash is required. |
| Unsafe shell execution | Security — High | 60 | `os.system()` executes a shell command using a filename that may contain unsafe input. | Remove the shell command and use a safe Python print statement. |
| Use of `eval()` | Security — Medium | 44 | `eval()` executes an expression supplied as a string, which may allow arbitrary code execution. | Replace it with a safe discount calculation using validated numeric input. |
| Mutable default argument | Code quality / Bug | 15 | `audit_log=[]` creates a shared list that may retain entries between calls. | Use `None` as the default and initialize a new list when needed. |
| Bare exception handler | Code quality / Security | 26–29 | The bare `except` catches all exceptions and silently ignores errors. | Catch the specific expected exception and handle it appropriately. |
| Insecure random number generation | Security — Low | 53 | `random.randint()` is not designed for security-sensitive PIN generation. | Use `secrets` for a security-sensitive checkout PIN. |
| Unused import | Code quality / Style | 4 | The `math` module is imported but never used. | Remove the unused import. |
| Unused variables and comparison style | Code quality / Style | 33–43 | Unused variables and comparison with `None` reduce code clarity. | Remove unused variables and use `is None` for the comparison. |

