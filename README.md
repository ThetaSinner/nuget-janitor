# NuGet Janitor

Helper for cleaning a NuGet package repository on a file share.

## Packaging and install

Make sure you have the tools you'll need

`python -m pip install --user --upgrade setuptools wheel`

Then prepare your distribution

`python setup.py sdist bdist_wheel`

The wheel can then installed directly

```
python -m venv venv
pip install <path-to-dist>\nuget-janitor-*.whl
python .\venv\Scripts\nuget_janitor --source <package-source> --dry-run
```


## Testing

Here's a very helpful PowerShell command `$(Get-Item abc.nupkg).lastwritetime=$(Get-Date)`
