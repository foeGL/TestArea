
var dataPPB = JSON.parse(document.getElementById('tests').textContent);

const columns = [
    {title:"Name",              field:"name",           visible:1,  width:130,      textAlign:"left",       editor:false},
    {title:"ProtocolIdent",     field:"protocolIdent",  visible:0,  width:0,        textAlign:"center",     editor:false},
    {title:"TestIdent",         field:"testIdent",      visible:0,  width:0,        textAlign:"center",     editor:false},
    {title:"Prüfung_Voll",      field:"testNameFull",   visible:0,  width:0,        textAlign:"center",     editor:false},
    {title:"Abgerechnet",       field:"invoice",        visible:0,  width:0,        textAlign:"center",     editor:false},
    {title:"Datum",             field:"date",           visible:1,  width:110,       textAlign:"center",    editor:true},
    {title:"Start",             field:"start",          visible:1,  width:90,       textAlign:"center",     editor:false},
    {title:"Stop",              field:"stop",           visible:1,  width:90,       textAlign:"center",     editor:false},
    {title:"Gesamtzeit",        field:"totalTime",      visible:1,  width:84,       textAlign:"center",     editor:false},
    {title:"Abrechnungsart",    field:"invoiceType",    visible:1,  width:110,      textAlign:"center",     editor:false},
    {title:"Beendet",           field:"isTestFinished", visible:1,  width:56,       textAlign:"center",     editor:false},
    {title:"Prüfer",            field:"operator",       visible:1,  width:56,       textAlign:"center",     editor:false},
    {title:"Kommentar",         field:"comment",        visible:1,  width:'auto',   textAlign:"center",     editor:false},
    {title:"Element",           field:"element",        visible:0,  width:0,        textAlign:"center",     editor:false},
    {title:"TreeLevel",         field:"treeLevel",      visible:0,  width:0,        textAlign:"center",     editor:false},
];


const borderStyle = '1px solid #999';

const Invoice = {
    "-1": 'Nicht Abrechnen',
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

const headerRows = getHeaderRows()


$(window).on('load', function(){
    var body = document.getElementById("ppb-table"),
        tbl = document.createElement('table');
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
        var headlineID = headerRows['visibleTitle'][el]['title']
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
    var p = document.createElement("p")   
    switch(field){
        case 'name':
            cellValue = row[field]
            td.appendChild(document.createTextNode(cellValue));
            break;

        case 'invoiceType':
            if (row[field] < 1){
                cellValue = Invoice[row[field]]
            } else {
                cellValue = 'Pauschale #'+(row[field])
            }            
            td.appendChild(document.createTextNode(cellValue));
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
        case 'start':                    
            addEditForTime(td, field, row);
            break;            
        case 'stop':  
            addEditForTime(td, field, row);
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

function format_two_digits(n) {
    return n < 10 ? '0' + n : n;
}

function addEditForTime(td, field, row){
    var p = document.createElement("p")   
    var cellWidth = "";  
    for (let el in headerRows['visibleTitle']){
        if (headerRows['visibleTitle'][el]['field'] == field){
            cellWidth=headerRows['visibleTitle'][el]['width']
        }
    }
    cellValue = String(row[field]).substring(0,5)     
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

$("#pdfButton").click(function(){    
    var doc = new jspdf.jsPDF("p", "mm", "a4");
    //window.jsPDF = window.jspdf.jsPDF;
    html2canvas(document.getElementById('main-table')).then(function (canvas) {
        canvas.imageSmoothingEnabled = false;
        var imgdata = canvas.toDataURL("image/jpeg");
        doc.setFontSize(18);
        doc.text(15, 15, 'elektronische Prüfplatzbelegung -- 2021-10-27');
        doc.setFontSize(14);
        doc.text(15, 30, 'Projekt: 21-0305');
        doc.text(15, 45, 'Firma: HMS Technology Center Ravensburg GmbH');      
        doc.text(15, 60, 'Prüfauftrag: 21-0305OR42-001');      
        doc.text(15, 75, 'Prüfling: 21-0305PR41-001');
        const imgProps= doc.getImageProperties(imgdata);
        const pdfWidth = doc.internal.pageSize.getWidth()-40;
        const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
        const marginX = (doc.internal.pageSize.getWidth() - pdfWidth) / 2;
        const marginY = 100;   
        doc.addImage(imgdata, "JPEG", marginX, marginY, pdfWidth, pdfHeight);
        doc.save("sample.pdf");
    });
});
    


function pdf_formatTableDate(){
    var pdfTable = [];
    for (let key in dataPPB){
        var row = dataPPB[key];
        pdfTable.push(pdf_formatRow(row))
        pdfTable = pdf_addChildren(pdfTable, row)
    }    
    return pdfTable
}

function pdf_addChildren(pdfTable, row){
    var tmpPDFTable = pdfTable;
    if ('_children' in row){
        console.log("ist drin!")
        for (child in row['_children']){
            console.log(row['_children'])
            var rowChild = row['_children'][child];
            console.log(rowChild)
            tmpPDFTable.push(pdf_formatRow(rowChild))
            tmpPDFTable = pdf_addChildren(tmpPDFTable, rowChild)
        }
    } else {
        console.log("hat keine kinder!")
    }
    return tmpPDFTable
}

function pdf_formatRow(row){
    var formattedRow = {}
    for (let cell in headerRows['visible']){
        var field = headerRows['visible'][cell]
        if (field in row){
            console.log("schreibt in feld "+field)
            formattedRow[field] = formatCell(row, field);
        }
    }
    return formattedRow
}

function demoFromHTML(){
    window.jsPDF = window.jspdf.jsPDF;
    var doc = new jsPDF('p', 'pt', 'letter');  
    var pdfTable = pdf_formatTableDate();

    console.log(pdfTable)




    var test = 1;
    if (test == 1){
        doc.autoTable({
            styles: { fillColor: [255, 0, 0] },
            columnStyles: { 0: { halign: 'center', fillColor: [0, 255, 0] } }, // Cells in first column centered and green
            margin: { top: 10 },
            body: pdfTable, /*[
                
            ['Sweden', 'Japan', 'Canada'],
            ['Norway', 'China', 'USA'],
            ['Denmark', 'China', 'Mexico'],
            
            ],*/
        })
    } else {      
      // Example usage of columns property. Note that America will not be included even though it exist in the body since there is no column specified for it.
      doc.autoTable({
        columnStyles: { europe: { halign: 'center' } }, // European countries centered
        body: [
          { europe: 'Sweden', america: 'Canada', asia: 'China' },
          { europe: 'Norway', america: 'Mexico', asia: 'Japan' },
        ],
        columns: [
          { header: 'Europe', dataKey: 'europe' },
          { header: 'Asia', dataKey: 'asia' },
        ],
      })
    }
    
    doc.save('ePPB.pdf');  
}

function demoFromHTML1() {
    window.jsPDF = window.jspdf.jsPDF;
    var doc = new jsPDF('p', 'pt', 'letter');  
    var htmlstring = '';  
    var tempVarToCheckPageHeight = 0;  
    var pageHeight = 0;  
    pageHeight = doc.internal.pageSize.height;  
    specialElementHandlers = {  
        // element with id of "bypass" - jQuery style selector  
        '#bypassme': function(element, renderer) {  
            // true = "handled elsewhere, bypass text extraction"  
            return true  
        }  
    };  
    margins = {  
        top: 150,  
        bottom: 60,  
        left: 40,  
        right: 40,  
        width: 600  
    };  
    var y = 20;  
    doc.setLineWidth(2);  
    doc.text(200, y = y + 30, "elektronische Prüfplatzbelegung");  
    mywidth=60;
    doc.autoTable({  
        html: '#main-table',  
        startY: 70,  
        theme: 'grid',  
        columnStyles: {  
            0: {  
                cellWidth: 40,  
            },  
            1: {  
                cellWidth: mywidth,  
            },  
            2: {  
                cellWidth: mywidth,  
            },    
            3: {  
                cellWidth: mywidth,  
            } ,    
            4: {  
                cellWidth: mywidth,  
            } ,    
            5: {  
                cellWidth: mywidth,  
            } ,    
            6: {  
                cellWidth: mywidth,  
            } ,    
            7: {  
                cellWidth: mywidth,  
            } ,    
            8: {  
                cellWidth: mywidth,  
            } 
        },  
        styles: {  
            minCellHeight: 40  
        }  
    })  
    doc.save('ePPB.pdf');  
}



$(document).on('click', '.ppb-start', function() {   // <--------------------------------------------------------------- Hier!
    onClickForEdit(this);
});

$(document).on('click', '.ppb-stop', function() {   // <--------------------------------------------------------------- Hier!
    onClickForEdit(this);
});

function onClickForEdit(el){
    el.classList.add("ppb-edit") 
    var childInput = $(el).children('input');
    var childP = $(el).children('p');
    $(childP).css('display','none')
    $(childInput).css('display','inline')
    $(childInput).val($(childP).text());
}


$('body').on('click', '.svgCheck', function(){
    this.classList.add("ppb-edit")
    var e = $(this).attr('ischecked');

    var childSVG = $(this).children('svg');
    var childBox = $(this).children('input');
    $(childSVG).css('display','none')
    $(childBox).css('display','inline')
});

$('body').on('click', '.finishedCheckBox', function(){
    var checked = this.checked;
    $(this).attr('value', checked);
});


document.addEventListener('mouseup', function(e) {
    var box = document.getElementsByClassName('ppb-edit')[0];
    if (box != null){
        var initialClass = box.classList[0];
        //var classCat = String(initialClass).substring(4);
        switch (initialClass){
            case "svgCheck":
                var childSVG = $(box).children('svg');
                var childBox = $(box).children('input');
                $(childSVG).css('display','inline')
                $(childBox).css('display','none')   

                var appearance = $(childSVG).attr('appearance')
                var childBoxValue = $(childBox).attr('value');
                if (appearance != childBoxValue){   
                    
                    var childPath = $(childSVG).children('path');   
                    console.log(childPath, $(childPath).attr('fill'))  
                    if (childBoxValue == 'true'){         
                        var [color, figure] = setCheckboxTrue();
                    } else {      
                        var [color, figure] = getCheckboxFalse();  
                    }        
                    console.log("set to :"+color+" and "+figure)
                    $(childPath).attr('fill', color);
                    $(childPath).attr('d', figure);
                    $(childSVG).attr('appearance',childBoxValue);
                }
                break;
            default:
                var childView = $(box).children('p');
                var childEdit = $(box).children('input');
                var newValue = $(childEdit).val();
                if (isTime(newValue) == true){
                    $(childView).text(newValue);
                }
                $(childEdit).css('display','none');
                $(childView).css('display','inline');
                break;                    
        }
        $(box).removeClass('ppb-edit');        
    }
});

function isTime(time){
    var isTime = true
    if (String(time).substring(2,3)!=':'){ 
        isTime = false; 
    } else {
        var hours = parseInt(String(time).substring(0,2));
        var minutes = parseInt(String(time).substring(3,5));
        if (hours<0 | hours>24){isTime = false;}
        if (minutes<0 | minutes>60){isTime = false;}
    }
    return isTime
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