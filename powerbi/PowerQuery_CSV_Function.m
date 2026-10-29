// Paste into a Blank Query, open Advanced Editor, and name the query fxLoadCsv.
// This function returns a CSV table with promoted headers. Keep ProjectFolder as an
// explicit argument so the project remains portable across Windows computers.
(ProjectFolder as text, FileName as text) as table =>
let
    FullPath = ProjectFolder & "\" & FileName,
    Source = Csv.Document(
        File.Contents(FullPath),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true])
in
    PromotedHeaders

// Example after saving the function:
// = fxLoadCsv("C:\\Users\\YOUR_NAME\\Downloads\\Aarohan-Consumer-Products-Analytics\\outputs", "fact_orders_clean.csv")
// For dimension files, pass the ...\\data folder and the correct CSV filename.
