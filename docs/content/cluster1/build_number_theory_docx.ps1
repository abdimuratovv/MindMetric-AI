param([switch]$ExportPdf)
$ErrorActionPreference = 'Stop'
$sourcePath = Join-Path $PSScriptRoot '1.4-mavzu.md'
$outputPath = Join-Path $PSScriptRoot '1.4-mavzu.docx'
$qaPath = Join-Path $PSScriptRoot '..\..\..\backups\number-theory-docx-qa'
New-Item -ItemType Directory -Path $qaPath -Force | Out-Null
$qaPath = (Resolve-Path -LiteralPath $qaPath).Path
$wordApp = $null
$document = $null
try {
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $document = $wordApp.Documents.Add()
    $document.PageSetup.PaperSize = 7
    $document.PageSetup.TopMargin = 56.7
    $document.PageSetup.BottomMargin = 56.7
    $document.PageSetup.LeftMargin = 56.7
    $document.PageSetup.RightMargin = 56.7
    foreach ($styleId in @(-1,-2,-3,-63)) {
        $style = $document.Styles.Item($styleId)
        $style.Font.Name = 'Calibri'
        $style.Font.Color = 0
        $style.Font.Underline = 0
    }
    $document.Styles.Item(-1).Font.Size = 11
    $document.Styles.Item(-1).ParagraphFormat.SpaceAfter = 6
    $document.Styles.Item(-63).Font.Size = 20
    $progressPath = Join-Path $qaPath 'word-build.log'
    'Authoring started' | Set-Content -LiteralPath $progressPath
    $paragraphTexts = New-Object 'System.Collections.Generic.List[string]'
    $headings = @()
    $lessonIndex = 0
    foreach ($line in (Get-Content -LiteralPath $sourcePath -Encoding UTF8)) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        $text = $line
        if ($line.StartsWith('# ')) {
            $headings += @{ Index = $paragraphTexts.Count + 1; Style = -63; NewPage = 0 }
            $text = 'Sonlar nazariyasi va diskret matematika'
        } elseif ($line.StartsWith('### ')) {
            $lessonIndex += 1
            $headings += @{ Index = $paragraphTexts.Count + 1; Style = -3; NewPage = (-[int]($lessonIndex -gt 1)) }
            $text = $line.Substring(4)
        } elseif ($line.StartsWith('## ')) {
            $headings += @{ Index = $paragraphTexts.Count + 1; Style = -2; NewPage = (-[int](($lessonIndex -gt 0) -and ($line -notlike '## Baholash*'))) }
            $text = $line.Substring(3)
        }
        $paragraphTexts.Add($text)
    }
    $document.Content.Text = ($paragraphTexts -join "`r")
    'Content inserted' | Add-Content -LiteralPath $progressPath
    foreach ($entry in $headings) {
        $paragraph = $document.Paragraphs.Item($entry.Index)
        $paragraph.Style = $document.Styles.Item($entry.Style)
        $paragraph.Format.PageBreakBefore = $entry.NewPage
    }
    for ($index = 0; $index -lt $paragraphTexts.Count; $index++) {
        if (($paragraphTexts[$index] -like 'numbers-*') -or ($paragraphTexts[$index] -match '^[a-d]\)')) {
            $document.Paragraphs.Item($index + 1).Format.KeepWithNext = -1
        }
    }
    'Headings formatted' | Add-Content -LiteralPath $progressPath
    $document.Repaginate()
    'Saving DOCX' | Add-Content -LiteralPath $progressPath
    # Serialize Word's native Flat OPC package without the interactive Save As
    # integration (which can wait for account dialogs on desktop Office).
    [xml]$flatPackage = $document.Content.WordOpenXML
    Add-Type -AssemblyName System.IO.Compression
    $namespaces = New-Object System.Xml.XmlNamespaceManager($flatPackage.NameTable)
    $namespaces.AddNamespace('pkg','http://schemas.microsoft.com/office/2006/xmlPackage')
    $parts = $flatPackage.SelectNodes('/pkg:package/pkg:part',$namespaces)
    $stream = [System.IO.File]::Open($outputPath,[System.IO.FileMode]::Create)
    $zip = New-Object System.IO.Compression.ZipArchive($stream,[System.IO.Compression.ZipArchiveMode]::Create)
    try {
        $contentTypes = '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        foreach ($part in $parts) {
            $name = $part.GetAttribute('name','http://schemas.microsoft.com/office/2006/xmlPackage')
            $contentType = $part.GetAttribute('contentType','http://schemas.microsoft.com/office/2006/xmlPackage')
            $contentTypes += '<Override PartName="' + $name + '" ContentType="' + $contentType + '"/>'
            $entry = $zip.CreateEntry($name.TrimStart('/'))
            $entryStream = $entry.Open()
            try {
                $xmlData = $part.SelectSingleNode('pkg:xmlData',$namespaces)
                if ($null -ne $xmlData) {
                    $bytes = [System.Text.Encoding]::UTF8.GetBytes($xmlData.InnerXml)
                } else {
                    $bytes = [System.Convert]::FromBase64String($part.SelectSingleNode('pkg:binaryData',$namespaces).InnerText)
                }
                $entryStream.Write($bytes,0,$bytes.Length)
            } finally { $entryStream.Dispose() }
        }
        $contentTypes += '</Types>'
        $entry = $zip.CreateEntry('[Content_Types].xml')
        $entryStream = $entry.Open()
        try {
            $bytes = [System.Text.Encoding]::UTF8.GetBytes($contentTypes)
            $entryStream.Write($bytes,0,$bytes.Length)
        } finally { $entryStream.Dispose() }
    } finally { $zip.Dispose(); $stream.Dispose() }
    if ($ExportPdf) {
        'Exporting PDF' | Add-Content -LiteralPath $progressPath
        $document.ExportAsFixedFormat((Join-Path $qaPath '1.4-mavzu.pdf'),17)
    }
    Write-Output ('Word resource saved; pages: ' + $document.ComputeStatistics(2))
} finally {
    if ($null -ne $document) { $document.Close(0) }
    if ($null -ne $wordApp) { $wordApp.Quit() }
}
