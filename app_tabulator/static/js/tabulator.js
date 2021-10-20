/*
const array_tests = JSON.parse(document.getElementById('tests').textContent);

var tableDataNested = []        
for (const [key1, arr] of Object.entries(array_tests)){
    tableDataNested.push(arr)
}
*/
console.log("tableDataNested", tableDataNested)






var dateEditor = function(cell, onRendered, success, cancel, editorParams){
    var cellValue = cell.getValue(),
    input = document.createElement("input");
    
    input.setAttribute("type", "text");
    
    input.style.padding = "4px";
    input.style.width = "100%";
    input.style.boxSizing = "border-box";
    
    input.value = typeof cellValue !== "undefined" ? cellValue : "";
    
    onRendered(function(){
        input.style.height = "100%";
        $(input).datepicker({
            onClose: onChange
        }); //turn input into datepicker
        input.focus();
    });

    function onChange(e){
        if(((cellValue === null || typeof cellValue === "undefined") && input.value !== "") || input.value != cellValue){
            success(input.value);
        }else{
            cancel();
        }
    }

    
    //submit new value on blur or change
    input.addEventListener("change", onChange);
    input.addEventListener("blur", onChange);

    //submit new value on enter
    input.addEventListener("keydown", function(e){
        switch(e.keyCode){
            case 13:
            success(input.value);
            break;

            case 27:
            cancel();
            break;
        }
    });
    return input;
    
}


// http://tabulator.info/docs/4.9/format#row
// http://tabulator.info/docs/4.9/tree

var table = new Tabulator("#example-nested-table", {
    backgroundColor:"#efefef",
    minHeight:"300px",
    width:"500px",
    dataTree:true,
    data:tableDataNested,
    dataTreeStartExpanded:true,
    layout:"fitDataStretch",      //fit columns to width of table
    columns:[
    {title:"Name", field:"name", formatter: function(cell, formatterParams) {
        return formatRow(cell)
        }, width: "8px"
    }, //never hide this column
    {title:"ProtocolIdent", field:"ProtocolIdent", hozAlign:"center", visible:0,  resizable:true},
    {title:"TestIdent", field:"TestIdent", hozAlign:"center", visible:0, resizable:true},
    {title:"Prüfung_Voll", field:"TestNameFull", hozAlign:"center", visible:0},
    {title:"Abgerechnet", field:"Invoice", hozAlign:"center", formatter:"tickCross", visible:0},
    {title:"Datum", field:"Date",  hozAlign:"center", resizable:true,  editor:dateEditor, width: "5px"},
    {title:"Start", field:"Start",  hozAlign:"center", resizable:true,  editor:dateEditor, width: "5px"},
    {title:"Stop", field:"Stop",  hozAlign:"center", resizable:true,  editor:dateEditor, width: "5px"},
    {title:"Gesamtzeit", field:"TotalTime",  hozAlign:"center", resizable:true, width: "5px"},
    {title:"Abrechnungsart", field:"InvoiceType",  hozAlign:"center", resizable:true, editor:"select", editorParams:{}, formatter: function(cell, formatterParams) {
        var cellValue = cell.getValue()
        if(cellValue == 0){return 'Nicht abrechnen'}
        if(cellValue == 1){return 'Aufwand'}
        if(cellValue > 1){return 'Pauschale #' + (cellValue-1)}
    }, width: "10px"},
    {title:"Beendet", field:"isTestFinished", hozAlign:"center", editor:true, formatter:"tickCross", resizable:true, formatterParams:{allowEmpty:true}, width: "3px"},//allowTruthy:true 
    {title:"Prüfer", field:"Operator", hozAlign:"center", editor:"input", resizable:true, width: "3px"},
    {title:"Kommentar", field:"Comment",  hozAlign:"center", editor:"input", resizable:true, width: "10px"},
    {title:"Element", field:"element",  hozAlign:"center", visible:0, resizable:true},
    {title:"TreeLevel", field:"treeLevel",  hozAlign:"center", visible:0, resizable:true},
    ],
});

function formatRow(cell){    
    var cellValue = cell.getValue()
    var row = cell.getRow()
    var element = row.getCell('element').getValue()
    var treeLevel = row.getCell('treeLevel').getValue()
    switch(treeLevel){
        case 0:         
            row.getElement().style.paddingTop = "5px";
            row.getElement().style.paddingLeft = "4px";
            break;
        case 2:
            row.getElement().style.paddingLeft = "2px";
            break;
        case 3:
            row.getElement().style.paddingLeft = "4px";
            break;
        default:
            break;
    }
    switch(element){
        case 'header': //1.Überschrift
            switch(treeLevel){
                case 0:
                    row.getElement().style.height = "35px";
                    row.getElement().style.fontSize = "20px";
                    row.getElement().style.fontWeight = 'bold';
                    break;
                case 1: //2. Überschrift
                    row.getElement().style.height = "30px";
                    row.getElement().style.fontSize = "18px";
                    row.getElement().style.paddingBottom = "5px";
                    row.getElement().style.fontWeight = 'bold';
                    break;
                case 4: //3. Überschrift
                    break;
                default:
                    break;
            }
            break;
        case 'test':
            row.getElement().style.paddingTop = "3px";
            row.getElement().style.fontWeight = 'bold';
            break;
        case 'ppb':
            row.getElement().style.backgroundColor = "white";
            break;
        default:
            break;
    }
    if (element != 'ppb'){
        var cells = row.getCells()
        for (let i=0; i<cells.length; i++){
            if (i==0){
                cells[i].getElement().style.width = "100%"; // layout:"fitColumns" ist hier essentiell!!
            }
            if (i<cells.length-1){
                cells[i].getElement().style.border = "none";        
            }  
        }
    }
    return cellValue
}