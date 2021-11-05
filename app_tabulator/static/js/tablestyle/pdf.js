
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

