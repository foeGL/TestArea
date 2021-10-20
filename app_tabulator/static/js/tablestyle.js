const array_tests = JSON.parse(document.getElementById('tests').textContent);
const borderStyle = '1px solid #999'

var tableDataNested = []        
for (const [key1, arr] of Object.entries(array_tests)){
    tableDataNested.push(arr)
}

var columns = [
    {title:"Name",              field:"name",           visible:1,  width:100}, //never hide this column
    {title:"ProtocolIdent",     field:"ProtocolIdent",  visible:0,  width:100},
    {title:"TestIdent",         field:"TestIdent",      visible:0,  width:100},
    {title:"Prüfung_Voll",      field:"TestNameFull",   visible:0,  width:100},
    {title:"Abgerechnet",       field:"Invoice",        visible:0,  width:100},
    {title:"Datum",             field:"Date",           visible:1,  width:100},
    {title:"Start",             field:"Start",          visible:1,  width:100},
    {title:"Stop",              field:"Stop",           visible:1,  width:100},
    {title:"Gesamtzeit",        field:"TotalTime",      visible:1,  width:100},
    {title:"Abrechnungsart",    field:"InvoiceType",    visible:1,  width:100},
    {title:"Beendet",           field:"isTestFinished", visible:1,  width:100},
    {title:"Prüfer",            field:"Operator",       visible:1,  width:100},
    {title:"Kommentar",         field:"Comment",        visible:1,  width:100},
    {title:"Element",           field:"element",        visible:0,  width:100},
    {title:"TreeLevel",         field:"treeLevel",      visible:0,  width:100},
]

function tableCreate() {
    const   body = document.body,
            tbl = document.createElement('table');
    tbl.style.width = '100px';
    //tbl.style.border = '1px solid #999';
    tbl.style.backgroundColor = '#efefef';
    

    var headerRows = getHeaderRows(columns)
    const tr = tbl.insertRow();
    createHeadline(tr, headerRows)

    for (let key in tableDataNested){
        var row = tableDataNested[key];
        insertRow(tbl, row, headerRows)
        checkForChildren(tbl, row, headerRows)
    }
    
    body.appendChild(tbl);
}
  
function getHeaderRows(e){
    var visibleRows = [];    
    var visibleRowsTitle = [];    
    var invisibleRows = [];
    for (let el in e){
        if (e[el]['visible'] == 1){
            visibleRowsTitle.push(e[el]['title']);
            visibleRows.push(e[el]['field']);
        } else {            
            invisibleRows.push(e[el]['field']);
        }
    }
    return {'visible': visibleRows, 'invisible': invisibleRows, 'visibleTitle': visibleRowsTitle}
}

function createHeadline(e, headerRows){
    for (let el in headerRows['visibleTitle']){
        const td = e.insertCell();
        td.appendChild(document.createTextNode(headerRows['visibleTitle'][el]));
        td.style.border = borderStyle;
        td.style.fontSize = "14px";    
        td.style.fontWeight = "700";    
        td.style.color = "white";    
        td.style.backgroundColor = "#005797";    
        
    }
}

function insertRow(tbl, row, headerRows){
    const tr = tbl.insertRow();
    tr.classList.add(row['element'] +'-level'+row['treeLevel']);
    switch(row['element']){
        case 'header':
            var td = tr.insertCell();
            td.appendChild(document.createTextNode(row['name']));
            //td.style.border = borderStyle;
            td.setAttribute('colSpan', headerRows['visible'].length);
            switch(row['treeLevel']){
                case 0:
                    td.style.fontSize = "20px";
                    td.style.fontWeight = "bold";
                    break;
                default:
                    break;
            }
            break;
        case 'test':
            var td = tr.insertCell();
            td.appendChild(document.createTextNode(row['name']));
            //td.style.border = borderStyle;
            td.setAttribute('colSpan', headerRows['visible'].length);
            td.style.fontSize = "14px";
            td.style.fontWeight = "bold";
            break;
        case 'ppb':
            for (let visibleRow in headerRows['visible']){
                var td = tr.insertCell();
                td.appendChild(document.createTextNode(row[headerRows['visible'][visibleRow]]));
                td.setAttribute('field', headerRows['visible'][visibleRow]);
                td.style.borderRight = borderStyle;
                td.style.fontSize = "14px";     
                td.style.backgroundColor = "white";     
            }
            for (let invisibleRow in headerRows['invisible']){
                var td = tr.insertCell();
                td.appendChild(document.createTextNode(row[headerRows['invisible'][invisibleRow]]));
                td.style.display = 'none';
                td.setAttribute('field', headerRows['invisible'][invisibleRow]);
            }       
            break;
        default:
            break;
    }
}

function checkForChildren(tbl, row, headerRows){    
    if ('_children' in row){
        var row0 = row['_children']
        for (let subkey in row['_children']){
            var row0 = row['_children'][subkey]
            insertRow(tbl, row0, headerRows)
            checkForChildren(tbl, row0, headerRows)
        }
    }
}

tableCreate();