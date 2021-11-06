$(document).on('click', '.ppb-name', function() {
    onClickDDForEdit(this);
});

$(document).on('click', '.ppb-invoiceType', function() {
    onClickDDForEdit(this);
});

function onClickDDForEdit(el){
    var childList = $(el).children('ul');
    var expanded = $(childList).attr("expanded");
    if (expanded == 'false'){
        el.classList.add("ppb-edit") 
        $(childList).css('display','block')    
        $(childList).attr("expanded", 'true');
    } else {        
        $(el).removeClass('ppb-edit');
        $(el).children('ul').attr("expanded", 'false')
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
    var parentTR=$(this).parents('tr');
    var newTestIdent = $(this).attr("testident");
    $(parentTR).attr("testident",newTestIdent);

    var parentTD=$(this).parents('td');
    var childP = $(parentTD).children('p');    
    var value = 'TE'+ parseInt($(this).attr("testnumber")).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false});
    $(childP).text(value); 

    
    var childList = $(parentTD).children('ul');
    console.log(childList)
    $(childList).css('display','none');
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
