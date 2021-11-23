# Upgrade

1. File is a `.pptm` file, PowerPoint presentation with Macros
2. Open it in PowerPoint and find a macro called `OnSlideShowPageChange` which changes the title on slide 2 when run
3. Unpacking it reveals a `vbaProject.bin` binary in `ppt/`
4. Use [oletools](https://github.com/decalage2/oletools) to unpack the VBA
5. Running `olevba Upgrades.pptm` gives us this output
```
cosmin@pc-6-15 upgrades % olevba Upgrades.pptm
olevba 0.60 on Python 3.9.7 - http://decalage.info/python/oletools
===============================================================================
FILE: Upgrades.pptm
Type: OpenXML
WARNING  For now, VBA stomping cannot be detected for files in memory
-------------------------------------------------------------------------------
VBA MACRO Module1.bas
in file: ppt/vbaProject.bin - OLE stream: 'VBA/Module1'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Private Function q(g) As String
q = ""
For Each I In g
q = q & Chr((I * 59 - 54) And 255)
Next I
End Function
Sub OnSlideShowPageChange()
j = Array(q(Array(245, 46, 46, 162, 245, 162, 254, 250, 33, 185, 33)), _
q(Array(215, 120, 237, 94, 33, 162, 241, 107, 33, 20, 81, 198, 162, 219, 159, 172, 94, 33, 172, 94)), _
q(Array(245, 46, 46, 162, 89, 159, 120, 33, 162, 254, 63, 206, 63)), _
q(Array(89, 159, 120, 33, 162, 11, 198, 237, 46, 33, 107)), _
q(Array(232, 33, 94, 94, 33, 120, 162, 254, 237, 94, 198, 33)))
g = Int((UBound(j) + 1) * Rnd)
With ActivePresentation.Slides(2).Shapes(2).TextFrame
.TextRange.Text = j(g)
End With
If StrComp(Environ$(q(Array(81, 107, 33, 120, 172, 85, 185, 33))), q(Array(154, 254, 232, 3, 171, 171, 16, 29, 111, 228, 232, 245, 111, 89, 158, 219, 24, 210, 111, 171, 172, 219, 210, 46, 197, 76, 167, 233)), vbBinaryCompare) = 0 Then
VBA.CreateObject(q(Array(215, 11, 59, 120, 237, 146, 94, 236, 11, 250, 33, 198, 198))).Run (q(Array(59, 185, 46, 236, 33, 42, 33, 162, 223, 219, 162, 107, 250, 81, 94, 46, 159, 55, 172, 162, 223, 11)))
End If
End Sub


-------------------------------------------------------------------------------
VBA MACRO Slide1.cls
in file: ppt/vbaProject.bin - OLE stream: 'VBA/Slide1'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Private Sub Label1_Click()

End Sub
+----------+--------------------+---------------------------------------------+
|Type      |Keyword             |Description                                  |
+----------+--------------------+---------------------------------------------+
|AutoExec  |Label1_Click        |Runs when the file is opened and ActiveX     |
|          |                    |objects trigger events                       |
|Suspicious|Environ             |May read system environment variables        |
|Suspicious|Run                 |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|CreateObject        |May create an OLE object                     |
|Suspicious|Chr                 |May attempt to obfuscate specific strings    |
|          |                    |(use option --deobf to deobfuscate)          |
|Suspicious|Hex Strings         |Hex-encoded strings were detected, may be    |
|          |                    |used to obfuscate strings (option --decode to|
|          |                    |see all)                                     |
+----------+--------------------+---------------------------------------------+
```
6. There are a lot of arrays of numbers, resembling some kind of string with ASCII characters in decimal.
7. `q()` seems to be a function that does some number processing before actually returning an ASCII string.
8. In `solve.py` we replicate the same number processing sequence for `q()` with the same number arrays as in the VBA and we get the flag
```
cosmin@pc-6-15 upgrades % python3 solve.py 
Add A Theme
Write Useful Content
Add More TODO
More Slides
Better Title
username
HTB{33zy_VBA_M4CR0_3nC0d1NG}
WScript.Shell
cmd.exe /C shutdown /S
```