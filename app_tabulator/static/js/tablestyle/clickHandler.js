$(document).on('click', '.ppb-name', function() {
    onClickDDForEdit(this);
});

$(document).on('click', '.ppb-invoiceType', function() {
    onClickDDForEdit(this);
});

$(document).on('click', '.ppb-start', function() {
    onClickForEdit(this);
});

$(document).on('click', '.ppb-stop', function() {
    onClickForEdit(this);
});

$(document).on('click', '.ppb-comment', function() {
    onClickForEdit(this);
});


$(document).on('click', '.ppb-date', function() {
    onClickForEdit(this);
});


$(document).on('click', '.ppb-operator', function() {
    onClickForEdit(this);
});

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

$(document).on('click', '.ppb-name-dd-item', function() {    
    //-----------------------------------------------------
    // Move PPB-TR beneath Test-TR
    //-----------------------------------------------------
    var newTestIdent = $(this).attr("testident");
    var row=$(this).parents('tr');
    var oldTestIdent = $(row).attr("testident");
    if (newTestIdent == '-1'){        
        $(row).remove();
    } else {
        // Bevor verschoben wurde
        var newParent = document.getElementById(newTestIdent);
        $(row).attr("testident",newTestIdent);
        row.insertAfter(newParent);
        
        // Nachdem verschoben wurde
        setNewTreeLevel(row, newParent);
        addSubsToClass(row, newParent);
        checkTreeControlForParentsAfterMove(oldTestIdent, newTestIdent);

        //-----------------------------------------------------
        // Set Values and switch visibility of DropDown
        //-----------------------------------------------------
        var parentTD=$(this).parents('td');
        var childP = $(parentTD).children('p');  
        var childList = $(parentTD).children('ul');  
        var value = 'TE'+ parseInt($(this).attr("testnumber")).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false});
        $(childP).text(value);     
        $(childList).css('display','none');
        applyVisibilityOfParent(newParent);
    }
});

$(document).on('click', '.ppb-invoice-dd-item', function() {
    var parent=$(this).parents('td');
    var childP = $(parent).children('p');
    var value = $(this).attr("invoicetype"); 
    
    $(childP).text(getInvoiceType(value)); 
    var childList = $(parent).children('ul');
    $(childList).css('display','none');    
    $(this).removeClass('ppb-edit');     
});

document.addEventListener('mouseup', function(e) {
    var box = document.getElementsByClassName('ppb-edit')[0];
    if (box != null){
        var initialClass = box.classList[0];
        //var classCat = String(initialClass).substring(4);
        switch (initialClass){
            case "ppb-name":      
                hideDD(box);  
                break;
            case "ppb-invoiceType":  
                hideDD(box);  
                break;
            case "svgCheck":
                var childSVG = $(box).children('svg');
                var childBox = $(box).children('input');
                $(childSVG).css('display','inline')
                $(childBox).css('display','none')   

                var appearance = $(childSVG).attr('appearance')
                var childBoxValue = $(childBox).attr('value');
                if (appearance != childBoxValue){   
                    
                    var childPath = $(childSVG).children('path');   
                    if (childBoxValue == 'true'){         
                        var [color, figure] = setCheckboxTrue();
                    } else {      
                        var [color, figure] = getCheckboxFalse();  
                    }        
                    $(childPath).attr('fill', color);
                    $(childPath).attr('d', figure);
                    $(childSVG).attr('appearance',childBoxValue);
                }
                break;
            case "ppb-start":
                switchViewAndEditTime(box);
                break;
            case "ppb-stop":
                switchViewAndEditTime(box);
                break;
            default:
                var childView = $(box).children('p');
                var childEdit = $(box).children('input');
                var newValue = $(childEdit).val();
                $(childView).text(newValue);
                $(childEdit).css('display','none');
                $(childView).css('display','inline');
                break;                    
        }
        //$(box).children('ul').attr("expanded", 'false') 
        $(box).removeClass('ppb-edit');     
    }
});

$(document).on('click', '.table-tree-control', function() {   
    var status = $(this).attr("status");
    if (status == "show"){
        collapseTreeControl(this);
    } else {        
        expandTreeControl(this);
    }
});

$(document).on('click', '#collapse-list', function() {
    var el = document.getElementsByClassName("table-tree-control");
    for (var e in Object.keys(el)){
        collapseTreeControl(el[e]);
    }
});

$(document).on('click', '#expand-list', function() {
    var el = document.getElementsByClassName("table-tree-control");
    for (var e in Object.keys(el)){
        expandTreeControl(el[e]);
    }
});

$(document).on('click', '#add-row', function() {
    var tr = tbl.insertRow(1);
    row = {
        comment: "",
        date: getTodaysDate(),
        element: "ppb",
        id: 0,
        invoiceType: -1,
        isTestFinished: false,
        name: "",
        operator: operator,
        protocolIdent: "",
        start: "",
        stop: "",
        testIdent: "",
        totalTime: "",
        treeElement: "0",
        treeLevel: 0,
    }
    handlePPB(tr, row)
});

$(document).on('click', '#hide-ppbs', function() {
    var expanders = document.getElementsByClassName('table-tree-control');
    for (var expander in Object.keys(expanders)){
        var el = expanders[expander];
        if ($(el).attr("element") == "test"){
            collapseTreeControl(el);
        } else {            
            expandTreeControl(el);
        }
    }
});