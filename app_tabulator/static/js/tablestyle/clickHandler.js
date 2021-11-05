

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
            case "start":
                switchViewAndEditTime();
                break;
            case "stop":
                switchViewAndEditTime();
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

function switchViewAndEditTime(){
    var childView = $(box).children('p');
    var childEdit = $(box).children('input');
    var newValue = $(childEdit).val();
    if (isTime(newValue) == true){
        $(childView).text(newValue);
    }
    $(childEdit).css('display','none');
    $(childView).css('display','inline');
}

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
