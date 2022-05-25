# PowerShell basics
---
# Navigation
- **[[#Commands and Operators]]**
	- [[#Listing examples for a command]]
	- [[#List commands by type and function]]
	- [[#Output Formats]]
	- [[#Useful Operators for Parsing]]
	- [[#Difference between Double and single quotes]]
	- [[#Writing Multi-lines]]
	- [[#Get variable type]]
- **[[#Arrays]]**
- **[Hashtables dictionaries](#Hashtables%20dictionaries)**
- **[[#Conditional statements]]**
	- [[#If Statement]]
	- [[#Switch Statement]]
- **[[#Loop statements]]**
	- [[#For loop]]
	- [[#While loop]]
	- [[#Where-object]]
- **[[#Functions]]**
	- [[#Using parameters]]
	- [[#Passing parameters]]
	- [[#Positioning parameters]]
	- [[#Identifying alot of parameters than defined in the function]]
	- [[#Using switch parameter]]
	- [[#Advanced Functions]]
	- [[#Advanced Scripting]]
- **[[#Remoting]]**
	- [[#Running commands remotely]]
	- [[#Making a Credential object]]
- **[[#Jobs]]**
- **[[#Modules]]**
	- [[#Listing modules]]
	- [[#Importing modules]]
	- [[#List module commands]]
	- [[#Remove module]]
	- [[#Module manifest]]
---
# Commands and Operators
## Listing examples for a command
```powershell
Get-Help <COMMAND> -Examples 
#Getting parameter list  
Get-Help <COMMAND> -Parameter *
```
## List commands by type and function
- For example i want to know which command list the processes
```powershell
Get-Command -commandType cmdlet -name *process*
#You can pipe above command to 'Measure-Object' to print number of lines
Get-Command -commandType cmdlet -name *process* | Measure-Object
```
## Output Formats
```powershell
Get-Command -name out *  
Get-command -name format *
```
## Useful Operators for Parsing
```powershell
"string" -replace "ing","aight"  #output -> straight
"string string string" -split " ",<number to split upon on>  
"welcome","zeyad" -join " "   #output -> welcome zeyad
```
## Difference between Double and single quotes
```powershell
$a = "hello"  
$b = "zeyad"  
"$a $b" #Prints -> hello zeyad  
'$a $b' #Prints -> $a $b
```
## Writing Multi-lines
```powershell
@" <press enter>  
<text>  
"@ <press enter>
```
## Get variable type
```powershell
$<var>.GetType()
```
---
## Arrays
- **Implicit creation**: $array = 4,6,1,60,23,53
- **Explicit creation**: $array = @(4,6,”s”,60,”yes”,5.3)
- **Ranged creation**: $array = 1..100
- **Strongly typed**: [int32[]]$array = 1500,1600,1700,1800
```powershell
$a = 1 + 6.5  
[int]$a #Prints 8  
  
#Empty array  
$a = @()  
  
#Array with elements  
$a = 1,2,"ss",3  
  
#Print a specific element  
$a[0]
```
- Arrays are immutable - there’s no easy way to remove an element from an array... in order to do that use:
```powershell
$ArrayList = New-Object System.Collections.ArrayList
$ArrayList.Add($Value) and $arraylist.Remove($Value)
$ArrayList.ToArray()
```
## Hashtables (dictionaries)
- PowerShell Version 3+ also has **\[ordered\]** hash tables
- Keys/Values can be any .NET object type
```powershell
[ordered]@{ <name> = <value>; [<name> = <value> ] ...}
@{ <name> = <value>; [<name> = <value> ] ...}
$hash = @{one = "apple"; two=2; three="orange"}

# Get a value
$hash["one"]

$hash.keys # return the keys of the hash table
$hash.values # return the values of the hash table

#Key/value addition:
$hash.Add('Key', 'Value')
$hash = $hash + @{Key="Value"}
#Can be nested: 
$Hash = $Hash + @{"Value2"= @{a=1; b=2; c=3}}

#Only way to remove a key
$hash.Remove("Key")
```
> Read about hashtables splatting
---
# Conditional statements
## If Statement
```powershell
if ( 1 -gt 0){"hello"} else {"not hello"}  
if (((Get-Process).count) -lt 50 ){"less than 50"} else {"more than 50"}
```

## Switch Statement
```powershell
switch (1) { 1 {"you chose number one"} 2 {"you chose number two"} default {"default"}}  
switch -wildcard ('abc') { a* {"A"} *b* {"B"} c* {"C"}}
```
---
# Loop statements
## For loop
```powershell  
$s = Get-ChildItem  
foreach ($a in $s){"item is $a"} #prints the content of the current directory  
Get-Process | ForEach-Object {$_.ProcessName}  
Get-Process | ForEach-Object processname #Similar to the upper one  
```  
## While loop
```powershell
$count = 0  
while ($count -lt 7){"item is : $count", $count++}
```
## Where-object
```powershell
Get-ChildItem -Recurse C:\\ | Where-Object {$_.name -match "txt"}   
```
## Getting the path for every process
```powershell
Get-Process | ForEach-Object {$_.path}
```
---
# Functions
```powershell
function add { 4 + 5 }  
add #calls the function and prints the answer  
```
## Using parameters
```powershell
function parameter { $args }  
parameter "hello" # calls the function and assignes "hello" to the $args (while $args is an array) then outputs "hello"  
  
function parameter { $args[0] + $args[1] }  
parameter 4 7 #Outputs the output from the adding  
```
## Passing parameters
```powershell
function add ($num1,$num2){$num1 + $num2}  
add 4 7   
```  
## Positioning parameters
```powershell
function parameter ($param1,$param2){$param1}  
parameter -param2 5 -param1 4 #Prints 4
```
## Identifying alot of parameters than defined in the function
```powershell
 function params ($p1,$p2){$p1,$p2,$args}  
params g g g #prints 3 g's  
```
## Using switch parameter  
```powershell
 function switchable ($p1,$p2,[switch]$p3) {if ($p3){$p1 + $p2}}  
 switchable 1 2 #outputs notthing  
 switchable 1 2 -p3 #outputs 3   
#You can assign the function to a variable  
$output = switchable 1 2 -p3   
$output #Prints 3   
  
#Example: a function that accept a process name,pid,service name then stop it   
function process-mon($proc,$serv,$procid,[switch]$stop_pd,[switch]$stop_ps,[switch]$stop_sv){if ($stop_ps){stop-process -name $proc}},{if ($stop_sv){stop-service -name $serv}},{if ($stop_pd){stop-process -id $procid}}  
#The above function needs fixing for the pid parameter to work
```
## Advanced Functions
```powershell
function advanced  
{  
    param (  
        [parameter (mandatory = $true , position = 0 , valuefrompipeline = $true)][AllowNull()][string]$a  #Mandatory   & position is for providing the position & and value frompipeline is for passing a value from a pipe |  
        ,  
        [parameter (position = 1)]$b  #If you provided a position attribute for one parameter you must provide it for the rest.  
        )  
write-output " a is $a"  
write-output " b is $b"  
}
```
## Advanced Scripting
```powershell
function advanced {  
    [cmdletbinding(SupportsShouldProcess=$true)]  
  
    param (  
        [parameter()]$filepath  
        )  
  
        Write-Verbose " Removing the $filepath "  #Works when i provide -verbose option with the script  
  
        if ($PSCmdlet.ShouldProcess("$filepath","Deleting the file permanently"))   #To specify a custom message when running the script  
        {Remove-Item $filepath}  
        }  
          
#Options when running the script :  
-whatif  
-verbose  
-<manymore>
```
---
# Remoting
You need to be in the administrative group in the remote machine and to be in the same domain or to be in a trusted workgroup  
1. Put the host name/ip in the `trustedhosts` file after enabling the ps-remoting.
2.  `enable-psremoting`  
3.  `set-item wsman:\localhost\client\trustedhosts -Value computername/ip`  (accept regex)
> **Note:**
> You need to do this for both machines.
## Running commands remotely
```powershell
#Commands with "computername" parameter can execute commnads remotley  
#To get these commands  
Get-Command -Type cmdlet -ParameterName computername  
  
#You can execute a command on multiple hosts with a for loop statement or if using invoke-commnad just put a ',' between computer names (requires to be the admin for the domain those computers are in)  
invoke-command -scriptblock { command } -computername <value> -credentials Pcname\username  
  
#To open a session   
enter-pssession -computername <name> -credentials pcname\username  
  
#You can save a session as a variable and invoke commnads to  
$sess = new-pssession <with its parameters>  
invoke-command <Commands> -session $sess
```
## Making a Credential object
```powershell
$password = ConvertTo-SecureString 'SuperSecurePassword' -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential ('<Domanin>\<User>', $password)
Invoke-Command -Credential $credential -ComputerName abuqasemPC -FilePath 'C:\Scripts\Pwned.ps1'
```
> **Source:**
> https://duffney.io/addcredentialstopowershellfunctions/
---
## Jobs
```powershell
start-job -scriptblock {}  
recieve-job #to get the output  
stop-job  
  
#running commands as jobs in remote computer  
invoke-commnad <parameters> -asjob  
  
#running commands in a specific session  
$sess = new-pssession <parameters>  
invoke-commnad <parameters> -session $sess
```
---
# Modules
Modules PATH `$Env:PSModulePath`
## Listing modules
```powershell
Get-Module -ListAvailable
#Get loaded modules
Get-Module
```
## Importing modules
```powershell
Import-Module <PowerShellScript>
#In Case of blocking our scripts
set-ExecutionPolicy bypass -Force 
# -Force: suppresses all confirmation prompts.
# Bypass: Nothing is blocked.
```
## List module commands
```powershell
Get-Command -Module <PowerShellScript>
#List parameters for a specific function or a cmdlet
(Get-Command <Cmdlet/Function>).parameters
#Example: (Get-Command Get-ChildItem).parameters
Get-Help <cmdlet/Function> -Full #(Detailed)
#Example: Get-Help Invoke-PortScan -Full 
```
## Remove module
```powershell
Remove-Module <PowerShellScript>
```
## Module manifest
A **module manifest** is a PowerShell data file (`.psd1`) that describes the contents of a module and determines how a module is processed. The manifest file is a text file that contains a hash table of keys and values. You link a manifest file to a module by naming the manifest the same as the module, and storing the manifest in the module's root directory.
```powershell
New-ModuleManifest -Path C:\myModuleName.psd1
#Testing the Manifest after creation to confirm that any paths described in the manifest are correct
Test-ModuleManifest myModuleName.psd1
```
> **Further Reading**: https://docs.microsoft.com/en-us/powershell/scripting/developer/module/how-to-write-a-powershell-module-manifest?view=powershell-7.1