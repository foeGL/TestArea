const array_tests = JSON.parse(document.getElementById('tests').textContent);
console.log(array_tests)

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

console.log("tableDataNested", tableDataNested)


var tableDataNested = []        
for (const [key1, arr] of Object.entries(array_tests)){
    tableDataNested.push(arr)
}

console.log("tableDataNested", tableDataNested)


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
        width:200, responsive:0, widthGrow:3 
    }, //never hide this column
    {title:"Location", field:"location", width:150},
    {title:"Gender", field:"gender", width:150, responsive:2}, //hide this column first
    {title:"Favourite Color", field:"col", width:150},
    {title:"Date Of Birth", field:"dob", hozAlign:"center", sorter:"date", width:150},
    {title:"Driver", field:"driver", width:150},
    ],
});