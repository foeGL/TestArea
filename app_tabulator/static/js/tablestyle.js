const array_tests = JSON.parse(document.getElementById('tests').textContent);

const columns = [
    {title:"Name",              field:"name",           visible:1,  width:130,      textAlign:"left"},
    {title:"ProtocolIdent",     field:"ProtocolIdent",  visible:0,  width:0,        textAlign:"center"},
    {title:"TestIdent",         field:"TestIdent",      visible:0,  width:0,        textAlign:"center"},
    {title:"Prüfung_Voll",      field:"TestNameFull",   visible:0,  width:0,        textAlign:"center"},
    {title:"Abgerechnet",       field:"Invoice",        visible:0,  width:0,        textAlign:"center"},
    {title:"Datum",             field:"Date",           visible:1,  width:94,       textAlign:"center"},
    {title:"Start",             field:"Start",          visible:1,  width:94,       textAlign:"center"},
    {title:"Stop",              field:"Stop",           visible:1,  width:94,       textAlign:"center"},
    {title:"Gesamtzeit",        field:"TotalTime",      visible:1,  width:84,       textAlign:"center"},
    {title:"Abrechnungsart",    field:"InvoiceType",    visible:1,  width:110,      textAlign:"center"},
    {title:"Beendet",           field:"isTestFinished", visible:1,  width:56,       textAlign:"center"},
    {title:"Prüfer",            field:"Operator",       visible:1,  width:56,       textAlign:"center"},
    {title:"Kommentar",         field:"Comment",        visible:1,  width:'auto',   textAlign:"center"},
    {title:"Element",           field:"element",        visible:0,  width:0,        textAlign:"center"},
    {title:"TreeLevel",         field:"treeLevel",      visible:0,  width:0,        textAlign:"center"},
]

const headerRows = getHeaderRows()
const borderStyle = '1px solid #999'

const Invoice = {
    0: 'Nicht Abrechnen',
    1: 'Aufwand',
    2: 'Pauschal'
}

const settingsDIV = {
    1: {
        marginLeft: "9px",
    },
    2: {
        marginLeft: "30px",
    },
    3: {
        marginLeft: "49px",
    }
}

var tableDataNested = []        
for (const [key1, arr] of Object.entries(array_tests)){
    tableDataNested.push(arr)
}

function tableCreate() {
    var body = document.getElementById("ppb-table"),
        tbl = document.createElement('table');
    tbl.setAttribute("id", "main-table");    
    var tr = tbl.insertRow();
    tr.setAttribute("id", "headline");    
    createHeadline(tr, headerRows)

    for (let key in tableDataNested){
        var row = tableDataNested[key];
        insertRow(tbl, row)
        checkForChildren(tbl, row)
    }
    
    body.appendChild(tbl);
}
  
function getHeaderRows(){
    var visibleRows = [];    
    var visibleRowsTitle = [];    
    var invisibleRows = [];
    for (let el in columns){
        if (columns[el]['visible'] == 1){
            visibleRowsTitle.push(columns[el]);
            visibleRows.push(columns[el]['field']);
        } else {            
            invisibleRows.push(columns[el]['field']);
        }
    }
    return {'visible': visibleRows, 'invisible': invisibleRows, 'visibleTitle': visibleRowsTitle}
}

function createHeadline(e, headerRows){
    var tableWidth = $("#ppb-table").width();
    summedWidth = 0
    for (let el in headerRows['visibleTitle']){
        const th = e.insertCell()
        th.appendChild(document.createTextNode(headerRows['visibleTitle'][el]['title']));
        th.setAttribute('id', 'headline-'+headerRows['visibleTitle'][el]['title']);
        if (headerRows['visibleTitle'][el]['width'] != 'auto'){
            currentCellWidth = headerRows['visibleTitle'][el]['width'];
            summedWidth += currentCellWidth;
            th.style.width = currentCellWidth;
        } else {
            var test = tableWidth-summedWidth+"px";
            th.style.width = test;
        }
        
    }
}

function insertRow(tbl, row){
    var tr = tbl.insertRow();
    tr.classList.add(row['element'], 'level'+row['treeLevel']);
    switch(row['element']){
        case 'header':
            handleHeader(tr, row)
            break;
        case 'test':
            handleTest(tr, row)
            break;
        case 'ppb':
            handlePPB(tr, row)
            break;
        default:
            break;
    }
}

function checkForChildren(tbl, row){    
    if ('_children' in row){
        var row0 = row['_children']
        for (let subkey in row['_children']){
            var row0 = row['_children'][subkey]
            insertRow(tbl, row0)
            checkForChildren(tbl, row0)
        }
    }
}

function handleHeader(tr, row){
    addSubClass(tr, row)
    var td = tr.insertCell();
    var field = 'name'
    td.classList.add(row['element']+"-name")
    addTreeBranch(row, td, field)
    addTreeContorl(row, td, field)
    td.appendChild(document.createTextNode(row['name']));
    td.setAttribute('colSpan', headerRows['visible'].length);
    switch(row['treeLevel']){
        case 0:     
            break;
        default:
            break;
    }
}

function addSubClass(tr, row){
    var elem = row['treeElement'];
    if (elem != ""){
        if(elem.search('-') > -1){
            var e = elem.split('-');
            e.pop();
            if (e.length > 1){
                for (let index in e){
                    var tmpsub = "sub";
                    for (let i=0; i<parseInt(index)+1; i++){
                        tmpsub = tmpsub +"-"+e[i];
                    }
                    tr.classList.add(tmpsub);
                }
            } else {
                tr.classList.add("sub-"+e)
            }
        }
    }
}


function handleTest(tr, row){
    addSubClass(tr, row)
    var td = tr.insertCell();           
    var field = 'name'
    td.classList.add(row['element']+"-name")
    addTreeBranch(row, td, field)     
    addTreeContorl(row, td, field)  
    td.appendChild(document.createTextNode(row['name']));
    td.setAttribute('colSpan', headerRows['visible'].length);      
}

function handlePPB(tr, row){
    addSubClass(tr, row)
    for (let visibleRow in headerRows['visibleTitle']){
        var field = headerRows['visibleTitle'][visibleRow]['field']
        var td = tr.insertCell();
        td.classList.add('ppb-'+field)
        addTreeBranch(row, td, field)
        var cellValue="";
        switch(field){
            case 'InvoiceType':
                if (row[field] < 2){
                    cellValue = Invoice[row[field]]
                } else {
                    cellValue = 'Pauschale #'+(row[field]-1)
                }
                break;
            default:
                cellValue = row[field]
                break;
        }
        td.appendChild(document.createTextNode(cellValue));
        td.setAttribute('field', field);
        td.style.textAlign = headerRows['visibleTitle'][visibleRow]['textAlign'];
    }
    for (let invisibleRow in headerRows['invisible']){
        var td = tr.insertCell();
        td.appendChild(document.createTextNode(row[headerRows['invisible'][invisibleRow]]));
        td.style.display = 'none';       
        td.setAttribute('field', headerRows['invisible'][invisibleRow]);
    }       
}

function addTreeBranch(row, td, field){
    var treeLevel = row['treeLevel'];
    if (treeLevel>0){
        if (field == 'name'){ 
            var div=document.createElement("div")             
            td.appendChild(div);
            div.classList.add('table-tree-branch');
            for (let e in settingsDIV[treeLevel]){
                $(div).css(e, settingsDIV[treeLevel][e])
            }
        }
    }
}

function addTreeContorl(row, td, field){
    if (field == 'name'){ 
        if ("_children" in row){
            var div=document.createElement("div")  ;
            var subdiv=document.createElement("div");
            td.appendChild(div);
            div.classList.add("table-tree-control");
            div.setAttribute("controlelements", "sub-"+row['treeElement']);    
            div.setAttribute("status", "show");
            //div.innerHTML = "-";
            div.appendChild(subdiv);
            subdiv.classList.add("table-tree-control-expand");
        }
    }
}

$(document).on('click', '.table-tree-control', function() {   
    console.log("wurde getriggert")  
    var status = $(this).attr("status");
    var contolElements = $(this).attr("controlelements");
    var child = $(this).children('div')
    if (status == "show"){
        $(child).addClass('table-tree-control-collapse')
        $(child).removeClass('table-tree-control-expand')
        $(this).attr("status","hide");
        $("."+contolElements).hide()
    } else {        
        $(child).addClass('table-tree-control-expand')
        $(child).removeClass('table-tree-control-collapse')
        $(this).attr("status","show");
        $("."+contolElements).show()
        $("."+contolElements).each(function(index, item){
            var subChild_td = $(item).children('td')[0];
            var subChilds_div = $(subChild_td).children('div');
            if (subChilds_div.length==2){
                var controlElement = subChilds_div[1];
                var subStatus = $(controlElement).attr("status")                
                var subContolElements = $(controlElement).attr("controlelements")
                if (subStatus == 'show'){
                    $("."+subContolElements).show();
                } else {
                    $("."+subContolElements).hide();
                }
            }
        });
    }
});
