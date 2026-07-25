# 上游依据

- Microsoft “Uninstall or remove apps and programs in Windows”：优先 Windows 和厂商支持的卸载路径。
- Microsoft Windows Installer：使用精确 ProductCode 卸载 MSI 产品。
- Microsoft Authenticode 与 `Get-AuthenticodeSignature`：执行前验证卸载器发布者状态。
- Microsoft Sysinternals Autoruns、Process Explorer/Handle、Sigcheck：用于只读归属和残留调查。
- 360 官方产品页面、自保护说明和官方社区的卸载残留案例：用于 360 双产品测试边界。

实现吸收公开方法，不包含或再分发任何厂商安装包、卸载器或第三方代码。
