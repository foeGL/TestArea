const array_tests = JSON.parse(document.getElementById('tests').textContent);

var tableDataNested = []        
for (const [key1, arr] of Object.entries(array_tests)){
    tableDataNested.push(arr)
}

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
    backgroundColor: "#efefef",
    width: "10px",
    dataTree:true,
    //dataTreeChildField:"childRows", //look for the child row data array in the childRows field -- only the top-tier rows
    //minheight:"100px",
    data:tableDataNested,
    dataTreeStartExpanded:true,
    layout:"fitColumns",      //fit columns to width of table
    /*
    dataTreeStartExpanded:function(row, level){
        return row.getData().driver; //expand rows where the "driver" data field is true;
    },
    */
    columns:[
    {title:"Name", field:"name", formatter: function(cell, formatterParams) {
        var cellValue = cell.getValue()
        var row = cell.getRow()
        //console.log("parent of "+cellValue, row.getTreeParent())
        //console.log("children of"+cellValue, row.getTreeChildren())
        //console.log("children.length", children.length)
        var hierarchy = row.getCell('hierarchy').getValue()
        switch(hierarchy){
            case 0: //PPB
                row.getElement().style.fontWeight = 'bold';
                break;
            case 1: //TE
                row.getElement().style.backgroundColor = "white";
                break;
            case 2: //1.Überschrift
                row.getElement().style.height = "30px";
                row.getElement().style.fontSize = "20px";
                row.getElement().style.marginTop = "10px";
                row.getElement().style.fontWeight = 'bold';
                break;
            case 3: //2. Überschrift
                row.getElement().style.height = "30px";
                row.getElement().style.fontSize = "18px";
                row.getElement().style.marginTop = "5px";
                row.getElement().style.marginBottom = "5px";
                row.getElement().style.fontWeight = 'bold';
                break;
            case 4: //3. Überschrift
                break;
            default:
                break;
        }
        if (hierarchy != 1){
            var cells = row.getCells()
            for (let i=0; i<cells.length; i++){
                if (i==0){
                    cells[i].getElement().style.width = "auto"; // layout:"fitColumns" ist hier essentiell!!
                }
                if (i<cells.length-1){
                    cells[i].getElement().style.border = "none";        
                }  
            }
        }
        return cellValue
        }, width: '10px', responsive:0,resizable:true
    }, //never hide this column
    /*
    {title:"Location", field:"location", width:150},
    {title:"Gender", field:"gender", width:150, responsive:2}, //hide this column first
    {title:"Favourite Color", field:"col", width:150},
    {title:"Date Of Birth", field:"dob", hozAlign:"center", sorter:"date", width:150},
    {title:"Driver", field:"driver", width:150},
    */
    //{title:"TestIdent", field:"id", hozAlign:"center", visible:0,  resizable:false},
    //{title:"Norm", field:"Norm", hozAlign:"center", visible:0},        
    {title:"ProtocolIdent", field:"ProtocolIdent", hozAlign:"center", visible:0,  resizable:true},
    {title:"TestIdent", field:"TestIdent", hozAlign:"center", visible:0, resizable:true},
    {title:"Prüfung_Voll", field:"TestNameFull", hozAlign:"center", visible:0},
    {title:"Abgerechnet", field:"Invoice", hozAlign:"center", formatter:"tickCross", visible:0},
    {title:"Datum", field:"Date",  hozAlign:"center", resizable:true,  editor:dateEditor},
    {title:"Start", field:"Start",  hozAlign:"center", resizable:true,  editor:dateEditor},
    {title:"Stop", field:"Stop",  hozAlign:"center", resizable:true,  editor:dateEditor},
    {title:"Gesamtzeit", field:"TotalTime",  hozAlign:"center", resizable:true},
    {title:"Abrechnungsart", field:"InvoiceType",  hozAlign:"center", resizable:true, editor:"select", editorParams:{}, formatter: function(cell, formatterParams) {
        var cellValue = cell.getValue()
        if(cellValue == 0){return 'Nicht abrechnen'}
        if(cellValue == 1){return 'Aufwand'}
        if(cellValue > 1){return 'Pauschale #' + (cellValue-1)}
    }},
    {title:"Beendet", field:"isTestFinished", hozAlign:"center", editor:true, formatter:"tickCross", resizable:true, formatterParams:{allowEmpty:true}},//allowTruthy:true 
    {title:"Prüfer", field:"Operator", hozAlign:"center", editor:"input", resizable:true},
    {title:"Kommentar", field:"Comment",  hozAlign:"center", editor:"input", resizable:true},
    {title:"Hierarchy", field:"hierarchy",  hozAlign:"center", visible:0, resizable:true},
    ],
});