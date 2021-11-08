function onClickDDForEdit(el){
    var expanded = $(el).attr("expanded");
    //console.log(el.classList)
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

function onClickForEdit(el){
    el.classList.add("ppb-edit") 
    var childInput = $(el).children('input');
    var childP = $(el).children('p');
    $(childP).css('display','none')
    $(childInput).css('display','inline')
    $(childInput).val($(childP).text());
}

function getTreeLevelOfElement(treeElement, variable){    
    if (variable == "level"){
        var returnValue;
        for (var i=0, l=treeElement.length; i<l; ++i) {
            if(/level.*/.test(treeElement[i])) {
                returnValue = parseInt(treeElement[i].replace("level",""));
                break;
            }
        }
    } else {
        var returnValue=[];
        for (var i=0, l=treeElement.length; i<l; ++i) {
            if(/sub-.*/.test(treeElement[i])) {
                returnValue.push(treeElement[i]);
            }
        }
    }
    return returnValue
}

function setNewTreeLevel(parentTR, newParent){
    var oldTreeLevel = getTreeLevelOfElement($(parentTR).attr("class").split(/\s+/), 'level')
    $(parentTR).removeClass("level"+oldTreeLevel);
    var newTreeLevel = getTreeLevelOfElement(newParent.classList, 'level')+1;
    $(parentTR).addClass("level"+newTreeLevel);
}

function removeOldSubsFromElement(el){
    treeElement = $(el).attr("class").split(/\s+/)
    for (var i=0, l=treeElement.length; i<l; ++i) {
        if(/sub-.*/.test(treeElement[i])) {
            $(el).removeClass(treeElement[i]);
        }
    }
}

function addSubsToClass(row, newParent){
    removeOldSubsFromElement(row);
    var subsFromNewParent = getTreeLevelOfElement($(newParent).attr("class").split(/\s+/), 'sub-')
    for (var subClass in Object.keys(subsFromNewParent)){
        $(row).addClass(subsFromNewParent[subClass]);
    }
    var newSubFromNewParent = "sub-"+$(newParent).attr("treeelement");
    $(row).addClass(newSubFromNewParent);
}


function getTreeControlOfTR(parent){
    var childTD = $(parent).children("td");
    var childsDIV = $(childTD).children("div");
    var treeControl;
    for (var child in Object.keys(childsDIV)){
        if (childsDIV[child].classList.contains("table-tree-control")){
            treeControl = childsDIV[child];
            break;
        }
    }
    return treeControl
}

function handleTreeControlForParent(parentTestIdent){
    var parent = document.getElementById(parentTestIdent);
    var subClass = "sub-"+$(parent).attr("treeelement");
    var ppbs = document.getElementsByClassName(subClass);
    var treeControl = getTreeControlOfTR(parent);
    if (ppbs.length>0){
        $(treeControl).removeClass("table-tree-control-invisible");
    } else {
        $(treeControl).addClass("table-tree-control-invisible");
        collapseTreeControl(treeControl);
    }
}

function checkTreeControlForParentsAfterMove(oldTestIdent, newTestIdent){
    if (oldTestIdent){handleTreeControlForParent(oldTestIdent);}
    handleTreeControlForParent(newTestIdent);
};

function applyVisibilityOfParent(parent){    
    var el = getTreeControlOfTR(parent);
    expandTreeControl(el);
}


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

function collapseTreeControl(el){
    var contolElements = $(el).attr("controlelements");
    var child = $(el).children('div')
    $(child).addClass('table-tree-control-collapse')
    $(child).removeClass('table-tree-control-expand')
    $(el).attr("status","hide");
    $("."+contolElements).hide();
}


function expandTreeControl(el){
    var controledElements = $(el).attr("controlelements");
    var child = $(el).children('div');
    $(child).addClass('table-tree-control-expand');
    $(child).removeClass('table-tree-control-collapse');
    $(el).attr("status","show");
    $("."+controledElements).show()
    $("."+controledElements).each(function(index, item){
        var subChild_td = $(item).children('td')[0];
        var subChilds_div = $(subChild_td).children('div');
        var controlElement;
        if(subChilds_div){
            for (var child in Object.keys(subChilds_div)){
                if (subChilds_div[child]){
                    if (subChilds_div[child].classList.contains("table-tree-control")){
                        controlElement = subChilds_div[child];
                        break;
                    }
                }
            }
            if (controlElement){
                var subStatus = $(controlElement).attr("status")                
                var subContolElements = $(controlElement).attr("controlelements")
                if (subStatus == 'show'){
                    $("."+subContolElements).show();
                } else {
                    $("."+subContolElements).hide();
                }
            }
        }
    });
}

function expandElement(el){
    var controledElements = $(el).attr("controlelements");
    var child = $(el).children('div');
    $(child).addClass('table-tree-control-expand');
    $(child).removeClass('table-tree-control-collapse');
    $(el).attr("status","show");
    $("."+controledElements).show()
}