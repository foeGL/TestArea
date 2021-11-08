
const dataPPB = JSON.parse(document.getElementById('ppb').textContent);
const testCases = JSON.parse(document.getElementById('tests').textContent);
const operator = JSON.parse(document.getElementById('operator').textContent);

const columns = [
    {title:"Name",              field:"name",           visible:1,  width:130,      textAlign:"left"},
    {title:"Datum",             field:"date",           visible:1,  width:110,      textAlign:"center"},
    {title:"Start",             field:"start",          visible:1,  width:90,       textAlign:"center"},
    {title:"Stop",              field:"stop",           visible:1,  width:90,       textAlign:"center"},
    {title:"Gesamtzeit",        field:"totalTime",      visible:1,  width:84,       textAlign:"center"},
    {title:"Abrechnungsart",    field:"invoiceType",    visible:1,  width:110,      textAlign:"center"},
    {title:"Beendet",           field:"isTestFinished", visible:1,  width:56,       textAlign:"center"},
    {title:"Prüfer",            field:"operator",       visible:1,  width:56,       textAlign:"center"},
    {title:"Kommentar",         field:"comment",        visible:1,  width:474,      textAlign:"center"},
];


const borderStyle = '1px solid #999';

const Invoice = {
    "-1": 'Nicht abrechnen',
    "0": 'Aufwand',
    "1": 'Pauschal'
};

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
};

const headerRows = getHeaderRows();
const body = document.getElementById("ppb-table"),
    tbl = document.createElement('table');

$(window).on('load', function(){
    tbl.setAttribute("id", "main-table");   
    var tableWidth = $("#ppb-table").width();
    tbl.setAttribute("width", tableWidth);     
    var tr = tbl.insertRow();
    tr.setAttribute("id", "headline");
    createHeadline(tr, headerRows)

    for (let key in dataPPB){
        var row = dataPPB[key];
        insertRow(tbl, row)
        checkForChildren(tbl, row)
    }    
    body.appendChild(tbl);
});
  
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
        var headlineID = headerRows['visibleTitle'][el]['field']
        th.setAttribute('id', 'headline-'+headlineID);
        if (headerRows['visibleTitle'][el]['width'] != 'auto'){
            currentCellWidth = headerRows['visibleTitle'][el]['width'];
            summedWidth += currentCellWidth;
            th.style.width = currentCellWidth+"px";
        } else {
            var test = tableWidth-summedWidth+"px";
            th.style.width = test;
        }
        
    }
}

function insertRow(tbl, row){
    var tr = tbl.insertRow();
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
    tr.classList.add(row['element'], 'level'+row['treeLevel']);
    //$(tr).attr("treeElement", row['treeElement']);
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
    tr.classList.add(row['element'], 'level'+row['treeLevel']);
    $(tr).attr("treeElement", row['treeElement']);
    addSubClass(tr, row);
    $(tr).attr('id', row['testIdent']);
    var td = tr.insertCell();           
    var field = 'name';
    td.classList.add(row['element']+"-name");
    addTreeBranch(row, td, field);
    addTreeContorl(row, td, field);
    td.appendChild(document.createTextNode(row['name']));
    td.setAttribute('colSpan', headerRows['visible'].length);      
}

function handlePPB(tr, row){
    tr.classList.add(row['element'], 'level'+row['treeLevel']);
    addSubClass(tr, row)
    tr.setAttribute("testident",row["testIdent"])
    tr.setAttribute("protocolident",row["protocolIdent"])
    for (let visibleRow in headerRows['visibleTitle']){
        var field = headerRows['visibleTitle'][visibleRow]['field']
        var td = tr.insertCell();
        td.classList.add('ppb-'+field)
        addTreeBranch(row, td, field)
        formatCell(row, td, field);
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

function formatCell(row, td, field){
    var cellValue="";
    var p = document.createElement("p");   
    switch(field){
        case 'name':
            cellValue = row[field];            
            p.appendChild(document.createTextNode(cellValue));  
            p.classList.add("ppb-p");
            td.appendChild(p);            
            var ul = document.createElement("ul")    
            ul.classList.add("ppb-name-dd");
            td.setAttribute("expanded",false)
            var li = document.createElement("li");
            li.classList.add("ppb-name-dd-item");
            var node = '-- Eintrag löschen --';
            li.appendChild(document.createTextNode(node))
            li.setAttribute("testIdent", -1);
            ul.appendChild(li);
            for (var el in testCases){       
                var li = document.createElement("li");
                li.classList.add("ppb-name-dd-item");
                var node = 'TE'+ testCases[el]['TestNumber'].toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false}) + ' - ' + testCases[el]['Description'];
                li.appendChild(document.createTextNode(node))
                li.setAttribute("testIdent", testCases[el]['TestIdent']);
                li.setAttribute("testNumber", testCases[el]['TestNumber']);
                ul.appendChild(li);
            }
            td.appendChild(ul);
            break;
        case 'invoiceType':
            cellValue = getInvoiceType(row[field]);
            p.appendChild(document.createTextNode(cellValue));  
            p.classList.add("ppb-p"); 
            td.appendChild(p);   
            var ul = document.createElement("ul")    
            ul.classList.add("ppb-invoice-dd");    
            td.setAttribute("expanded",false)
            for (let i=0; i<Object.keys(Invoice).length; i++){ 
                var li = document.createElement("li");
                li.classList.add("ppb-invoice-dd-item");
                li.setAttribute("invoicetype", i-1)
                li.appendChild(document.createTextNode(Invoice[i-1]));
                ul.appendChild(li);
            }
            td.appendChild(ul);
            break;
        case 'isTestFinished':              
            var div = document.createElement("div")    
            var checkbox = document.createElement("input")
            checkbox.type = 'checkbox';
            checkbox.value  = row[field];
            checkbox.checked = row[field];
            $(checkbox).css('display',"none");
            $(checkbox).css('margin-top', '7px');
            checkbox.classList.add("finishedCheckBox");
            var svg = document.createElementNS("http://www.w3.org/2000/svg","svg");     
            var newPath = document.createElementNS("http://www.w3.org/2000/svg","path");   
            td.appendChild(div);
            div.classList.add('svgCheck');     
            div.setAttribute('isChecked', row[field]) 
            div.appendChild(svg);
            svg.setAttributeNS(null, 'height', "14"); 
            svg.setAttributeNS(null, 'width', "14");
            svg.setAttributeNS(null, 'viewBox', '0 0 24 24');
            svg.setAttributeNS(null, 'appearance', row[field]); 
            $(svg).css('margin-top', "6px");
  
            if (row[field] == true){         
                var [fill, d] = setCheckboxTrue();
            } else {      
                var [fill, d] = getCheckboxFalse();  
            }        
            newPath.setAttributeNS(null, 'fill', fill)   
            newPath.setAttributeNS(null, "d", d)
                
            svg.appendChild(newPath);            
            div.appendChild(checkbox);
            td.appendChild(document.createTextNode(cellValue));
            //console.log("isTestFinished: " +row[field])
            //cellValue = row[field];
            break;
        case 'date':          
            cellValue = String(row[field]);          
            addEditForCell(td, field, row, cellValue);
            break;
        case 'start':  
            cellValue = String(row[field]).substring(0,5);                     
            addEditForCell(td, field, row, cellValue);
            break;            
        case 'stop':  
            cellValue = String(row[field]).substring(0,5);    
            addEditForCell(td, field, row, cellValue);
            break;               
        case 'comment':  
            cellValue = String(row[field]);    
            addEditForCell(td, field, row, cellValue);
            break;                 
        case 'operator':  
            cellValue = String(row[field]);    
            addEditForCell(td, field, row, cellValue);
            break;
        default:
            cellValue = row[field]
            td.appendChild(p);
            p.classList.add("ppb-cellValue");
            p.appendChild(document.createTextNode(cellValue));
            break;
    }
    return cellValue
}

function getInvoiceType(value){    
    if (value < 1){
        cellValue = Invoice[value]
    } else {
        cellValue = Invoice[1] + 'e #'+(value)
    } 
    return cellValue
}

function format_two_digits(n) {
    return n < 10 ? '0' + n : n;
}

function addEditForCell(td, field, row, cellValue){
    var p = document.createElement("p")   
    var cellWidth = "";  
    for (let el in headerRows['visibleTitle']){
        if (headerRows['visibleTitle'][el]['field'] == field){
            cellWidth=headerRows['visibleTitle'][el]['width']
        }
    } 
    var textInput = document.createElement("input");
    textInput.type = 'text';
    textInput.value  = cellValue;
    textInput.classList.add(field+"-edit")
    td.appendChild(textInput);
    $(textInput).width((cellWidth-20)+"px");
    $(textInput).css("display", "none");            
    td.appendChild(p);
    p.classList.add("ppb-cellValue");
    p.appendChild(document.createTextNode(cellValue));
}

function addTreeBranch(row, td, field){
    var treeLevel = row['treeLevel'];
    //if (treeLevel>0){
    if (field == 'name'){ 
        var div=document.createElement("div")             
        td.appendChild(div);
        div.classList.add('table-tree-branch');
        /*äää
        for (let e in settingsDIV[treeLevel]){
            $(div).css(e, settingsDIV[treeLevel][e])
        }
        */
    }
    //}
}

function addTreeContorl(row, td, field){
    if (field == 'name'){ 
        var div=document.createElement("div")  ;
        var subdiv=document.createElement("div");
        div.classList.add("table-tree-control");
        div.setAttribute("element", row['element']);    
        div.setAttribute("controlelements", "sub-"+row['treeElement']);    
        div.setAttribute("status", "show");
        td.appendChild(div);
        //div.innerHTML = "-";
        subdiv.classList.add("table-tree-control-expand");
        div.appendChild(subdiv);
        if (!row.hasOwnProperty("_children")){            
            div.classList.add("table-tree-control-invisible");
        }
    }
}

function setCheckboxTrue(){
    var fill = "#2DC214";
    var d = "M21.652,3.211c-0.293-0.295-0.77-0.295-1.061,0L9.41,14.34 c-0.293,0.297-0.771,0.297-1.062,0L3.449,9.351C3.304,9.203,3.114,9.13,2.923,9.129C2.73,9.128,2.534,9.201,2.387,9.351  l-2.165,1.946C0.078,11.445,0,11.63,0,11.823c0,0.194,0.078,0.397,0.223,0.544l4.94,5.184c0.292,0.296,0.771,0.776,1.062,1.07  l2.124,2.141c0.292,0.293,0.769,0.293,1.062,0l14.366-14.34c0.293-0.294,0.293-0.777,0-1.071L21.652,3.211z";
    return [fill, d]
}


function getCheckboxFalse(){
    var fill = "#CE1515";
    var d = "M22.245,4.015c0.313,0.313,0.313,0.826,0,1.139l-6.276,6.27c-0.313,0.312-0.313,0.826,0,1.14l6.273,6.272 c0.313,0.313,0.313,0.826,0,1.14l-2.285,2.277c-0.314,0.312-0.828,0.312-1.142,0l-6.271-6.271c-0.313-0.313-0.828-0.313-1.141,0  l-6.276,6.267c-0.313,0.313-0.828,0.313-1.141,0l-2.282-2.28c-0.313-0.313-0.313-0.826,0-1.14l6.278-6.269  c0.313-0.312,0.313-0.826,0-1.14L1.709,5.147c-0.314-0.313-0.314-0.827,0-1.14l2.284-2.278C4.308,1.417,4.821,1.417,5.135,1.73  L11.405,8c0.314,0.314,0.828,0.314,1.141,0.001l6.276-6.267c0.312-0.312,0.826-0.312,1.141,0L22.245,4.015z";
    return [fill, d]
}

function getTodaysDate(){
    var today = new Date();
    var day = String(today.getDate()).padStart(2, '0');
    var month = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var year = today.getFullYear();

    today = year + '-' + month + '-' + day;
    return today;
}