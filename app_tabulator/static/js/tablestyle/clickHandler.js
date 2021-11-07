$(document).on('click', '.ppb-name', function() {
    onClickDDForEdit(this);
});

$(document).on('click', '.ppb-invoiceType', function() {
    onClickDDForEdit(this);
});

function onClickDDForEdit(el){
    var expanded = $(el).attr("expanded");
    //console.log(el.classList)
    console.log(expanded)
    if (expanded == 'false') { //!el.classList.contains('ppb-edit')){
        el.classList.add("ppb-edit") 
        var childList = $(el).children('ul');
        $(childList).css('display','block')    
        $(childList).attr("expanded", 'true');
    } else {        
        $(el).removeClass('ppb-edit');
        $(el).attr("expanded", 'false')
    }    
}

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

$(document).on('click', '.ppb-name-dd-item', function() {    
    //-----------------------------------------------------
    //           Move PPB-TR beneath Test-TR
    //-----------------------------------------------------
    var newTestIdent = $(this).attr("testident");
    var parentTR=$(this).parents('tr');
    if (newTestIdent != '-1'){
        var newParent = document.getElementById(newTestIdent);
        $(parentTR).attr("testident",newTestIdent);
        parentTR.insertAfter(newParent);

        //-----------------------------------------------------
        //           Set Values and switch visibility
        //-----------------------------------------------------
        var parentTD=$(this).parents('td');
        var childP = $(parentTD).children('p');  
        var childList = $(parentTD).children('ul');  
        var value = 'TE'+ parseInt($(this).attr("testnumber")).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false});
        $(childP).text(value);     
        $(childList).css('display','none');
    } else {
        $(parentTR).remove();
    }

});

$(document).on('click', '.ppb-invoice-dd-item', function() {
    var parent=$(this).parents('td');
    var childP = $(parent).children('p');
    var value = $(this).attr("invoicetype"); 
    
    $(childP).text(getInvoiceType(value)); 
    var childList = $(parent).children('ul');
    console.log(childList)
    $(childList).css('display','none');
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

function switchViewAndEditTime(box){
    var childView = $(box).children('p');
    var childEdit = $(box).children('input');
    var newValue = $(childEdit).val();
    if (isTime(newValue) == true){
        $(childView).text(newValue);
    }
    $(childEdit).css('display','none');
    $(childView).css('display','inline');
}

function hideDD(box){
    var childList = $(box).children('ul');
    $(childList).css('display','none');
    //$(childList).attr("expanded", 'false')
}

function isTime(time){
    var isTime = true
    if (String(time).indexOf(':')==-1){ 
        isTime = false; 
    } else {
        var splitted = String(time).split(':')
        var hours = parseInt(splitted[0]);
        var minutes = parseInt(splitted[1]);
        if (hours<0 | hours>24){isTime = false;}
        if (minutes<0 || minutes>59){isTime = false;}
    }
    return isTime
}


$(document).on('click', '.table-tree-control', function() {   
    var status = $(this).attr("status");
    if (status == "show"){
        collapseTreeControl(this);
    } else {        
        expandTreeControl(this);
    }
});

function expandTreeControl(el){
    var contolElements = $(el).attr("controlelements");
    var child = $(el).children('div')
    $(child).addClass('table-tree-control-expand')
    $(child).removeClass('table-tree-control-collapse')
    $(el).attr("status","show");
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

function collapseTreeControl(el){
    var contolElements = $(el).attr("controlelements");
    var child = $(el).children('div')
    $(child).addClass('table-tree-control-collapse')
    $(child).removeClass('table-tree-control-expand')
    $(el).attr("status","hide");
    $("."+contolElements).hide();
}

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
    console.log("Neue Zeile sollte angelegt werden:")
    var tr = tbl.insertRow(1);
    row = {
        comment: "",
        date: getTodaysDate(),
        element: "ppb",
        id: 0,
        invoiceType: -1,
        isTestFinished: false,
        name: "",
        operator: "Penis",
        protocolIdent: "",
        start: "",
        stop: "",
        testIdent: "",
        totalTime: "",
        treeElement: "0",
        treeLevel: 1,
    }
    handlePPB(tr, row)
});

