## PyAudio

``` zsh : Error 
SystemError: PY_SSIZE_T_CLEAN macro must be defined for '#' formats
```

通常，インストールされる `PyAudio` のバージョンは `0.2.11` だがこれを

``` zsh : Upgrade
pip install --upgrade PyAudio==0.2.12
```

とすることで回避できる．