function makeVisible(elementId, visible) {
    var elementId = document.getElementById(elementId);
    if (visible) {
        elementId.style.display = "block"
    } else {
        elementId.style.display = "none"
    }
}

function showLoading(menuIconId) {
    makeVisible(menuIconId, false)
    makeVisible(menuIconId + '-loading', true)
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip({html:true});
})