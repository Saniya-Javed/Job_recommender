let navItems= ['#home', '#skills', '#academics', '#project', '#about'];
function handleNavigation(e) {
    var id =(e.target.getAttribute('data-value'))
    navItems.map(function(item) {
        if(id === item ) {
            $(item).addClass("active");
        }
        else {
        $(item).removeClass("active");
        }
    })
}

$(document).ready(function(){
    document.getElementsByTagName('meta')['viewport'].content='min-width: 980px;';
});