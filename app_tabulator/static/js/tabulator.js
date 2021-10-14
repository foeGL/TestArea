const array_tests = JSON.parse(document.getElementById('tests').textContent);
const array_protocol = JSON.parse(document.getElementById('protocol').textContent);

var invoiceTypes = ["Nicht abrechnen", "Aufwand", "Pauschal"]      // Auswahl für InvoiceTypes 
var groupByField = "TestNameFull" //["Norm", "TestNameFull"]               // Tabelle nach TestNameFull gruppieren
var global_id_DB = [];                          // Wird für InvoiceType verwendet!!
var tests_id = []                               // array mit ids für tabledata
var tests_name = []                             // array mit (kurzem) testName
var tests_description = []
var tests_tabledata = []    


for (var key in array_tests){
    value = array_tests[key]
    tests_id.push(key)
    tests_name.push(value['name'])
    tests_tabledata.push(value['formatted'])
};

var tabledata = []
var tablePos = 0
for (var key in array_protocol){
    var TestIdent = array_protocol[key]['TestIdent']         
    var InvoiceType_exchange = '';
    var formattedName = ""
    var TestName = ""
    var Standard = ""
    if (TestIdent == 0){
        TestIdent = ""
    } else {        
        formattedName = typeof array_tests[TestIdent]['formatted'] !== "undefined" ? array_tests[TestIdent]['formatted'] : "";
        TestName = array_tests[TestIdent]['name']
        Standard = array_tests[TestIdent]['standard']
    }
    tabledata.push({
        //id:             tablePos,
        Norm:           Standard,
        ProtocolIdent:  array_protocol[key]['ProtocolIdent'],
        TestIdent:      TestIdent, 
        TestNameFull:   formattedName, 
        TestName:       TestName, 
        Operator:       array_protocol[key]['Operator'], 
        InvoiceType:    InvoiceType_exchange, 
        Date:           array_protocol[key]['Date'], 
        Start:          array_protocol[key]['Start'], 
        Stop:           array_protocol[key]['Stop'], 
        TotalTime:      array_protocol[key]['TotalTime'].toFixed(1), 
        isTestFinished: array_protocol[key]['isTestFinished'],
        Comment:        array_protocol[key]['Comment'],
        _children: []
    })
    tablePos += 1;
};

//define data array
/*
var tabledata = [
    {id:1, name:"Oli Bob", progress:12, gender:"male", rating:1, col:"red", dob:"19/02/1984", car:1},
    {id:2, name:"Mary May", progress:1, gender:"female", rating:2, col:"blue", dob:"14/05/1982", car:true},
    {id:3, name:"Christine Lobowski", progress:42, gender:"female", rating:0, col:"green", dob:"22/05/1982", car:"true"},
    {id:4, name:"Brendon Philips", progress:100, gender:"male", rating:1, col:"orange", dob:"01/08/1980"},
    {id:5, name:"Margret Marmajuke", progress:16, gender:"female", rating:5, col:"yellow", dob:"31/01/1999"},
    {id:6, name:"Frank Harbours", progress:38, gender:"male", rating:4, col:"red", dob:"12/05/1966", car:1},
];
*/
//initialize table
/*
var table = new Tabulator("#example-table", {
    data:tabledata, //assign data to table
    autoColumns:true, //create columns from data field names
});
*/


var table = new Tabulator("#example-table", {
    data:tabledata,           //load row data from array
    dataTree:true,
    dataTreeStartExpanded:true,
    layout:"fitColumns",      //fit columns to width of table
    responsiveLayout:"hide",  //hide columns that dont fit on the table
    tooltips:true,            //show tool tips on cells
    addRowPos:"top",          //when adding a new row, add it to the top of the table
    //history:true,             //allow undo and redo actions on the table
    //pagination:"local",       //paginate the data
    //paginationSize:7,         //allow 7 rows per page of data
    //movableColumns:true,      //allow column order to be changed
    //groupBy:["Norm","TestNameFull"],
    resizableRows:true,       //allow row order to be changed
    /*initialSort:[             //set the initial sort order of the data
        {column:"Norm", dir:"asc"},
        {column:"TestNameFull", dir:"asc"},
        {column:"Date", dir:"asc"},
        {column:"Start", dir:"asc"},
    ],*/
    columns:[                 //define the table columns
        /*
        {title:"Name", field:"name", editor:"input"},
        {title:"Task Progress", field:"progress", hozAlign:"left", formatter:"progress", editor:true},
        {title:"Gender", field:"gender", width:95, editor:"select", editorParams:{values:["male", "female"]}},
        {title:"Rating", field:"rating", formatter:"star", hozAlign:"center", width:100, editor:true},
        {title:"Color", field:"col", width:130, editor:"input"},
        {title:"Date Of Birth", field:"dob", width:130, sorter:"date", hozAlign:"center"},
        {title:"Driver", field:"car", width:90,  hozAlign:"center", formatter:"tickCross", sorter:"boolean", editor:true},
   */
        {title:"TestIdent", field:"id", hozAlign:"center", visible:0,  resizable:false},
        {title:"Norm", field:"Norm", hozAlign:"center", visible:0},        
        {title:"ProtocolIdent", field:"ProtocolIdent", hozAlign:"center", visible:0,  resizable:false},
        {title:"TestIdent", field:"TestIdent", hozAlign:"center", visible:0, resizable:false},
        {title:"Prüfung_Voll", field:"TestNameFull", hozAlign:"center", visible:0},
        {title:"Abgerechnet", field:"Invoice", hozAlign:"center", formatter:"tickCross", visible:0},
        {title:"Prüfung", field:"TestName", hozAlign:"center", editor:"select", editorParams:{values:tests_tabledata}, resizable:false, width:90},
        {title:"Datum", field:"Date",  hozAlign:"center", resizable:false,  width:100, editor:"input", sorter:"date"},
        {title:"Start", field:"Start",  hozAlign:"center", resizable:false,  width:90, editor:"input", sorter:"time"},
        {title:"Stop", field:"Stop",  hozAlign:"center", resizable:false,  width:90, editor:"input"},
        {title:"Gesamtzeit", field:"TotalTime",  hozAlign:"center", resizable:false, width:110},
        {title:"Abrechnungsart", field:"InvoiceType",  hozAlign:"center", resizable:false,  width:150, editor:"select", editorParams:invoiceTypes},
        {title:"Beendet", field:"isTestFinished", hozAlign:"center", editor:true, formatter:"tickCross", resizable:false,  width:100},
        {title:"Prüfer", field:"Operator", hozAlign:"center", editor:"input", resizable:false,  width:80},
        {title:"Kommentar", field:"Comment",  hozAlign:"center", editor:"input", resizable:false}, 
    ],
    
});




var tableDataNested = [
    {id:1, name:"hödiofha dfha isodhf aosihf iaohe ioahe iofahse iofahse iofah oiefha ief", "_children":[
        {id:2, name:"Mary May", age:"1", driver:1}, //child rows nested under billy bob
        {id:3, name:"Christine Lobowski", age:"42", driver:1},
        {id:4, name:"Brendon Philips", age:"125", driver:1, "_children":[
            {id:5, name:"Margret Marmajuke", age:"16", driver:1}, //child rows nested under brendon philps
            {id:6, name:"Frank Peoney", age:"12", driver:1},
        ]},
    ]},
    {id:7, name:"Jenny Jane", age:"1", driver:0},
    {id:8, name:"Martha Tiddly", age:"42", driver:0, "_children":[
        {id:9, name:"Frasier Franks", age:"125", driver:0}, //child row nested under martha tiddly
    ]},
    {id:10, name:"Bobby Green", age:"11", driver:1},
]

// http://tabulator.info/docs/4.9/format#row
// http://tabulator.info/docs/4.9/tree

var table = new Tabulator("#example-nested-table", {
    dataTree:true,
    //dataTreeChildField:"childRows", //look for the child row data array in the childRows field -- only the top-tier rows
    minheight:"100px",
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
        if (cellValue == "hödiofha dfha isodhf aosihf iaohe ioahe iofahse iofahse iofah oiefha ief"){
            row.getElement().style.backgroundColor = "white";
            var cells = row.getCells()
            console.log(cells)
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
        }, 
        width:200, responsive:0, widthGrow:3 }, //never hide this column
    {title:"Location", field:"location", width:150},
    {title:"Gender", field:"gender", width:150, responsive:2}, //hide this column first
    {title:"Favourite Color", field:"col", width:150},
    {title:"Date Of Birth", field:"dob", hozAlign:"center", sorter:"date", width:150},
    {title:"Driver", field:"driver", width:150},
    ],
});