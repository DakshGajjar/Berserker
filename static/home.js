//const chstyle = document.getElementById('choice').style.display

function func(x){
    x.classList.toggle("change")
    btns = document.getElementById('btns')
    fraw = document.getElementById('fraw')
    if (btns.style.display == 'block'){
        btns.style.display = 'none'
        fraw.style.border = 'none'
    } else{
        btns.style.display = 'block'
        fraw.style.border = '2px solid white' 
    } 
}

var sb = document.getElementById('sb')
if(sb){
    sb.onclick = function validate(){
        if (document.getElementById('qry').value==""){
            document.getElementById('qry').setCustomValidity('keyword can not be empty');
        }
        else{
            console.log(document.getElementById('qry').value)
        }
    }
}


function cls(){
    window.close()
    //window.open(window.location.href+"/ranproc/")
}

history.pushState(null, null, location.href);
window.onpopstate = function () {
    history.go(1);
};