function openNav() {
    var sidebar = document.getElementById("sidebar");
    var overlay = document.getElementById("overlay");
    overlay.style.display="block"
    sidebar.style.left="0px"
    sidebar.style.zIndex="10";
}
function closeNav() {
    var sidebar = document.getElementById("sidebar");
    var overlay = document.getElementById("overlay");
    sidebar.style.left="-250px"
    overlay.style.display="none"
}
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const menubtn = document.getElementById('menu-btn');
    
    menubtn.addEventListener('click', (event) => {
        event.stopPropagation();
        openNav();
    });
    document.addEventListener('click', (event) => {
        if (event.target !== sidebar && !sidebar.contains(event.target)) {
            closeNav();
        }
    });
});
