# Curated official Fabric item icons

Eight unmodified SVGs are included: lakehouse, notebook, ML experiment, ML model,
pipeline, Dataflow Gen2, semantic model and Power BI report.
Use `icon_path("lakehouse", family="fabric")` from the bundled helper.
Unknown families/keys or modified files fail explicitly; no network fetch occurs.

Source: [Microsoft's official Fabric icon page](https://learn.microsoft.com/en-us/fabric/fundamentals/icons),
which links to `microsoft/fabric-samples/docs-samples/Icons.zip`.
This copy is pinned at [commit 564ec4139742b838468fcf8aa44dac4afe02ce92](https://github.com/microsoft/fabric-samples/commit/564ec4139742b838468fcf8aa44dac4afe02ce92);
the archive contains package **v6.1.0**.
Archive SHA-256: `fc22e71b0545ed15e22c53f16bf4fb06ffe72daabd3c90a947a6e481c9675e6b`.
Reviewed **2026-11-02**.

The archive's original [Microsoft MIT license](LICENSE) is preserved unchanged.
This differs from the Foundry/Azure icon archive's permitted-use notice.
Microsoft's Fabric icon page additionally gives architecture/training/documentation
usage guidance: retain original appearance, do not crop/flip/rotate/distort, label
the products, and do not use their symbols to represent your own service.
No trademark ownership or Microsoft endorsement is implied.

[catalog.json](catalog.json) records exact archive members and SVG hashes.
Only the selected SVGs and license are copied, not package JavaScript, the
entire archive or dependencies. The icon size suffix identifies the upstream
variant; scaling with its aspect ratio preserved does not alter its source.

See the [official-icon Fabric example](../../examples/fabric-official/README.md).
A pipeline icon is not a copy-activity icon; generic activities remain neutral
when no correctly corresponding symbol is included.
