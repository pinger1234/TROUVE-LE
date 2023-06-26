

function load_theme(){
    var theme = localStorage.getItem('theme');

    if (theme == null) {
        setTheme('light');
        document.getElementsByTagName("body").setAttribute("data-theme","light");
    } else {
        document.getElementsByTagName("body").setAttribute("data-theme",theme);
    }
    
function toggleTheme() {
    if (localStorage.getItem('theme') === 'dark') {
        setTheme('light');
    } else {
        setTheme('dark');
    }
}
}

function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
}
